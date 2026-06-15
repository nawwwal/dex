#!/usr/bin/env python3
"""Ask for a Portent write-back pass after durable work.

ponytail: one heuristic pass only. The hook reminds the agent; core:portent and
Tolaria MCP own the actual write.
"""

from __future__ import annotations

import argparse
import json
import sys


DURABLE_TERMS = (
    "added",
    "changed:",
    "committed",
    "created",
    "decision",
    "fixed",
    "handoff",
    "implemented",
    "pull request",
    "released",
    "updated",
    "verified:",
)
DONE_TERMS = (
    "Portent skipped:",
    "Created or updated objects",
    "Updated objects",
)
REASON = (
    "Before stopping, decide whether this turn created durable Portent knowledge "
    "(project context, decisions, session log, changed files, TODOs, or handoff value). "
    "If yes, use core:portent with Tolaria MCP to log or capture it. "
    "If no, finish with `Portent skipped: <reason>`."
)


def should_remind(payload: dict[str, object]) -> bool:
    if payload.get("stop_hook_active"):
        return False
    message = str(payload.get("last_assistant_message") or "")
    if not message.strip():
        return False
    if any(term in message for term in DONE_TERMS):
        return False
    lower = message.lower()
    return any(term in lower for term in DURABLE_TERMS)


def self_test() -> int:
    assert should_remind({"last_assistant_message": "Implemented X\nVerified: tests passed"})
    assert not should_remind({"stop_hook_active": True, "last_assistant_message": "Implemented X"})
    assert not should_remind({"last_assistant_message": "Portent skipped: unrelated"})
    assert not should_remind({"last_assistant_message": "The capital is Paris."})
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Remind agents to write durable Portent updates.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        payload = {}
    if should_remind(payload):
        print(json.dumps({"decision": "block", "reason": REASON}))
    else:
        print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
