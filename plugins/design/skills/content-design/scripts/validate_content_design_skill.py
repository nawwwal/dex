#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "references/operating-model.md",
    "references/context-model.md",
    "references/voice-system.md",
    "references/in-product-marketing.md",
    "references/surface-playbook.md",
    "references/risk-and-tone.md",
    "references/errors-and-recovery.md",
    "references/accessibility-and-localization.md",
    "references/source-map.md",
    "references/quality-rubric.md",
    "evals/payment-failure.md",
    "evals/razorpay-marketing.md",
    "evals/voice-system.md",
    "evals/destructive-modal.md",
    "evals/missing-context.md",
    "evals/consistency-audit.md",
    "evals/accessibility-localization.md",
    "evals/in-product-marketing.md",
]

SKILL_REQUIRED_PATTERNS = [
    r"name:\s*content-design",
    r"description:.*UI copy",
    r"## Runtime Workflow",
    r"## Reference Map",
    r"## Output Modes",
    r"## Quality Gates",
    r"## Source Grounding",
]

REFERENCE_REQUIRED_TERMS = {
    "references/voice-system.md": [
        "Razorpay voice",
        "founders",
        "startups",
        "entrepreneurs",
        "Term",
        "execution",
        "avoid",
    ],
    "references/in-product-marketing.md": [
        "Platform authority",
        "Speed to value",
        "Scale proof",
        "Operational control",
        "Growth outcome",
        "Trust and compliance",
        "founder",
        "aspirational",
        "Aspiration ladder",
    ],
    "references/source-map.md": [
        "DESK",
        "Razorpay",
        "Shopify",
        "Material",
        "Wise",
        "Wix",
        "GOV.UK",
    ],
}

MARKETING_REQUIRED_PATTERNS = {
    "SKILL.md": [
        r"marketing.*must include.*aspirational",
        r"recommend.*aspirational",
    ],
    "references/in-product-marketing.md": [
        r"Marketing output contract",
        r"at least one aspirational",
        r"Recommended option",
        r"Take your first sale live",
        r"Turn every conversation into a checkout",
    ],
    "evals/razorpay-marketing.md": [
        r"must not return only feature-descriptive",
        r"labels the aspiration level",
    ],
}

EVAL_REQUIRED_SECTIONS = [
    "## Prompt",
    "## Expected behavior",
    "## Pass criteria",
    "## Fail signals",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = read("SKILL.md")
    for pattern in SKILL_REQUIRED_PATTERNS:
        if not re.search(pattern, skill, re.IGNORECASE | re.DOTALL):
            fail(f"SKILL.md missing pattern: {pattern}")

    for ref, required_terms in REFERENCE_REQUIRED_TERMS.items():
        text = read(ref).lower()
        for term in required_terms:
            if term.lower() not in text:
                fail(f"{ref} missing required term: {term}")

    for path, required_patterns in MARKETING_REQUIRED_PATTERNS.items():
        text = read(path)
        for pattern in required_patterns:
            if not re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                fail(f"{path} missing marketing behavior pattern: {pattern}")

    for path in REQUIRED_FILES:
        if not path.startswith("evals/"):
            continue
        text = read(path)
        for section in EVAL_REQUIRED_SECTIONS:
            if section not in text:
                fail(f"{path} missing eval section: {section}")

    linked_refs = set(re.findall(r"`(references/[^`]+\.md)`", skill))
    expected_refs = {path for path in REQUIRED_FILES if path.startswith("references/")}
    missing_links = sorted(expected_refs - linked_refs)
    if missing_links:
        fail("SKILL.md does not link references: " + ", ".join(missing_links))

    print("PASS: content-design skill structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
