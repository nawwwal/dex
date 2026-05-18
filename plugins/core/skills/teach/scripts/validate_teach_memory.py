#!/usr/bin/env python3
"""Validate Teach concept memory indexing without touching user memory."""

from __future__ import annotations

import json
import os
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
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"


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


def hook_command() -> str:
    data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    return data["hooks"]["Stop"][0]["hooks"][0]["command"]


def run_configured_hook(memory_dir: Path, include_plugin_root: bool) -> subprocess.CompletedProcess[str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(Path.home()),
        "TEACH_MEMORY_DIR": str(memory_dir),
    }
    if include_plugin_root:
        env["CLAUDE_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    result = subprocess.run(
        hook_command(),
        text=True,
        capture_output=True,
        check=False,
        shell=True,
        env=env,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"configured hook failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"configured hook did not emit JSON: {result.stdout!r}") from exc
    if payload.get("continue") is not True:
        raise AssertionError(f"configured hook must continue, got {payload}")
    return result


def main() -> int:
    tmp_root = Path(tempfile.mkdtemp(prefix="dex-teach-memory-"))
    memory_dir = tmp_root / "teach"
    try:
        run("validate", "--memory-dir", str(memory_dir))
        missing_root_result = run_configured_hook(memory_dir, include_plugin_root=False)
        if "plugin root env missing" not in missing_root_result.stdout:
            raise AssertionError("configured hook without plugin root must skip safely with a system message")
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

        configured_result = run_configured_hook(memory_dir, include_plugin_root=True)
        if not configured_result.stdout.strip().startswith("{"):
            raise AssertionError(f"configured hook must emit JSON, got {configured_result.stdout!r}")

        print("teach memory validator passed")
        return 0
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
