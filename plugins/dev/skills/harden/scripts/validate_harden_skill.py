#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "references/frontend-foundations.md",
    "references/review.md",
    "references/a11y.md",
    "references/anti-patterns.md",
    "references/arrange.md",
    "references/harden.md",
    "references/normalize.md",
    "evals/evals.json",
    "evals/files/brittle-settings-panel.tsx",
    "evals/files/payment-filter-form.tsx",
    "evals/files/marketing-card.css",
]

SKILL_REQUIRED_PATTERNS = [
    r"name:\s*harden",
    r"description:.*semantic frontend structure",
    r"## Core Mechanics",
    r"references/frontend-foundations\.md",
]

FOUNDATION_REQUIRED_TERMS = [
    "Semantic HTML ->",
    "Flow-first CSS ->",
    "Low cascade cost ->",
    "Readable JavaScript ->",
    "Dependency restraint ->",
    "Asset and render cost ->",
    "Visual polish",
]

REQUIRED_EVAL_IDS = {
    "frontend-substrate-review",
    "state-and-form-hardening",
    "browser-route-out",
    "blade-route-out",
    "visual-polish-secondary",
}

ASSERTION_COVERAGE_TERMS = [
    "semantic",
    "layout",
    "cascade",
    "dependency",
    "runtime",
    "form",
    "agent-browser",
    "blade",
    "premium",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = read("SKILL.md")
    for pattern in SKILL_REQUIRED_PATTERNS:
        if not re.search(pattern, skill, re.IGNORECASE | re.DOTALL):
            fail(f"SKILL.md missing pattern: {pattern}")

    foundations = read("references/frontend-foundations.md")
    for term in FOUNDATION_REQUIRED_TERMS:
        if term not in foundations:
            fail(f"references/frontend-foundations.md missing term: {term}")

    data = json.loads(read("evals/evals.json"))
    if data.get("skill_name") != "harden":
        fail("evals/evals.json must set skill_name to harden")

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 5:
        fail("evals/evals.json must contain at least five eval cases")

    seen_ids: set[str] = set()
    all_assertions: list[str] = []
    for index, case in enumerate(evals, start=1):
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(f"eval case {index} missing string id")
        if case_id in seen_ids:
            fail(f"duplicate eval id: {case_id}")
        seen_ids.add(case_id)

        for key in ("prompt", "expected_output"):
            if not isinstance(case.get(key), str) or len(case[key].strip()) < 20:
                fail(f"{case_id} missing meaningful {key}")

        files = case.get("files")
        if not isinstance(files, list):
            fail(f"{case_id} files must be a list")
        for path in files:
            if not isinstance(path, str) or not (ROOT / path).exists():
                fail(f"{case_id} references missing file: {path}")

        assertions = case.get("assertions")
        if not isinstance(assertions, list) or len(assertions) < 3:
            fail(f"{case_id} must include at least three assertions")
        for assertion in assertions:
            if not isinstance(assertion, str) or len(assertion.strip()) < 20:
                fail(f"{case_id} has a weak assertion: {assertion!r}")
            if "good" in assertion.lower() and "not only" not in assertion.lower():
                fail(f"{case_id} assertion is too vague: {assertion}")
            all_assertions.append(assertion.lower())

        checks = case.get("deterministic_checks")
        if not isinstance(checks, dict):
            fail(f"{case_id} must include deterministic_checks")
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

    assertion_blob = "\n".join(all_assertions)
    missing_terms = [term for term in ASSERTION_COVERAGE_TERMS if term not in assertion_blob]
    if missing_terms:
        fail("eval assertions missing coverage terms: " + ", ".join(missing_terms))

    print("PASS: harden skill eval structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
