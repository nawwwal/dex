---
name: portent
description: "Use when retrieving from or writing to Aditya's Tolaria/Portent knowledge base: project context, decisions, RCAs, blockers, PR or DevRev state, Slack/Gmail/Calendar meeting context, behavioral rules, technical/design/team knowledge, ways of working, session logs, handoffs, current todos, tasks, people, topics, archived records, and durable agent memory. Use qmd for retrieval; use Tolaria/direct Markdown for vault discovery, note opening, refresh, and writeback."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__qmd__status, mcp__qmd__search, mcp__qmd__query, mcp__qmd__get, mcp__qmd__multi_get, mcp__tolaria__list_vaults, mcp__tolaria__get_vault_context, mcp__tolaria__create_note, mcp__tolaria__open_note, mcp__tolaria__refresh_vault
---

# Portent

Use the knowledge base as a habit loop:

1. **Orient**: use the configured default vault from global `~/.agents/AGENTS.md`, read vault `AGENTS.md` when present, and check qmd health when retrieval matters.
2. **Retrieve**: use qmd, not Tolaria search. Pick the cheapest qmd mode that fits: `search` for exact anchors, `vsearch` for semantic recall, `query` for synthesis or reranking, then read source text with `get` or `multi_get`.
3. **Decide**: answer from retrieved text and live sources when facts may drift.
4. **Write**: update the best existing Markdown object when durable knowledge appeared.
5. **Refresh**: refresh Tolaria and qmd after edits when tooling works.
6. **Report**: say what was read, what changed, and what was unavailable.

Tolaria is the vault UI and note surface. qmd is the search brain. Portent is the shape of memory.

Do not use Tolaria full-text search as the main retrieval path. If qmd is unavailable, use direct Markdown search in the resolved vault path and say qmd is degraded.

## References

- Read `references/retrieval.md` for qmd search patterns, source-reading rules, and degraded retrieval fallback.
- Read `references/writeback.md` for what to write, where to put it, and how to avoid "no update needed" mistakes.
- Read `references/hooks.md` when changing hook behavior or checking how hooks support the Portent loop.
- Read `references/portent-spec.md` only when object type, lifecycle, relationship, source packet, derived assertion, or MOC choices are unclear.
- Read `references/setup.md` when Tolaria, qmd, the `portent` collection, or local qmd models are missing or broken.

## Hook Layer

Hooks are receipts and reminders, not the memory system. The bundled `UserPromptSubmit` hook should only inject the default vault/qmd/writeback contract. Keep retrieval, source reading, and note edits in this skill flow.

## Start Pattern

1. Use configured vault:
   - Default to the vault path and qmd collection recorded in global `~/.agents/AGENTS.md`.
   - For this machine, that is `/Users/aditya.nawal/Documents/oddly-specific` and qmd collection `portent`.
   - Treat that configured path as already resolved. Do not call `mcp__tolaria__list_vaults` just to confirm it.
   - Do not rediscover the vault on every run.
   - Use `mcp__tolaria__list_vaults` only when the configured path is missing or unreadable, the user names another vault, multiple vaults are plausibly involved, or a Tolaria operation fails because the vault target is ambiguous.
   - If the selected vault path is missing or unreadable, stop; do not write elsewhere.
2. Read vault instructions:
   - If `hasAgentInstructions` is true and `AGENTS.md` exists, read it before writing.
3. Retrieve with qmd:
   - Use `mcp__qmd__search`/`qmd search` for exact anchors.
   - Use `qmd vsearch` for semantic recall when the user's words may not match the saved note.
   - Use `mcp__qmd__query`/`qmd query` for hybrid reranked synthesis with `intent`, `lex`, `vec`, and `hyde`.
   - Use `mcp__qmd__get`, `mcp__qmd__multi_get`, `qmd get`, or `qmd multi-get` before trusting snippets.
   - Do not run every qmd mode by default. Escalate only when the first mode is weak, partial, contradictory, or the stakes justify broader recall.
4. Write if useful:
   - Update existing notes first.
   - Create a new note only when no current object owns the fact.
   - Use direct Markdown edits inside the vault path, or `mcp__tolaria__create_note` when it is available and appropriate.
5. Refresh:
   - Use `mcp__tolaria__refresh_vault` after note edits when visible.
   - Run `qmd update -c portent` and `qmd embed -c portent` after Markdown edits when qmd works.

## What To Keep

Write durable, Aditya-relevant knowledge freely:

- behavior: agent corrections, preferred workflows, repeated failure modes, communication rules
- technical: APIs, contracts, repo behavior, test paths, server maps, data/state shape
- design: UI decisions, system constraints, visual direction, interaction rules
- team: owners, reviewers, source-of-truth channels, escalation paths, dependency maps
- work state: decisions, blockers, RCAs, PR state, DevRev state, meeting outcomes, handoffs
- personal operating context: Aditya's ways of working, recurring preferences, focus constraints, review style

Skip broad team noise, transient chat, stale bot output, and unsupported guesses.

## Writeback Audit

Before the final response on non-trivial work, ask:

1. Did this create or change a reusable decision, RCA, blocker, source boundary, task, handoff, behavior rule, system behavior, or working-style preference?
2. Would Aditya or a future agent search for this later?
3. Is there an existing object that should own it?

If yes, write it. "No update needed" is allowed only after this audit.

Behavior corrections usually go to `[[agent-behavior-gotchas]]`. Knowledge-base maintenance goes to `[[brain-log]]`. Project state goes to the owning Project, Operation, Responsibility, Event, or Task.

## Object Defaults

Use the default types before inventing anything:

- PORT: `Project`, `Operation`, `Responsibility`, `Task`
- ENTP: `Event`, `Note`, `Topic`, `Person`

Use `belongs_to` for the main parent and `related_to` for useful secondary links.

Use lifecycle fields:

```yaml
organized: false
archived: false
```

Set `organized: true` only when the object has a clear title, type, and enough relationships to help future retrieval.

## Source Discipline

Separate:

- source packet: raw evidence, usually an `Event` or `Note`
- derived assertion: agent conclusion with provenance in `Key assertions` or fields such as `derived_from`
- MOC: map of content with `Current`, `Historical`, `Key assertions`, `Open gaps`, and `Read next`

Do not turn every inference into memory. Store only durable, source-bounded, Aditya-relevant facts.

## Response Contract

After retrieval or writeback, keep the chat response short:

- Sources read or qmd/direct-Markdown fallback used
- Objects created or updated
- Type, lifecycle, and key relationships when a note changed
- qmd/Tolaria/source gaps

Never claim qmd, Tolaria, or live systems were checked if they were unavailable.
