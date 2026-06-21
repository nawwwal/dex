#!/usr/bin/env python3
"""Validate the nemesis fun skill: frontmatter, auto-invocation, references, scripts, and contract."""
from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

NAME = 'nemesis'
REQUIRED_STRINGS = ['survivor', 'judge', 'convictions']
REQUIRED_SCRIPTS = []
REQUIRED_FILES = ['references/judge.md']


def fail(message: str) -> None:
    print(f"FAIL[{NAME}]: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1]
    if root.name != NAME:
        fail(f"skill directory {root.name!r} does not match {NAME!r}")
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        fail("missing SKILL.md")
    text = skill_md.read_text()

    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("missing YAML frontmatter")
    front = match.group(1)
    if not re.search(rf"^name:\s*{NAME}\s*$", front, re.M):
        fail(f"frontmatter name must be {NAME!r}")
    desc = re.search(r'^description:\s*"?(.+)', front, re.M)
    if not desc or len(desc.group(1)) < 80:
        fail("description missing or too short for reliable auto-invocation")
    if re.search(r"^disable-model-invocation:\s*true", front, re.M):
        fail("fun skills must stay model-invocable (no disable-model-invocation: true)")

    plugin_root = root.parents[1]
    refs = sorted(set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s`\")\]]+)", text)))
    for ref in refs:
        if not (plugin_root / ref).exists():
            fail(f"referenced file does not exist: {ref}")

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            fail(f"missing required file: {rel}")

    for rel in REQUIRED_SCRIPTS:
        path = root / rel
        if not path.exists():
            fail(f"missing required script: {rel}")
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"script does not compile: {rel}: {exc}")

    lowered = text.lower()
    for needle in REQUIRED_STRINGS:
        if needle.lower() not in lowered:
            fail(f"SKILL.md must preserve contract phrase: {needle!r}")

    print(f"OK: {NAME} skill frontmatter, references, scripts, and contract are valid")


if __name__ == "__main__":
    main()
