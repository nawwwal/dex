#!/usr/bin/env python3
"""Validate the Why eval suite shape and coverage."""

from __future__ import annotations

import json
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
REPO_ROOT = ROOT.parents[3]
REQUIRED_COVERAGE = {
    "explicit trigger",
    "alias trigger",
    "learn-alias trigger",
    "implicit trigger",
    "contextual trigger",
    "negative-control",
    "known failure",
    "artifact case",
    "eval suite health",
    "repair regression",
    "benchmark comparison",
    "response quality",
    "knowledge-base profile lookup",
    "knowledge-base writeback",
    "frontend-personalized teaching",
    "over-teaching regression",
    "execution-gate regression",
    "no-local-memory regression",
    "concept-leakage regression",
    "brief handoff",
    "subagent handoff",
}
REQUIRED_QUALITY = {
    "Builds a mental model before details.",
    "Uses the active context or artifact instead of generic explanation.",
    "Searches PMB for learner, learning, teach, or why profile context before non-trivial personalization.",
    "Uses the learner profile to choose frontend or design-to-code examples when that helps.",
    "Defines unfamiliar terms once and then uses them naturally.",
    "Explains alternatives through when they win and fail.",
    "States tradeoffs as benefit, cost, and risk.",
    "Names concepts used by clever code or abstractions.",
    "Gives focused read-next topics.",
    "Asks one grounding question before execution.",
    "Avoids over-teaching when a compact answer is enough.",
    "Does not claim the user has learned a concept without confirmation or observed use.",
    "Does not create local Teach or Why memory files when PMB is the requested knowledge base.",
    "Routes HTML output, report, and shareable-site artifact requests through brief while Why owns the learning spine.",
}
ALLOWED_RUN_MODES = {"clean-context-forward", "deterministic-or-clean-context"}
ALLOWED_DETERMINISTIC_KEYS = {
    "commands",
    "must_include_any",
    "must_not_include_any",
    "expected_index_path",
    "expected_search_title",
}
QUALITY_MINIMUMS = {"pass_threshold", "scale", "evidence_rule"}
BENCHMARK_FIELDS = {
    "baseline",
    "runs",
    "score_dimensions",
    "must_record",
}
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
    raise SystemExit(f"why eval validation failed: {message}")


def resolve_fixture(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "evals":
        return ROOT / path
    return ROOT / "evals" / path


def command_paths_exist(case_id: str, command: str) -> None:
    for token in shlex.split(command):
        if token.endswith(".py") and token.startswith("plugins/"):
            if not (REPO_ROOT / token).exists():
                fail(f"{case_id} deterministic command references missing script {token}")


def group_contains(group: object, *terms: str) -> bool:
    if not isinstance(group, list):
        return False
    text = " ".join(str(item).lower() for item in group)
    return all(term.lower() in text for term in terms)


def validate_brief_handoff_case(case_id: str, case: dict) -> None:
    deterministic = case.get("deterministic_checks")
    if not isinstance(deterministic, dict):
        fail(f"{case_id} brief/subagent handoff case must define deterministic_checks")
    include_groups = deterministic.get("must_include_any")
    if not isinstance(include_groups, list):
        fail(f"{case_id} brief/subagent handoff case must define deterministic_checks.must_include_any")
    has_brief_and_boundary = any(
        group_contains(group, "brief", "subagent")
        or group_contains(group, "brief", "handoff")
        for group in include_groups
    )
    if not has_brief_and_boundary:
        fail(f"{case_id} must require brief plus subagent or handoff evidence")

    not_include_groups = deterministic.get("must_not_include_any")
    if not isinstance(not_include_groups, list):
        fail(f"{case_id} brief/subagent handoff case must define deterministic_checks.must_not_include_any")
    deck_terms = {"reveal.js", "powerpoint", "figma slides"}
    blocked_terms = {
        term
        for group in not_include_groups
        if isinstance(group, list)
        for item in group
        for term in [str(item).lower()]
    }
    missing_deck_terms = deck_terms - blocked_terms
    if missing_deck_terms:
        fail(f"{case_id} must block deck route terms {sorted(missing_deck_terms)}")

    evidence = {str(item).lower() for item in case.get("required_evidence", [])}
    for required in ("brief route", "subagent or clean handoff boundary"):
        if required not in evidence:
            fail(f"{case_id} required_evidence must include {required!r}")


def main() -> int:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "why":
        fail("skill_name must be why")
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
        if not isinstance(case["should_trigger"], bool):
            fail(f"{case_id} should_trigger must be boolean")
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
        if "artifact case" in coverage and case["run_mode"] == "clean-context-forward":
            prompt_has_existing_absolute_path = any(
                Path(token.strip("`.,")).is_absolute() and Path(token.strip("`.,")).exists()
                for token in str(case["prompt"]).split()
            )
            if not files and not prompt_has_existing_absolute_path:
                fail(f"{case_id} artifact case needs files or an existing absolute path in prompt")
        if "response quality" in coverage:
            if "quality_rubric" not in case:
                fail(f"{case_id} covers response quality but has no quality_rubric")
            rubric = case["quality_rubric"]
            if not isinstance(rubric, dict) or not rubric:
                fail(f"{case_id} quality_rubric must be a non-empty object")
            for dimension, weight in rubric.items():
                if not isinstance(dimension, str) or not isinstance(weight, int) or not 1 <= weight <= 3:
                    fail(f"{case_id} quality_rubric values must be integer weights 1-3")
            rubric_count += 1
        if "deterministic_checks" in case:
            deterministic = case["deterministic_checks"]
            if not isinstance(deterministic, dict):
                fail(f"{case_id} deterministic_checks must be an object")
            unknown_keys = set(deterministic) - ALLOWED_DETERMINISTIC_KEYS
            if unknown_keys:
                fail(f"{case_id} deterministic_checks has unknown keys {sorted(unknown_keys)}")
            commands = deterministic.get("commands", [])
            if commands:
                if not isinstance(commands, list) or not all(isinstance(command, str) for command in commands):
                    fail(f"{case_id} deterministic commands must be strings")
                for command in commands:
                    command_paths_exist(case_id, command)
            for key in ("must_include_any", "must_not_include_any"):
                if key in deterministic and not isinstance(deterministic[key], list):
                    fail(f"{case_id} {key} must be a list")
        if "brief handoff" in coverage and "subagent handoff" in coverage:
            validate_brief_handoff_case(case_id, case)
        if case["category"] == "known-failure":
            for key in ("known_failure_source", "before_failure_signal", "fixed_by"):
                if key not in case and case_id != "eval-suite-health-before-forward-run":
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
    if rubric_count < 5:
        fail("at least five cases should carry a response-quality rubric")

    print("why eval suite valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
