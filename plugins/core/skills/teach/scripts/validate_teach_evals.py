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
        for key in (
            "category",
            "coverage",
            "should_trigger",
            "run_mode",
            "prompt",
            "expected_output",
            "assertions",
            "required_evidence",
        ):
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
