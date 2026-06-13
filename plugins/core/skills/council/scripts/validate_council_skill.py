#!/usr/bin/env python3
"""Validate the council skill contract, references, and durable eval suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_REFERENCE_MENTIONS = [
    "references/router.md",
    "references/synthesis.md",
    "references/depths.md",
]

OPTIONAL_POST_REDESIGN = [
    "references/lens-composer.md",
    "references/domain-overlays.md",
    "references/lens-archetypes.md",
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

    if "devil's advocate" not in skill_md.lower() and "devil" not in skill_md.lower():
        fail("SKILL.md must require devil's advocate lens")

    if "disable-model-invocation: true" not in skill_md:
        fail("SKILL.md must keep disable-model-invocation: true")

    subprocess.run(
        [sys.executable, str(skill_root / "scripts" / "validate_eval_suite.py"), str(suite_path)],
        check=True,
    )

    suite = json.loads(read(suite_path))
    evals = suite["evals"]
    ids = {case["id"] for case in evals}

    required_artifact_ids = {
        "artifact-onboarding-flow",
        "artifact-product-prioritization",
        "artifact-kyc-copy",
    }
    missing_artifacts = required_artifact_ids - ids
    if missing_artifacts:
        fail(f"missing required artifact eval IDs: {sorted(missing_artifacts)}")

    debate_cases = [case for case in evals if case["category"] == "debate-format"]
    if len(debate_cases) < 2:
        fail("expected at least two debate-format eval cases")

    # Post-redesign references are optional until Task 3
    post_redesign = all((skill_root / ref).exists() for ref in OPTIONAL_POST_REDESIGN)
    if post_redesign:
        for mention in OPTIONAL_POST_REDESIGN:
            if mention not in skill_md:
                fail(f"SKILL.md must mention {mention} after lens redesign")

    print("OK: council skill contract, references, and eval suite are valid")


if __name__ == "__main__":
    main()
