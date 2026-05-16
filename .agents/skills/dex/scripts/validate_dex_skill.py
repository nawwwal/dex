#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parents[4]
AGENTS = REPO / ".agents" / "skills" / "dex"
CLAUDE = REPO / ".claude" / "skills" / "dex"
CODEX_LINK = REPO / ".codex" / "skills" / "dex"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(REPO)}")
    return path.read_text(encoding="utf-8")


def require(text: str, pattern: str, label: str) -> None:
    if not re.search(pattern, text, re.IGNORECASE | re.DOTALL | re.MULTILINE):
        fail(f"{label} missing pattern: {pattern}")


def require_file(path: Path) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(REPO)}")


def validate_skill_md() -> None:
    agents_skill = read(AGENTS / "SKILL.md")
    claude_skill = read(CLAUDE / "SKILL.md")

    for label, text in {
        ".agents/skills/dex/SKILL.md": agents_skill,
        ".claude/skills/dex/SKILL.md": claude_skill,
    }.items():
        require(text, r"name:\s*dex", label)
        require(text, r"description:.*plugin releases", label)
        require(text, r"description:.*skill evals", label)
        require(text, r"description:.*multi-round skill repair", label)
        require(text, r"argument-hint:.*release.*eval", label)
        require(text, r"\*\*release\*\*\s*->\s*Read `\./release\.md`", label)
        require(text, r"\*\*eval\*\*\s*->\s*Read `\./eval\.md`", label)
        require(text, r"\*\*skill eval / benchmark / repair intent\*\*\s*->\s*Read `\./eval\.md`", label)
        require(text, r"If no argument: ask whether to run a plugin release or a skill eval\.", label)

    require(claude_skill, r"disable-model-invocation:\s*true", ".claude/skills/dex/SKILL.md")


def validate_mirrored_docs() -> None:
    for name in ("release.md", "eval.md", "eval-framework.md"):
        agents_text = read(AGENTS / name)
        claude_text = read(CLAUDE / name)
        if agents_text != claude_text:
            fail(f"{name} differs between .agents and .claude dex skills")

    eval_md = read(AGENTS / "eval.md")
    for pattern in (
        r"rounds=3",
        r"Stop after round 2 only if",
        r"skill-creator/SKILL\.md",
        r"Repair with skill-creator",
        r"Re-run the same evals",
        r"If round 3 still has critical failures",
    ):
        require(eval_md, pattern, ".agents/skills/dex/eval.md")

    framework = read(AGENTS / "eval-framework.md")
    for pattern in (
        r"explicit trigger",
        r"implicit trigger",
        r"contextual trigger",
        r"negative-control",
        r"known failure",
        r"Judge Rubric",
        r"Benchmark Shape",
        r"Codex Exec Launch",
        r"codex exec",
        r"--model gpt-5\.5",
        r"model_reasoning_effort",
        r"Do not default to `gpt-5\.4-mini`",
        r"Diagnosis Labels",
        r"Stop Criteria",
        r"round 3",
    ):
        require(framework, pattern, ".agents/skills/dex/eval-framework.md")


def validate_scripts_and_link() -> None:
    require_file(AGENTS / "scripts" / "validate_dex_skill.py")
    require_file(CLAUDE / "scripts" / "validate_dex_skill.py")

    if not CODEX_LINK.is_symlink():
        fail(".codex/skills/dex must remain a symlink")
    target = os.readlink(CODEX_LINK)
    if target != "../../.claude/skills/dex":
        fail(f".codex/skills/dex symlink target changed: {target}")


def validate_repo_docs() -> None:
    readme = read(REPO / "README.md")
    require(readme, r"/dex eval plugins/design/skills/crux", "README.md")
    require(readme, r"skill-creator", "README.md")
    require(readme, r"\.dex/evals/", "README.md")

    gitignore = read(REPO / ".gitignore")
    require(gitignore, r"^\.dex/evals/$", ".gitignore")


def main() -> int:
    validate_skill_md()
    validate_mirrored_docs()
    validate_scripts_and_link()
    validate_repo_docs()
    print("PASS: dex skill eval workflow is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
