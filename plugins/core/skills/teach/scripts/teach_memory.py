#!/usr/bin/env python3
"""Manage Teach concept notes and their SQLite FTS index."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path


DEFAULT_MEMORY_DIR = Path.home() / ".agents" / "memory" / "teach"
INDEX_NAME = "index.sqlite3"
PROFILE_NAME = "profile.md"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "concept"


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_list_value(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",") if part.strip()]
    return [raw.strip('"').strip("'")]


def format_yaml_list(values: list[str]) -> str:
    escaped = [value.replace('"', '\\"') for value in values if value]
    return "[" + ", ".join(f'"{value}"' for value in escaped) + "]"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text

    metadata: dict[str, object] = {}
    current_key: str | None = None
    for line in lines[1:end_index]:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            existing = metadata.setdefault(current_key, [])
            if isinstance(existing, list):
                existing.append(line[4:].strip().strip('"').strip("'"))
            continue
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        current_key = key
        if raw_value == "":
            metadata[key] = []
        elif raw_value.startswith("["):
            metadata[key] = parse_list_value(raw_value)
        else:
            metadata[key] = raw_value.strip('"').strip("'")

    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    return metadata, body


def list_value(metadata: dict[str, object], key: str) -> list[str]:
    value = metadata.get(key, [])
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str) and value:
        return [value]
    return []


def string_value(metadata: dict[str, object], key: str) -> str:
    value = metadata.get(key, "")
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value) if value is not None else ""


def note_path(memory_dir: Path, title: str) -> Path:
    return memory_dir / f"{slugify(title)}.md"


def ensure_memory(memory_dir: Path) -> None:
    memory_dir.mkdir(parents=True, exist_ok=True)
    index_path = memory_dir / INDEX_NAME
    with sqlite3.connect(index_path) as conn:
        create_schema(conn)


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS concepts (
          slug TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          path TEXT NOT NULL,
          aliases TEXT NOT NULL DEFAULT '[]',
          tags TEXT NOT NULL DEFAULT '[]',
          source_context TEXT NOT NULL DEFAULT '',
          confidence TEXT NOT NULL DEFAULT '',
          related_concepts TEXT NOT NULL DEFAULT '[]',
          learned_at TEXT NOT NULL DEFAULT '',
          body TEXT NOT NULL DEFAULT '',
          updated_at TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS concepts_fts USING fts5(
          slug UNINDEXED,
          title,
          aliases,
          tags,
          source_context,
          related_concepts,
          body
        );
        """
    )


def concept_files(memory_dir: Path) -> list[Path]:
    if not memory_dir.exists():
        return []
    return sorted(
        path
        for path in memory_dir.glob("*.md")
        if path.is_file() and path.name.lower() not in {"readme.md", PROFILE_NAME}
    )


def load_concept(path: Path, memory_dir: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(text)
    slug = path.stem
    title = string_value(metadata, "title") or slug.replace("-", " ").title()
    aliases = list_value(metadata, "aliases")
    tags = list_value(metadata, "tags")
    related = list_value(metadata, "related_concepts")
    return {
        "slug": slug,
        "title": title,
        "path": str(path.relative_to(memory_dir)),
        "aliases": json.dumps(aliases, ensure_ascii=True),
        "tags": json.dumps(tags, ensure_ascii=True),
        "source_context": string_value(metadata, "source_context"),
        "confidence": string_value(metadata, "confidence"),
        "related_concepts": json.dumps(related, ensure_ascii=True),
        "learned_at": string_value(metadata, "learned_at"),
        "body": body.strip(),
        "updated_at": dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).isoformat(),
    }


def rebuild_index(memory_dir: Path) -> int:
    ensure_memory(memory_dir)
    index_path = memory_dir / INDEX_NAME
    concepts = [load_concept(path, memory_dir) for path in concept_files(memory_dir)]
    with sqlite3.connect(index_path) as conn:
        create_schema(conn)
        conn.execute("DELETE FROM concepts")
        conn.execute("DROP TABLE IF EXISTS concepts_fts")
        create_schema(conn)
        for concept in concepts:
            conn.execute(
                """
                INSERT INTO concepts (
                  slug, title, path, aliases, tags, source_context, confidence,
                  related_concepts, learned_at, body, updated_at
                )
                VALUES (
                  :slug, :title, :path, :aliases, :tags, :source_context, :confidence,
                  :related_concepts, :learned_at, :body, :updated_at
                )
                """,
                concept,
            )
            conn.execute(
                """
                INSERT INTO concepts_fts (
                  slug, title, aliases, tags, source_context, related_concepts, body
                )
                VALUES (
                  :slug, :title, :aliases, :tags, :source_context, :related_concepts, :body
                )
                """,
                concept,
            )
    return len(concepts)


