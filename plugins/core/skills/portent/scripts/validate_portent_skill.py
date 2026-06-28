#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"

REQUIRED_FILES = {
    "SKILL.md",
    "references/retrieval.md",
    "references/writeback.md",
    "references/hooks.md",
    "references/setup.md",
    "references/portent-spec.md",
    "evals/evals.json",
}

SKILL_REQUIRED = [
    r"Use the knowledge base as a habit loop",
    r"Orient.*Retrieve.*Write.*Refresh.*Report",
    r"global `~/.agents/AGENTS.md`",
    r"already resolved",
    r"Do not call `mcp__tolaria__list_vaults` just to confirm it",
    r"Do not rediscover the vault on every run",
    r"fails because the vault target is ambiguous",
    r"qmd is the search brain",
    r"Do not use Tolaria full-text search",
    r"cheapest qmd mode that fits",
    r"references/retrieval\.md",
    r"references/writeback\.md",
    r"references/hooks\.md",
    r"references/setup\.md",
    r"mcp__tolaria__create_note",
    r"qmd vsearch",
    r"qmd query",
    r"qmd get",
    r"Do not run every qmd mode by default",
    r"qmd update -c portent",
    r"qmd embed -c portent",
    r"Behavior corrections usually go to `\[\[agent-behavior-gotchas\]\]`",
    r"Knowledge-base maintenance goes to `\[\[brain-log\]\]`",
    r"No update needed",
    r"PORT: `Project`, `Operation`, `Responsibility`, `Task`",
    r"ENTP: `Event`, `Note`, `Topic`, `Person`",
    r"source packet",
    r"derived assertion",
    r"MOC",
]

FORBIDDEN_SKILL = [
    r"mcp__tolaria__search_notes",
    r"Use Tolaria search as",
    r"Tolaria search for",
]

RETRIEVAL_REQUIRED = [
    r"qmd is the retrieval plane",
    r"Tolaria search is not",
    r"already resolved",
    r"vault target is ambiguous",
    r"lex",
    r"vec",
    r"hyde",
    r"qmd get",
    r"qmd multi-get",
    r"qmd search",
    r"qmd vsearch",
    r"qmd query",
    r"Mode Selection",
    r"Do not run every qmd mode by default",
    r"at least three angles",
    r"agent-behavior-gotchas",
    r"qmd is degraded",
    r"direct Markdown search",
]

WRITEBACK_REQUIRED = [
    r"Writeback should feel easy",
    r"Update existing notes before creating new notes",
    r"agent behavior corrections",
    r"Aditya working-style preferences",
    r"technical contracts",
    r"design decisions",
    r"team ownership",
    r"source packet",
    r"derived assertion",
    r"no update needed",
]

SETUP_REQUIRED = [
    r"# Portent Setup",
    r"npm install -g @tobilu/qmd",
    r"qmd collection add",
    r"qmd update",
    r"qmd search",
    r"qmd vsearch",
    r"qmd query",
    r"qmd embed -c portent",
    r"Do not run installs.*without user confirmation",
    r"Readiness Check",
    r"Persist The Default Vault",
    r"~/.agents/AGENTS.md",
    r"Do not rediscover the vault on every run",
    r"Hooks",
    r"UserPromptSubmit",
    r"portent_context_receipt\.py --self-test",
]

HOOKS_REQUIRED = [
    r"Hooks keep the knowledge loop present",
    r"do not replace the skill",
    r"Prompt receipt",
    r"already-resolved default vault",
    r"UserPromptSubmit",
    r"Future stop audit",
    r"Do not put retrieval inside hooks",
    r"portent_context_receipt\.py",
    r"hooks\.json",
    r"hooks are degraded",
    r"not to call `list_vaults` just to confirm it",
]

REQUIRED_EVAL_IDS = {
    "search-before-answering-known-work",
    "write-agent-behavior-correction",
    "capture-working-style-preference",
    "update-project-state-from-pr-and-devrev",
    "capture-meeting-transcript-signal",
    "brief-current-plate-from-vault",
    "retrieve-design-technical-context",
    "qmd-degraded-markdown-fallback",
    "do-not-write-broad-team-noise",
    "handoff-after-nontrivial-codex-work",
    "prevent-duplicate-knowledge-object",
    "setup-repair-is-interactive",
    "use-configured-vault-not-rediscovery",
    "readiness-check-before-setup-complete",
    "pulse-daily-digest-writeback",
    "come-back-list-update",
    "slack-thread-routing-memory",
    "promotion-growth-context-brief",
    "posthog-analytics-context",
    "visual-direction-retrieval",
    "access-route-retrieval",
    "people-and-owner-map",
    "hooks-support-not-replace-skill",
}

REQUIRED_CATEGORIES = {"retrieval", "writeback", "brief", "fallback", "boundary", "setup"}
MUTATION_POLICIES = {"none", "dry_run_portent", "repo_guidance"}


