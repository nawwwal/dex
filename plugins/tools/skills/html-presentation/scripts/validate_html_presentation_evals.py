#!/usr/bin/env python3
"""Validate the html-presentation eval suite shape and coverage."""

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
    "contextual trigger",
    "negative-control",
    "known failure",
    "artifact case",
    "eval suite health",
    "repair regression",
    "benchmark comparison",
    "response quality",
    "revealjs docs routing",
    "working deck artifact",
    "full-bleed layout",
    "visual system consistency",
    "accessibility contrast",
    "synthetic javascript generation",
    "configuration profile",
    "motion guidance",
    "speaker notes and export",
    "brand reference grounding",
    "present handoff",
    "no generic slideware",
    "negative route away",
}

REQUIRED_QUALITY = {
    "Builds or specifies an actual browser-native Reveal.js deck artifact, not just an outline.",
    "Uses current Reveal.js documentation for syntax, configuration, plugins, and version-sensitive behavior.",
    "Chooses a deck-wide visual system before styling individual slides.",
    "Keeps typography, color foundations, and object language consistent across slides.",
    "Uses Reveal.js background attributes or generated equivalents for full-viewport backgrounds.",
    "Verifies readable contrast for body text, labels, panels, muted text, and code.",
    "Uses speaker notes, fragments, vertical stacks, and appendix slides only when they serve the presentation.",
    "Generates JavaScript decks from structured data with validation, stable IDs, typed renderers, and safe text handling.",
    "States configuration profile assumptions and tradeoffs for standalone, embedded, kiosk, docs, or report contexts.",
    "Routes narrative-only presentation coaching to present and non-HTML deck creation to the appropriate deck/Figma workflow.",
}

ALLOWED_RUN_MODES = {"clean-context-forward", "deterministic-or-clean-context"}
ALLOWED_CATEGORIES = {"positive", "contextual", "negative-control", "known-failure", "benchmark"}
ALLOWED_DETERMINISTIC_KEYS = {"commands", "must_include_any", "must_not_include_any"}
QUALITY_MINIMUMS = {"pass_threshold", "scale", "evidence_rule"}
BENCHMARK_FIELDS = {"baseline", "runs", "score_dimensions", "must_record"}
BENCHMARK_MUST_RECORD = {
    "pass_rate",
    "routing_accuracy",
    "time_seconds",
    "tokens_or_unknown",
    "turns_or_commands",
    "quality_delta",
    "accepted_cost_tradeoff",
}


def fail(message: str) -> None:
    raise SystemExit(f"html-presentation eval validation failed: {message}")


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
        if token.endswith((".py", ".js", ".json")) and not (REPO_ROOT / token).exists():
            fail(f"{case_id} deterministic command references missing path {token}")


def validate_check_groups(case_id: str, checks: dict) -> None:
    if not isinstance(checks, dict) or not checks:
        fail(f"{case_id} deterministic_checks must be a non-empty object")
    unknown = set(checks) - ALLOWED_DETERMINISTIC_KEYS
    if unknown:
        fail(f"{case_id} deterministic_checks has unknown keys {sorted(unknown)}")

    commands = checks.get("commands", [])
    if commands:
        if not isinstance(commands, list) or not all(isinstance(command, str) for command in commands):
            fail(f"{case_id} deterministic commands must be strings")
        for command in commands:
            command_paths_exist(case_id, command)

    for key in ("must_include_any", "must_not_include_any"):
        if key not in checks:
            continue
        groups = checks[key]
        if not isinstance(groups, list):
            fail(f"{case_id} {key} must be a list")
        for group in groups:
            if not isinstance(group, list) or not group:
                fail(f"{case_id} every {key} group must be a non-empty list")
            if not all(isinstance(item, str) and item.strip() for item in group):
                fail(f"{case_id} every {key} entry must be a non-empty string")


