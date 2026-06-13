#!/usr/bin/env python3
"""Validate the media-tools skill contract, references, script, and eval suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_REFERENCE_MENTIONS = [
    "references/generate.md",
    "references/optimize.md",
]

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
    "routing",
    "generate",
    "optimize",
    "explicit-trigger",
    "implicit-trigger",
    "negative-control",
    "companion-routing",
    "repair-regression",
}

PINNED_OPTIMO = "optimo@0.0.24"
FLASH_MODEL = "gemini-3.1-flash-image-preview"
PRO_MODEL = "gemini-3-pro-image-preview"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def validate_frontmatter(skill_md: str) -> None:
    if "name: media-tools" not in skill_md:
        fail("SKILL.md frontmatter must set name: media-tools")
    if "disable-model-invocation: true" not in skill_md:
        fail("SKILL.md must keep disable-model-invocation: true")
    if "Replaces generate-image and media-optimizer" not in skill_md:
        fail("SKILL.md description must mention replacing legacy skills")


def validate_check_groups(eval_id: str, checks: dict) -> None:
    if not isinstance(checks, dict) or not checks:
        fail(f"{eval_id}: deterministic_checks must be a non-empty object")

    allowed = {"must_include_any", "must_not_include_any"}
    unknown = set(checks) - allowed
    if unknown:
        fail(f"{eval_id}: unknown deterministic check keys: {sorted(unknown)}")

    for key, groups in checks.items():
        if not isinstance(groups, list) or not groups:
            fail(f"{eval_id}: {key} must be a non-empty list")
        for group in groups:
            if not isinstance(group, list) or not group:
                fail(f"{eval_id}: every {key} group must be a non-empty list")
            if not all(isinstance(item, str) and item.strip() for item in group):
                fail(f"{eval_id}: every {key} entry must be a non-empty string")


def validate_eval_suite(skill_root: Path) -> None:
    suite_path = skill_root / "evals" / "exhaustive-suite.json"
    data = json.loads(read(suite_path))

    if data.get("skill_name") != "media-tools":
        fail("exhaustive-suite.json skill_name must be media-tools")

    coverage = set(data.get("coverage_requirements", []))
    missing_coverage = REQUIRED_CATEGORIES - coverage
    if missing_coverage:
        fail(f"coverage_requirements missing: {sorted(missing_coverage)}")

    evals = data.get("evals", [])
    if not isinstance(evals, list) or len(evals) < 18:
        fail("expected at least 18 eval cases for exhaustive media-tools coverage")

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

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(f"evals missing required categories: {sorted(missing_categories)}")

    if trigger_values[True] < 14:
        fail("expected at least 14 positive trigger cases")
    if trigger_values[False] < 4:
        fail("expected at least 4 negative-control cases")


def main() -> None:
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1]
    skill_md = read(skill_root / "SKILL.md")
    generate_md = read(skill_root / "references" / "generate.md")
    optimize_md = read(skill_root / "references" / "optimize.md")
    generate_py = read(skill_root / "scripts" / "generate.py")

    validate_frontmatter(skill_md)

    for mention in REQUIRED_REFERENCE_MENTIONS:
        if mention not in skill_md:
            fail(f"SKILL.md must mention {mention}")

    if PINNED_OPTIMO not in skill_md or PINNED_OPTIMO not in optimize_md:
        fail(f"SKILL.md and optimize.md must pin {PINNED_OPTIMO}")

    if FLASH_MODEL not in generate_md or PRO_MODEL not in generate_md:
        fail("generate.md must document allowed Gemini model IDs")

    if "gemini-2.5-flash-image" not in generate_md:
        fail("generate.md must ban legacy gemini-2.x image models")

    if "scripts/generate.py" not in skill_md:
        fail("SKILL.md must reference scripts/generate.py")

    if "media-tools" not in generate_py:
        fail("generate.py docstring should identify media-tools skill")

    if "skills/generate-image" in skill_md or "/generate-image" in skill_md:
        fail("SKILL.md must not reference legacy generate-image invocation paths")

    validate_eval_suite(skill_root)

    print("OK: media-tools skill contract, references, script, and eval suite are valid")


if __name__ == "__main__":
    main()
