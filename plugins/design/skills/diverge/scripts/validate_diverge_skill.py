#!/usr/bin/env python3
"""Validate the diverge skill contract, references, and durable eval suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_REFERENCE_MENTIONS = [
    "references/divergence-axes.md",
    "references/concept-enrichment.md",
    "references/companion-skill-routing.md",
    "references/bluff-and-slop-firewall.md",
    "references/copywriting-divergence.md",
    "references/interaction-divergence.md",
]

REQUIRED_REGRESSION_IDS = {
    "repair-regression-companion-visible",
    "repair-regression-compact-not-deep",
    "repair-regression-api-down-vs-auth",
    "repair-regression-obvious-baseline-verdict",
    "repair-regression-layers-changed-required",
}

LEGACY_MARKDOWN_EVALS = [
    "evals/agent-dashboard.md",
    "evals/calibrate-bar.md",
    "evals/companion-skill-routing.md",
    "evals/connector-health.md",
    "evals/emotional-payment-failure.md",
    "evals/product-vs-brand-register.md",
    "evals/refund-step.md",
    "evals/user-education.md",
]


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

    if "Compact mode is the default" not in skill_md:
        fail("SKILL.md must keep compact mode as default")
    if "Companion Skill Routing Gate" not in skill_md:
        fail("SKILL.md must keep Companion Skill Routing Gate explicit")
    if "A direction only counts if it changes a specific design layer" not in skill_md:
        fail("SKILL.md must preserve layer-change principle")

    for legacy_eval in LEGACY_MARKDOWN_EVALS:
        if not (skill_root / legacy_eval).exists():
            fail(f"missing legacy markdown eval retained for human review: {legacy_eval}")

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

    companion_cases = [case for case in evals if case["category"] == "companion-routing"]
    if len(companion_cases) < 4:
        fail("expected at least four companion-routing eval cases")

    slop_cases = [case for case in evals if case["category"] == "slop-firewall"]
    if len(slop_cases) < 2:
        fail("expected at least two slop-firewall eval cases")

    print("OK: diverge skill contract, references, legacy evals, and eval suite are valid")


if __name__ == "__main__":
    main()
