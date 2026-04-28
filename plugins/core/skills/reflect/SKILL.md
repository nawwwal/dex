---
name: reflect
description: "Use when surfacing patterns from sessions, finding high-leverage focus, or checking which projects have gone quiet."
argument-hint: "[emerge | ideas for X | drift]"
allowed-tools: Bash, Read, Write, Edit, mcp__qmd__search, mcp__qmd__vsearch, mcp__qmd__query, mcp__qmd__get
---

# Reflect

Read $ARGUMENTS. Mode:
- "emerge" or "patterns" → surface what's crystallizing
- "ideas for [X]" → find leverage for X
- "drift" or "what's quiet" → detect silence

## Shared Context (load once, all modes)

```bash
find ~/.claude/log -name "*.md" -mtime -14 | grep -v compact | sort -r | head -30
```

Read:
- `~/.claude/memory/projects.md` — active projects, DevRev IDs, Slack anchors
- `~/.claude/memory/patterns.md` — patterns added or applied recently

---

## Mode: Emerge

From shared context: look for insights not yet captured in `patterns.md` or `decisions.md`.

1. **Extract TILs** — novel approaches, non-obvious bug fixes, tool discoveries, process improvements
2. **Graduate ideas** — scan sessions for `#idea` tags, "I should", "worth exploring"; promote 1-3 to a `learn/` or `til/` note
3. **Fabrication check** — before reporting a pattern, search the vault for it stated plainly. Already in `decisions.md` or `patterns.md`? Skip it.

Assign confidence markers: `[solid]` / `[evolving]` / `[hypothesis]`

---

## Mode: Leverage

From shared context: map where effort will compound most.

1. For each active project in `projects.md`: estimate hours invested vs impact delivered
2. For each DevRev issue: is there a gap one more delivery would close?
3. Find leverage points:
   - Relationship leverage — one conversation changes multiple outcomes
   - Skill compounding — learning X improves A, B, and C
   - High-signal low-effort — what takes 2 hours but looks like 2 weeks?

Output 3-5 specific leverage points:
```
**[title]** — Evidence: [vault signal] / Effort: [time] / Impact: [what changes] / Action: [next step]
```

---

## Mode: Drift

From shared context: detect what's gone quiet.

1. **Projects** — for each entry in `projects.md`: when did it last appear in sessions?
2. **Relationships** — read `memory/people.md`; when was each key stakeholder last mentioned?
3. **Tasks** — read `~/.claude/TASKS.md`; any item open >14 days without a session mention?

For each drifted item: how long / why / risk of continued silence.

After reporting: offer to run Emerge to check if the silence signals something.
