#!/usr/bin/env python3
"""Validate playground HTML artifacts against slop bans and required contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BANNED_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"linear-gradient\s*\([^)]*(?:#(?:7[0-9a-f]{2}|8[0-9a-f]{2}|9[0-9a-f]{2})[0-9a-f]{3}|purple|violet|indigo)[^)]*\)",
            re.IGNORECASE,
        ),
        "purple gradient",
    ),
    (
        re.compile(
            r"linear-gradient\s*\([^)]*(?:purple|violet|indigo|#(?:6[0-9a-f]{2}|7[0-9a-f]{2}|8[0-9a-f]{2})[0-9a-f]{3})[^)]*(?:blue|#(?:0[0-9a-f]|1[0-9a-f]|2[0-9a-f]|3[0-9a-f])[0-9a-f]{4})",
            re.IGNORECASE,
        ),
        "purple-blue gradient AI slop",
    ),
    (
        re.compile(r"font-family\s*:\s*[^;]*\bInter\b", re.IGNORECASE),
        "Inter font default",
    ),
    (
        re.compile(r"""@import\s+url\([^)]*fonts\.googleapis\.com[^)]*Inter""", re.IGNORECASE),
        "Inter Google Fonts import",
    ),
    (
        re.compile(
            r"\b(?:fake|sample|demo|placeholder)\s+(?:metric|kpi|stat|analytics)\b",
            re.IGNORECASE,
        ),
        "fake metric label",
    ),
    (
        re.compile(
            r"\b\d{1,3}(?:\.\d+)?%?\s+(?:uptime|conversion|engagement|retention|satisfaction)\b",
            re.IGNORECASE,
        ),
        "decorative metric without derivation context",
    ),
    (
        re.compile(r"\blorem ipsum\b", re.IGNORECASE),
        "lorem ipsum",
    ),
    (
        re.compile(r"\bdolor sit amet\b", re.IGNORECASE),
        "lorem ipsum body",
    ),
]

REQUIRED_CONTRACT: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"source\s+assumptions|assumptions|source-notes|data-source-assumptions",
            re.IGNORECASE,
        ),
        "source assumptions section or marker",
    ),
    (
        re.compile(
            r"export|updatePrompt|paste-back|copy-prompt|export-prompt|export-output",
            re.IGNORECASE,
        ),
        "export output or renderer",
    ),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_html(path: Path) -> None:
    if not path.exists():
        fail(f"HTML file not found: {path}")
    if path.suffix.lower() != ".html":
        fail(f"expected .html file: {path}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        fail(f"{path.name}: file is empty")

    violations: list[str] = []
    for pattern, label in BANNED_PATTERNS:
        if pattern.search(content):
            violations.append(label)

    missing: list[str] = []
    for pattern, label in REQUIRED_CONTRACT:
        if not pattern.search(content):
            missing.append(label)

    if violations:
        fail(f"{path.name}: banned patterns found: {', '.join(violations)}")
    if missing:
        fail(f"{path.name}: missing required contract: {', '.join(missing)}")

    print(f"OK: {path.name} passes playground HTML contract")


def main() -> None:
    html_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).parents[1] / "assets" / "templates" / "artifact-editor.html"
    )
    validate_html(html_path)


if __name__ == "__main__":
    main()
