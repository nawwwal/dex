# 7-Day Forward Plan

Generates a concrete day-by-day plan for the next 7 working days.

## Step 1: Load Context
- Read memory/goals.md — current priorities and OKRs
- Read memory/projects.md — active project status
- Read ~/.claude/TASKS.md — all open tasks
- Check Google Calendar (if MCP available) — events and constraints next 7 days
- Run /think drift — what's been quiet that needs attention?

## Step 2: Identify Constraints
- Which days have heavy meetings (>3h scheduled)?
- Any TCDs (tight commitments with dates)?
- Any leave or travel planned?
- Carry-forwards from last week that are now urgent?

## Step 3: Generate Plan
7 working days (Mon–Fri only, skip weekends):

```
## 7-Day Plan: {DATE_RANGE}

### Monday {DATE}
**Focus:** [main theme]
- [ ] Task 1 (est. Xh)
- [ ] Task 2 (est. Xh)
**Risk:** [what could block this?]

### Tuesday {DATE}
...
```

## Step 4: Highlight Drift Items
For each project that's been quiet >5 days: flag it with "SILENT since [date]"

## Step 5: Leave-Adjacent Risk
If any TCD falls within 2 days of planned leave: flag prominently in red.
