---
name: symphony
description: Use when setting up a daemon that polls DevRev issues and dispatches Claude Code automatically per issue, writing or debugging a WORKFLOW.md config, implementing the orchestrator poll loop or workspace lifecycle, or debugging issues like wrong dispatch order, Claude not continuing turns, or retry not backing off.
---

# Symphony

Symphony is a long-running automation daemon. It polls DevRev, creates an isolated workspace per issue, and runs Claude Code for each one. It is a **scheduler/runner** — not business logic. Ticket mutations, state transitions, and PR comments belong to the agent and WORKFLOW.md prompt, not the orchestrator.

**Success condition:** reaching a handoff state (e.g. `Human Review`), not `Done`.

## When to Use

- Setting up a daemon that polls DevRev and dispatches Claude Code to issues
- Writing or debugging a `WORKFLOW.md` config file
- Implementing the orchestrator poll loop, workspace lifecycle, or agent subprocess
- Debugging: issues dispatched in wrong order, Claude Code not continuing turns, retry not backing off

## Stack (Razorpay)

| Layer | Tool |
|---|---|
| Tracker | DevRev — `mcp__plugin_compass_devrev__*` |
| Coding agent | Claude Code CLI — `claude --print --output-format stream-json` |
| Config | `WORKFLOW.md` in the project root — YAML frontmatter + prompt template |

## How to Run Symphony

Symphony is not yet a published package — you implement it from this spec. The entry point:

1. Set `$DEVREV_TOKEN` in your environment
2. Create `WORKFLOW.md` at the root of the repo Claude Code will work in (see `workflow-md-schema.md`)
3. Create DevRev issues with a stage matching `active_states` in WORKFLOW.md
4. Start the daemon: `node symphony.js --workflow ./WORKFLOW.md`
5. When Claude Code finishes, your DevRev issue moves to the stage in `terminal_states` — check DevRev

**Solo designer config:** Set `max_concurrent_agents: 1` to run one issue at a time. Safest starting point.

## Bootstrap: Starting from a PRD

Symphony needs existing DevRev issues to poll. See `workflow-md-schema.md § Bootstrap` for how to create them from a PRD, including linking `blocked_by` dependencies.

## Reference Files

- `workflow-md-schema.md` — YAML schema, TypeScript interface, Blade example, Bootstrap guide
- `orchestration.md` — poll tick sequence, concurrency, retry backoff, DevRev MCP mapping
- `agent-protocol.md` — Claude Code CLI invocation, turn lifecycle, token accounting
- `workspace-safety.md` — path invariants, hook semantics, security notes
