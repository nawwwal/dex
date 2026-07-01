---
name: reflect
description: "Use when reflecting over PMB memory: surfacing emerging patterns, finding leverage across active projects, detecting drift or silence, and turning reflection output into durable memory when useful."
argument-hint: "[emerge | leverage | drift | ideas for X]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Reflect

Read $ARGUMENTS. Mode:
- "emerge" or "patterns" → surface what's crystallizing
- "leverage" or "ideas for [X]" → find leverage for X
- "drift" or "what's quiet" → detect silence

Use PMB as the memory source. PMB event types are the unit of meaning; files and transcripts are only source material.

## Start Here

1. Call `prepare` or `overview` for the reflection topic.
2. Use `recall` for specific anchors, people, projects, or decisions.
3. Use `list_goals` when drift or leverage depends on active work.
4. Use `record_batch` only when the reflection creates durable facts, lessons, goals, activities, or milestones worth preserving.
5. If PMB is unavailable, say so and reflect only from visible context.

## PMB Reading Model

Read active memory first:

- `goal`: ongoing or future work.
- `fact`: stable project or user context.
- `lesson`: reusable rule, correction, or failure to avoid.
- `activity`: recent work log.
- `milestone`: checkpoint in a larger chain.
- indexed project context: files, commits, and code records.

For every object used as evidence, capture:

- event type
- source
- active or archived state
- related entities
- recency signal from date/frontmatter/content when present

Ignore archived objects by default. Use them only for historical comparison, recurring regressions, or when the user asks for older context.

## Mode: Emerge

Find patterns that are becoming durable knowledge but are not already captured as a PMB fact, lesson, goal, or milestone.

1. Read recent activities and related active goals, facts, lessons, and milestones.
2. Extract repeated decisions, non-obvious fixes, tool discoveries, process changes, project patterns, and recurring concerns.
3. Search for each candidate pattern stated plainly in PMB.
4. Skip patterns that already exist unless new evidence changes their meaning.
5. Promote only 1-3 patterns that have future use. Use `record_batch` with:
   - `lesson` for a reusable rule or failure to avoid.
   - `fact` for stable context.
   - `goal` for ongoing work.
   - `milestone` for a checkpoint.

Assign confidence markers: `[solid]` / `[evolving]` / `[hypothesis]`

Use PMB metadata only when the tool supports it. Otherwise keep the content concise and source-bounded.

## Mode: Leverage

Map where effort will compound across active PMB memory.

1. For each active project or goal: compare recent effort signals against output, blocker, and decision signals.
2. For recurring activities: check whether they still support the right goal.
3. For open goals or external task references: check whether they are current or stale.
4. For important collaborators: check whether one conversation would unblock multiple goals.
3. Find leverage points:
   - Relationship leverage — one conversation changes multiple outcomes
   - Skill compounding — learning X improves A, B, and C
   - High-signal low-effort — what takes 2 hours but looks like 2 weeks?
   - Memory cleanup — one relationship, update, or archive decision makes future briefs more accurate

Output 3-5 specific leverage points:
```
**[title]** — Evidence: [PMB records] / Effort: [time or unknown] / Impact: [what changes] / Action: [next step]
```

Separate facts from recommendations. If effort or impact is inferred, say so.

## Mode: Drift

Detect active work, relationships, or responsibilities that have gone quiet.

Use the current date from the environment or `date` command. Derive ages from actual dates when present; otherwise label recency as unknown.

Check:

1. Goals with no recent activity.
2. Recurring activities whose cadence is stale.
3. Important collaborators with no recent interaction.
4. Open tasks older than 14 days without a related activity or clear owner.
5. Ideas with no attached goal or project context.

For each drifted item: how long / why / risk of continued silence.

Do not mark something drifted just because it is archived. Archived means hidden from active work by default.

## Output Contract

Keep the response concise and evidence-led:

```markdown
## Findings
- **[record]** — [pattern/leverage/drift]. Evidence: [PMB record] -> [PMB record]. Confidence: [solid/evolving/hypothesis].

## Actions
- [next step, only when it follows from evidence]

## Sources
- [PMB records or source context read]

## Not Checked
- [unavailable PMB tools or external systems not consulted]
```

If writing to PMB, report the record type and summary. If not writing, say "No PMB records changed."
