# End of Day Journal

Comprehensive end-of-day capture. Scans all sessions today, Slack, calendar, email.

## Step 1: Gather Today's Sessions
```bash
TODAY=$(date +%Y-%m-%d)
ls ~/.claude/log/${TODAY}-*.md 2>/dev/null | grep -v "compact\|commits\|changes\|dashboard"
```
Read each file found. Synthesize what was accomplished across all sessions.

## Step 2: Read ~/.claude/TASKS.md
Check open items. Note what moved, what's stuck, what's new.

## Step 3: Optional — Check Slack + Calendar
If user has time: check Slack for any DMs needing response tomorrow.
Check tomorrow's calendar for preparation needed.

## Step 4: Write EOD Journal
Write to `~/.claude/log/YYYY-MM-DD-eod.md`:

```markdown
---
date: YYYY-MM-DD
type: eod
---

# EOD — {Date}

## Today's Summary
[2-3 sentence synthesis of the day's work]

## Sessions
[bullet list of sessions and their main outcomes]

## Tasks Status
- Completed: [list]
- Progressed: [list]
- Blocked: [list]

## Tomorrow's Focus
[top 3 priorities]

## Knowledge Graph
[3-5 wikilinks added today: [[decision]], [[pattern]], [[project]]]
```

## Step 5: Compound step — capture what was solved

Ask: **"What did we solve today that a future session should know?"**

**If yes or if there was a commit this session:** write a solution doc.
**If no or user doesn't answer:** skip entirely. Do not force it.

Write to `~/.claude/learn/solutions/YYYY-MM-DD-{slug}.md`:

```yaml
---
type: solution
date: YYYY-MM-DD
tags: [topic1, topic2]
source: session
project: {project-name}
---
```

# {Problem class title — generalized, not session-specific}

## Problem
[What class of problem this solves — specific enough to match in future sessions]

## Approach
[What worked and why]

## Reusable pattern
[The generalizable takeaway in one sentence]

## Anti-patterns
[What to avoid]

---

Then add a wikilink to `~/.claude/learn/index.md`. Theme from first tag:
- `testing` → Testing
- `blade`, `react`, `frontend` → Blade / React / Frontend
- `vault`, `hook`, `agent` → Meta-System / Vault
- `design`, `figma`, `ux` → Design Thinking
- `process`, `tooling` → Process / Documentation / Tooling
- `people`, `communication` → People & Interpersonal
- anything else → All Notes (top-level)

## Step 6: Update QMD
```bash
qmd update && qmd embed
```
