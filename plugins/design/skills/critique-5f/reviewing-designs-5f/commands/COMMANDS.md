# User Commands for 5F Learning System

**Purpose:** Commands to view, control, and manage what the 5F reviewer has learned.

---

## Core Commands

### `/critique-5f`
**View all learned context**

```bash
/critique-5f
```

**Output:**
```markdown
# 5F Reviewer - Learned Context

## Summary
- Reviews conducted: 47
- Context confidence: High
- Last learning cycle: March 17, 2026

## Business Rules (3 rules learned)
1. 2FA mandatory for transactions >₹50,000 (RBI requirement)
2. Explicit consent required for PAN/GST collection
3. Security indicators needed on payment pages

## User Personas
- Primary users: Business managers at SMEs
- Environment: Tier 1/2/3 cities, 3G/4G networks
- Performance threshold: <2s load time

## Scoring Calibrations
- Fast: 2s threshold (stricter than default 3s)
- Focused: 15 fields OK for dashboards
- Fair: Explicit consent flows required

## Design Patterns (2 patterns)
1. Table layouts for financial data (9/10 reviews)
2. Modal forms preferred over inline editing (7/10 reviews)

## Active Experiments (1)
- H002: Bottom sheets vs. modals (5/10 data points)

## Pending Questions (2)
- Q003: Accessibility stance (WCAG priority)
- Q007: Localization timeline

[View Details] [Edit Context] [Generate Report]
```

---

### `/critique-5f edit`
**Manually edit a context file**

```bash
/critique-5f edit user-personas
/critique-5f edit business-rules
/critique-5f edit design-system
/critique-5f edit competitive-context
```

**Opens:** The corresponding file from `.claude/5f-reviews/context/` for editing

**Use cases:**
- Fix incorrect learnings
- Remove outdated rules
- Add context manually without waiting for patterns

---

### `/critique-5f report`
**Generate monthly learning report**

```bash
/critique-5f report           # Current month
/critique-5f report --month 2  # February 2026
```

**Output:** Generates the monthly learning report (see `improvement-tracker.md`)

---

### `/critique-5f analyze`
**Manually trigger the learning cycle**

```bash
/critique-5f analyze              # Analyze last 7 days
/critique-5f analyze --week 2      # Analyze specific past week
/critique-5f analyze --all         # Re-analyze all data
```

**Use cases:**
- Force immediate learning after important feedback
- Re-analyze after editing feedback logs

---

### `/critique-5f status`
**View learning system status**

```bash
/critique-5f status
```

**Output:**
```markdown
# 5F Learning System - Status

## Overview
- Total reviews: 47
- Feedback received: 38 (81% response rate)
- Average rating: 4.2/5
- Time period: Feb 1 - Mar 17, 2026

## Learning Progress
- Business rules learned: 3
- Scoring calibrations: 3
- Design patterns recognized: 2
- Hypotheses validated: 1
- Hypotheses archived: 1

## Context Coverage
- User personas: complete
- Business rules: complete
- Competitive context: partial
- Design system: partial
- Product specifics: complete

## Pending Questions
- Q003: Accessibility stance (WCAG priority)
- Q007: Localization timeline
```

---

### `/critique-5f reset`
**Reset learned context**

```bash
/critique-5f reset                    # Full reset (requires confirmation)
/critique-5f reset --keep-rules       # Reset scores, keep business rules
/critique-5f reset --keep-calibrations # Reset rules, keep scoring
```

**Confirmation prompt:**
```markdown
Warning: This will delete learned context

You're about to reset:
- 3 business rules
- 3 scoring calibrations
- 2 design patterns
- 1 active hypothesis
- 47 review session logs

Backup location: `.claude/5f-reviews/backups/2026-03-17/`

Confirm reset? (yes/no)
```

---

### `/critique-5f disable`
**Disable learning for the current session**

```bash
/critique-5f disable
```

Toggles Mode A session logging only. Mode B and C are unaffected. Context already learned is preserved.

---

### `/critique-5f enable`
**Re-enable learning after disabling**

```bash
/critique-5f enable
```

Re-enables learning features if previously disabled.

---

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/critique-5f` | View learned context | View all rules and patterns |
| `/critique-5f status` | View system status | Review counts, coverage |
| `/critique-5f edit` | Edit context manually | Fix incorrect learning |
| `/critique-5f report` | Generate learning report | Monthly summary |
| `/critique-5f analyze` | Run learning cycle | Force immediate learning |
| `/critique-5f reset` | Reset learned context | Start fresh |
| `/critique-5f disable` | Disable learning | Skip learning for session |
| `/critique-5f enable` | Re-enable learning | Turn learning back on |

---

## Context File Location

All learned context is stored in `.claude/5f-reviews/`:

```
.claude/5f-reviews/
  context/
    user-personas.md       # User context
    business-rules.md      # Confirmed business rules
    design-system.md       # Design patterns
    competitive-context.md # Competitive landscape
  review-sessions.jsonl    # Per-review logs
  improvement-tracker.md   # Learning history
  active-hypotheses.md     # Patterns under validation
  backups/                 # Reset backups
```

