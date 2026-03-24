# Weekly Synthesis

Friday end-of-week review. Creates weekly-review entry and chains to evidence capture.

## Step 1: Gather Week's Sessions
```bash
WEEK_START=$(date -v-Mon +%Y-%m-%d 2>/dev/null || date -d 'last Monday' +%Y-%m-%d 2>/dev/null)
ls ~/.claude/log/ | grep -E "^202[0-9]-[0-9]{2}-[0-9]{2}" | while read f; do
  FILE_DATE=$(echo "$f" | cut -c1-10)
  if [[ "$FILE_DATE" > "$WEEK_START" ]]; then echo "$f"; fi
done
```
Read all session files from this week. Also read ~/.claude/TASKS.md and memory/decisions.md for this week's entries.

## Step 2: Write Weekly Review
Write to `~/.claude/log/YYYY-WNN-review.md` (ISO week number):

```markdown
---
date: YYYY-MM-DD
week: WNN
type: weekly-review
---

# Week WNN Review — {Date Range}

## Shipped / Completed
[concrete deliverables]

## Key Decisions
[link to decisions made this week in memory/decisions.md]

## Patterns Observed
[new patterns added to memory/patterns.md]

## Promotion Evidence This Week
[mapped to competency buckets]

## Next Week's Focus
[top 3 priorities]

## Drift Check
[what went quiet this week that shouldn't have?]
```

## Step 3: Chain to Evidence
1. Run `/think emerge` for this week's intelligence synthesis.
2. **Promotion case synthesis:** If it is Friday OR `career/gaps.md` is >7 days old → spawn `case-synthesizer` agent (foreground).
   - Report inline: "Case: [N competencies evidenced]. Top gap: [X]. gaps.md updated."
   - NEVER touch `case.md` — agent writes to `career/gaps.md` only.
3. Check if learnings are queued → `/claude-reflect:reflect`
