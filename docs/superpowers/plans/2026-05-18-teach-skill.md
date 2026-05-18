# Teach Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Dex Core `teach` skill that explains unfamiliar context before execution, records learned concepts as Markdown notes in `~/.agents/memory/teach/`, and rebuilds a SQLite FTS index from those notes through a Codex hook.

**Architecture:** Keep Markdown concept notes as the canonical memory record and generate `index.sqlite3` as a rebuildable search index. Keep `SKILL.md` as the runtime teaching contract, put deterministic memory/index operations in `scripts/teach_memory.py`, wire a plugin-bundled Codex `Stop` hook to rebuild stale indexes, and validate the skill with a Dex-style eval suite that grades response quality as well as routing.

**Tech Stack:** Markdown skills, YAML frontmatter, Python 3 standard library, SQLite FTS5, Codex plugin hooks, Dex plugin manifests, system `quick_validate.py`, `rtk`.

---

## File Structure

Create:

- `plugins/core/skills/teach/SKILL.md`
  Runtime contract for implicit and explicit teaching, concept explanation, execution gating, clever-function explanation, and learned-concept memory updates.

- `plugins/core/skills/teach/scripts/teach_memory.py`
  Deterministic CLI for creating `~/.agents/memory/teach/`, writing/reading the learner profile, parsing concept Markdown frontmatter, rebuilding `index.sqlite3`, validating schema, and searching the FTS index.

- `plugins/core/skills/teach/scripts/validate_teach_memory.py`
  Repository-local validation script that creates a temporary teach memory directory, writes sample concept notes, indexes them, searches them, and verifies SQLite results.

- `plugins/core/skills/teach/scripts/validate_teach_evals.py`
  Repository-local validation script that checks the teach eval suite for required Dex coverage, gradeable assertions, quality rubric fields, deterministic checks, and unique IDs.

- `plugins/core/skills/teach/evals/evals.json`
  Dex-style eval suite covering explicit trigger, implicit trigger, contextual trigger, negative control, artifact teaching, clever-function explanation, memory update, hook indexing, response look and feel, over-teaching regression, execution-gate regression, and benchmark comparison.

- `plugins/core/skills/teach/agents/openai.yaml`
  Minimal UI metadata for the new skill.

- `plugins/core/hooks/hooks.json`
  Codex plugin hook configuration for the Core plugin. The hook is bundled but only runs when Codex plugin hooks are enabled and trusted.

- `plugins/core/hooks/reindex_teach_memory.py`
  Stop-hook script that checks `~/.agents/memory/teach/` and rebuilds `index.sqlite3` only when Markdown concept notes are newer than the index or the index is missing.

Modify:

- `README.md`
  Add `teach` to the Core skill table and update the Core plugin description where skill inventory is summarized.

- `plugins/core/.codex-plugin/plugin.json`
  Add teaching to the short and long Core plugin descriptions and point Codex at the bundled hook config.

- `plugins/core/.claude-plugin/plugin.json`
  Add teaching to the Core plugin description.

Do not modify:

- Existing user memory under `~/.agents/memory/`.
  Exception: write or update `~/.agents/memory/teach/profile.md` only when the user explicitly asks to personalize Teach memory.
- Release versions or marketplace metadata in this implementation pass.
- Existing untracked plugin marker files such as `.in_use` or `.orphaned_at`.

---

### Task 1: Scaffold the `teach` Skill

**Files:**
- Create: `plugins/core/skills/teach/SKILL.md`
- Create: `plugins/core/skills/teach/scripts/`
- Create: `plugins/core/skills/teach/agents/openai.yaml`

- [ ] **Step 1: Run the system skill initializer**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/init_skill.py teach \
  --path plugins/core/skills \
  --resources scripts \
  --interface display_name="Teach" \
  --interface short_description="Explain concepts before execution" \
  --interface default_prompt="Use $teach to explain this unfamiliar code or context before doing the task."
```

Expected:

```text
Created skill: plugins/core/skills/teach
```

If the exact success text differs, accept zero exit code and a created `plugins/core/skills/teach/SKILL.md`.

- [ ] **Step 2: Confirm scaffolded files**

Run:

```bash
find plugins/core/skills/teach -maxdepth 3 -type f | sort
```

Expected output contains:

```text
plugins/core/skills/teach/SKILL.md
plugins/core/skills/teach/agents/openai.yaml
```

- [ ] **Step 3: Commit the scaffold**

Run:

```bash
git add plugins/core/skills/teach
git commit -m "feat: scaffold teach core skill"
```

Expected: commit succeeds.

---

### Task 2: Write the Runtime Skill Contract

**Files:**
- Modify: `plugins/core/skills/teach/SKILL.md`
- Modify: `plugins/core/skills/teach/agents/openai.yaml`

- [ ] **Step 1: Replace `SKILL.md` with the final runtime contract**

Replace `plugins/core/skills/teach/SKILL.md` with:

````markdown
---
name: teach
description: "Use when the user explicitly invokes teach or asks to learn, understand, explain, walk through, unpack, or be taught unfamiliar code, tools, concepts, architecture, design choices, tradeoffs, or clever functions before execution. Also use implicitly when the user says they do not understand something, asks what concepts a solution uses, asks what to read to understand a design choice, or asks the agent to explain before doing the task."
---

# Teach

Turn unfamiliar territory into a clear learning pass before execution.

Assume the active context is unfamiliar to the user. Teach the concepts, mechanics, alternatives, and tradeoffs first. Move to the requested task only after the user has a workable grasp or explicitly asks you to proceed.

## Core Workflow

1. Identify the learning target from the user request, active files, pasted text, error output, code diff, tool output, or design context.
2. Read `~/.agents/memory/teach/profile.md` when present and use it to choose examples, analogies, learning depth, and reading paths.
3. Explain how it works in concrete terms. Define unfamiliar terms once, then use them naturally.
4. Name the important concepts involved.
5. Compare alternatives and tradeoffs.
6. Tell the user what to read next to understand the design choices.
7. Ask one grounding question or confirmation before execution:
   - "Should I slow down on any concept before I do the task?"
   - "Does this mental model work well enough for me to proceed?"
   - "Which part should I unpack further before I change the code?"
8. After the user confirms or shows understanding, perform the original task if it was part of the request.
9. Record learned concepts in `~/.agents/memory/teach/` when the concept is durable enough to matter later.
10. Let the bundled Codex hook rebuild the SQLite index after concept notes change. If hooks are disabled or the user asks for an immediate search, run the index command manually.

## Learner Profile

Personalization lives in:

```text
~/.agents/memory/teach/profile.md
```

If the file exists, read it before choosing examples or depth. If it does not exist and the user provides learning context, create it. Do not index `profile.md` as a concept note.

Seed this user's profile with:

```markdown
---
title: "Teach Learner Profile"
updated_at: "2026-05-18"
current_identity: "Designer moving toward design engineering"
target_identity: "Design engineer with strong frontend implementation taste"
primary_learning_lanes: ["html", "css", "javascript", "typescript", "react", "browser rendering", "accessibility", "component architecture", "interaction design"]
current_grasp: "Strong design/product intuition; building deeper frontend and engineering mental models"
teaching_preference: "Use design-to-code bridges, concrete UI examples, frontend mechanics, and tradeoffs before abstract backend/tooling explanations."
---

# Teach Learner Profile

The user is a designer on the path to becoming a design engineer.

