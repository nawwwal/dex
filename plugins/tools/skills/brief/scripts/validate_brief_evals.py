#!/usr/bin/env python3
"""Validate the brief eval suite shape and coverage."""

from __future__ import annotations

import json
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]
EVALS = ROOT / "evals" / "evals.json"

REQUIRED_COVERAGE = {
    "explicit trigger",
    "implicit trigger",
    "negative-control",
    "artifact case",
    "eval suite health",
    "response quality",
    "normal-user prompts",
    "contextual trigger",
    "dynamic sectioning",
    "blackline visuals",
    "no image placeholders",
    "inline links and read next",
    "floating switcher",
    "roller switcher",
    "scroll containment",
    "adaptive theme",
    "route away from decks",
}

ALLOWED_CATEGORIES = {"positive", "negative-control", "known-failure"}
ALLOWED_RUN_MODES = {"clean-context-forward", "deterministic-or-clean-context"}
SPECIALIZED_FORWARD_PROMPT_TERMS = {
    "$brief",
    "evals/fixtures",
    "deterministic_checks",
    "run_mode",
    "assertions",
    "expected_output",
}


def fail(message: str) -> None:
    raise SystemExit(f"brief eval validation failed: {message}")


def resolve_fixture(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "evals":
        return ROOT / path
    return ROOT / "evals" / path


def command_paths_exist(case_id: str, command: str) -> None:
    for token in shlex.split(command):
        if not token.startswith("plugins/"):
            continue
        if token.endswith((".py", ".js", ".json", ".html", ".css")) and not (REPO_ROOT / token).exists():
            fail(f"{case_id} deterministic command references missing path {token}")


def validate_checks(case_id: str, checks: dict) -> None:
    if not isinstance(checks, dict) or not checks:
        fail(f"{case_id} deterministic_checks must be a non-empty object")
    for key in ("commands", "must_include_any", "must_not_include_any"):
        if key not in checks:
            continue
        if key == "commands":
            if not isinstance(checks[key], list) or not all(isinstance(command, str) for command in checks[key]):
                fail(f"{case_id} commands must be a list of strings")
            for command in checks[key]:
                command_paths_exist(case_id, command)
            continue
        groups = checks[key]
        if not isinstance(groups, list):
            fail(f"{case_id} {key} must be a list")
        for group in groups:
            if not isinstance(group, list) or not group:
                fail(f"{case_id} every {key} group must be non-empty")
            if not all(isinstance(item, str) and item.strip() for item in group):
                fail(f"{case_id} every {key} entry must be a non-empty string")


def main() -> int:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "brief":
        fail("skill_name must be brief")
    if data.get("skill_type") != "artifact":
        fail("skill_type must be artifact")

    standards = data.get("standards", {})
    missing = REQUIRED_COVERAGE - set(standards.get("required_coverage", []))
    if missing:
        fail(f"standards.required_coverage missing {sorted(missing)}")

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 8:
        fail("evals must include at least eight focused cases")

    ids: set[str] = set()
    coverage_seen: set[str] = set()
    negative_count = 0
    artifact_count = 0
    normal_prompt_count = 0

    for case in evals:
        case_id = case.get("id")
        if not case_id:
            fail("case missing id")
        if case_id in ids:
            fail(f"duplicate id {case_id}")
        ids.add(case_id)

        for key in ("category", "coverage", "should_trigger", "run_mode", "prompt", "expected_output", "assertions", "required_evidence", "deterministic_checks"):
            if key not in case:
                fail(f"{case_id} missing {key}")

        if case["category"] not in ALLOWED_CATEGORIES:
            fail(f"{case_id} category must be one of {sorted(ALLOWED_CATEGORIES)}")
        if case["run_mode"] not in ALLOWED_RUN_MODES:
            fail(f"{case_id} run_mode must be one of {sorted(ALLOWED_RUN_MODES)}")
        if case["run_mode"] == "clean-context-forward":
            prompt = case["prompt"]
            if any(term in prompt for term in SPECIALIZED_FORWARD_PROMPT_TERMS):
                fail(f"{case_id} clean-context-forward prompt is too eval-specific")
            if "normal-user prompts" in case["coverage"]:
                normal_prompt_count += 1
        if not isinstance(case["should_trigger"], bool):
            fail(f"{case_id} should_trigger must be boolean")
        if case["category"] == "negative-control":
            negative_count += 1
            if case["should_trigger"] is not False:
                fail(f"{case_id} negative-control must set should_trigger false")

        coverage = case["coverage"]
        if not isinstance(coverage, list) or not coverage:
            fail(f"{case_id} coverage must be a non-empty list")
        coverage_seen.update(coverage)

        files = case.get("files", [])
        if "artifact case" in coverage:
            artifact_count += 1
            if not files:
                fail(f"{case_id} artifact case needs fixture files")
        for file_name in files:
            if not resolve_fixture(file_name).exists():
                fail(f"{case_id} fixture missing: {file_name}")

        if not isinstance(case["assertions"], list) or len(case["assertions"]) < 3:
            fail(f"{case_id} needs at least three assertions")
        if not isinstance(case["required_evidence"], list) or not case["required_evidence"]:
            fail(f"{case_id} needs required evidence")

        validate_checks(case_id, case["deterministic_checks"])

    missing_cases = REQUIRED_COVERAGE - coverage_seen
    if missing_cases:
        fail(f"no eval case covers {sorted(missing_cases)}")
    if negative_count < 3:
        fail("at least three negative controls are required")
    if artifact_count < 4:
        fail("at least four artifact-backed cases are required")
    if normal_prompt_count < 5:
        fail("at least five clean-context cases must use normal-user prompts")

    print("brief eval suite valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
