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
- Treat this hook as a reminder, not retrieval: use the core:portent skill flow for qmd queries, source reads, and writeback.
- If this prompt may depend on prior project context, use core:portent before behavior-changing work: use `/Users/aditya.nawal/Documents/oddly-specific` and qmd collection `portent` by default; use Tolaria MCP for note opening, refresh, and writeback, not routine vault rediscovery.
- Treat the configured vault path as already resolved. Do not call `list_vaults` just to confirm it; call it only if the configured path is unreadable, another vault is named, multiple vaults are plausible, or a Tolaria operation fails because the vault target is ambiguous.
- Choose the qmd mode that fits when context matters: `qmd search` for exact anchors, `qmd vsearch` for semantic recall, `qmd query` for synthesis or reranking with lex/vec/hyde, then source reads with `qmd get`/`qmd multi-get` before answering from snippets.
- Do not run every qmd mode by default; escalate when recall is weak, partial, contradictory, or high-stakes.
- Do not use Tolaria full-text search as the retrieval fallback; if qmd is unavailable, use direct Markdown search in the resolved vault path and say qmd is degraded.
- Do not conclude "no context" from one weak search. First search harder with qmd or direct Markdown: try aliases, project names, people, recent notes, `portent-index`, `brain-log`, and `agent-behavior-gotchas`; open likely partial matches and carry forward concrete details.
- If no relevant context is found, say which qmd queries, Markdown paths, or Tolaria sources were checked. If they were not checked, say `Portent skipped: <reason>`.
- Capture first for non-trivial work. Before the final response, if this turn created durable project context, decisions, design or technical rationale, rejected options, session notes, TODOs, handoff value, user workflow behavior, system behavior, or agent-behavior corrections, use core:portent and Tolaria MCP to update the best existing object first.
- Be context-hungry: when the why, rationale, tradeoff, owner, source boundary, or future-use angle is missing, ask one focused question or record the gap instead of silently dropping it.
- Treat user corrections as writeback triggers, not debates. Update `agent-behavior-gotchas` or the owning object before claiming the lesson is handled.
- Avoid tiny duplicate notes. Prefer the existing project, operation, responsibility, map, gotcha, or `brain-log` owner before creating a new object.
- "No update needed" is allowed only after checking for reusable decisions, RCAs, blockers, source boundaries, behavior changes, design or technical rationale, and handoff value; name the skip reason when no write is made.
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
    assert "reminder, not retrieval" in CONTEXT
    assert "/Users/aditya.nawal/Documents/oddly-specific" in CONTEXT
    assert "already resolved" in CONTEXT
    assert "Do not call `list_vaults` just to confirm it" in CONTEXT
    assert "fails because the vault target is ambiguous" in CONTEXT
    assert "not routine vault rediscovery" in CONTEXT
    assert "qmd mode that fits" in CONTEXT
    assert "qmd search" in CONTEXT
    assert "qmd vsearch" in CONTEXT
    assert "qmd query" in CONTEXT
    assert "lex/vec/hyde" in CONTEXT
    assert "qmd get" in CONTEXT
    assert "qmd multi-get" in CONTEXT
    assert "Do not run every qmd mode by default" in CONTEXT
    assert "Do not use Tolaria full-text search" in CONTEXT
    assert "qmd is degraded" in CONTEXT
    assert "Do not conclude \"no context\" from one weak search" in CONTEXT
    assert "portent-index" in CONTEXT
    assert "agent-behavior-gotchas" in CONTEXT
    assert "which qmd queries, Markdown paths, or Tolaria sources were checked" in CONTEXT
    assert "Capture first for non-trivial work" in CONTEXT
    assert "Before the final response" in CONTEXT
    assert "design or technical rationale" in CONTEXT
    assert "rejected options" in CONTEXT
    assert "Be context-hungry" in CONTEXT
    assert "ask one focused question" in CONTEXT
    assert "user corrections as writeback triggers" in CONTEXT
    assert "Avoid tiny duplicate notes" in CONTEXT
    assert "No update needed" in CONTEXT
    assert "behavior changes" in CONTEXT
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
