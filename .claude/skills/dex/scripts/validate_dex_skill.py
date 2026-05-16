#!/usr/bin/env python3
from __future__ import annotations

import os
import json
import re
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parents[4]
AGENTS = REPO / ".agents" / "skills" / "dex"
CLAUDE = REPO / ".claude" / "skills" / "dex"
CODEX_LINK = REPO / ".codex" / "skills" / "dex"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(REPO)}")
    return path.read_text(encoding="utf-8")


def require(text: str, pattern: str, label: str) -> None:
    if not re.search(pattern, text, re.IGNORECASE | re.DOTALL | re.MULTILINE):
        fail(f"{label} missing pattern: {pattern}")


def require_file(path: Path) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(REPO)}")


def require_contains(values: set[str], expected: set[str], label: str) -> None:
    missing = expected - values
    if missing:
        fail(f"{label} missing: {', '.join(sorted(missing))}")


def validate_skill_md() -> None:
    agents_skill = read(AGENTS / "SKILL.md")
    claude_skill = read(CLAUDE / "SKILL.md")

    for label, text in {
        ".agents/skills/dex/SKILL.md": agents_skill,
        ".claude/skills/dex/SKILL.md": claude_skill,
    }.items():
        require(text, r"name:\s*dex", label)
        require(text, r"description:.*plugin releases", label)
        require(text, r"description:.*skill evals", label)
        require(text, r"description:.*multi-round skill repair", label)
        require(text, r"`release <core\|design\|dev\|tools> \[patch\|minor\|major\|initial\]`", label)
        require(text, r"`eval <skill-path-or-plugin-skill> \[rounds=N\] \[baseline=previous\|none\|snapshot\]`", label)
        require(text, r"\*\*release\*\*\s*->\s*Read `\./release\.md`", label)
        require(text, r"\*\*eval\*\*\s*->\s*Read `\./eval\.md`", label)
        require(text, r"\*\*skill eval / benchmark / repair intent\*\*\s*->\s*Read `\./eval\.md`", label)
        require(text, r"If no argument: ask whether to run a plugin release or a skill eval\.", label)

    require(claude_skill, r"disable-model-invocation:\s*true", ".claude/skills/dex/SKILL.md")


def validate_mirrored_docs() -> None:
    for name in ("release.md", "eval.md", "eval-framework.md"):
        agents_text = read(AGENTS / name)
        claude_text = read(CLAUDE / name)
        if agents_text != claude_text:
            fail(f"{name} differs between .agents and .claude dex skills")

    for name in ("evals/evals.json",):
        require_file(AGENTS / name)
        require_file(CLAUDE / name)
        agents_text = read(AGENTS / name)
        claude_text = read(CLAUDE / name)
        if agents_text != claude_text:
            fail(f"{name} differs between .agents and .claude dex skills")

    agents_script = read(AGENTS / "scripts" / "validate_dex_skill.py")
    claude_script = read(CLAUDE / "scripts" / "validate_dex_skill.py")
    if agents_script != claude_script:
        fail("scripts/validate_dex_skill.py differs between .agents and .claude dex skills")

    eval_md = read(AGENTS / "eval.md")
    for pattern in (
        r"rounds=3",
        r"Stop after round 2 only if",
        r"skill-creator/SKILL\.md",
        r"Execution Architecture",
        r"Fresh subagents or `codex exec` runs own evaluation",
        r"Do not create a separate `skill-eval-rubric` skill",
        r"Do not require a persistent custom eval agent by default",
        r"Design eval suite",
        r"Inspect existing evals, scripts, fixtures, and known failure notes before running anything",
        r"Write or update the relevant eval cases before touching the target skill",
        r"Run the designed eval suite, not an improvised prompt set",
        r"Repair with skill-creator",
        r"Re-run the same evals",
        r"a relevant eval suite was designed or refreshed before target-skill repair",
        r"If round 3 still has critical failures",
    ):
        require(eval_md, pattern, ".agents/skills/dex/eval.md")

    release_md = read(AGENTS / "release.md")
    for pattern in (
        r"Release commits must also update the README current-version table",
        r"dex-current-versions:start",
        r"Update version files and README current versions",
        r"README\.md missing dex-current-versions block",
        r"README\.md does not list \$PLUGIN v\$NEW_VERSION",
        r"git add[\s\\]+.*README\.md",
    ):
        require(release_md, pattern, ".agents/skills/dex/release.md")

    framework = read(AGENTS / "eval-framework.md")
    for pattern in (
        r"Design the relevant eval suite before repairing the skill",
        r"explicit trigger",
        r"implicit trigger",
        r"contextual trigger",
        r"negative-control",
        r"known failure",
        r"Eval Design Gate",
        r"Do not let repair discovery become the eval design method",
        r"Execution Surfaces",
        r"Custom eval agent",
        r"ordinary fresh subagents already provide independent evaluation",
        r"Do not introduce a separate `skill-eval-rubric` skill",
        r"Judge Rubric",
        r"Benchmark Shape",
        r"Codex Exec Launch",
        r"codex exec",
        r"--model gpt-5\.5",
        r"model_reasoning_effort",
        r"Do not default to `gpt-5\.4-mini`",
        r"Diagnosis Labels",
        r"Stop Criteria",
        r"round 3",
    ):
        require(framework, pattern, ".agents/skills/dex/eval-framework.md")


