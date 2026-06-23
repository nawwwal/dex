#!/usr/bin/env python3
"""Emit a tiny Portent/Tolaria context reminder.

ponytail: prompt hooks are the hot path, so this does no vault scanning. If we
need retrieval later, use a precompiled index instead of raw Markdown reads.
"""

from __future__ import annotations

import argparse
import json
import sys


CONTEXT = """Portent context receipt
required action:
- If this prompt may depend on prior project context, use core:portent and Tolaria MCP before behavior-changing work.
- Do not conclude "no context" from one weak search. First search harder: try aliases, project names, people, recent notes, `portent-index`, and `brain-log`; open likely partial matches and carry forward concrete details.
- If no relevant context is found, say which Tolaria sources or queries were checked. If they were not checked, say `Portent skipped: <reason>`.
- Before the final response, if this turn created durable project context, decisions, session notes, TODOs, or handoff value, use core:portent and Tolaria MCP to log or capture it.
- If Tolaria tools are not visible, try tool discovery before using any fallback.
- If skipped, state `Portent skipped: <reason>`.
- Use direct Markdown only as the core:portent fallback when Tolaria MCP is unavailable."""


def emit(event_name: str = "UserPromptSubmit") -> None:
    print(
        json.dumps(
            {
                "continue": True,
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "additionalContext": CONTEXT,
                },
            }
        )
    )


def self_test() -> int:
    assert "Tolaria MCP" in CONTEXT
    assert "Do not conclude \"no context\" from one weak search" in CONTEXT
    assert "portent-index" in CONTEXT
    assert "which Tolaria sources or queries were checked" in CONTEXT
    assert "Before the final response" in CONTEXT
    assert "tool discovery" in CONTEXT
    assert "Portent skipped" in CONTEXT
    assert "Markdown only as the core:portent fallback" in CONTEXT
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit Portent context receipt.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    try:
        payload = json.loads(sys.stdin.read() or "{}")
        emit(str(payload.get("hook_event_name") or "UserPromptSubmit"))
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
