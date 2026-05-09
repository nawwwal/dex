# Learning System (Phase 6 - Optional)

This phase runs AFTER the main review completes and is completely optional.

---

## Overview

The user can skip this phase by:
- Not providing feedback
- Declining to answer context questions
- Disabling learning with `/context-5f disable`

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

If a writable learning store is configured, save to that store. Do not write into the installed skill directory.

**No user interaction required.** This happens in the background.

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

If a writable learning store is configured, store answers there. If not, keep the answer in the current review context only.

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
- Store in the configured learning store when available.
- If rating <3, add to `feedback/improvement-tracker.md` for weekly analysis
- If score overrides provided, note for calibration

**If user skips:**
- No problem! The review is complete.

---

## Weekly Learning Cycle (Automated)

**Runs automatically every 7 days OR manually via `/context-5f analyze`**

**Steps:**
1. Load last 7 days of reviews from the configured learning store
2. Analyze patterns (business rules, scoring calibrations, design patterns)
3. Identify high-confidence learnings (need 5+ data points, 80%+ consistency)
4. Update the configured learning store:
   - business rules
   - user/persona data
   - design-system patterns
   - medium-confidence hypotheses
5. Validate active hypotheses (promote to rules if 10+ data points, 70%+ confidence)
6. Generate an improvement report in the configured learning store
7. Notify user if major changes detected (>2 new rules, >1 calibration, or hypotheses promoted)

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
- Allow user to edit/override learned context via `/context-5f edit`
- Provide rollback capability (keep last 3 versions of context files)

---

## User Controls

Users can manage the learning system via commands:

```bash
/context-5f status           # Show current learnings, confidence levels
/context-5f report           # View improvement tracker
/context-5f edit             # Manually edit context files
/context-5f analyze          # Run weekly learning cycle now
/context-5f disable          # Disable all learning (Mode A/B/C)
/context-5f enable           # Re-enable learning
/context-5f reset            # Clear all learned context (keeps reviews)
```

---

## Confidence Thresholds

| Learning Type | Minimum Data Points | Minimum Confidence | Action |
|---------------|--------------------|--------------------|--------|
| Business Rule | 5 | N/A | Add to learning store |
| Business Rule (hypothesis) | 3-4 | N/A | Add as hypothesis |
| Scoring Calibration | 5 | 80% consistency | Update scoring weights |
| Design Pattern | 3 | N/A | Add to learning store |
| Hypothesis Promotion | 10 | 70% | Promote to rule |
| Hypothesis Archive | 10 | <70% | Archive as inconclusive |
