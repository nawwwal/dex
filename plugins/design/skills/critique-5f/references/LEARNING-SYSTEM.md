# Learning System (Phase 6 - Optional)

This phase runs AFTER the main review completes and is completely optional.

**Full technical details:** See `workflows/weekly-learning-cycle.md`

---

## Overview

The user can skip this phase by:
- Not providing feedback
- Declining to answer context questions
- Disabling learning with `/critique-5f disable`

---

## Learning Modes

### Mode A: Pattern Observation (Non-Intrusive)

After delivering the review, **silently observe** for future pattern matching:

```json
{
  "review_id": "[UUID]",
  "timestamp": "[ISO 8601]",
  "context": {/* user_context from Phase 1 */},
  "scores": {/* Agent 1 5F scores */},
  "mood": "[Selected mood]",
  "view": "[Simple/Advanced]",
  "design_type": "[Inferred type: dashboard, onboarding, checkout, etc.]"
}
```

Save to: `.claude/5f-reviews/feedback/review-sessions.jsonl`

**No user interaction required.** This happens when invoked.

---

### Mode B: Context Questions (When Gaps Detected)

If Agent 3 (Story Generator) found **significant research gaps** (>50% of critical issues lack evidence):

**Ask 1-2 targeted questions to learn context:**

Example:
> "Quick question for future reviews: I noticed this is a [design type] for [industry]. Are there specific [industry] regulations I should know about?
>
> - [ ] Yes → [Tell me briefly]
> - [ ] No
> - [ ] Skip"

**Only ask if:**
- Research coverage <50%
- Pattern appears in 3+ reviews
- Question hasn't been asked before

**Store answers in:** `.claude/5f-reviews/context/[relevant-file].md`

**Context file routing (Mode B):**
- Regulatory/compliance answers → `business-rules.md`
- User persona/target audience answers → `user-personas.md`
- Design system/component details → `design-system.md`
- Competitive context answers → `competitive-context.md`

---

### Mode C: Feedback Collection (Opt-In)

At the very end, offer optional feedback:

> "⭐ **Optional:** Help me improve future reviews!
>
> **How useful was this review? (1-5)**
> 1 - Not useful | 5 - Very useful
>
> **Did I miss any important context?** [Free text]
>
> **Were any scores off?** [Override any F-scores if needed]
>
> [Submit] [Skip]"

**If user provides feedback:**
- Store in `.claude/5f-reviews/feedback/review-sessions.jsonl` (update existing entry)
- If rating <3, add to `.claude/5f-reviews/feedback/improvement-tracker.md` for weekly analysis
- If score overrides provided, note for calibration

**If user skips:**
- No problem! The review is complete.

---

## Weekly Learning Cycle (Manual)

When invoked via `/critique-5f analyze`: reads last 7 days of reviews from `.claude/5f-reviews/feedback/review-sessions.jsonl`, detects high-confidence patterns, and proposes updates to context files. See `reviewing-designs-5f/workflows/weekly-learning-cycle.md` for the full workflow.

---

## Guardrails

**Never:**
- Interrupt the main review (Phases 1-5)
- Fabricate user research if HeyMarvin has no data
- Update context files without sufficient confidence (5+ data points)
- Ask the same context question twice
- Make the user feel obligated to provide feedback

**Always:**
- Make feedback completely optional
- Keep context questions under 2 per review
- Flag low-confidence learnings as hypotheses, not rules
- Allow user to edit/override learned context via `/critique-5f edit`
- Provide rollback capability (keep last 3 versions of context files)

---

## User Controls

Manage the learning system via commands — see **Command Routing** in `SKILL.md`.

---

## Confidence Thresholds

See confidence thresholds in `reviewing-designs-5f/workflows/weekly-learning-cycle.md`.