They want frontend intricacies explained in detail: HTML semantics, CSS layout and cascade, responsive constraints, browser rendering, JavaScript runtime behavior, TypeScript type modeling, React component architecture, state, effects, accessibility, interaction polish, and design-system implementation.

Use frontend examples as the default bridge when they clarify a concept. Backend, indexing, tooling, or infrastructure concepts should still be explained when relevant, but connect them back to UI behavior, developer ergonomics, product experience, or design-to-code tradeoffs whenever possible.
```

## Teaching Shape

Use this shape when it helps scanning:

```markdown
**Mental Model**
[plain explanation of the system]

**Concepts**
- `term` -> meaning -> where it appears here -> why it matters

**Alternatives**
- [alternative] -> what changes -> when it wins -> when it fails

**Tradeoffs**
- [choice] -> benefit -> cost -> risk

**Read Next**
- [topic or doc] -> why it matters
```

Do not turn every answer into a lecture. Compress when the user only needs a quick explanation.

## Frontend Teaching Lane

When the concept touches frontend work, prefer this ladder:

1. User-visible behavior: what changes in the interface.
2. HTML semantics: what structure or meaning the browser sees.
3. CSS mechanics: cascade, specificity, box model, layout, containment, responsive constraints, transitions, or stacking context.
4. JavaScript runtime: events, closures, promises, modules, data transformation, browser APIs, or scheduling.
5. TypeScript model: what shape the data has and what invariants the compiler can protect.
6. React model: component boundary, props, state, effects, memoization, rendering, hydration, or reconciliation.
7. Design-engineering tradeoff: maintainability, accessibility, performance, design-system fit, ergonomics, and failure modes.

For design-to-code explanations, translate visual or interaction language into mechanics:

- hierarchy -> DOM order, semantic headings, spacing scale, type scale, contrast, and reading path
- responsiveness -> grid/flex constraints, min/max sizes, container queries, overflow behavior
- polish -> event timing, transition easing, focus states, reduced-motion handling, and loading states
- design-system fit -> token use, component API, variant boundaries, and escape-hatch cost

## Clever Function Rule

When you write or propose a clever function, abstraction, parser, index, state machine, cache, scheduler, retry loop, ranking function, data model, or concurrency pattern, include a short explanation:

```markdown
**Concepts Used**
- [concept] -> [what it means] -> [how this code uses it]

**Why This Shape**
[why this design beats the simpler alternative here]

**To Understand This Choice**
- [reading topic] -> [what it teaches]
```

Do this even if the user did not ask, because clever code without a learning trail becomes future confusion.

## Memory Contract

Canonical concept memory lives in:

```text
~/.agents/memory/teach/
```

Use one Markdown file per concept:

```text
~/.agents/memory/teach/<slug>.md
```

Use this note format:

```markdown
---
title: "SQLite FTS5"
aliases: ["full text search", "FTS"]
tags: ["sqlite", "search", "indexing"]
learned_at: "2026-05-18"
source_context: "Teach skill"
confidence: "introduced"
related_concepts: ["inverted index", "BM25", "canonical source"]
---

# SQLite FTS5

## Concept

FTS5 is SQLite's built-in full-text search engine.

## Why It Matters

It makes local concept notes searchable without running a separate service.

## How It Works

SQLite stores tokenized text in a virtual table and ranks matches with BM25.

## Alternatives

- Plain grep
- SQLite `LIKE`
- Vector embeddings
- External search services

## Tradeoffs

FTS5 is local and reliable, but it is lexical search. Semantic usefulness comes from good titles, aliases, tags, related concepts, and body wording.

## What To Read Next

- SQLite FTS5 virtual tables
- Inverted indexes
- BM25 ranking

## Seen In

- Dex teach skill concept index
```

Use `confidence` values:

- `introduced`: user has seen the concept and basic meaning.
- `practiced`: user applied the concept in a task.
- `comfortable`: user can likely recognize or explain it later.

Do not overwrite a user's existing concept note blindly. Read it first, preserve useful existing material, then add a dated `## Seen In` or `## Notes` entry.

## SQLite Index

The SQLite index is generated, not canonical:

```text
~/.agents/memory/teach/index.sqlite3
```

Indexing is normally handled by the bundled Codex `Stop` hook in the Core plugin. Plugin hooks are opt-in in Codex and require trust review; when they are disabled, Markdown notes remain canonical and usable.

If the user asks for immediate search before the hook runs, or if the hook is disabled, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" index
```

For a health check, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" validate
```

For search, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" search "query words"
```

If `$CLAUDE_SKILL_DIR` is not available, resolve the script relative to the loaded skill directory.

## Search Semantics

SQLite FTS5 is lexical search. It is not vector embedding search.

Make it semantically useful by writing strong frontmatter:

- `title`: canonical concept name.
- `aliases`: common names, abbreviations, and phrases the user might search.
- `tags`: domain and mechanism words.
- `related_concepts`: neighboring ideas.
- body: plain-language explanation with concrete examples.

If the user later asks for embedding search, keep Markdown as canonical and add embeddings as a derived index.

## Output Rules

- Answer the learning need first.
- Use concrete examples from the active context.
- Explain alternatives through when they win and fail.
- Explain tradeoffs as benefit, cost, and risk.
- Ask only one grounding question before execution.
- Avoid fake certainty about what the user has learned; use confirmation or observed user response.
- Keep memory updates focused on durable concepts, not every small fact.
- Never put private project details into a reusable concept note unless the source context matters for recall.
- Do not claim the hook ran unless you saw hook output or verified `index.sqlite3` was refreshed.
````

- [ ] **Step 2: Replace `agents/openai.yaml`**

Replace `plugins/core/skills/teach/agents/openai.yaml` with:

````yaml
interface:
  display_name: "Teach"
  short_description: "Explain concepts before execution"
  default_prompt: "Use $teach to explain this unfamiliar code or context before doing the task."
````

- [ ] **Step 3: Validate skill frontmatter**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/core/skills/teach
```

Expected:

```text
Validation passed
```

If the exact success text differs, accept zero exit code and no reported errors.

- [ ] **Step 4: Commit runtime contract**

Run:

```bash
git add plugins/core/skills/teach/SKILL.md plugins/core/skills/teach/agents/openai.yaml
git commit -m "feat: define teach skill behavior"
```

Expected: commit succeeds.

---

### Task 3: Add the Markdown and SQLite Memory Script

**Files:**
- Create: `plugins/core/skills/teach/scripts/teach_memory.py`

- [ ] **Step 1: Create the script**

Create `plugins/core/skills/teach/scripts/teach_memory.py` with:

````python
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
EXCLUDED_MARKDOWN = {"readme.md", "profile.md"}
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
          body,
          content=''
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
        conn.execute("DELETE FROM concepts_fts")
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
    parser = argparse.ArgumentParser(description="Manage Teach concept memory.")
    parser.add_argument(
        "--memory-dir",
        type=Path,
        default=DEFAULT_MEMORY_DIR,
        help="Teach memory directory. Defaults to ~/.agents/memory/teach.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ensure", help="Create the memory directory and SQLite schema.")
    subparsers.add_parser("index", help="Rebuild the SQLite index from Markdown notes.")
    subparsers.add_parser("validate", help="Validate the memory directory and SQLite schema.")

    search_parser = subparsers.add_parser("search", help="Search indexed concept notes.")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)

    note_parser = subparsers.add_parser("note", help="Create a concept note from arguments/stdin.")
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

    profile_parser = subparsers.add_parser("profile", help="Create or replace the learner profile.")
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
````

