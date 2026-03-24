# Weekly Learning Cycle

**Purpose:** Pattern analysis that reviews recent sessions to update context files in `.claude/5f-reviews/`.

**Trigger:** This cycle runs when you invoke `/critique-5f analyze`. It is user-initiated — there is no automatic background process.

---

## How to Run

```bash
/critique-5f analyze              # Analyze last 7 days
/critique-5f analyze --week 2      # Analyze a specific past week
/critique-5f analyze --all         # Re-analyze all logged sessions
```

Run this after a batch of reviews, after editing feedback logs, or when you want to force a context refresh.

---

## What Gets Analyzed

When you invoke `analyze`, the skill reads review session logs from `.claude/5f-reviews/feedback/review-sessions.jsonl` and looks for:

**1. Low-rated reviews (rating < 3)**
- What context was flagged as missing
- Which 5F dimension was most disputed

**2. Score overrides**
- When you corrected a dimension score, what direction and by how much
- Consistent override patterns signal a scoring calibration is needed

**3. Feedback on missed context**
- Phrases like "you didn't mention X" or "this product requires Y"
- Repeated mentions become candidates for business rules

**4. Context questions answered**
- When you answered a Mode B question, what you said
- These directly update user-personas and product-specifics files

**5. Design type patterns**
- Which layout patterns appeared repeatedly across reviews

---

## What Gets Updated

After analysis, the skill updates these files in `.claude/5f-reviews/`:

| File | Updated when |
|------|-------------|
| `context/business-rules.md` | A rule is mentioned 5+ times with consistency |
| `experiments/active-hypotheses.md` | A pattern appears 3-4 times (needs more data) |
| `context/design-system.md` | A design pattern appears 3+ times |
| `LEARNINGS.md` | Summary is refreshed after any updates (kept under 200 lines) |
| `feedback/improvement-tracker.md` | A dated report entry is appended |

---

## Confidence Thresholds

| Learning Type | Minimum Data Points | Minimum Confidence | Action |
|---------------|--------------------|--------------------|--------|
| Business Rule | 5 | N/A | Add to `context/business-rules.md` |
| Business Rule (hypothesis) | 3-4 | N/A | Add to `active-hypotheses.md` |
| Scoring Calibration | 5 | 80% consistency | Update scoring notes |
| Design Pattern | 3 | N/A | Add to `context/design-system.md` |
| Hypothesis Promotion | 10 | 70% | Promote to confirmed rule |
| Hypothesis Archive | 10 | <70% | Archive as inconclusive |

---

## Hypothesis Lifecycle

Hypotheses in `active-hypotheses.md` are patterns that appear promising but haven't met the confidence bar yet.

When `analyze` runs, each active hypothesis is checked:
- **10+ data points AND 70%+ confidence** — promoted to `context/business-rules.md`
- **10+ data points AND <70% confidence** — archived as inconclusive

Hypotheses that haven't reached 10 data points stay active and accumulate evidence across future reviews.

---

## Guardrails

The skill applies these checks before writing any learning to a context file:

- **Conflict check** — if the new learning contradicts an existing rule, it is flagged for your review rather than silently overwriting
- **Confidence threshold** — patterns below the minimum data point count go to hypotheses, not rules
- **Consistency check** — score overrides that point in opposite directions are flagged rather than averaged

Flagged items appear in the `analyze` output for you to resolve manually via `/critique-5f edit`.

---

## Report Output

After `analyze` completes, a summary is printed and appended to `.claude/5f-reviews/feedback/improvement-tracker.md`:

```
Learning cycle complete.

Analyzed 12 reviews from March 11-17, 2026.

Patterns detected:
  - Low ratings: 2 reviews
  - Missed context mentions: 3 unique
  - Score overrides: 8 across all dimensions
  - Context questions answered: 4

High-confidence learnings applied:
  - 1 new business rule added (5 data points)
  - 1 scoring calibration updated (Fast dimension, 8 overrides, 85% consistency)
  - 0 design patterns (need more data)

Hypothesis updates:
  - H001 promoted (10 data points, 90% confidence)
  - H003 archived (12 data points, 50% confidence — inconclusive)

Report saved to feedback/improvement-tracker.md.
```

If significant changes were made (new rules, calibrations, or hypothesis promotions), the output will note: "Review changes with `/critique-5f` or edit with `/critique-5f edit`."