def fail(message: str) -> None:
    raise SystemExit(f"portent validation failed: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8")


def require_patterns(name: str, text: str, patterns: list[str]) -> None:
    for pattern in patterns:
        if not re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            fail(f"{name} missing pattern: {pattern}")


def forbid_patterns(name: str, text: str, patterns: list[str]) -> None:
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            fail(f"{name} contains forbidden pattern: {pattern}")


def validate_evals() -> None:
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    if data.get("skill_name") != "portent":
        fail("evals/evals.json skill_name must be portent")
    if data.get("version") != 2:
        fail("evals/evals.json version must be 2")
    if data.get("judge_contract", {}).get("strategy") != "rubric-based outcome evaluation":
        fail("judge_contract must use rubric-based outcome evaluation")
    if data.get("judge_contract", {}).get("pass_threshold", 0) < 0.8:
        fail("pass_threshold must be at least 0.8")
    scoring = data.get("judge_contract", {}).get("scoring", {})
    if not scoring.get("formula") or "dimension_score" not in scoring.get("formula", ""):
        fail("judge_contract.scoring.formula must define weighted dimension scoring")
    if scoring.get("must_include_groups_required") is not True:
        fail("judge_contract.scoring.must_include_groups_required must be true")
    if scoring.get("must_not_include_violation") != "fail":
        fail("judge_contract.scoring.must_not_include_violation must be fail")
    scale = scoring.get("dimension_scale", {})
    if not all(str(i) in scale for i in range(4)):
        fail("judge_contract.scoring.dimension_scale must define 0, 1, 2, and 3")

    execution = data.get("execution", {})
    if execution.get("requires_mock_vault") is not True:
        fail("execution.requires_mock_vault must be true")
    if execution.get("allow_live_vault_mutation") is not False:
        fail("execution.allow_live_vault_mutation must be false")
    if execution.get("allow_repo_mutation_by_default") is not False:
        fail("execution.allow_repo_mutation_by_default must be false")
    if execution.get("repo_mutation_requires_explicit_case") is not True:
        fail("execution.repo_mutation_requires_explicit_case must be true")
    if execution.get("do_not_leak_judge_criteria") is not True:
        fail("execution.do_not_leak_judge_criteria must be true")
    judge_only = set(execution.get("judge_only_fields", []))
    for field in ("expected_behavior", "rubric", "must_include_any", "must_not_include_any"):
        if field not in judge_only:
            fail(f"execution.judge_only_fields must include {field}")
    forbidden_actor_reads = "\n".join(execution.get("forbidden_actor_reads", []))
    for path in ("evals/evals.json", ".codex/memories", "MEMORY.md"):
        if path not in forbidden_actor_reads:
            fail(f"execution.forbidden_actor_reads must include {path}")
    allowed_actor_context = "\n".join(execution.get("allowed_actor_context", []))
    for source in ("natural prompt", "Portent skill path", "task artifacts"):
        if source not in allowed_actor_context:
            fail(f"execution.allowed_actor_context must include {source}")
    if execution.get("actor_write_root") != "/tmp/portent-eval/<eval-id>":
        fail("execution.actor_write_root must be /tmp/portent-eval/<eval-id>")
    mutation_policies = execution.get("mutation_policies", {})
    for policy in MUTATION_POLICIES:
        if policy not in mutation_policies:
            fail(f"execution.mutation_policies must define {policy}")
    forbidden_output = "\n".join(execution.get("forbidden_actor_output_patterns", []))
    for pattern in (".codex/memories", "MEMORY.md", "skills/portent/evals", "expected_behavior"):
        if pattern not in forbidden_output:
            fail(f"execution.forbidden_actor_output_patterns must include {pattern}")
    pre_post_checks = "\n".join(execution.get("pre_post_checks", []))
    for check in ("git status before", "git status after", "fail repo diffs", "fail live vault diffs"):
        if check not in pre_post_checks:
            fail(f"execution.pre_post_checks must include {check}")
    transcript_required = set(execution.get("actor_transcript_required", []))
    for field in ("tools or commands used", "files read", "files written", "dry-run targets", "live-vault mutation check"):
        if field not in transcript_required:
            fail(f"execution.actor_transcript_required must include {field}")

    standards = "\n".join(data.get("standards", {}).get("must", []))
    require_patterns(
        "eval standards",
        standards,
        [
            r"qmd.*Tolaria",
            r"mode.*search.*vsearch.*query.*get",
            r"Do not force every qmd mode",
            r"Read source text",
            r"Update existing Portent objects",
            r"behavioral, technical, design, team, system",
            r"no update needed",
            r"judge-only",
            r"isolated read/write contract",
            r"must not read Codex memory",
            r"must not mutate repo files unless",
        ],
    )

    evals = data.get("evals")
    if not isinstance(evals, list):
        fail("evals must be a list")
    ids = {case.get("id") for case in evals}
    missing = REQUIRED_EVAL_IDS - ids
    if missing:
        fail(f"missing eval ids: {sorted(missing)}")

    categories = {case.get("category") for case in evals}
    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(f"missing eval categories: {sorted(missing_categories)}")

    for case in evals:
        case_id = case.get("id")
        for key in ("category", "prompt", "expected_behavior", "rubric", "must_include_any", "must_not_include_any"):
            if key not in case:
                fail(f"{case_id} missing {key}")
        if case.get("mutation_policy") not in MUTATION_POLICIES:
            fail(f"{case_id} must declare mutation_policy")
        if not isinstance(case.get("live_allowed"), bool):
            fail(f"{case_id} must declare live_allowed boolean")
        if case.get("mutation_policy") == "repo_guidance" and case_id not in {
            "use-configured-vault-not-rediscovery",
            "hooks-support-not-replace-skill",
        }:
            fail(f"{case_id} may not use repo_guidance mutation policy")
        if case_id == "qmd-degraded-markdown-fallback":
            degraded = case.get("qmd_degraded_contract", {})
            if degraded.get("allowed_qmd_calls") != 1:
                fail("qmd-degraded-markdown-fallback must allow only one qmd failure capture")
            if "direct Markdown" not in degraded.get("after_failure", ""):
                fail("qmd-degraded-markdown-fallback must require direct Markdown after failure")
        if len(str(case["prompt"]).strip()) < 30:
            fail(f"{case_id} prompt is too weak")
        prompt_lower = str(case["prompt"]).lower()
        for leak_term in ("expected_behavior", "rubric", "must_include", "must_not_include"):
            if leak_term in prompt_lower:
                fail(f"{case_id} prompt leaks judge term {leak_term}")
        rubric = case["rubric"]
        if not isinstance(rubric, dict) or not rubric:
            fail(f"{case_id} rubric must be a non-empty object")
        for dimension, weight in rubric.items():
            if not isinstance(dimension, str) or not isinstance(weight, int) or not 1 <= weight <= 3:
                fail(f"{case_id} rubric weights must be integers 1-3")

        forbidden = " ".join(
            term
            for group in case.get("must_not_include_any", [])
            if isinstance(group, list)
            for term in group
            if isinstance(term, str)
        ).lower()
        if case_id != "setup-repair-is-interactive" and "installed without asking" not in forbidden:
            pass
        if case_id in {"search-before-answering-known-work", "qmd-degraded-markdown-fallback"}:
            if "tolaria search" not in forbidden and "mcp__tolaria__search_notes" not in forbidden:
                fail(f"{case_id} must forbid Tolaria search")
        if case_id in {
            "brief-current-plate-from-vault",
            "retrieve-design-technical-context",
            "slack-thread-routing-memory",
            "promotion-growth-context-brief",
            "posthog-analytics-context",
            "visual-direction-retrieval",
            "access-route-retrieval",
            "people-and-owner-map",
        }:
            if "qmd_retrieval" not in rubric or "source_read" not in rubric:
                fail(f"{case_id} must score qmd retrieval and source reads")
            if "mode_choice" not in rubric:
                fail(f"{case_id} must score qmd mode choice")
            include_text = " ".join(
                term
                for group in case.get("must_include_any", [])
                if isinstance(group, list)
                for term in group
                if isinstance(term, str)
            ).lower()
            if not any(
                term in include_text
                for term in ("qmd search", "qmd vsearch", "qmd query", "mcp__qmd__search", "mcp__qmd__query")
            ):
                fail(f"{case_id} must require at least one qmd retrieval mode")
            if not any(
                term in include_text
                for term in (
                    "qmd get",
                    "qmd multi-get",
                    "mcp__qmd__get",
                    "mcp__qmd__multi_get",
                    "source text",
                    "sources read",
                )
            ):
                fail(f"{case_id} must require source reads")


def main() -> int:
    for path in sorted(REQUIRED_FILES):
        if not (ROOT / path).exists():
            fail(f"missing required file {path}")

    skill = read("SKILL.md")
    require_patterns("SKILL.md", skill, SKILL_REQUIRED)
    forbid_patterns("SKILL.md", skill, FORBIDDEN_SKILL)
    require_patterns("retrieval.md", read("references/retrieval.md"), RETRIEVAL_REQUIRED)
    require_patterns("writeback.md", read("references/writeback.md"), WRITEBACK_REQUIRED)
    require_patterns("hooks.md", read("references/hooks.md"), HOOKS_REQUIRED)
    require_patterns("setup.md", read("references/setup.md"), SETUP_REQUIRED)
    require_patterns(
        "portent-spec.md",
        read("references/portent-spec.md"),
        [r"Memory Layers", r"Source packet", r"Derived assertion", r"MOC", r"Project", r"Event"],
    )
    validate_evals()
    print("Portent skill valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