- [ ] **Step 2: Make the script executable**

Run:

```bash
chmod +x plugins/core/skills/teach/scripts/teach_memory.py
```

Expected: command exits with status 0.

- [ ] **Step 3: Run an empty-memory validation**

Run:

```bash
rm -rf /tmp/dex-teach-memory-empty
python3 plugins/core/skills/teach/scripts/teach_memory.py validate --memory-dir /tmp/dex-teach-memory-empty
```

Expected:

```text
teach memory valid: /tmp/dex-teach-memory-empty
```

- [ ] **Step 4: Create a sample note through the script**

Run:

```bash
rm -rf /tmp/dex-teach-memory
python3 plugins/core/skills/teach/scripts/teach_memory.py note "SQLite FTS5" \
  --memory-dir /tmp/dex-teach-memory \
  --aliases "full text search,FTS" \
  --tags "sqlite,search,indexing" \
  --related "inverted index,BM25" \
  --source-context "teach memory validation" \
  --body $'# SQLite FTS5\n\n## Concept\n\nFTS5 is SQLite full-text search.\n\n## Why It Matters\n\nIt makes concept notes searchable without a service.\n'
```

Expected output contains:

```text
wrote /tmp/dex-teach-memory/sqlite-fts5.md
indexed 1 concept note(s): /tmp/dex-teach-memory/index.sqlite3
```

- [ ] **Step 5: Create the learner profile and verify it is not indexed**

Run:

```bash
python3 plugins/core/skills/teach/scripts/teach_memory.py profile \
  --memory-dir /tmp/dex-teach-memory \
  --force
python3 plugins/core/skills/teach/scripts/teach_memory.py index --memory-dir /tmp/dex-teach-memory
python3 - <<'PY'
import sqlite3
from pathlib import Path

with sqlite3.connect("/tmp/dex-teach-memory/index.sqlite3") as conn:
    paths = [row[0] for row in conn.execute("SELECT path FROM concepts ORDER BY path")]
assert "profile.md" not in paths, paths
assert paths == ["sqlite-fts5.md"], paths
print("profile excluded from concept index")
PY
```

Expected output contains:

```text
wrote /tmp/dex-teach-memory/profile.md
indexed 1 concept note(s): /tmp/dex-teach-memory/index.sqlite3
profile excluded from concept index
```

- [ ] **Step 6: Search the sample note**

Run:

```bash
python3 plugins/core/skills/teach/scripts/teach_memory.py search "full text" --memory-dir /tmp/dex-teach-memory
```

Expected output contains:

```text
SQLite FTS5 (sqlite-fts5.md)
```

- [ ] **Step 7: Commit the memory script**

Run:

```bash
git add plugins/core/skills/teach/scripts/teach_memory.py
git commit -m "feat: add teach concept memory index"
```

Expected: commit succeeds.

---

### Task 4: Add Script Validation and Skill Evals

**Files:**
- Create: `plugins/core/skills/teach/scripts/validate_teach_memory.py`
- Create: `plugins/core/skills/teach/scripts/validate_teach_evals.py`
- Create: `plugins/core/skills/teach/evals/evals.json`

- [ ] **Step 1: Create the validation script**

Create `plugins/core/skills/teach/scripts/validate_teach_memory.py` with:

````python
#!/usr/bin/env python3
"""Validate Teach concept memory indexing without touching user memory."""

from __future__ import annotations

import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "teach_memory.py"
PLUGIN_ROOT = ROOT.parents[1]
HOOK = PLUGIN_ROOT / "hooks" / "reindex_teach_memory.py"


