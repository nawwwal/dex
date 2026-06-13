#!/usr/bin/env python3
"""Validate the durable diverge eval suite shape and coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {"skill_name", "version", "skill_type", "coverage_requirements", "evals"}
REQUIRED_EVAL_FIELDS = {
    "id",
    "category",
    "should_trigger",
    "prompt",
    "expected_output",
    "assertions",
    "deterministic_checks",
}
REQUIRED_CATEGORIES = {
    "explicit-trigger",
    "implicit-trigger",
    "contextual-trigger",
    "negative-control",
    "known-failure",
    "artifact",
    "repair-regression",
    "compact-mode",
    "deep-mode",
    "altitude-detection",
    "companion-routing",
    "layer-quality",
    "register",
    "output-mode",
    "state-handling",
    "slop-firewall",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_check_groups(eval_id: str, checks: dict) -> None:
    if not isinstance(checks, dict):
        fail(f"{eval_id}: deterministic_checks must be an object")

    allowed = {"must_include_any", "must_not_include_any"}
    unknown = set(checks) - allowed
    if unknown:
        fail(f"{eval_id}: unknown deterministic check keys: {sorted(unknown)}")

    if not checks:
        fail(f"{eval_id}: deterministic_checks must not be empty")

    for key, groups in checks.items():
        if not isinstance(groups, list) or not groups:
            fail(f"{eval_id}: {key} must be a non-empty list")
        for group in groups:
            if not isinstance(group, list) or not group:
                fail(f"{eval_id}: every {key} group must be a non-empty list")
            if not all(isinstance(item, str) and item.strip() for item in group):
                fail(f"{eval_id}: every {key} entry must be a non-empty string")


def main() -> None:
    suite_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).parents[1] / "evals" / "exhaustive-suite.json"
    )
    skill_root = suite_path.parents[1]

    data = json.loads(suite_path.read_text())
    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        fail(f"missing top-level keys: {sorted(missing_top)}")

    if data["skill_name"] != "diverge":
        fail("skill_name must be diverge")

    coverage = set(data["coverage_requirements"])
    missing_coverage = REQUIRED_CATEGORIES - coverage
    if missing_coverage:
        fail(f"coverage_requirements missing: {sorted(missing_coverage)}")

    evals = data["evals"]
    if not isinstance(evals, list) or len(evals) < 30:
        fail("expected at least 30 eval cases for exhaustive diverge coverage")

    seen_ids: set[str] = set()
    categories: set[str] = set()
    trigger_values = {True: 0, False: 0}

    for case in evals:
        missing = REQUIRED_EVAL_FIELDS - set(case)
        if missing:
            fail(f"{case.get('id', '<missing-id>')}: missing keys {sorted(missing)}")

        eval_id = case["id"]
        if eval_id in seen_ids:
            fail(f"duplicate eval id: {eval_id}")
        seen_ids.add(eval_id)

        category = case["category"]
        categories.add(category)
        if category not in coverage:
            fail(f"{eval_id}: category {category!r} not listed in coverage_requirements")

        should_trigger = case["should_trigger"]
        if not isinstance(should_trigger, bool):
            fail(f"{eval_id}: should_trigger must be boolean")
        trigger_values[should_trigger] += 1

        if not isinstance(case["assertions"], list) or len(case["assertions"]) < 2:
            fail(f"{eval_id}: expected at least two assertions")

        validate_check_groups(eval_id, case["deterministic_checks"])

        for file_path in case.get("files", []):
            candidate = skill_root / file_path
            if not candidate.exists():
                fail(f"{eval_id}: fixture does not exist: {file_path}")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(f"evals missing required categories: {sorted(missing_categories)}")

    if trigger_values[True] < 24:
        fail("expected at least 24 positive trigger cases")
    if trigger_values[False] < 4:
        fail("expected at least 4 negative-control cases")

    repair_cases = [case for case in evals if case["category"] == "repair-regression"]
    if len(repair_cases) < 5:
        fail("expected at least five repair-regression cases")

    artifact_cases = [case for case in evals if case["category"] == "artifact"]
    if len(artifact_cases) < 3:
        fail("expected at least three artifact cases")

    print(
        f"OK: {len(evals)} evals, {len(categories)} categories, "
        f"{trigger_values[True]} trigger cases, {trigger_values[False]} negative controls"
    )


if __name__ == "__main__":
    main()
