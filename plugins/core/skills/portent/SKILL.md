---
name: portent
description: "Use when storing, organizing, retrieving, or briefing from the user's Tolaria knowledge base using the Portent object model: project context, responsibilities, operations, session logs, decisions, current todos, tasks, events, notes, topics, people, archived records, and durable handoffs."
argument-hint: "[capture | log | organize | brief | todo | archive | search]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__tolaria__list_vaults, mcp__tolaria__open_note
---

# Portent

Use the user's Tolaria vault as the knowledge base and Portent as the organizing model.

Portent is object-first: folders are storage, not meaning. Every durable object must answer "what is this?" with a Portent type, and every organized object must answer "what will this be useful for?" with relationships.

Read `references/portent-spec.md` when classification, lifecycle, or relationship choices are unclear.

## Start Here

1. Resolve the active Tolaria vault with `mcp__tolaria__list_vaults` when it is available.
2. Treat only the tools listed in this skill frontmatter as guaranteed: `mcp__tolaria__list_vaults` and `mcp__tolaria__open_note`.
3. Select the vault deterministically:
   - If `list_vaults` returns one vault, use it.
   - If the user gives a vault label, name, or path hint, match that hint against the listed vault labels and paths.
   - If multiple plausible writable vaults remain and the user gave no hint, ask which vault to use before writing.
   - If the selected vault has no path, or the path is missing or unreadable, stop and report that the Tolaria vault cannot be used.
4. Read the vault's AGENTS.md first when `hasAgentInstructions` is true and the file exists.
5. When Tolaria only provides vault discovery/opening, use direct Markdown fallback inside the resolved vault path:
   - Verify the resolved path exists and is readable before searching or writing.
   - Orient with filesystem reads of AGENTS.md, index notes, and nearby README files when present.
   - Search Markdown files in the vault path by title, frontmatter, wikilinks, and content.
   - Read matching Markdown files directly from the vault path.
   - Write by creating or editing Markdown files in the vault path with YAML frontmatter and wikilinks.
   - Never write outside the resolved vault path as a substitute for Tolaria.
6. Do not invent Tolaria write, search, create, update, or delete tool names.
7. Open created or edited notes with `mcp__tolaria__open_note` when useful for review.

Do not write canonical knowledge records to `~/.claude/log`, `~/.claude/TASKS.md`, or generic Codex memory. Those may be legacy inputs, but Tolaria is the source of truth.

## Compiled Portent Operations

When the active vault contains the operating notes below, load them for brain-grade behavior:

- `[[portent-operating-contract]]`
- `[[portent-write-templates]]`
- `[[portent-ingest-query-lint-runbook]]`
- `[[portent-index]]`
- `[[brain-log]]`

Use existing Tolaria MCP tools for discovery, search, note reads, note creation, opening, and refresh.

Use direct Markdown edits inside the resolved Tolaria vault path for updating existing notes, saved views, index notes, log notes, relationship repair, and contract maintenance.

Prefer compiled Portent objects over raw source re-reading. Verify live systems when facts are drift-prone.

## Portent Defaults

Use these types before inventing anything custom:

- PORT: `Project`, `Operation`, `Responsibility`, `Task`
- ENTP: `Event`, `Note`, `Topic`, `Person`

Use these relationships first:

- `belongs_to`: primary context, ownership, or composition; usually one main parent.
- `related_to`: secondary usefulness, association, or many-to-many context.

Use lifecycle fields:

```yaml
organized: false
archived: false
```

Set `organized: true` only when the object has a clear title, type, and enough relationships to explain future use.

## Mode Routing

Choose the mode from the user's request. If no mode is named, infer it from the outcome they want.

### Capture

Use for quick dumping, rough notes, links, screenshots, fragments, or "remember this".

Create the lightest useful object. Default to `Note` for knowledge, `Event` for something that happened, and `Task` only when the user is recording work to do. Keep `organized: false` unless the parent/type/relationships are clear.

Minimum capture frontmatter:

```yaml
---
type: Note
organized: false
archived: false
related_to: []
---
```

### Log

Use for completed work sessions, decisions, incidents, meetings, achievements, or handoffs that should survive the chat.

Create an `Event` unless the output is itself a durable artifact, in which case create or update a `Note` and relate it to the event. Prefer one event per meaningful session.

The event should include:

- What happened, with concrete evidence.
- Decisions and rationale.
- Changed files, commits, links, DevRev IDs, PRs, docs, or external anchors when available.
- Carry-forward tasks or open questions.
- Relationships to the primary `Project`, `Responsibility`, people, and topics.

### Organize

Use when the user asks to clean up captured material, attach context, build project maps, or convert loose notes into Portent objects.

For each candidate:

1. Pick a default Portent type.
2. Improve the title so it names the real object.
3. Add one primary `belongs_to` when there is a clear parent.
4. Add `related_to` links for useful secondary context.
5. Set `organized: true` only when future use is obvious.
6. Delete or leave captured when no useful attachment exists.

### Brief

Use for "brief me", "what should I know", "what changed", "what is active", project briefings, weekly reviews, and handoff prep.

Build the briefing from organized Portent objects first, then recent captured objects. Cover:

- Active projects and the latest event per project.
- Open tasks or external task references related to those projects.
- Decisions made since the last brief.
- Quiet projects or responsibilities that may need attention.
- Useful next actions, separated from facts.

### Todo

Use when the user asks for current todos, next actions, backlog, or what to do next.

Tasks may live outside the knowledge base. In Tolaria, store a `Task` object only when the task needs durable context or relationships. Otherwise, record a reference to the external task tool or issue and relate it to its `Project`, `Operation`, or `Responsibility`.

When external task tools are unavailable, say which sources were checked and which were not.

### Archive

Use when something is done, stale, no longer active, or should disappear from active views while staying searchable.

Set `archived: true`. Preserve relationships and add a short archive note explaining why it is no longer active.

### Search

Use when the user asks what exists, what is known, or where something lives.

Search by title, type, relationship, and content. If no Tolaria search tool is exposed, search the resolved vault's Markdown files directly. Return the object title, type, lifecycle state, and why it matters. Do not turn search results into a briefing unless the user asks for synthesis.

## Object Writing Rules

Use Markdown frontmatter plus wikilinks:

```yaml
---
type: Event
organized: true
archived: false
belongs_to: "[[Launch Portent v0.1]]"
related_to:
  - "[[Alice Example]]"
  - "[[Knowledge graphs]]"
---
```

Keep filenames stable and boring. The title and frontmatter carry meaning; the folder does not.

Prefer updating an existing object over creating a duplicate. Before writing a new `Project`, `Responsibility`, `Operation`, `Topic`, or `Person`, search for a likely existing object.

## Response Contract

After a write, report:

- Created or updated objects.
- Type and lifecycle state.
- Key relationships added or missing.
- Any sources not checked.

Keep the answer short. The knowledge base should hold the detail; the chat response should state what changed and what remains uncertain.
