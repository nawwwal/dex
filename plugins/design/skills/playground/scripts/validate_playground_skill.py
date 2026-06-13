#!/usr/bin/env python3
"""Validate the playground skill contract, references, templates, and eval suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_REFERENCE_MENTIONS = [
    "references/modes.md",
    "references/playground.md",
    "references/topic-modeling.md",
    "references/interaction-models.md",
    "references/visual-language.md",
    "references/artifact-contract.md",
    "references/interactive-html.md",
    "references/export-output.md",
]

REQUIRED_TEMPLATES = [
    "assets/templates/artifact-editor.html",
    "assets/templates/canvas-node-map.html",
    "assets/templates/simulator.html",
    "assets/templates/review-surface.html",
    "assets/templates/narrative-walkthrough.html",
]

MIGRATED_V1_IDS = {
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


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text()


def main() -> None:
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1]
    skill_md = read(skill_root / "SKILL.md")
    suite_path = skill_root / "evals" / "exhaustive-suite.json"
    legacy_evals = skill_root / "evals" / "evals.json"

    for mention in REQUIRED_REFERENCE_MENTIONS:
        if mention not in skill_md:
            fail(f"SKILL.md must mention {mention}")
        if not (skill_root / mention).exists():
            fail(f"referenced file does not exist: {mention}")

    if "Route companion skills before building" not in skill_md:
        fail("SKILL.md must keep companion routing before build")
    if "Do not route production UI to `playground`" not in skill_md:
        fail("SKILL.md must decline production UI ownership")
    if "Static output is valid only when interaction would add no understanding" not in skill_md:
        fail("SKILL.md must preserve static-output boundary rule")

    if not legacy_evals.exists():
        fail("evals/evals.json must be retained after exhaustive-suite migration")

    legacy = json.loads(read(legacy_evals))
    if legacy.get("skill_name") != "playground":
        fail("evals/evals.json skill_name must remain playground")

    for template in REQUIRED_TEMPLATES:
        template_path = skill_root / template
        if not template_path.exists():
            fail(f"missing required HTML template: {template}")

    subprocess.run(
        [sys.executable, str(skill_root / "scripts" / "validate_eval_suite.py"), str(suite_path)],
        check=True,
    )

    suite = json.loads(read(suite_path))
    evals = suite["evals"]
    ids = {case["id"] for case in evals}
    missing_migrated = MIGRATED_V1_IDS - ids
    if missing_migrated:
        fail(f"missing migrated v1 eval ids in exhaustive suite: {sorted(missing_migrated)}")

    html_validator = skill_root / "scripts" / "validate_playground_html.py"
    for template in REQUIRED_TEMPLATES:
        subprocess.run(
            [sys.executable, str(html_validator), str(skill_root / template)],
            check=True,
        )

    visual_cases = [case for case in evals if case["category"] == "visual-quality"]
    if len(visual_cases) < 5:
        fail("expected at least five visual-quality eval cases")

    html_cases = [case for case in evals if case["category"] == "html-contract"]
    if len(html_cases) < 5:
        fail("expected at least five html-contract eval cases")

    print("OK: playground skill contract, templates, HTML scaffolds, and eval suite are valid")


if __name__ == "__main__":
    main()
