#!/usr/bin/env python3
"""Validate the crux skill contract, references, and durable eval suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_REFERENCE_MENTIONS = [
    "references/protocol.md",
    "references/layered-pipeline.md",
    "references/evidence-and-tests.md",
    "references/examples.md",
]

REQUIRED_REGRESSION_IDS = {
    "repair-regression-placeholder-bet",
    "repair-regression-no-shape-first",
    "repair-regression-source-before-question",
    "repair-regression-dashboard-accountability",
    "repair-regression-read-only-update",
    "repair-regression-source-prd-legibility",
}

STRATEGY_BANNED_OPENINGS = {
    "go deep",
    "go wide",
    "do both",
    "it depends",
    "my recommendation: go deep",
}

PROHIBITED_VISIBLE_METHOD_HEADINGS = {
    "dao:",
    "qi:",
    "evidence ledger:",
    "method agent:",
    "ground truth pass:",
    "crux candidate collation:",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def main() -> None:
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1]
    skill_md = read(skill_root / "SKILL.md")
    suite_path = skill_root / "evals" / "exhaustive-suite.json"

    for mention in REQUIRED_REFERENCE_MENTIONS:
        if mention not in skill_md:
            fail(f"SKILL.md must mention {mention}")
        if not (skill_root / mention).exists():
            fail(f"referenced file does not exist: {mention}")

    if "Layered Pipeline Mode" not in skill_md:
        fail("SKILL.md must keep Layered Pipeline Mode explicit")
    if "Strategy Frame Gate" not in skill_md:
        fail("SKILL.md must keep Strategy Frame Gate explicit")
    if "read-only by default" not in skill_md:
        fail("SKILL.md must preserve read-only default")

    subprocess.run(
        [sys.executable, str(skill_root / "scripts" / "validate_eval_suite.py"), str(suite_path)],
        check=True,
    )

    suite = json.loads(read(suite_path))
    evals = suite["evals"]
    ids = {case["id"] for case in evals}
    missing_regressions = REQUIRED_REGRESSION_IDS - ids
    if missing_regressions:
        fail(f"missing required regression IDs: {sorted(missing_regressions)}")

    strategy_cases = [case for case in evals if case["category"] == "strategy-frame"]
    if len(strategy_cases) < 3:
        fail("expected at least three strategy-frame eval cases")

    strategy_text = json.dumps(strategy_cases).lower()
    for phrase in STRATEGY_BANNED_OPENINGS:
        if phrase not in strategy_text:
            fail(f"strategy evals must guard banned opening/recommendation: {phrase}")

    visible_surfaces = [
        skill_root / "SKILL.md",
        skill_root / "references" / "examples.md",
        skill_root / "evals" / "core-behavior.md",
    ]
    for surface in visible_surfaces:
        text = read(surface)
        for heading in PROHIBITED_VISIBLE_METHOD_HEADINGS:
            if f"\n{heading}" in text.lower():
                fail(f"{surface.name} leaks visible method heading {heading!r}")

    openai_yaml = read(skill_root / "agents" / "openai.yaml")
    if "Crux" not in openai_yaml or "core bet" not in openai_yaml:
        fail("agents/openai.yaml looks stale for the current crux contract")

    print("OK: crux skill contract, references, metadata, and eval suite are valid")


if __name__ == "__main__":
    main()
