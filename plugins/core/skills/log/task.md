# Task Journal

You are writing a task-scoped session journal. This captures what was accomplished in the current task.

## Step 1: Run /simplify
Before documenting, run `/simplify` on any files changed this session.
Tell the user: "Running /simplify on changed files first..."

## Step 2: Determine Session Name
```bash
TODAY=$(date +%Y-%m-%d)
PROJECT=$(git branch --show-current 2>/dev/null | sed 's/the user\///' | sed 's/\//\-/g' | cut -c1-30)
if [[ -z "$PROJECT" ]] || [[ "$PROJECT" == "main" ]]; then
  PROJECT=$(basename "$PWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')
fi
echo "$TODAY-$PROJECT"
```

## Step 3: Write Session Journal
Write to `~/.claude/log/YYYY-MM-DD-{project}-{topic}.md`:

```markdown
---
date: YYYY-MM-DD
project: {project}
type: session
decisions-count: N
---

# {Topic} — {Date}

## Accomplished
- [what was actually done, specific and concrete]

## Decisions Made
- [any significant choices, with rationale]

## Carry Forward
- [what's next, what's blocked]

## Git log
[output of: git log --oneline -5]
```

## Step 4: Update TASKS.md
If any tasks were completed, mark them done in ~/.claude/TASKS.md.

## Step 5: Loop Suggestion
If this session ran >1 hour, suggest for next time:
"/loop 20m Update session note with progress since last checkpoint"