def run(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def run_hook(memory_dir: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(HOOK), "--memory-dir", str(memory_dir)],
        text=True,
        capture_output=True,
        check=False,
        env={"CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT)},
    )
    if result.returncode != 0:
        raise AssertionError(
            f"hook failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def main() -> int:
    tmp_root = Path(tempfile.mkdtemp(prefix="dex-teach-memory-"))
    memory_dir = tmp_root / "teach"
    try:
        run("validate", "--memory-dir", str(memory_dir))
        run(
            "note",
            "Inverted Index",
            "--memory-dir",
            str(memory_dir),
            "--aliases",
            "posting list,search index",
            "--tags",
            "search,indexing",
            "--related",
            "SQLite FTS5,BM25",
            "--source-context",
            "validator",
            "--body",
            "# Inverted Index\n\n## Concept\n\nAn inverted index maps terms to documents.\n",
        )
        run(
            "note",
            "Tradeoff",
            "--memory-dir",
            str(memory_dir),
            "--aliases",
            "benefit cost risk",
            "--tags",
            "decision-making",
            "--related",
            "alternative,design choice",
            "--source-context",
            "validator",
            "--body",
            "# Tradeoff\n\n## Concept\n\nA tradeoff is the cost paid for a benefit.\n",
        )
        run("index", "--memory-dir", str(memory_dir))
        run("profile", "--memory-dir", str(memory_dir), "--force")
        search_result = run("search", "posting", "--memory-dir", str(memory_dir))
        if "Inverted Index" not in search_result.stdout:
            raise AssertionError(f"expected Inverted Index search result, got:\n{search_result.stdout}")

        index_path = memory_dir / "index.sqlite3"
        with sqlite3.connect(index_path) as conn:
            count = conn.execute("SELECT count(*) FROM concepts").fetchone()[0]
            if count != 2:
                raise AssertionError(f"expected 2 indexed concepts, got {count}")
            indexed_paths = {row[0] for row in conn.execute("SELECT path FROM concepts")}
            if "profile.md" in indexed_paths:
                raise AssertionError("profile.md must not be indexed as a concept")

        deleted_note = memory_dir / "tradeoff.md"
        deleted_note.unlink()
        run_hook(memory_dir)
        with sqlite3.connect(index_path) as conn:
            indexed_paths = {row[0] for row in conn.execute("SELECT path FROM concepts")}
            if "tradeoff.md" in indexed_paths:
                raise AssertionError("hook must remove deleted concept notes from the index")
            if indexed_paths != {"inverted-index.md"}:
                raise AssertionError(f"expected only inverted-index.md after hook, got {indexed_paths}")

        print("teach memory validator passed")
        return 0
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
````

- [ ] **Step 2: Make the validator executable**

Run:

```bash
chmod +x plugins/core/skills/teach/scripts/validate_teach_memory.py
```

Expected: command exits with status 0.

- [ ] **Step 3: Run the validator**

Run:

```bash
python3 plugins/core/skills/teach/scripts/validate_teach_memory.py
```

Expected:

```text
teach memory validator passed
```

- [ ] **Step 4: Create eval cases**

Create `plugins/core/skills/teach/evals/evals.json` with:

````json
{
  "skill_name": "teach",
  "version": 1,
  "notes": "Dex eval suite for Teach. Cases judge routing, source-backed explanation, response look and feel, concept memory, and hook-backed SQLite indexing. Passing output must feel like useful teaching, not a generic framework dump.",
  "standards": {
    "required_coverage": [
      "explicit trigger",
      "implicit trigger",
      "contextual trigger",
      "negative-control",
      "known failure",
      "artifact case",
      "eval suite health",
      "repair regression",
      "benchmark comparison",
      "response quality",
      "hook behavior",
      "frontend-personalized teaching",
      "over-teaching regression",
      "execution-gate regression"
    ],
      "response_quality": [
        "Builds a mental model before details.",
        "Uses the active context or artifact instead of generic explanation.",
        "Uses the learner profile to choose frontend or design-to-code examples when that helps.",
        "Defines unfamiliar terms once and then uses them naturally.",
        "Explains alternatives through when they win and fail.",
      "States tradeoffs as benefit, cost, and risk.",
      "Names concepts used by clever code or abstractions.",
      "Gives focused read-next topics.",
      "Asks one grounding question before execution.",
      "Avoids over-teaching when a compact answer is enough.",
      "Does not claim the user has learned a concept without confirmation or observed use."
    ],
    "passing_run_must_record": [
      "route chosen",
      "files or artifacts inspected",
      "whether execution was gated",
      "concepts taught",
      "memory files written or intentionally skipped",
      "index or hook evidence",
      "response-quality score",
      "blocking failures"
    ]
  },
  "evals": [
    {
      "id": "eval-suite-health-before-forward-run",
      "category": "known-failure",
      "coverage": ["eval suite health", "repair regression"],
      "should_trigger": true,
      "run_mode": "deterministic-or-clean-context",
      "prompt": "Use the dex skill to eval plugins/core/skills/teach. Before any clean-context evaluator runs, validate that the Teach eval suite is healthy and gradeable.",
      "expected_output": "The agent validates eval JSON and Teach-specific coverage first, fixes suite blockers before forward runs, and records suite-health evidence.",
      "assertions": [
        "Runs `python3 -m json.tool plugins/core/skills/teach/evals/evals.json` before clean-context forward runs.",
        "Runs `python3 plugins/core/skills/teach/scripts/validate_teach_evals.py` before clean-context forward runs.",
        "Blocks or repairs the run if response-quality, hook, or benchmark coverage is missing.",
        "Records suite-health evidence in the eval summary or round artifact."
      ],
      "deterministic_checks": {
        "commands": [
          "python3 -m json.tool plugins/core/skills/teach/evals/evals.json",
          "python3 plugins/core/skills/teach/scripts/validate_teach_evals.py"
        ]
      },
      "required_evidence": ["json validation output", "coverage validator output", "proceed/block/repair decision"]
    },
    {
      "id": "explicit-teach-unfamiliar-context",
      "category": "positive",
      "coverage": ["explicit trigger", "response quality", "execution-gate regression"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Use $teach to explain how SQLite FTS indexing works before implementing anything.",
      "expected_output": "The agent teaches SQLite FTS with a mental model, alternatives, tradeoffs, read-next topics, and one grounding question before implementation.",
      "assertions": [
        "Builds a mental model before implementation details.",
        "Defines SQLite FTS5 and distinguishes lexical search from semantic embedding search.",
        "Compares grep, SQLite LIKE, FTS5, and vector embeddings through when they win and fail.",
        "Explains tradeoffs as benefit, cost, and risk.",
        "Asks one grounding question before doing implementation work."
      ],
      "quality_rubric": {
        "mental_model": 2,
        "context_grounding": 1,
        "alternatives_tradeoffs": 2,
        "read_next": 1,
        "execution_gate": 2
      },
      "required_evidence": ["trigger route", "response-quality score", "grounding question"]
    },
    {
      "id": "implicit-explain-trigger",
      "category": "positive",
      "coverage": ["implicit trigger", "response quality"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "I don't understand this parser function. Walk me through what concepts it uses before changing it.",
      "expected_output": "The agent implicitly routes to Teach, explains parser concepts before edits, and asks whether to proceed before changing code.",
      "assertions": [
        "Routes as teach behavior even without explicit $teach.",
        "Names parser-related concepts such as tokenization, grammar, syntax tree, state, or validation only when relevant to the given function.",
        "Explains concepts through the function's actual behavior rather than abstract textbook prose.",
        "Does not edit code before a grounding question or user confirmation."
      ],
      "quality_rubric": {
        "implicit_routing": 2,
        "artifact_grounding": 2,
        "concept_clarity": 2,
        "execution_gate": 2
      },
      "required_evidence": ["implicit route", "concept list", "no pre-confirmation edit"]
    },
    {
      "id": "clever-function-explanation",
      "category": "positive",
      "coverage": ["contextual trigger", "response quality"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Write a compact ranking function for search results and explain the clever parts.",
      "expected_output": "The answer includes code plus a plain explanation of concepts, why the function has that shape, and what to read to understand the choice.",
      "assertions": [
        "Includes `Concepts Used`, `Why This Shape`, and `To Understand This Choice` sections or equivalent headings.",
        "Explains ranking concepts such as weighting, normalization, token match, or BM25 only if the code uses them.",
        "States the simpler alternative and why the chosen shape wins or fails.",
        "Does not hide cleverness behind unexplained terse code."
      ],
      "quality_rubric": {
        "code_explanation": 2,
        "design_choice": 2,
        "read_next": 1,
        "no_unexplained_cleverness": 2
      },
      "required_evidence": ["concepts used", "design-choice explanation", "read-next topics"]
    },
    {
      "id": "artifact-backed-script-teaching",
      "category": "positive",
      "coverage": ["artifact case", "response quality"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Use $teach to explain /Users/aditya.nawal/projects/dex/plugins/core/skills/teach/scripts/teach_memory.py to me like I have never seen frontmatter parsing or SQLite FTS before.",
      "expected_output": "The agent inspects the script, teaches from the actual file, explains frontmatter parsing and SQLite FTS, and avoids generic database advice disconnected from the code.",
      "assertions": [
        "Inspects the target file before explaining it.",
        "Uses concrete functions or flow from the script in the explanation.",
        "Explains frontmatter parsing and FTS indexing in plain language.",
        "Names alternatives and tradeoffs from this script's design.",
        "Asks one grounding question before proposing changes."
      ],
      "quality_rubric": {
        "source_grounding": 3,
        "concept_clarity": 2,
        "alternatives_tradeoffs": 2,
        "execution_gate": 1
      },
      "required_evidence": ["file inspected", "source-grounded explanation", "quality score"]
    },
    {
      "id": "markdown-memory-and-hook-index",
      "category": "positive",
      "coverage": ["hook behavior", "artifact case"],
      "should_trigger": true,
      "run_mode": "deterministic-or-clean-context",
      "prompt": "Teach me the concept of inverted indexes and save it to my teach memory using /tmp/dex-teach-eval-memory. The SQLite index should be refreshed by the hook path, not by assuming manual indexing is enough.",
      "expected_output": "The agent writes a Markdown concept note with frontmatter, runs or validates the hook reindex path against the temp memory dir, and searches the SQLite index.",
      "assertions": [
        "Writes a concept note under the requested memory directory.",
        "Uses Markdown frontmatter with title, aliases, tags, learned_at, source_context, confidence, and related_concepts.",
        "Runs `plugins/core/hooks/reindex_teach_memory.py` or records why plugin hooks are unavailable and validates the hook script directly.",
        "Searches the generated SQLite index and finds the concept.",
        "Does not use the old deeply nested memory path."
      ],
      "deterministic_checks": {
        "commands": [
          "python3 plugins/core/skills/teach/scripts/validate_teach_memory.py",
          "CLAUDE_PLUGIN_ROOT=\"$PWD/plugins/core\" python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-eval-memory --force"
        ],
        "must_not_include_any": [
          ["old deeply nested teach concept path"],
          ["old nested records memory path"]
        ]
      },
      "quality_rubric": {
        "memory_shape": 2,
        "hook_evidence": 3,
        "search_evidence": 2
      },
      "required_evidence": ["concept note path", "frontmatter", "hook command output", "search result"]
    },
    {
      "id": "response-feel-not-lecture",
      "category": "known-failure",
      "coverage": ["known failure", "response quality", "repair regression", "over-teaching regression", "execution-gate regression"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Before fixing this small shell command, explain why it failed: `python3 script.py --path foo` says `unrecognized arguments: --path`.",
      "expected_output": "The answer teaches argparse basics compactly, uses the exact error, names the likely mismatch, gives one alternative, and avoids a long unrelated Python CLI lecture.",
      "assertions": [
        "Starts from the actual error message.",
        "Explains the concept of CLI argument definitions and parser mismatch.",
        "Keeps the response compact enough for a small error.",
        "Does not include a broad tutorial on argparse internals.",
        "Asks one grounding or proceed question before changing code."
      ],
      "quality_rubric": {
        "right_sized_depth": 3,
        "source_grounding": 2,
        "concept_clarity": 2,
        "execution_gate": 1
      },
      "required_evidence": ["right-sized response", "actual error referenced", "no broad lecture"]
    },
    {
      "id": "frontend-personalized-teaching",
      "category": "positive",
      "coverage": ["response quality", "artifact case", "frontend-personalized teaching"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Use $teach to explain why this React component has layout shift and hydration warnings. Assume the learner profile says the user is a designer becoming a design engineer and wants frontend intricacies.",
      "expected_output": "The answer explains the issue through design-to-code mechanics: user-visible behavior, HTML structure, CSS layout constraints, JavaScript/React rendering, TypeScript or prop invariants when relevant, and design-engineering tradeoffs.",
      "assertions": [
        "Uses the designer-to-design-engineer profile as the teaching lens.",
        "Explains frontend mechanics in detail instead of defaulting to backend or database examples.",
        "Connects React behavior to HTML, CSS, browser rendering, and user-visible UI behavior.",
        "Names tradeoffs such as accessibility, performance, maintainability, and design-system fit.",
        "Gives focused read-next topics across HTML, CSS, JavaScript, TypeScript, or React."
      ],
      "quality_rubric": {
        "profile_use": 3,
        "frontend_mechanics": 3,
        "design_to_code_bridge": 2,
        "read_next": 1
      },
      "required_evidence": ["learner profile used", "frontend mechanics", "design-to-code bridge", "read-next topics"]
    },
    {
      "id": "negative-control-direct-implementation",
      "category": "negative-control",
      "coverage": ["negative-control"],
      "should_trigger": false,
      "run_mode": "clean-context-forward",
      "prompt": "Add a missing comma in plugins/core/.codex-plugin/plugin.json. Do not explain anything unless needed.",
      "expected_output": "The Teach workflow should not take over. The agent should perform the narrow edit and maybe mention validation, without a concept lesson.",
      "assertions": [
        "Does not route to Teach.",
        "Does not produce a teaching scaffold.",
        "Keeps the edit narrow.",
        "Runs JSON validation if the file changed."
      ],
      "required_evidence": ["no teach route", "scoped edit", "json validation"]
    },
    {
      "id": "benchmark-against-no-skill-baseline",
      "category": "benchmark",
      "coverage": ["benchmark comparison", "response quality"],
      "should_trigger": true,
      "run_mode": "clean-context-forward",
      "prompt": "Benchmark Teach against a no-skill baseline for explaining a compact parser function. Record whether Teach improves mental model, tradeoffs, read-next guidance, and execution gating.",
      "expected_output": "The eval records a no-skill baseline, a Teach run, and a response-quality delta across the named dimensions.",
      "assertions": [
        "Uses baseline=none for the new skill unless comparing against a snapshot.",
        "Records both baseline and with-skill outputs or summaries.",
        "Scores mental model, tradeoffs, read-next guidance, and execution gate.",
        "Names any quality regression instead of only reporting pass/fail."
      ],
      "quality_rubric": {
        "baseline_recorded": 2,
        "with_skill_recorded": 2,
        "delta_quality": 3,
        "failure_notes": 1
      },
      "required_evidence": ["baseline output", "with-skill output", "quality delta", "release recommendation"]
    }
  ]
}
````

- [ ] **Step 5: Create the eval-suite validator**

Create `plugins/core/skills/teach/scripts/validate_teach_evals.py` with:

````python
#!/usr/bin/env python3
"""Validate the Teach eval suite shape and coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
REQUIRED_COVERAGE = {
    "explicit trigger",
    "implicit trigger",
    "contextual trigger",
    "negative-control",
    "known failure",
    "artifact case",
    "eval suite health",
    "repair regression",
    "benchmark comparison",
    "response quality",
    "hook behavior",
    "frontend-personalized teaching",
    "over-teaching regression",
    "execution-gate regression",
}
REQUIRED_QUALITY = {
    "Builds a mental model before details.",
    "Uses the active context or artifact instead of generic explanation.",
    "Uses the learner profile to choose frontend or design-to-code examples when that helps.",
    "Defines unfamiliar terms once and then uses them naturally.",
    "Explains alternatives through when they win and fail.",
    "States tradeoffs as benefit, cost, and risk.",
    "Names concepts used by clever code or abstractions.",
    "Gives focused read-next topics.",
    "Asks one grounding question before execution.",
    "Avoids over-teaching when a compact answer is enough.",
    "Does not claim the user has learned a concept without confirmation or observed use.",
}


def fail(message: str) -> None:
    raise SystemExit(f"teach eval validation failed: {message}")


def main() -> int:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "teach":
        fail("skill_name must be teach")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        fail("evals must be a non-empty list")

    standards = data.get("standards", {})
    required = set(standards.get("required_coverage", []))
    missing_required = REQUIRED_COVERAGE - required
    if missing_required:
        fail(f"standards.required_coverage missing {sorted(missing_required)}")

    quality = set(standards.get("response_quality", []))
    missing_quality = REQUIRED_QUALITY - quality
    if missing_quality:
        fail(f"standards.response_quality missing {sorted(missing_quality)}")

    ids: set[str] = set()
    coverage_seen: set[str] = set()
    rubric_count = 0
    for index, case in enumerate(evals, start=1):
        case_id = case.get("id")
        if not case_id:
            fail(f"case {index} missing id")
        if case_id in ids:
            fail(f"duplicate id {case_id}")
        ids.add(case_id)
        for key in ("category", "coverage", "should_trigger", "run_mode", "prompt", "expected_output", "assertions", "required_evidence"):
            if key not in case:
                fail(f"{case_id} missing {key}")
        if not isinstance(case["assertions"], list) or len(case["assertions"]) < 3:
            fail(f"{case_id} needs at least three assertions")
        if not isinstance(case["required_evidence"], list) or not case["required_evidence"]:
            fail(f"{case_id} needs required evidence")
        coverage = case["coverage"]
        if not isinstance(coverage, list) or not coverage:
            fail(f"{case_id} coverage must be a non-empty list")
        coverage_seen.update(coverage)
        if "response quality" in coverage:
            if "quality_rubric" not in case:
                fail(f"{case_id} covers response quality but has no quality_rubric")
            rubric_count += 1

    missing_cases = REQUIRED_COVERAGE - coverage_seen
    if missing_cases:
        fail(f"no eval case covers {sorted(missing_cases)}")
    if rubric_count < 5:
        fail("at least five cases should carry a response-quality rubric")

    print("teach eval suite valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

- [ ] **Step 6: Make the eval validator executable**

Run:

```bash
chmod +x plugins/core/skills/teach/scripts/validate_teach_evals.py
```

Expected: command exits with status 0.

- [ ] **Step 7: Validate eval JSON and coverage**

Run:

```bash
python3 -m json.tool plugins/core/skills/teach/evals/evals.json >/tmp/teach-evals.json
python3 plugins/core/skills/teach/scripts/validate_teach_evals.py
```

Expected:

```text
teach eval suite valid
```

- [ ] **Step 8: Commit validation and evals**

Run:

```bash
git add plugins/core/skills/teach/scripts/validate_teach_memory.py plugins/core/skills/teach/scripts/validate_teach_evals.py plugins/core/skills/teach/evals/evals.json
git commit -m "test: add teach eval and memory validation"
```

Expected: commit succeeds.

---

### Task 5: Add the Codex Hook for SQLite Reindexing

**Files:**
- Create: `plugins/core/hooks/hooks.json`
- Create: `plugins/core/hooks/reindex_teach_memory.py`
- Modify: `plugins/core/.codex-plugin/plugin.json`

- [ ] **Step 1: Create the hook directory**

Run:

```bash
mkdir -p plugins/core/hooks
```

Expected: command exits with status 0.

- [ ] **Step 2: Create the hook script**

Create `plugins/core/hooks/reindex_teach_memory.py` with:

````python
#!/usr/bin/env python3
"""Rebuild the Teach SQLite index when concept Markdown changed.

This is intended to run as a Codex Stop hook. It must be cheap on no-op turns
and must never block the agent just because indexing failed.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path


DEFAULT_MEMORY_DIR = Path.home() / ".agents" / "memory" / "teach"
INDEX_NAME = "index.sqlite3"


def concept_files(memory_dir: Path) -> list[Path]:
    if not memory_dir.exists():
        return []
    return sorted(
        path
        for path in memory_dir.glob("*.md")
        if path.is_file() and path.name.lower() not in EXCLUDED_MARKDOWN
    )


def index_is_stale(memory_dir: Path) -> bool:
    files = concept_files(memory_dir)
    index_path = memory_dir / INDEX_NAME
    if not index_path.exists():
        return bool(files)

    current_paths = {path.name for path in files}
    try:
        with sqlite3.connect(index_path) as conn:
            indexed_paths = {row[0] for row in conn.execute("SELECT path FROM concepts")}
    except sqlite3.Error:
        return True

    if current_paths != indexed_paths:
        return True

    if not files:
        return False

    index_mtime = index_path.stat().st_mtime
    return any(path.stat().st_mtime > index_mtime for path in files)


def plugin_root() -> Path:
    env_root = os.environ.get("PLUGIN_ROOT") or os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return Path(__file__).resolve().parents[1]


def emit_system_message(message: str) -> None:
    print(json.dumps({"continue": True, "systemMessage": message}))


def emit_continue() -> None:
    print(json.dumps({"continue": True}))


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild stale Teach concept index.")
    parser.add_argument("--memory-dir", type=Path, default=DEFAULT_MEMORY_DIR)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    memory_dir = args.memory_dir.expanduser()
    if not args.force and not index_is_stale(memory_dir):
        emit_continue()
        return 0

    script = plugin_root() / "skills" / "teach" / "scripts" / "teach_memory.py"
    if not script.exists():
        emit_system_message(f"Teach memory hook skipped: {script} not found.")
        return 0

    result = subprocess.run(
        [sys.executable, str(script), "index", "--memory-dir", str(memory_dir)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        suffix = f" {detail[-1]}" if detail else ""
        emit_system_message(f"Teach memory index rebuild failed.{suffix}")
        return 0

    emit_system_message("Teach memory index rebuilt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

- [ ] **Step 3: Make the hook executable**

Run:

```bash
chmod +x plugins/core/hooks/reindex_teach_memory.py
```

Expected: command exits with status 0.

- [ ] **Step 4: Create the hook config**

Create `plugins/core/hooks/hooks.json` with:

````json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/reindex_teach_memory.py\"",
            "timeout": 30,
            "statusMessage": "Checking Teach memory index"
          }
        ]
      }
    ]
  }
}
````

- [ ] **Step 5: Add the hook path to the Codex plugin manifest**

In `plugins/core/.codex-plugin/plugin.json`, add the top-level hook field after `"skills": "./skills/",`:

````json
  "hooks": "./hooks/hooks.json",
````

The top of the manifest should become:

````json
{
  "name": "core",
  "version": "1.1.0",
  "description": "Agent environment setup, council, communication, reflection, DevRev, session wrap-up, and logging",
  "author": {
    "name": "Aditya Nawal"
  },
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "interface": {
````

- [ ] **Step 6: Validate hook JSON**

Run:

```bash
python3 -m json.tool plugins/core/hooks/hooks.json >/tmp/core-hooks.json
python3 -m json.tool plugins/core/.codex-plugin/plugin.json >/tmp/core-codex-plugin.json
```

Expected: both commands exit with status 0.

- [ ] **Step 7: Validate hook behavior with stale notes**

Run:

```bash
rm -rf /tmp/dex-teach-hook
python3 plugins/core/skills/teach/scripts/teach_memory.py note "Hook Reindex" \
  --memory-dir /tmp/dex-teach-hook \
  --aliases "stop hook,index hook" \
  --tags "codex,hooks,sqlite" \
  --related "SQLite FTS5" \
  --source-context "hook validation" \
  --body $'# Hook Reindex\n\n## Concept\n\nThe hook rebuilds the Teach SQLite index when Markdown notes change.\n'
rm /tmp/dex-teach-hook/index.sqlite3
CLAUDE_PLUGIN_ROOT="$PWD/plugins/core" python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-hook
python3 plugins/core/skills/teach/scripts/teach_memory.py search "stop hook" --memory-dir /tmp/dex-teach-hook
```

Expected output contains:

```text
Teach memory index rebuilt.
Hook Reindex (hook-reindex.md)
```

- [ ] **Step 8: Validate hook no-op behavior**

Run:

```bash
CLAUDE_PLUGIN_ROOT="$PWD/plugins/core" python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-hook >/tmp/dex-teach-hook-noop.json
python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/tmp/dex-teach-hook-noop.json").read_text())
assert data == {"continue": True}, data
print("hook no-op returned continue JSON")
PY
```

Expected:

```text
hook no-op returned continue JSON
```

- [ ] **Step 9: Document plugin-hook runtime constraint in the plan**

Confirm this implementation note stays in the final PR or release notes:

```text
The hook is bundled with the Core Codex plugin. Codex currently loads plugin-bundled hooks only when `[features].plugin_hooks = true`, and non-managed hooks still require trust review through `/hooks`.
```

- [ ] **Step 10: Commit hook support**

Run:

```bash
git add plugins/core/hooks plugins/core/.codex-plugin/plugin.json
git commit -m "feat: add teach memory reindex hook"
```

Expected: commit succeeds.

---

### Task 6: Update Core Plugin Documentation and Metadata

**Files:**
- Modify: `README.md`
- Modify: `plugins/core/.codex-plugin/plugin.json`
- Modify: `plugins/core/.claude-plugin/plugin.json`

- [ ] **Step 1: Update the README intro sentence**

In `README.md`, replace:

```markdown
Dex is a small agent toolkit for the work that keeps repeating: setting up an agent environment, finding the crux of a product problem, checking design quality, shipping Blade-heavy dashboard work, reviewing plans with another model, and turning media or memory into something usable.
```

with:

```markdown
Dex is a small agent toolkit for the work that keeps repeating: setting up an agent environment, teaching unfamiliar concepts before execution, finding the crux of a product problem, checking design quality, shipping Blade-heavy dashboard work, reviewing plans with another model, and turning media or memory into something usable.
```

- [ ] **Step 2: Update the plugin split table**

In `README.md`, replace the `core` row:

```markdown
| `core` | Agent setup, council-style investigation, communication, reflection, DevRev, session wrap-up, session logs | Design implementation, browser tooling, media utilities |
```

with:

```markdown
| `core` | Agent setup, teaching unfamiliar concepts, council-style investigation, communication, reflection, DevRev, session wrap-up, session logs | Design implementation, browser tooling, media utilities |
```

- [ ] **Step 3: Update the Core section description**

In `README.md`, replace:

```markdown
`core` is the control plane. It should stay boring in the best way: setup, routing to durable records, and workflows that help agents reason across context and close sessions cleanly.
```

with:

```markdown
`core` is the control plane. It should stay boring in the best way: setup, teaching, routing to durable records, and workflows that help agents reason across context and close sessions cleanly.
```

- [ ] **Step 4: Add the `teach` skill row**

In the Core skill table in `README.md`, add this row after `dex`:

```markdown
| `teach` | Explaining unfamiliar code, architecture, concepts, alternatives, tradeoffs, and clever functions before execution; recording learned concepts in `~/.agents/memory/teach/` with a hook-refreshed SQLite search index |
```

- [ ] **Step 5: Update Codex plugin manifest text**

In `plugins/core/.codex-plugin/plugin.json`, keep the hook field added in Task 5:

```json
"hooks": "./hooks/hooks.json"
```

Then replace:

```json
"description": "Agent environment setup, council, communication, reflection, DevRev, session wrap-up, and logging"
```

with:

```json
"description": "Agent environment setup, teaching, council, communication, reflection, DevRev, session wrap-up, and logging"
```

Replace:

```json
"shortDescription": "Setup, council, communication, reflection, DevRev, wrap-up, and logging"
```

with:

```json
"shortDescription": "Setup, teaching, council, reflection, DevRev, wrap-up, and logging"
```

Replace:

```json
"longDescription": "Core Dex workflows for agent environment setup, multi-agent council analysis, communication, memory-aware reflection, DevRev workflows, end-of-session wrap-up, meaningful micro-commits, and logging."
```

with:

```json
"longDescription": "Core Dex workflows for agent environment setup, teaching unfamiliar concepts before execution, multi-agent council analysis, communication, memory-aware reflection, DevRev workflows, end-of-session wrap-up, meaningful micro-commits, and logging."
```

- [ ] **Step 6: Update Claude plugin manifest text**

In `plugins/core/.claude-plugin/plugin.json`, replace:

```json
"description": "Agent environment setup, council, communication, reflection, DevRev, session wrap-up, and logging"
```

with:

```json
"description": "Agent environment setup, teaching, council, communication, reflection, DevRev, session wrap-up, and logging"
```

- [ ] **Step 7: Validate manifest JSON**

Run:

```bash
python3 -m json.tool plugins/core/.codex-plugin/plugin.json >/tmp/core-codex-plugin.json
python3 -m json.tool plugins/core/.claude-plugin/plugin.json >/tmp/core-claude-plugin.json
```

Expected: both commands exit with status 0.

- [ ] **Step 8: Commit documentation and metadata**

Run:

```bash
git add README.md plugins/core/.codex-plugin/plugin.json plugins/core/.claude-plugin/plugin.json
git commit -m "docs: list teach in core plugin"
```

Expected: commit succeeds.

---

### Task 7: Validate the Full Skill Surface

**Files:**
- Test: `plugins/core/skills/teach/SKILL.md`
- Test: `plugins/core/skills/teach/agents/openai.yaml`
- Test: `plugins/core/skills/teach/scripts/teach_memory.py`
- Test: `plugins/core/skills/teach/scripts/validate_teach_memory.py`
- Test: `plugins/core/skills/teach/scripts/validate_teach_evals.py`
- Test: `plugins/core/skills/teach/evals/evals.json`
- Test: `plugins/core/hooks/hooks.json`
- Test: `plugins/core/hooks/reindex_teach_memory.py`
- Test: `README.md`
- Test: `plugins/core/.codex-plugin/plugin.json`
- Test: `plugins/core/.claude-plugin/plugin.json`

- [ ] **Step 1: Run skill validation**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/core/skills/teach
```

Expected:

```text
Validation passed
```

If the exact success text differs, accept zero exit code and no reported errors.

- [ ] **Step 2: Run memory script validator**

Run:

```bash
python3 plugins/core/skills/teach/scripts/validate_teach_memory.py
python3 plugins/core/skills/teach/scripts/validate_teach_evals.py
```

Expected:

```text
teach memory validator passed
teach eval suite valid
```

- [ ] **Step 3: Validate hook and direct CLI commands**

Run:

```bash
rm -rf /tmp/dex-teach-final
python3 plugins/core/skills/teach/scripts/teach_memory.py ensure --memory-dir /tmp/dex-teach-final
python3 plugins/core/skills/teach/scripts/teach_memory.py profile --memory-dir /tmp/dex-teach-final --force
python3 plugins/core/skills/teach/scripts/teach_memory.py note "BM25 Ranking" \
  --memory-dir /tmp/dex-teach-final \
  --aliases "ranking function,search scoring" \
  --tags "search,ranking,sqlite" \
  --related "SQLite FTS5,inverted index" \
  --source-context "final validation" \
  --body $'# BM25 Ranking\n\n## Concept\n\nBM25 ranks search matches by term frequency and document length.\n'
rm /tmp/dex-teach-final/index.sqlite3
CLAUDE_PLUGIN_ROOT="$PWD/plugins/core" python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-final
python3 plugins/core/skills/teach/scripts/teach_memory.py search "ranking" --memory-dir /tmp/dex-teach-final
```

Expected output contains:

```text
teach memory ready: /tmp/dex-teach-final
wrote /tmp/dex-teach-final/profile.md
wrote /tmp/dex-teach-final/bm25-ranking.md
indexed 1 concept note(s): /tmp/dex-teach-final/index.sqlite3
Teach memory index rebuilt.
BM25 Ranking (bm25-ranking.md)
```

- [ ] **Step 4: Validate JSON files**

Run:

```bash
python3 -m json.tool plugins/core/.codex-plugin/plugin.json >/tmp/core-codex-plugin.json
python3 -m json.tool plugins/core/.claude-plugin/plugin.json >/tmp/core-claude-plugin.json
python3 -m json.tool plugins/core/hooks/hooks.json >/tmp/core-hooks.json
python3 -m json.tool plugins/core/skills/teach/evals/evals.json >/tmp/teach-evals.json
```

Expected: all commands exit with status 0.

- [ ] **Step 5: Check README parity**

Run:

```bash
rtk grep -n "teach|~/.agents/memory/teach|teaching" README.md plugins/core/.codex-plugin/plugin.json plugins/core/.claude-plugin/plugin.json
rtk grep -n "\"hooks\"|hooks/hooks.json|reindex_teach_memory|CLAUDE_PLUGIN_ROOT" plugins/core/.codex-plugin/plugin.json plugins/core/hooks/hooks.json plugins/core/hooks/reindex_teach_memory.py
```

Expected: matches in README, both plugin manifests, the Codex hook manifest field, and the hook files.

- [ ] **Step 6: Check for stale nested path**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

needles = [
    "records/" + "teach/" + "concepts",
    "memory/" + "records/" + "teach",
    "teach/" + "concepts",
]
paths = [
    Path("plugins/core/skills/teach/SKILL.md"),
    Path("README.md"),
    Path("plugins/core/.codex-plugin/plugin.json"),
    Path("plugins/core/.claude-plugin/plugin.json"),
]
found = []
for path in paths:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            found.append(f"{path}: contains {needle}")
if found:
    print("\n".join(found))
    raise SystemExit(1)
print("no stale nested teach memory path")
PY
```

Expected:

```text
no stale nested teach memory path
```

- [ ] **Step 7: Check diff whitespace**

Run:

```bash
git diff --check -- plugins/core/skills/teach plugins/core/hooks README.md plugins/core/.codex-plugin/plugin.json plugins/core/.claude-plugin/plugin.json
```

Expected: no output.

- [ ] **Step 8: Commit validation cleanup if needed**

If validation caused small file fixes, run:

```bash
git add plugins/core/skills/teach plugins/core/hooks README.md plugins/core/.codex-plugin/plugin.json plugins/core/.claude-plugin/plugin.json
git commit -m "test: validate teach skill"
```

Expected: commit succeeds only if there are validation fixes. Skip this step when there is nothing to commit.

---

### Task 8: Forward-Test the Runtime Behavior

**Files:**
- Test: `plugins/core/skills/teach/SKILL.md`
- Test: `plugins/core/skills/teach/scripts/teach_memory.py`
- Test: `plugins/core/skills/teach/evals/evals.json`

- [ ] **Step 1: Forward-test explicit trigger**

Use a fresh agent or clean session. Prompt:

```text
Use $teach at /Users/aditya.nawal/projects/dex/plugins/core/skills/teach to explain how the script at /Users/aditya.nawal/projects/dex/plugins/core/skills/teach/scripts/teach_memory.py works before suggesting any changes.
```

Expected:

```text
The answer teaches the mental model, names concepts such as frontmatter parsing and SQLite FTS, compares alternatives, explains tradeoffs, and asks one grounding question before implementation.
```

- [ ] **Step 2: Forward-test implicit trigger**

Use a fresh agent or clean session. Prompt:

```text
I don't understand why this code uses SQLite FTS instead of grep. Walk me through the design choice before doing anything.
```

Expected:

```text
The teach behavior triggers implicitly, explains the design choice, compares SQLite FTS with grep and vector embeddings, gives tradeoffs, and does not implement anything before checking whether to proceed.
```

- [ ] **Step 3: Forward-test clever function behavior**

Use a fresh agent or clean session. Prompt:

```text
Write a compact search ranking helper and explain the concepts I would need to read to understand why you shaped it that way.
```

Expected:

```text
The answer includes Concepts Used, Why This Shape, and To Understand This Choice.
```

- [ ] **Step 4: Forward-test frontend-personalized teaching**

Use a fresh agent or clean session. Prompt:

```text
Use $teach at /Users/aditya.nawal/projects/dex/plugins/core/skills/teach. Explain why a React component with an image grid has layout shift, hydration warnings, and inconsistent spacing. Assume the learner is a designer becoming a design engineer and wants detailed frontend mechanics.
```

Expected:

```text
The answer uses the learner profile, explains the issue through user-visible behavior, HTML structure, CSS layout constraints, browser rendering, JavaScript/React rendering, TypeScript or prop invariants when relevant, accessibility, performance, and design-system tradeoffs.
```

- [ ] **Step 5: Forward-test memory behavior without touching real memory**

Use a fresh agent or clean session. Prompt:

```text
Use $teach at /Users/aditya.nawal/projects/dex/plugins/core/skills/teach. Teach me inverted indexes and save the concept using memory dir /tmp/dex-teach-forward-memory.
```

Expected:

```text
The agent writes a Markdown concept note under /tmp/dex-teach-forward-memory, rebuilds /tmp/dex-teach-forward-memory/index.sqlite3, and can search it.
```

- [ ] **Step 6: Run the Dex eval workflow**

Run the project-local Dex eval workflow:

```text
/dex eval plugins/core/skills/teach rounds=3 baseline=none
```

Expected:

```text
The eval run validates suite health before forward runs, uses baseline=none, records response-quality scores, runs hook/index evidence, and reports blocking failures or a release recommendation.
```

If running the slash command is unavailable in the execution environment, run the deterministic health checks and record the skipped clean-context runs:

```bash
python3 -m json.tool plugins/core/skills/teach/evals/evals.json >/tmp/teach-evals.json
python3 plugins/core/skills/teach/scripts/validate_teach_evals.py
python3 plugins/core/skills/teach/scripts/validate_teach_memory.py
CLAUDE_PLUGIN_ROOT="$PWD/plugins/core" python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-forward-memory --force
```

Expected:

```text
teach eval suite valid
teach memory validator passed
Teach memory index rebuilt.
```

- [ ] **Step 7: Patch any failed behavior**

If a forward test fails, patch the smallest relevant file and commit:

```bash
git add plugins/core/skills/teach plugins/core/hooks
git commit -m "fix: tighten teach skill behavior"
```

Expected: commit succeeds only if there are fixes.

---

## Self-Review

Spec coverage:

- Implicit trigger is covered by Task 2 and Task 7.
- Markdown with proper frontmatter is covered by Task 2 and Task 3.
- Shorter memory path is `~/.agents/memory/teach/`, covered by Tasks 2, 3, 4, 6, and 7.
- Learner profile personalization is covered by Task 2, Task 3, Task 4, Task 7, and Task 8.
- Frontend/design-engineering teaching depth is covered by the `Frontend Teaching Lane`, the learner profile, the eval suite, and the forward test.
- SQLite index generation is covered by Task 3, wired as a Codex hook in Task 5, and validated in Tasks 4, 7, and 8.
- Markdown remains canonical and SQLite is generated, covered by Task 2.
- Clever function explanations are covered by Task 2 and Task 7.
- Dex eval-suite setup is covered by Task 4, including response look and feel, negative controls, artifact cases, hook behavior, and benchmark comparison.
- README and manifest parity are covered by Task 6.
- Skill validation and forward tests are covered by Tasks 7 and 8.

Placeholder scan:

- No placeholder markers, copy-forward shortcuts, vague error-handling instructions, or undefined code references remain.
- Every created file has exact content.
- Every command has an expected result.

Type and path consistency:

- Skill paths consistently use `plugins/core/skills/teach`.
- Hook paths consistently use `plugins/core/hooks`.
- User memory paths consistently use `~/.agents/memory/teach/`.
- Learner profile path consistently uses `~/.agents/memory/teach/profile.md`.
- SQLite database path consistently uses `index.sqlite3`.
- The implementation uses only Python standard library modules.
