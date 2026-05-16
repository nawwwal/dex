#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"
RUBRIC_SCHEMA_PATH = ROOT / "evals" / "rubric.schema.json"
ROUTING_PATH = ROOT / "evals" / "routing.md"

REQUIRED_CASE_IDS = {
    "artifact-editor-question-tool",
    "codebase-node-comments",
    "skill-review-surface",
    "inferno-balance-simulator",
    "presentation-walkthrough-routing",
    "content-state-routing",
    "image-seed-architecture",
    "static-api-diagram",
    "diverge-negative-control",
    "production-ui-negative-control",
}

REQUIRED_CATEGORIES = {
    "positive",
    "companion-routing",
    "boundary",
    "negative-control",
}

REQUIRED_ASSERTION_TERMS = {
    "interaction": "interaction",
    "export": "export",
    "source": "source",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is invalid JSON: {exc}")


def check_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def normalize_id(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def validate_eval_spec() -> None:
    if not EVALS_PATH.exists():
        fail(f"missing {EVALS_PATH.relative_to(ROOT)}")
    if not RUBRIC_SCHEMA_PATH.exists():
        fail(f"missing {RUBRIC_SCHEMA_PATH.relative_to(ROOT)}")
    if not ROUTING_PATH.exists():
        fail(f"missing {ROUTING_PATH.relative_to(ROOT)}")

    spec = load_json(EVALS_PATH)
    if spec.get("skill_name") != "playground":
        fail("evals.json skill_name must be playground")
    evals = spec.get("evals")
    if not isinstance(evals, list) or not evals:
        fail("evals.json evals must be a non-empty list")

    ids: set[str] = set()
    categories: set[str] = set()
    has_positive = False
    has_negative = False

    for index, case in enumerate(evals, start=1):
        if not isinstance(case, dict):
            fail(f"eval #{index} must be an object")

        case_id = check_string(case.get("id"), f"eval #{index} id")
        if case_id != normalize_id(case_id):
            fail(f"eval id must be lowercase hyphen-case: {case_id}")
        if case_id in ids:
            fail(f"duplicate eval id: {case_id}")
        ids.add(case_id)

        category = check_string(case.get("category"), f"{case_id} category")
        categories.add(category)

        should_trigger = case.get("should_trigger")
        if not isinstance(should_trigger, bool):
            fail(f"{case_id} should_trigger must be boolean")
        has_positive = has_positive or should_trigger
        has_negative = has_negative or not should_trigger

        check_string(case.get("prompt"), f"{case_id} prompt")
        check_string(case.get("expected_output"), f"{case_id} expected_output")

        assertions = case.get("assertions")
        if not isinstance(assertions, list) or len(assertions) < 3:
            fail(f"{case_id} must include at least 3 assertions")
        assertion_text = "\n".join(check_string(item, f"{case_id} assertion") for item in assertions).lower()
        if should_trigger:
            for label, term in REQUIRED_ASSERTION_TERMS.items():
                if term not in assertion_text and not (label == "source" and "assumption" in assertion_text):
                    fail(f"{case_id} assertions must cover {label}")
        else:
            if "route" not in assertion_text and "routes" not in assertion_text:
                fail(f"{case_id} negative-control assertions must cover routing")

        files = case.get("files", [])
        if files is None:
            files = []
        if not isinstance(files, list):
            fail(f"{case_id} files must be a list")
        for rel in files:
            rel_path = check_string(rel, f"{case_id} file path")
            if not (ROOT / rel_path).exists():
                fail(f"{case_id} references missing file: {rel_path}")

        checks = case.get("deterministic_checks")
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
                    check_string(term, f"{case_id} deterministic term")

    missing = sorted(REQUIRED_CASE_IDS - ids)
    if missing:
        fail("missing required eval cases: " + ", ".join(missing))

    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        fail("missing required eval categories: " + ", ".join(missing_categories))

    if not has_positive or not has_negative:
        fail("evals must include both should_trigger true and false cases")

    schema = load_json(RUBRIC_SCHEMA_PATH)
    if schema.get("type") != "object":
        fail("rubric.schema.json must define an object schema")
    for key in ("overall_pass", "score", "checks", "summary"):
        if key not in schema.get("required", []):
            fail(f"rubric.schema.json required fields must include {key}")

    routing_text = ROUTING_PATH.read_text(encoding="utf-8")
    for case_id in REQUIRED_CASE_IDS:
        if case_id.replace("-", " ") not in routing_text.lower() and case_id not in routing_text:
            fail(f"routing.md should mention eval case id or wording for {case_id}")

    print(f"PASS: {len(evals)} playground eval cases are valid")


def term_present(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def grade_output(case_id: str, output_path: Path) -> int:
    spec = load_json(EVALS_PATH)
    cases = {case["id"]: case for case in spec["evals"]}
    if case_id not in cases:
        fail(f"unknown eval case: {case_id}")
    if not output_path.exists():
        fail(f"missing output file: {output_path}")

    output = output_path.read_text(encoding="utf-8")
    case = cases[case_id]
    checks = case["deterministic_checks"]
    results = []

    for group in checks.get("must_include_any", []):
        passed = term_present(output, group)
        results.append({
            "text": "include " + " + ".join(group),
            "passed": passed,
            "evidence": "all terms found" if passed else "missing one or more terms",
        })

    for group in checks.get("must_not_include_any", []):
        passed = not term_present(output, group)
        results.append({
            "text": "exclude " + " + ".join(group),
            "passed": passed,
            "evidence": "terms absent" if passed else "forbidden terms found together",
        })

    passed_count = sum(1 for result in results if result["passed"])
    total = len(results)
    payload = {
        "case_id": case_id,
        "assertion_results": results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": passed_count / total if total else 0,
        },
    }
    print(json.dumps(payload, indent=2))
    return 0 if passed_count == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and grade playground skill evals.")
    parser.add_argument("--case", help="Eval case id to grade against an output file")
    parser.add_argument("--output", help="Path to captured agent output text for --case")
    args = parser.parse_args()

    validate_eval_spec()
    if args.case or args.output:
        if not args.case or not args.output:
            fail("--case and --output must be provided together")
        return grade_output(args.case, Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
