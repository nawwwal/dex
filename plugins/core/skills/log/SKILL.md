---
name: log
description: "Use when wrapping up a session ('done', 'eod', 'wrapping up'), synthesizing the week ('week'), or planning ahead ('plan my week'). NOT for morning briefing — use /assistant."
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /log — Session Lifecycle Router

You are a smart session lifecycle manager. Detect the user's intent and dispatch the appropriate sub-skill chain.

## Dispatch Logic

Read the user's message and apply the first matching rule:

### Morning / Briefing
Triggers: "morning", "hey", "good morning", "what's up", "start of day", session start from ~/
Action: Read and follow `$CLAUDE_SKILL_DIR/morning.md`

### Task Wrap-up
Triggers: "done", "task complete", "wrapping up this task", "finished X", /done
Action: Read and follow `$CLAUDE_SKILL_DIR/task.md`
Then: If today is Friday, also run day.md and week.md chains

### End of Day (not Friday)
Triggers: "eod", "done for the day", "end of day", "wrapping up" (weekday Mon–Thu)
Action: Read and follow `$CLAUDE_SKILL_DIR/day.md`

### End of Day (Friday)
Triggers: same as above but it IS Friday (check with Bash: `date +%A`)
Action: Run `$CLAUDE_SKILL_DIR/task.md` (if active task) → `$CLAUDE_SKILL_DIR/day.md` → `$CLAUDE_SKILL_DIR/week.md`
Then: Signal /think emerge for promotion evidence capture

### Weekly Synthesis
Triggers: "week", "weekly review", "friday synthesis", /week
Action: Read and follow `$CLAUDE_SKILL_DIR/week.md`
Then: Run /think emerge for evidence, run /claude-reflect:reflect if learnings queued

### 7-Day Planning
Triggers: "plan my week", "what should next 7 days look like", "planning session", "returning from leave", /7plan
Action: Read and follow `$CLAUDE_SKILL_DIR/plan.md`

## Loop Suggestion
For sessions expected to run >1 hour, suggest at the end of task.md:
"For long sessions: `/loop 20m Update session note with latest progress`"

## Session Note Naming
When writing session notes, use: `YYYY-MM-DD-{project-slug}-{topic}.md`
- project-slug: from `git branch --show-current | sed 's/the user\///' | sed 's/\//\-/g'`
- topic: 2-3 word slug from what was worked on