def safe_match_query(query: str) -> str:
    terms = re.findall(r"[A-Za-z0-9_+-]+", query)
    return " OR ".join(terms) if terms else query.replace('"', '""')


def search(memory_dir: Path, query: str, limit: int) -> list[dict[str, object]]:
    ensure_memory(memory_dir)
    index_path = memory_dir / INDEX_NAME
    match_query = safe_match_query(query)
    with sqlite3.connect(index_path) as conn:
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute(
                """
                SELECT c.slug, c.title, c.path, c.tags, c.confidence,
                       snippet(concepts_fts, 6, '[', ']', ' ... ', 18) AS snippet,
                       bm25(concepts_fts, 5.0, 3.0, 3.0, 1.5, 2.0, 1.0) AS score
                FROM concepts_fts
                JOIN concepts c ON c.slug = concepts_fts.slug
                WHERE concepts_fts MATCH ?
                ORDER BY score
                LIMIT ?
                """,
                (match_query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            like = f"%{query}%"
            rows = conn.execute(
                """
                SELECT slug, title, path, tags, confidence,
                       substr(body, 1, 220) AS snippet,
                       0 AS score
                FROM concepts
                WHERE title LIKE ? OR aliases LIKE ? OR tags LIKE ? OR related_concepts LIKE ? OR body LIKE ?
                ORDER BY title
                LIMIT ?
                """,
                (like, like, like, like, like, limit),
            ).fetchall()
    return [dict(row) for row in rows]


def create_note(args: argparse.Namespace) -> Path:
    memory_dir = args.memory_dir.expanduser()
    ensure_memory(memory_dir)
    path = args.path.expanduser() if args.path else note_path(memory_dir, args.title)
    if path.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing note: {path}")

    learned_at = args.learned_at or dt.date.today().isoformat()
    aliases = split_csv(args.aliases)
    tags = split_csv(args.tags)
    related = split_csv(args.related)
    confidence = args.confidence
    source_context = args.source_context
    body = sys.stdin.read().strip() if not args.body else args.body.strip()
    if not body:
        body = (
            f"# {args.title}\n\n"
            "## Concept\n\n"
            f"{args.title} is the concept being learned.\n\n"
            "## Why It Matters\n\n"
            "It matters because it changes how the user understands or evaluates a design choice.\n\n"
            "## How It Works\n\n"
            "Describe the mechanism in concrete terms.\n\n"
            "## Alternatives\n\n"
            "- Name the main alternative and when it wins.\n\n"
            "## Tradeoffs\n\n"
            "- Explain the benefit, cost, and risk.\n\n"
            "## What To Read Next\n\n"
            "- Add a focused reading topic.\n\n"
            "## Seen In\n\n"
            f"- {source_context or 'Teach session'}\n"
        )

    content = (
        "---\n"
        f'title: "{args.title}"\n'
        f"aliases: {format_yaml_list(aliases)}\n"
        f"tags: {format_yaml_list(tags)}\n"
        f'learned_at: "{learned_at}"\n'
        f'source_context: "{source_context}"\n'
        f'confidence: "{confidence}"\n'
        f"related_concepts: {format_yaml_list(related)}\n"
        "---\n\n"
        f"{body.rstrip()}\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_profile(args: argparse.Namespace) -> Path:
    memory_dir = args.memory_dir.expanduser()
    ensure_memory(memory_dir)
    path = memory_dir / PROFILE_NAME
    if path.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing profile: {path}")
    updated_at = args.updated_at or dt.date.today().isoformat()
    lanes = split_csv(args.primary_learning_lanes)
    content = (
        "---\n"
        'title: "Teach Learner Profile"\n'
        f'updated_at: "{updated_at}"\n'
        f'current_identity: "{args.current_identity}"\n'
        f'target_identity: "{args.target_identity}"\n'
        f"primary_learning_lanes: {format_yaml_list(lanes)}\n"
        f'current_grasp: "{args.current_grasp}"\n'
        f'teaching_preference: "{args.teaching_preference}"\n'
        "---\n\n"
        "# Teach Learner Profile\n\n"
        f"{args.body.strip()}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def validate(memory_dir: Path) -> None:
    ensure_memory(memory_dir)
    with sqlite3.connect(memory_dir / INDEX_NAME) as conn:
        conn.execute("SELECT count(*) FROM concepts").fetchone()
        conn.execute("SELECT count(*) FROM concepts_fts").fetchone()
        options = {row[0] for row in conn.execute("PRAGMA compile_options")}
        if not any("FTS5" in option for option in options):
            try:
                conn.execute("CREATE VIRTUAL TABLE temp_fts_check USING fts5(value)")
                conn.execute("DROP TABLE temp_fts_check")
            except sqlite3.OperationalError as exc:
                raise SystemExit(f"SQLite FTS5 is unavailable: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    memory_parent = argparse.ArgumentParser(add_help=False)
    memory_parent.add_argument(
        "--memory-dir",
        type=Path,
        default=argparse.SUPPRESS,
        help="Teach memory directory. Defaults to ~/.agents/memory/teach.",
    )
    parser = argparse.ArgumentParser(description="Manage Teach concept memory.")
    parser.add_argument(
        "--memory-dir",
        type=Path,
        default=DEFAULT_MEMORY_DIR,
        help="Teach memory directory. Defaults to ~/.agents/memory/teach.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "ensure",
        parents=[memory_parent],
        help="Create the memory directory and SQLite schema.",
    )
    subparsers.add_parser(
        "index",
        parents=[memory_parent],
        help="Rebuild the SQLite index from Markdown notes.",
    )
    subparsers.add_parser(
        "validate",
        parents=[memory_parent],
        help="Validate the memory directory and SQLite schema.",
    )

    search_parser = subparsers.add_parser(
        "search",
        parents=[memory_parent],
        help="Search indexed concept notes.",
    )
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)

    note_parser = subparsers.add_parser(
        "note",
        parents=[memory_parent],
        help="Create a concept note from arguments/stdin.",
    )
    note_parser.add_argument("title")
    note_parser.add_argument("--aliases", default="")
    note_parser.add_argument("--tags", default="")
    note_parser.add_argument("--related", default="")
    note_parser.add_argument("--source-context", default="")
    note_parser.add_argument("--confidence", default="introduced", choices=["introduced", "practiced", "comfortable"])
    note_parser.add_argument("--learned-at", default="")
    note_parser.add_argument("--body", default="")
    note_parser.add_argument("--path", type=Path)
    note_parser.add_argument("--force", action="store_true")

    profile_parser = subparsers.add_parser(
        "profile",
        parents=[memory_parent],
        help="Create or replace the learner profile.",
    )
    profile_parser.add_argument("--current-identity", default="Designer moving toward design engineering")
    profile_parser.add_argument("--target-identity", default="Design engineer with strong frontend implementation taste")
    profile_parser.add_argument(
        "--primary-learning-lanes",
        default="html,css,javascript,typescript,react,browser rendering,accessibility,component architecture,interaction design",
    )
    profile_parser.add_argument(
        "--current-grasp",
        default="Strong design/product intuition; building deeper frontend and engineering mental models",
    )
    profile_parser.add_argument(
        "--teaching-preference",
        default="Use design-to-code bridges, concrete UI examples, frontend mechanics, and tradeoffs before abstract backend/tooling explanations.",
    )
    profile_parser.add_argument(
        "--body",
        default=(
            "The user is a designer on the path to becoming a design engineer.\n\n"
            "They want frontend intricacies explained in detail: HTML semantics, CSS layout and cascade, responsive constraints, browser rendering, JavaScript runtime behavior, TypeScript type modeling, React component architecture, state, effects, accessibility, interaction polish, and design-system implementation.\n\n"
            "Use frontend examples as the default bridge when they clarify a concept. Backend, indexing, tooling, or infrastructure concepts should still be explained when relevant, but connect them back to UI behavior, developer ergonomics, product experience, or design-to-code tradeoffs whenever possible."
        ),
    )
    profile_parser.add_argument("--updated-at", default="")
    profile_parser.add_argument("--force", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    memory_dir = args.memory_dir.expanduser()

    if args.command == "ensure":
        ensure_memory(memory_dir)
        print(f"teach memory ready: {memory_dir}")
        return 0
    if args.command == "index":
        count = rebuild_index(memory_dir)
        print(f"indexed {count} concept note(s): {memory_dir / INDEX_NAME}")
        return 0
    if args.command == "validate":
        validate(memory_dir)
        print(f"teach memory valid: {memory_dir}")
        return 0
    if args.command == "search":
        for row in search(memory_dir, args.query, args.limit):
            print(f"{row['title']} ({row['path']})")
            print(f"  confidence: {row['confidence']}")
            print(f"  tags: {row['tags']}")
            print(f"  snippet: {row['snippet']}")
        return 0
    if args.command == "note":
        path = create_note(args)
        count = rebuild_index(memory_dir)
        print(f"wrote {path}")
        print(f"indexed {count} concept note(s): {memory_dir / INDEX_NAME}")
        return 0
    if args.command == "profile":
        path = write_profile(args)
        print(f"wrote {path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
