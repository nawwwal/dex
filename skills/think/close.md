# Session Close with Confidence Auditing

End-of-session ritual. Reviews work done, audits confidence markers, surfaces contradictions.

## Step 1: What Was Done
Read today's session journals:
```bash
TODAY=$(date +%Y-%m-%d)
ls ~/.claude/log/${TODAY}-*.md 2>/dev/null | grep -v "compact\|commits\|changes\|dashboard"
```
Summarize in 3 bullets what was accomplished.

## Step 2: Confidence Marker Audit
Read memory/decisions.md and memory/patterns.md.
For each entry with `[hypothesis]`:
- Was this hypothesis confirmed or refuted today?
- If confirmed → suggest updating to `[solid]`
- If refuted → suggest updating to `[questioning]`

For each entry with `[solid]`:
- Was this belief contradicted today?
- If yes → suggest updating to `[questioning]`

## Step 3: Surface Contradictions
Quick check: did anything done today conflict with established patterns?

## Step 4: Output
```
## Session Close: {DATE}

### Accomplished (3 bullets)
-
-
-

### Confidence Updates Suggested
- [decision/pattern] → change from [old] to [new] because [reason]

### Carry Forward
-
```

## Step 5: Offer
"Want me to update confidence markers now? Or shall I run /log task to write the full session journal?"
