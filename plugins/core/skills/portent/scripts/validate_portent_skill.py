#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[3]
EVALS = ROOT / "evals" / "evals.json"

REQUIRED_FILES = {
    "SKILL.md",
    "references/portent-spec.md",
    "evals/evals.json",
    "evals/fixtures/captured-material.md",
    "evals/fixtures/portent-vault-state.md",
    "evals/fixtures/pre-repair-log-snapshot.md",
    "evals/fixtures/tolaria-agents-vault.md",
    "evals/fixtures/tolaria-missing-path.md",
    "evals/fixtures/tolaria-single-vault.md",
    "evals/fixtures/tolaria-vault-list.md",
    "evals/fixtures/vault-snapshot.md",
}

SKILL_REQUIRED_PATTERNS = [
    r"name:\s*portent",
    r"description:.*Tolaria knowledge base",
    r"description:.*Portent object model",
    r"mcp__tolaria__list_vaults",
    r"mcp__tolaria__open_note",
    r"source packets",
    r"derived assertions",
    r"MOCs",
    r"If `list_vaults` returns one vault, use it",
    r"multiple plausible writable vaults remain.*ask which vault",
    r"path is missing or unreadable.*stop",
    r"Never write outside the resolved vault path",
    r"Do not invent Tolaria write, search, create, update, or delete tool names",
    r"Do not write canonical knowledge records to `~/.claude/log`",
    r"## Mode Routing",
    r"### Capture",
    r"### Log",
    r"### Organize",
    r"### Brief",
    r"### Todo",
    r"### Archive",
    r"### Search",
    r"`Project`, `Operation`, `Responsibility`, `Task`",
    r"`Event`, `Note`, `Topic`, `Person`",
    r"`belongs_to`",
    r"`related_to`",
    r"organized: false",
    r"archived: false",
    r"Prefer updating an existing object over creating a duplicate",
    r"Key assertions",
    r"derived_from",
    r"supersedes",
    r"Current.*Historical.*Open gaps.*Read next",
]

SPEC_REQUIRED_PATTERNS = [
    r"Model reality first",
    r"Project",
    r"Operation",
    r"Responsibility",
    r"Task",
    r"Event",
    r"Note",
    r"Topic",
    r"Person",
    r"belongs_to",
    r"related_to",
    r"Captured",
    r"Organized",
    r"Archived",
    r"Extension Rules",
    r"Memory Layers",
    r"Source packet",
    r"Derived assertion",
    r"MOC",
    r"supersedes",
]

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
    "tolaria mcp routing",
    "markdown fallback",
    "port types",
    "entp types",
    "lifecycle state",
    "relationship integrity",
    "duplicate prevention",
    "no legacy write regression",
    "mode capture",
    "mode log",
    "mode organize",
    "mode brief",
    "mode todo",
    "mode archive",
    "mode search",
}

REQUIRED_QUALITY = {
    "Models reality with Portent objects instead of folder names.",
    "Uses Tolaria as the canonical knowledge base.",
    "Chooses the smallest correct Portent type.",
    "Separates captured, organized, and archived lifecycle states.",
    "Uses belongs_to for primary context and related_to for secondary context.",
    "Searches for existing durable objects before creating duplicates.",
    "Keeps capture fast and organization pessimistic.",
    "Keeps briefings factual and separates next actions from facts.",
    "Names unchecked sources or unavailable tools.",
    "Reports created or updated objects with type, lifecycle, and relationships.",
}

REQUIRED_EVAL_IDS = {
    "eval-suite-health-before-forward-run",
    "explicit-portent-capture-note",
    "implicit-remember-this-capture",
    "wrap-handoff-session-log-event",
    "organize-captured-material",
    "brief-active-work-from-portent",
    "todo-durable-context-boundary",
    "archive-completed-project",
    "search-without-forced-synthesis",
    "duplicate-prevention-before-project-create",
    "project-context-update-existing-project",
    "legacy-log-path-regression",
    "mcp-limited-markdown-fallback",
    "multi-vault-selection-requires-disambiguation",
    "missing-unreadable-vault-path-stops",
    "concrete-markdown-fallback-single-vault",
    "vault-agents-read-before-write",
    "custom-type-resistance",
    "negative-control-devrev-sprint-workflow",
    "negative-control-repo-code-search",
    "negative-control-github-pr-release-execution",
    "negative-control-generic-implementation-request",
    "benchmark-against-log-snapshot",
}