def validate_eval_suite() -> None:
    suite = json.loads(read(AGENTS / "evals" / "evals.json"))
    if suite.get("skill_name") != "dex":
        fail("evals/evals.json skill_name must be dex")
    if suite.get("version", 0) < 2:
        fail("evals/evals.json must use behavior-first version 2 or newer")

    evals = suite.get("evals")
    if not isinstance(evals, list) or len(evals) < 12:
        fail("evals/evals.json must contain at least 12 behavior/regression cases")

    required_coverage = {
        "explicit trigger",
        "implicit trigger",
        "contextual trigger",
        "negative-control",
        "known failure",
        "artifact case",
        "eval suite health",
        "repair regression",
        "release gate",
        "benchmark comparison",
    }
    standards = suite.get("standards", {})
    require_contains(set(standards.get("required_coverage", [])), required_coverage, "standards.required_coverage")

    ids = set()
    coverage = set()
    categories = set()
    run_modes = set()
    for case in evals:
        case_id = case.get("id")
        if not case_id:
            fail("eval case missing id")
        if case_id in ids:
            fail(f"duplicate eval id: {case_id}")
        ids.add(case_id)

        for key in ("category", "should_trigger", "run_mode", "prompt", "expected_output", "assertions", "required_evidence"):
            if key not in case:
                fail(f"{case_id} missing {key}")
        if len(case.get("assertions", [])) < 3:
            fail(f"{case_id} must have at least three assertions")
        if len(case.get("required_evidence", [])) < 1:
            fail(f"{case_id} must name evidence required for a pass")
        if not isinstance(case.get("coverage"), list) or not case["coverage"]:
            fail(f"{case_id} must declare coverage")

        categories.add(case["category"])
        run_modes.add(case["run_mode"])
        coverage.update(case["coverage"])

    require_contains(coverage, required_coverage, "eval case coverage")
    require_contains(categories, {"positive", "contextual", "known-failure", "negative-control", "boundary"}, "eval categories")
    require_contains(run_modes, {"clean-context-forward", "deterministic"}, "eval run modes")

    required_ids = {
        "eval-suite-health-before-forward-run",
        "eval-real-skill-no-existing-evals",
        "eval-dirty-target-uses-snapshot-baseline",
        "bad-eval-suite-repaired-before-skill",
        "release-this-multi-plugin-diff-splits-releases",
        "release-dirty-worktree-blocks-version-bump",
        "release-updates-readme-current-version-table",
        "normal-skill-doc-edit-does-not-trigger-maintainer-eval",
    }
    require_contains(ids, required_ids, "eval ids")


def validate_scripts_and_link() -> None:
    require_file(AGENTS / "scripts" / "validate_dex_skill.py")
    require_file(CLAUDE / "scripts" / "validate_dex_skill.py")

    if not CODEX_LINK.is_symlink():
        fail(".codex/skills/dex must remain a symlink")
    target = os.readlink(CODEX_LINK)
    if target != "../../.claude/skills/dex":
        fail(f".codex/skills/dex symlink target changed: {target}")


def validate_repo_docs() -> None:
    readme = read(REPO / "README.md")
    require(readme, r"/dex eval plugins/design/skills/crux", "README.md")
    require(readme, r"skill-creator", "README.md")
    require(readme, r"design or refresh the relevant eval suite before touching the target skill", "README.md")
    require(readme, r"\.dex/evals/", "README.md")
    require(readme, r"<!-- dex-current-versions:start -->", "README.md")
    require(readme, r"<!-- dex-current-versions:end -->", "README.md")

    for plugin in ("core", "design", "dev", "tools"):
        claude_manifest = json.loads(read(REPO / "plugins" / plugin / ".claude-plugin" / "plugin.json"))
        codex_manifest = json.loads(read(REPO / "plugins" / plugin / ".codex-plugin" / "plugin.json"))
        if claude_manifest["version"] != codex_manifest["version"]:
            fail(f"{plugin} Claude/Codex manifest versions differ")
        version = re.escape(claude_manifest["version"])
        require(readme, rf"\| `{plugin}` \| `{version}` \|", "README.md")

    gitignore = read(REPO / ".gitignore")
    require(gitignore, r"^\.dex/evals/$", ".gitignore")


def main() -> int:
    validate_skill_md()
    validate_mirrored_docs()
    validate_eval_suite()
    validate_scripts_and_link()
    validate_repo_docs()
    print("PASS: dex skill eval workflow is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
