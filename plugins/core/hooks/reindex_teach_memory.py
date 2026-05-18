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
EXCLUDED_MARKDOWN = {"readme.md", "profile.md"}


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
    parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path(os.environ.get("TEACH_MEMORY_DIR", DEFAULT_MEMORY_DIR)),
    )
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