ALLOWED_RUN_MODES = {"clean-context-forward", "deterministic-or-clean-context"}
ALLOWED_DETERMINISTIC_KEYS = {
    "commands",
    "must_include_any",
    "must_not_include_any",
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

BENCHMARK_REQUIRED_EVIDENCE = {
    "baseline output",
    "current output",
    "scored delta",
}

POLARITY_TRAP_FORBIDDEN_TERMS = {
    "delete",
    "briefing",
    "type: project",
    "type: operation",
    "type: event",
    "type: task",
    "type: note",
    "portent object",
    "belongs_to",
    "belongs_to:",
    "related_to",
    "related_to:",
    "custom type",
    "custom relationship",
}

SOURCE_DEPENDENT_CASES = {
    "organize-captured-material",
    "brief-active-work-from-portent",
    "todo-durable-context-boundary",
    "archive-completed-project",
    "search-without-forced-synthesis",
    "duplicate-prevention-before-project-create",
    "project-context-update-existing-project",
    "mcp-limited-markdown-fallback",
    "vault-agents-read-before-write",
    "benchmark-against-log-snapshot",
}

MODE_SOURCE_TERMS = {
    "mode organize": {"fixture", "source", "captured", "existing"},
    "mode brief": {"fixture", "snapshot", "source", "record"},
    "mode todo": {"fixture", "source", "project", "external"},
    "mode archive": {"fixture", "source", "relationship", "link"},
    "mode search": {"fixture", "source", "result", "metadata", "search"},
}

ROUTE_AWAY_REQUIRED_IDS = {
    "negative-control-devrev-sprint-workflow",
    "negative-control-repo-code-search",
    "negative-control-github-pr-release-execution",
    "negative-control-generic-implementation-request",
}


def fail(message: str) -> None:
    raise SystemExit(f"portent eval validation failed: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8")


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


def validate_grouped_terms(case_id: str, key: str, value: object) -> None:
    if not isinstance(value, list):
        fail(f"{case_id} deterministic_checks.{key} must be a list")
    for group in value:
        if not isinstance(group, list) or not group:
            fail(f"{case_id} deterministic check groups must be non-empty lists")
        for term in group:
            if not isinstance(term, str) or not term.strip():
                fail(f"{case_id} deterministic check terms must be non-empty strings")


def flatten_groups(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [
        term.lower()
        for group in value
        if isinstance(group, list)
        for term in group
        if isinstance(term, str)
    ]


def validate_negative_polarity_traps(case_id: str, deterministic: dict) -> None:
    terms = flatten_groups(deterministic.get("must_not_include_any", []))
    for term in terms:
        normalized = " ".join(term.split())
        if normalized in POLARITY_TRAP_FORBIDDEN_TERMS:
            fail(
                f"{case_id} must_not_include_any forbids broad polarity-trap term "
                f"{term!r}; use a concrete bad-output phrase instead"
            )


def has_source_grounding(case: dict, coverage: list[str]) -> bool:
    evidence_terms = " ".join(case.get("required_evidence", [])).lower()
    assertion_terms = " ".join(case.get("assertions", [])).lower()
    prompt = str(case.get("prompt", "")).lower()
    files = case.get("files", [])
    for mode, terms in MODE_SOURCE_TERMS.items():
        if mode in coverage and not (
            any(term in evidence_terms for term in terms)
            or any(term in assertion_terms for term in terms)
            or (files and any(term in prompt for term in ("fixture", "snapshot", "source")))
        ):
            return False
    return True


def deterministic_checks_are_possible(case_id: str, case: dict) -> None:
    deterministic = case.get("deterministic_checks")
    if not isinstance(deterministic, dict):
        return
    include_terms = flatten_groups(deterministic.get("must_include_any", []))
    assertions = " ".join(case.get("assertions", [])).lower()
    expected = str(case.get("expected_output", "")).lower()

    if (
        "belongs_to" in include_terms
        and ("only if" in assertions or "when known" in assertions or "when known" in expected)
    ):
        fail(f"{case_id} requires belongs_to deterministically while allowing it only if known")
    if "belongs_to:" in flatten_groups(deterministic.get("must_not_include_any", [])):
        if any(term == "belongs_to" for term in include_terms):
            fail(f"{case_id} both requires and forbids belongs_to")


def main() -> int:
    for path in sorted(REQUIRED_FILES):
        if not (ROOT / path).exists():
            fail(f"missing required file {path}")

    skill = read("SKILL.md")
    for pattern in SKILL_REQUIRED_PATTERNS:
        if not re.search(pattern, skill, re.IGNORECASE | re.DOTALL):
            fail(f"SKILL.md missing pattern: {pattern}")

    spec = read("references/portent-spec.md")
    for pattern in SPEC_REQUIRED_PATTERNS:
        if not re.search(pattern, spec, re.IGNORECASE | re.DOTALL):
            fail(f"portent-spec.md missing pattern: {pattern}")

    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "portent":
        fail("evals/evals.json must set skill_name to portent")
    if data.get("version", 0) < 1:
        fail("evals/evals.json must set version >= 1")

    standards = data.get("standards")
    if not isinstance(standards, dict):
        fail("standards must be an object")
    required = set(standards.get("required_coverage", []))
    missing_required = REQUIRED_COVERAGE - required
    if missing_required:
        fail(f"standards.required_coverage missing {sorted(missing_required)}")
    quality = set(standards.get("response_quality", []))
    missing_quality = REQUIRED_QUALITY - quality
    if missing_quality:
        fail(f"standards.response_quality missing {sorted(missing_quality)}")
    benchmark_requirements = standards.get("benchmark_requirements")
    if not isinstance(benchmark_requirements, dict):
        fail("standards.benchmark_requirements must be an object")
    missing_benchmark = BENCHMARK_MUST_RECORD - set(benchmark_requirements.get("must_record", []))
    if missing_benchmark:
        fail(f"standards.benchmark_requirements.must_record missing {sorted(missing_benchmark)}")

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < len(REQUIRED_EVAL_IDS):
        fail("evals must contain the required Portent cases")

    ids: set[str] = set()
    coverage_seen: set[str] = set()
    categories: set[str] = set()
    rubric_count = 0
    assertion_blob: list[str] = []

    for index, case in enumerate(evals, start=1):
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(f"case {index} missing id")
        if case_id in ids:
            fail(f"duplicate eval id {case_id}")
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
        if not isinstance(case["prompt"], str) or len(case["prompt"].strip()) < 20:
            fail(f"{case_id} prompt is too weak")
        if not isinstance(case["expected_output"], str) or len(case["expected_output"].strip()) < 30:
            fail(f"{case_id} expected_output is too weak")

        coverage = case["coverage"]
        if not isinstance(coverage, list) or not coverage:
            fail(f"{case_id} coverage must be a non-empty list")
        coverage_seen.update(coverage)
        categories.add(str(case["category"]))
        if case_id in SOURCE_DEPENDENT_CASES and not case.get("files"):
            fail(f"{case_id} is source-dependent and must declare fixture files")
        if not has_source_grounding(case, coverage):
            fail(f"{case_id} mode-specific case lacks source-grounding evidence")

        assertions = case["assertions"]
        if not isinstance(assertions, list) or len(assertions) < 3:
            fail(f"{case_id} needs at least three assertions")
        for assertion in assertions:
            if not isinstance(assertion, str) or len(assertion.strip()) < 20:
                fail(f"{case_id} has a weak assertion")
            assertion_blob.append(assertion.lower())

        required_evidence = case["required_evidence"]
        if not isinstance(required_evidence, list) or not required_evidence:
            fail(f"{case_id} needs required_evidence")

        files = case.get("files", [])
        if files:
            if not isinstance(files, list):
                fail(f"{case_id} files must be a list")
            for fixture in files:
                if not isinstance(fixture, str):
                    fail(f"{case_id} file entries must be strings")
                if not resolve_fixture(fixture).exists():
                    fail(f"{case_id} fixture missing: {fixture}")
        if "artifact case" in coverage and not files and not any(token.startswith("/") for token in str(case["prompt"]).split()):
            fail(f"{case_id} artifact case needs fixture files or an absolute path")

        deterministic = case.get("deterministic_checks")
        if deterministic is not None:
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
                if key in deterministic:
                    validate_grouped_terms(case_id, key, deterministic[key])
            validate_negative_polarity_traps(case_id, deterministic)
            deterministic_checks_are_possible(case_id, case)

        if "response quality" in coverage:
            rubric = case.get("quality_rubric")
            if not isinstance(rubric, dict) or not rubric:
                fail(f"{case_id} covers response quality but has no quality_rubric")
            for dimension, weight in rubric.items():
                if not isinstance(dimension, str) or not isinstance(weight, int) or not 1 <= weight <= 3:
                    fail(f"{case_id} quality_rubric values must be integer weights 1-3")
            rubric_count += 1

        if case["category"] == "known-failure" and case_id != "eval-suite-health-before-forward-run":
            for key in ("known_failure_source", "before_failure_signal", "fixed_by"):
                if key not in case:
                    fail(f"{case_id} missing {key}")

        if "benchmark comparison" in coverage:
            benchmark = case.get("benchmark")
            if not isinstance(benchmark, dict):
                fail(f"{case_id} benchmark comparison case needs benchmark object")
            baseline_fixture = benchmark.get("baseline_fixture")
            if not isinstance(baseline_fixture, str) or not baseline_fixture.strip():
                fail(f"{case_id} benchmark comparison case needs benchmark.baseline_fixture")
            if baseline_fixture not in files:
                fail(f"{case_id} benchmark.baseline_fixture must also be declared in files")
            if not resolve_fixture(baseline_fixture).exists():
                fail(f"{case_id} benchmark.baseline_fixture missing: {baseline_fixture}")
            missing_record = BENCHMARK_MUST_RECORD - set(benchmark.get("must_record", []))
            if missing_record:
                fail(f"{case_id} benchmark.must_record missing {sorted(missing_record)}")
            missing_evidence = BENCHMARK_REQUIRED_EVIDENCE - set(required_evidence)
            if missing_evidence:
                fail(f"{case_id} required_evidence missing benchmark evidence {sorted(missing_evidence)}")

        if case_id == "vault-agents-read-before-write":
            agents_text = " ".join(
                [
                    str(case.get("prompt", "")),
                    str(case.get("expected_output", "")),
                    " ".join(case.get("assertions", [])),
                    " ".join(case.get("required_evidence", [])),
                ]
            ).lower()
            for term in ("agents.md", "read", "before", "hasagentinstructions", "inbox/captures"):
                if term not in agents_text:
                    fail(f"{case_id} missing AGENTS.md read-before-write term {term!r}")

    missing_ids = REQUIRED_EVAL_IDS - ids
    if missing_ids:
        fail(f"missing eval ids {sorted(missing_ids)}")
    missing_route_away = ROUTE_AWAY_REQUIRED_IDS - ids
    if missing_route_away:
        fail(f"missing route-away negative controls {sorted(missing_route_away)}")
    missing_coverage = REQUIRED_COVERAGE - coverage_seen
    if missing_coverage:
        fail(f"no eval case covers {sorted(missing_coverage)}")
    required_categories = {"positive", "contextual", "negative-control", "known-failure", "boundary", "benchmark"}
    missing_categories = required_categories - categories
    if missing_categories:
        fail(f"eval categories missing {sorted(missing_categories)}")
    if rubric_count < 10:
        fail("at least ten cases should carry a response-quality rubric")

    negative_ids = {
        case["id"]
        for case in evals
        if case.get("category") == "negative-control" and case.get("should_trigger") is False
    }
    if not ROUTE_AWAY_REQUIRED_IDS <= negative_ids:
        fail("negative controls must cover DevRev, repo search, GitHub/release, and implementation route-away cases")

    blob = "\n".join(assertion_blob)
    for term in ("tolaria", "type", "organized", "archived", "belongs_to", "related_to", "legacy", "duplicate"):
        if term not in blob:
            fail(f"eval assertions missing term {term}")

    print("Portent eval suite valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
