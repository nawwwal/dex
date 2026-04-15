# Drift Detection

Finds what's been quietly going silent.

## Step 1: Check Projects
Scan `~/.claude/work/` for active project slugs, then check when each last appeared in sessions:
```bash
for project in $(ls ~/.claude/work/ 2>/dev/null); do
  LAST=$(ls -t ~/.claude/log/ 2>/dev/null | grep "$project" | head -1)
  echo "$project: last session = ${LAST:-never}"
done
```

## Step 2: Check Relationships
Read memory/people.md. For key stakeholders: when was the last Slack mention found in sessions?

## Step 3: Check Tasks
Read ~/.claude/TASKS.md. Any item that's been open for >14 days without a session mention?

## Step 4: Check Goals
Read memory/goals.md. Any goal/priority not referenced in sessions this week?

## Step 5: Report
For each drifted item:
- How long has it been quiet?
- Why might it have gone quiet? (deprioritized, blocked, forgotten, completed)
- What's the risk of continued silence?

Then: offer to run emerge.md to surface whether the silence signals something important.
