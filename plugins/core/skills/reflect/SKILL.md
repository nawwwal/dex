---
name: reflect
description: "Use when reflecting over the user's Tolaria knowledge base through the Portent object model: surfacing emerging patterns, finding leverage across active projects/responsibilities/operations/tasks, detecting drift or silence, and turning reflection output into Portent notes when useful."
argument-hint: "[emerge | leverage | drift | ideas for X]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, mcp__tolaria__list_vaults, mcp__tolaria__open_note
---

# Reflect

Read $ARGUMENTS. Mode:
- "emerge" or "patterns" → surface what's crystallizing
- "leverage" or "ideas for [X]" → find leverage for X
- "drift" or "what's quiet" → detect silence

Use Tolaria as the knowledge base and Portent as the analysis model. Portent types are the unit of meaning; folders are storage.

## Start Here

1. Resolve the active Tolaria vault with `mcp__tolaria__list_vaults` when it is available.
2. Treat only these Tolaria tools as guaranteed: `mcp__tolaria__list_vaults` and `mcp__tolaria__open_note`.
3. Select the vault deterministically:
   - If one vault is returned, use it.
   - If the user gives a vault label, name, or path hint, match it against listed vault labels and paths.
   - If multiple plausible writable vaults remain and the user gave no hint, ask before reading widely or writing.
   - If the selected vault has no path, or the path is missing or unreadable, stop and report that reflection cannot run from Tolaria.
4. Read the vault's AGENTS.md first when `hasAgentInstructions` is true and the file exists.
5. Use direct Markdown fallback inside the resolved vault path:
   - Search Markdown by frontmatter, title, wikilinks, and content.
   - Read enough files to ground the answer in actual Portent objects.
   - Write only when the user asks to capture the reflection or when the reflection produces a durable pattern worth saving.
   - Never write outside the resolved vault path as a substitute for Tolaria.
6. Do not invent Tolaria write, search, create, update, or delete tool names.
7. Open created or edited notes with `mcp__tolaria__open_note` when useful for review.

Do not use `~/.claude/log`, `~/.claude/memory`, `~/.claude/TASKS.md`, or generic Codex memory as the reflection source of truth. Mention them only as legacy migration inputs when the user explicitly asks.

## Portent Reading Model

Read active organized objects first:

- `Project`: bounded outputs and current work.
- `Responsibility`: long-running outcomes that should not go quiet.
- `Operation`: recurring routines that maintain responsibilities or projects.
- `Task`: durable next actions or external task references.
- `Event`: what happened, decisions, meetings, sessions, incidents.
- `Note`: durable artifacts, references, decisions, checklists, summaries.
- `Topic`: conceptual lenses or areas of interest.
- `Person`: collaborators, stakeholders, customers, agents.

For every object used as evidence, capture:

- `type`
- `organized`
- `archived`
- `belongs_to`
- `related_to`
- recency signal from date/frontmatter/content when present

Ignore archived objects by default. Use them only for historical comparison, recurring regressions, or when the user asks for older context.

## Mode: Emerge

Find patterns that are becoming durable knowledge but are not already organized as a Portent `Note` or `Topic`.

1. Read recent `Event` objects and related active `Project`, `Responsibility`, `Operation`, `Note`, and `Topic` objects.
2. Extract repeated decisions, non-obvious fixes, tool discoveries, process changes, project patterns, and recurring concerns.
3. Search for each candidate pattern stated plainly in existing organized `Note` or `Topic` objects.
4. Skip patterns that already exist unless new evidence changes their meaning.
5. Promote only 1-3 patterns that have future use. Use:
   - `Note` for a durable artifact, decision record, checklist, or practice.
   - `Topic` for an ongoing conceptual lens.

Assign confidence markers: `[solid]` / `[evolving]` / `[hypothesis]`

If writing a pattern, use Portent frontmatter:

```yaml
---
type: Note
organized: true
archived: false
belongs_to: "[[Primary Project or Responsibility]]"
related_to:
  - "[[Relevant Topic]]"
---
```

Use `belongs_to` only when there is a clear primary context. Otherwise leave it out and explain the missing parent.

## Mode: Leverage

Map where effort will compound across active Portent objects.

1. For each active `Project`: compare recent effort signals against output, blocker, and decision signals.
2. For each active `Responsibility`: check whether related projects, operations, and tasks are maintaining the outcome.
3. For each recurring `Operation`: check whether it still supports the right responsibility or project.
4. For each open `Task` or external task reference: check whether it belongs to a current project/responsibility or is stale.
5. For each important `Person`: check whether one conversation would unblock multiple objects.
3. Find leverage points:
   - Relationship leverage — one conversation changes multiple outcomes
   - Skill compounding — learning X improves A, B, and C
   - High-signal low-effort — what takes 2 hours but looks like 2 weeks?
   - Object cleanup — one relationship or archive decision makes future briefs more accurate

Output 3-5 specific leverage points:
```
**[title]** — Evidence: [Portent object links] / Effort: [time or unknown] / Impact: [what changes] / Action: [next step]
```

Separate facts from recommendations. If effort or impact is inferred, say so.

## Mode: Drift

Detect active work, relationships, or responsibilities that have gone quiet.

Use the current date from the environment or `date` command. Derive ages from actual dates when present; otherwise label recency as unknown.

Check:

1. `Project`: last related `Event`, open tasks, blocked decisions, archived mismatch.
2. `Responsibility`: last supporting `Event`, active `Operation`, or active project.
3. `Operation`: last run and whether the cadence is stale.
4. `Person`: last related `Event` or project mention.
5. `Task`: open tasks older than 14 days without a related event or clear parent.
6. `Topic`: active ideas with no project/responsibility attachment.

For each drifted item: how long / why / risk of continued silence.

Do not mark something drifted just because it is archived. Archived means hidden from active work by default.

## Output Contract

Keep the response concise and evidence-led:

```markdown
## Findings
- **[object]** — [pattern/leverage/drift]. Evidence: [[Object]] → [[Object]]. Confidence: [solid/evolving/hypothesis].

## Actions
- [next step, only when it follows from evidence]

## Sources
- [objects or paths read]

## Not Checked
- [unavailable tools, missing vaults, external systems not consulted]
```

If writing back to Tolaria, report created or updated objects, type, lifecycle state, and relationships. If not writing, say "No Portent records changed."
