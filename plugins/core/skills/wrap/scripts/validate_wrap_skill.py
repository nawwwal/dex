#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "evals/evals.json",
]

SKILL_REQUIRED_PATTERNS = [
    r"name:\s*wrap",
    r"description:.*explicitly invokes /wrap",
    r"description:.*close out",
    r"description:.*coding-session recap-only requests",
    r"## Evidence",
    r"## Workflow",
    r"## Recap Format",
    r"git status --branch --short",
    r"git diff --stat",
    r"git diff --cached --stat",
    r"Keep unrelated local files",
    r"README and release-doc drift",
    r"Stage by exact path or hunk",
    r"do not create an empty commit",
    r"Run `log` when the session deserves a durable handoff",
    r"Do not run `log` for empty diffs",
    r"## Started With",
    r"## Log Created",
]

REQUIRED_COVERAGE = {
    "explicit trigger",
    "implicit trigger",
    "contextual trigger",
    "negative-control",
    "known failure",
    "artifact case",
    "log handoff",
    "commit boundary",
    "dirty worktree protection",
    "dex drift gate",
}

REQUIRED_EVAL_IDS = {
    "explicit-wrap-creates-micro-commits",
    "implicit-wrap-and-commit-trigger",
    "recap-only-asks-before-commit",
    "synonym-checkpoint-and-commit-triggers-wrap",
    "dirty-worktree-preserves-unrelated-files",
    "staged-incoherent-changes-ask-first",
    "meaningful-work-runs-log-after-commits",
    "empty-diff-skips-commit-and-log",
    "dex-skill-inventory-checks-readme-drift",
    "push-deploy-release-not-implied",
}

ASSERTION_COVERAGE_TERMS = [
    "commit",
    "recap",
    "staged",
    "unrelated",
    "log",
    "readme",
    "release",
    "push",
    "deploy",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.exists():
        fail(f"missing {path}")
    return file_path.read_text(encoding="utf-8")


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = read("SKILL.md")
    for pattern in SKILL_REQUIRED_PATTERNS:
        if not re.search(pattern, skill, re.IGNORECASE | re.DOTALL):
            fail(f"SKILL.md missing pattern: {pattern}")

    data = json.loads(read("evals/evals.json"))
    if data.get("skill_name") != "wrap":
        fail("evals/evals.json must set skill_name to wrap")
    if data.get("version", 0) < 1:
        fail("evals/evals.json must set version >= 1")

    standards = data.get("standards", {})
    required = set(standards.get("required_coverage", []))
    missing_coverage = sorted(REQUIRED_COVERAGE - required)
    if missing_coverage:
        fail("standards.required_coverage missing: " + ", ".join(missing_coverage))

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < len(REQUIRED_EVAL_IDS):
        fail("evals/evals.json must contain the required wrap eval cases")

    seen_ids: set[str] = set()
    coverage: set[str] = set()
    categories: set[str] = set()
    assertions_blob: list[str] = []

    for index, case in enumerate(evals, start=1):
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(f"eval case {index} missing string id")
        if case_id in seen_ids:
            fail(f"duplicate eval id: {case_id}")
        seen_ids.add(case_id)

        for key in ("category", "coverage", "should_trigger", "run_mode", "prompt", "expected_output", "assertions", "deterministic_checks"):
            if key not in case:
                fail(f"{case_id} missing {key}")

        if not isinstance(case["coverage"], list) or not case["coverage"]:
            fail(f"{case_id} must declare coverage")
        coverage.update(case["coverage"])
        categories.add(str(case["category"]))

        for key in ("prompt", "expected_output"):
            if not isinstance(case[key], str) or len(case[key].strip()) < 20:
                fail(f"{case_id} missing meaningful {key}")

        assertions = case["assertions"]
        if not isinstance(assertions, list) or len(assertions) < 3:
            fail(f"{case_id} must include at least three assertions")
        for assertion in assertions:
            if not isinstance(assertion, str) or len(assertion.strip()) < 20:
                fail(f"{case_id} has a weak assertion: {assertion!r}")
            assertions_blob.append(assertion.lower())

        checks = case["deterministic_checks"]
        if not isinstance(checks, dict):
            fail(f"{case_id} deterministic_checks must be an object")
        for key in ("must_include_any", "must_not_include_any"):
            groups = checks.get(key)
            if not isinstance(groups, list):
                fail(f"{case_id} deterministic_checks.{key} must be a list")
            for group in groups:
                if not isinstance(group, list) or not group:
                    fail(f"{case_id} deterministic check groups must be non-empty lists")
                for term in group:
                    if not isinstance(term, str) or not term.strip():
                        fail(f"{case_id} deterministic check term must be a non-empty string")

    missing_ids = sorted(REQUIRED_EVAL_IDS - seen_ids)
    if missing_ids:
        fail("missing eval ids: " + ", ".join(missing_ids))

    missing_case_coverage = sorted(REQUIRED_COVERAGE - coverage)
    if missing_case_coverage:
        fail("eval cases missing coverage: " + ", ".join(missing_case_coverage))

    required_categories = {"positive", "contextual", "negative-control", "known-failure", "boundary"}
    missing_categories = sorted(required_categories - categories)
    if missing_categories:
        fail("eval categories missing: " + ", ".join(missing_categories))

    assertion_blob = "\n".join(assertions_blob)
    missing_terms = [term for term in ASSERTION_COVERAGE_TERMS if term not in assertion_blob]
    if missing_terms:
        fail("eval assertions missing coverage terms: " + ", ".join(missing_terms))

    print("PASS: wrap skill eval structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