def main() -> int:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "html-presentation":
        fail("skill_name must be html-presentation")
    if data.get("skill_type") != "mixed":
        fail("skill_type must be mixed")

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 14:
        fail("evals must include at least 14 focused cases")

    standards = data.get("standards", {})
    required = set(standards.get("required_coverage", []))
    missing_required = REQUIRED_COVERAGE - required
    if missing_required:
        fail(f"standards.required_coverage missing {sorted(missing_required)}")

    quality = set(standards.get("response_quality", []))
    missing_quality = REQUIRED_QUALITY - quality
    if missing_quality:
        fail(f"standards.response_quality missing {sorted(missing_quality)}")

    quality_grading = standards.get("quality_grading")
    if not isinstance(quality_grading, dict) or not QUALITY_MINIMUMS <= set(quality_grading):
        fail("standards.quality_grading must define scale, pass_threshold, and evidence_rule")
    threshold = quality_grading.get("pass_threshold")
    if not isinstance(threshold, (int, float)) or not 0 < threshold <= 1:
        fail("standards.quality_grading.pass_threshold must be between 0 and 1")

    benchmark_requirements = standards.get("benchmark_requirements")
    if not isinstance(benchmark_requirements, dict):
        fail("standards.benchmark_requirements must be an object")
    missing_benchmark_record = BENCHMARK_MUST_RECORD - set(benchmark_requirements.get("must_record", []))
    if missing_benchmark_record:
        fail(f"standards.benchmark_requirements.must_record missing {sorted(missing_benchmark_record)}")

    ids: set[str] = set()
    coverage_seen: set[str] = set()
    categories_seen: set[str] = set()
    rubric_count = 0
    negative_count = 0
    artifact_count = 0

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

        category = case["category"]
        categories_seen.add(category)
        if category not in ALLOWED_CATEGORIES:
            fail(f"{case_id} category must be one of {sorted(ALLOWED_CATEGORIES)}")
        if category == "negative-control":
            negative_count += 1

        if not isinstance(case["should_trigger"], bool):
            fail(f"{case_id} should_trigger must be boolean")
        if category == "negative-control" and case["should_trigger"] is not False:
            fail(f"{case_id} negative-control must set should_trigger false")
        if case["run_mode"] not in ALLOWED_RUN_MODES:
            fail(f"{case_id} run_mode must be one of {sorted(ALLOWED_RUN_MODES)}")

        if not isinstance(case["assertions"], list) or len(case["assertions"]) < 3:
            fail(f"{case_id} needs at least three assertions")
        if not isinstance(case["required_evidence"], list) or not case["required_evidence"]:
            fail(f"{case_id} needs required evidence")

        files = case.get("files", [])
        if files:
            if not isinstance(files, list):
                fail(f"{case_id} files must be a list")
            for file_name in files:
                if not isinstance(file_name, str):
                    fail(f"{case_id} file entries must be strings")
                if not resolve_fixture(file_name).exists():
                    fail(f"{case_id} fixture missing: {file_name}")

        coverage = case["coverage"]
        if not isinstance(coverage, list) or not coverage:
            fail(f"{case_id} coverage must be a non-empty list")
        coverage_seen.update(coverage)
        if "artifact case" in coverage:
            artifact_count += 1
            if not files:
                fail(f"{case_id} artifact case needs fixture files")

        if "response quality" in coverage:
            rubric = case.get("quality_rubric")
            if not isinstance(rubric, dict) or not rubric:
                fail(f"{case_id} covers response quality but has no quality_rubric")
            for dimension, weight in rubric.items():
                if not isinstance(dimension, str) or not isinstance(weight, int) or not 1 <= weight <= 3:
                    fail(f"{case_id} quality_rubric values must be integer weights 1-3")
            rubric_count += 1

        deterministic = case.get("deterministic_checks")
        if not deterministic:
            fail(f"{case_id} missing deterministic_checks")
        validate_check_groups(case_id, deterministic)

        if category == "known-failure" and case_id != "eval-suite-health-before-forward-run":
            for key in ("known_failure_source", "before_failure_signal", "fixed_by"):
                if key not in case:
                    fail(f"{case_id} missing {key}")

        if "benchmark comparison" in coverage:
            benchmark = case.get("benchmark")
            if not isinstance(benchmark, dict) or not BENCHMARK_FIELDS <= set(benchmark):
                fail(f"{case_id} benchmark case must define {sorted(BENCHMARK_FIELDS)}")
            missing_record = BENCHMARK_MUST_RECORD - set(benchmark.get("must_record", []))
            if missing_record:
                fail(f"{case_id} benchmark.must_record missing {sorted(missing_record)}")

    missing_cases = REQUIRED_COVERAGE - coverage_seen
    if missing_cases:
        fail(f"no eval case covers {sorted(missing_cases)}")
    missing_categories = {"positive", "contextual", "negative-control", "known-failure", "benchmark"} - categories_seen
    if missing_categories:
        fail(f"evals missing categories {sorted(missing_categories)}")
    if rubric_count < 8:
        fail("at least eight cases should carry a response-quality rubric")
    if negative_count < 4:
        fail("at least four negative controls are required")
    if artifact_count < 5:
        fail("at least five artifact-backed cases are required")

    print("html-presentation eval suite valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
