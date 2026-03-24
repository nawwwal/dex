# 5F Design Review - Self-Learning System

**Version:** 1.0.0
**Created:** March 11, 2026
**Status:** Active

---

## 🚀 New User? Start Here

| If you have... | Read this... | Time |
|----------------|--------------|------|
| **30 seconds** | [30-SECOND-OVERVIEW.md](30-SECOND-OVERVIEW.md) | Visual quick-start |
| **1 minute** | [CHEAT-SHEET.md](CHEAT-SHEET.md) | Quick reference |
| **2 minutes** | [QUICKSTART.md](QUICKSTART.md) | Getting started guide |
| **5 minutes** | [HOW-TO-USE.md](HOW-TO-USE.md) | Best practices & tips |
| **20 minutes** | This README | Full documentation |

**Just want to start?** Run `reviewing-designs-5f [design]` and answer the first question you see.

---

## Overview

A **parallel learning system** that wraps around the `reviewing-designs-5f` skill to make it self-improving over time.

**Key Principle:** The original skill is NEVER modified. Learning happens externally through observation, feedback collection, and pattern analysis.

**What it learns:**
- Your business rules (compliance, regulations)
- Your users (personas, environment, behaviors)
- Your quality bar (calibrates 5F scoring to YOUR standards)
- Your design patterns (what's normal vs. deviation)

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  USER INVOKES: reviewing-designs-5f                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR WRAPS ORIGINAL SKILL                          │
│                                                             │
│  1. Load learned context (business rules, personas, etc.)  │
│  2. Run original skill with enhanced context               │
│  3. Append Mode A: Experimental observation (5%)           │
│  4. Append Mode B: Context question (if uncertain)         │
│  5. Collect optional feedback                              │
│  6. Log session to review-sessions.jsonl                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  WEEKLY LEARNING CYCLE (Sundays, automated)                │
│                                                             │
│  1. Analyze last 7 days of feedback                        │
│  2. Detect patterns (5+ data points = high confidence)     │
│  3. Update memory files (business rules, calibrations)     │
│  4. Validate hypotheses (10+ data points)                  │
│  5. Generate improvement report                            │
│  6. Notify user if major changes                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture

### Memory Structure

```
skill-memory/reviewing-designs-5f/
├── LEARNINGS.md                    # Main memory (<200 lines, always loaded)
├── context/
│   ├── business-rules.md           # Compliance, regulatory constraints
│   ├── user-personas.md            # Target users, environments
│   ├── design-system.md            # Patterns, brand guidelines
│   ├── competitive-context.md      # Benchmark products
│   └── product-specifics.md        # Pricing, growth, mobile strategy
├── feedback/
│   ├── review-sessions.jsonl       # All reviews + feedback log
│   └── improvement-tracker.md      # What changed when (changelog)
├── experiments/
│   ├── active-hypotheses.md        # Patterns being validated
│   └── pending-questions.md        # Skipped context questions
├── workflows/
│   ├── orchestrator.md             # Main coordination logic
│   ├── feedback-collector.md       # Post-review feedback prompt
│   ├── mode-a-observations.md      # Experimental observations
│   ├── mode-b-questions.md         # Context-triggered questions
│   └── weekly-learning-cycle.md    # Pattern analysis workflow
├── commands/
│   └── COMMANDS.md                 # User commands reference
└── README.md                       # This file
```

---

## Three Learning Modes

### Mode A: Experimental Observations (Every Review)

**Purpose:** Surface hypotheses being tested to collect validation data

**Example:**
```markdown
---
## 🧪 Learning Mode (experimental observation)

**Hypothesis I'm testing:**
"Indian B2B SaaS users prefer table layouts over card grids for financial data"

**Observation from this design:**
You're using a **table layout** for transaction history. This matches 7 of your last 9 reviews.

**Quick validation:**
Is table layout your standard pattern?
- ✅ Yes, tables are our standard
- ❌ No, we're experimenting
- 🤷 We haven't standardized yet
```

**Size:** 3-5 sentences (5% of review)
**Frequency:** Every review
**User can:** Validate, ignore, or skip

---

### Mode B: Context-Triggered Questions (5-50% of Reviews)

**Purpose:** Ask targeted questions when genuinely uncertain about scoring

**Example:**
```markdown
---
## ❓ Quick Context Question (helps score accurately)

I see 18 data fields. To score "Focused":

**Your primary users are:**
- [ ] Data analysts (dense tables OK)
- [ ] Business managers (need simplified views)
- [ ] Operations staff (task-focused)

**Why I ask:** Determines if 18 fields is focused or overwhelming.

[Skip for Now] [Answer]
```

**Triggers:** 10 categories (high density, forms, heavy media, etc.)
**Frequency:**
- Reviews 1-5: 50% (build context fast)
- Reviews 6-20: 20% (fill gaps)
- Reviews 21+: 5% (only new uncertainties)

**User can:** Answer, skip, answer later via `/context-5f answer`

---

### Mode C: Scoring Calibration (Invisible, Continuous)

**Purpose:** Auto-adjust 5F thresholds based on user score overrides

**How it works:**
- User consistently upgrades "Fast" scores by +1 when load is 2-2.5s
- After 5+ overrides with 80%+ consistency
- System learns: "User's Fast threshold is 2s (not default 3s)"
- Future reviews use stricter threshold automatically

**Frequency:** Weekly analysis
**User can:** View in reports, revert calibrations

---

## Feedback Loop

### After Every Review

```markdown
---
## 📊 Help This Reviewer Learn (Optional - 10 sec)

**How useful was this review?** ⭐️ [1-5]

**What was most helpful?**
- [ ] Specific issues identified
- [ ] Relevance to product/users
- [ ] Actionable recommendations
- [ ] 5F scoring accuracy

**What did I miss?** [Free text]

**Score adjustments?**
Fast: 7 → [Your score: ___]

[Skip] [Submit]
```

**Response rate target:** 70%+
**User can:** Skip entirely, disable globally

---

## Weekly Learning Cycle

**Runs:** Every Sunday (or first review of new week)
**Duration:** ~5-10 seconds
**User notification:** Only if major changes (2+ new rules, 1+ calibration)

**Process:**
1. Load last 7 days of feedback
2. Analyze patterns:
   - Missed context (5+ mentions → new business rule)
   - Score overrides (5+ consistent → calibrate threshold)
   - Design patterns (3+ occurrences → recognize pattern)
3. Update memory files
4. Validate hypotheses (10+ data points → promote or archive)
5. Generate improvement report
6. Notify user if needed

**Example output:**
```
🔄 Weekly learning cycle complete

✅ Added 1 business rule (2FA for >₹50k)
✅ Calibrated Fast threshold (3s → 2s)
✅ Validated 1 hypothesis (table layouts)

📚 Review changes: /context-5f report
```

---

## Confidence Thresholds

| Learning Type | Min Data Points | Min Confidence | Action |
|---------------|-----------------|----------------|--------|
| **Business Rule** | 5 | N/A | Add to context/business-rules.md |
| **Business Rule (hypothesis)** | 3-4 | N/A | Add to active-hypotheses.md |
| **Scoring Calibration** | 5 | 80% consistency | Update scoring weights |
| **Design Pattern** | 3 | N/A | Add to context/design-system.md |
| **Hypothesis Promotion** | 10 | 70% | Promote to business rule |
| **Hypothesis Archive** | 10 | <70% | Archive as inconclusive |

---

## User Commands

| Command | Purpose |
|---------|---------|
| `/context-5f` | View all learned context |
| `/context-5f edit` | Edit context files manually |
| `/context-5f answer` | Answer pending questions |
| `/context-5f report` | Generate monthly learning report |
| `/context-5f analyze` | Force weekly learning cycle now |
| `/context-5f history` | View feedback log |
| `/context-5f stats` | Learning statistics |
| `/context-5f reset` | Reset learned context |
| `/context-5f export` | Export context (backup/share) |
| `/context-5f import` | Import context (restore/copy) |

See `commands/COMMANDS.md` for full reference.

---

## Guardrails Against Bad Learning

### Prevent Overfitting
- ✅ Require 5+ data points before adding rules
- ✅ Track confidence (% consistency)
- ✅ Flag rules older than 6 months for revalidation
- ✅ Keep last 3 versions of memory files (rollback)
- ✅ User review required for major changes

### Prevent Learning Wrong Things
- ✅ Source attribution (every rule tagged with data points)
- ✅ Conflict detection (flag if new rule contradicts existing)
- ✅ Validation questions (if unclear, ask follow-up)
- ✅ Diff view (show exactly what will change)
- ✅ User can edit/remove anything anytime

### Example Guardrail in Action

```markdown
# Detected Pattern
User downgraded "Fair" scores 4 times when privacy policy was in footer

**Confidence Check:**
- Data points: 4 (below threshold of 5)
- Consistency: 100%

**Action:**
- ⏸️ HOLD - Need 1 more data point
- 📋 Add to active-hypotheses.md
- ❓ Next review: Ask "Where should privacy policy be linked?"
```

---

## Configuration

Edit learning behavior in `/context-5f config`:

```yaml
learning_enabled: true
feedback_enabled: true
mode_a_enabled: true
mode_b_enabled: true
weekly_cycle_enabled: true

# Frequency
mode_b_trigger_rate_early: 0.5    # 50% for reviews 1-5
mode_b_trigger_rate_mid: 0.2      # 20% for reviews 6-20
mode_b_trigger_rate_late: 0.05    # 5% for reviews 21+

# Confidence thresholds
business_rule_min_data_points: 5
scoring_calibration_min_consistency: 0.8
hypothesis_validation_min_data_points: 10
```

Or disable via environment variables:
```bash
export SKIP_5F_LEARNING=true      # Disable all learning
export SKIP_5F_FEEDBACK=true      # Disable only feedback
```

---

## Integration with Original Skill

**Key design principle:** The original `reviewing-designs-5f` skill is NEVER modified.

**How it works:**
1. Orchestrator loads learned context from memory files
2. Passes context to original skill as enhanced input
3. Original skill runs normally (untouched)
4. Orchestrator appends learning modes to output
5. User sees: [Original Review] + [Learning Content] + [Feedback Prompt]

**Benefits:**
- ✅ Original skill stays pristine
- ✅ Learning can be disabled entirely
- ✅ Easy to update either system independently
- ✅ No breaking changes to existing workflows

---

## Example: Learning in Action

### Review #1 (No Context)

**Review output:**
- Fast: 7/10 (2.5s load)
- Focused: 5/10 (18 fields - quite dense)
- Fair: 6/10 (privacy policy in footer)

**Learning mode:**
- Mode B question: "What are your primary users?" → User answers: Business managers
- Feedback: Rating 3/5, Missed: "2FA is mandatory for us"

**Learned:**
- User persona: Business managers (high confidence)
- Business rule candidate: 2FA mandatory (needs validation, n=1)

---

### Review #10 (Some Context)

**Review output:**
- Fast: 8/10 (2.3s - meets your <2.5s threshold) ✅ Learned from overrides
- Focused: 7/10 (18 fields - appropriate for business managers) ✅ Learned from personas
- Fair: 5/10 (❌ Missing 2FA - your requirement) ✅ Learned from feedback

**Learning mode:**
- Mode A: "Testing hypothesis: Table layouts preferred" - 7/10 reviews used tables
- Feedback: Rating 5/5, "Caught the 2FA issue!"

**Now knows:** 2FA rule, user personas, performance threshold

---

### Review #30 (Well-Calibrated)

**Review output:**
- All scores use learned context automatically
- Catches compliance issues (2FA, RBI consent)
- Uses correct thresholds (2s for Fast, 15 fields OK for Focused)
- Recognizes established patterns (tables, modals)

**Learning mode:**
- Mode A: Validating established patterns
- Mode B: Only asks genuinely new questions (5% rate)
- Feedback: Rating 5/5, no corrections needed

**System is now:** Self-sufficient, accurate, minimal learning overhead

---

## Monthly Learning Report

Auto-generated every month:

```markdown
# 5F Learning Report - March 2026

## What I Learned
- 3 business rules (RBI compliance)
- 3 scoring calibrations (Fast, Focused, Fair)
- 2 design patterns (tables, modals)
- 1 hypothesis validated

## Current Understanding
- Industry: Indian B2B SaaS (fintech)
- Users: Business managers, Tier 2/3 cities
- Regulatory: RBI-regulated
- Performance: <2s on 3G
- Design system: Evolving

## Action Required
- [ ] Review business-rules.md
- [ ] Approve calibrations
- [ ] Answer 2 pending questions

[Review Changes] [Reset] [Approve All]
```

---

## Troubleshooting

### Learning isn't working
```bash
/context-5f debug          # Check system health
/context-5f validate       # Check data quality
```

### Want to start fresh
```bash
/context-5f reset --keep-rules   # Reset scores, keep business rules
/context-5f reset               # Full reset (with backup)
```

### Want to disable learning
```bash
export SKIP_5F_LEARNING=true    # Global disable
# Or edit config: learning_enabled: false
```

### Want to review what changed
```bash
/context-5f report          # Monthly summary
/context-5f history         # All feedback
cat feedback/improvement-tracker.md  # Detailed changelog
```

---

## Files Reference

| File | Purpose | Size Limit | Update Frequency |
|------|---------|------------|------------------|
| `LEARNINGS.md` | Quick reference, always loaded | <200 lines | Every review (high-confidence only) |
| `context/*.md` | Deep context files | Unlimited | Weekly cycle |
| `review-sessions.jsonl` | Append-only feedback log | Unlimited | Every review |
| `improvement-tracker.md` | Transparent changelog | Unlimited | Weekly cycle |
| `active-hypotheses.md` | Patterns being validated | ~20 hypotheses | Per review |
| `pending-questions.md` | Skipped questions | ~50 questions | Per review |

---

## Design Principles

1. **Non-Invasive** - Original skill never modified
2. **Transparent** - All learning is visible
3. **Optional** - User can skip/disable anytime
4. **Gradual** - High frequency early, low frequency later
5. **Controllable** - User can edit/reset/import/export
6. **Confident** - Only learns from consistent patterns (5+ data points)
7. **Reversible** - Versioning + rollback support

---

## Future Enhancements

Potential additions (not implemented yet):

- [ ] A/B test different scoring approaches
- [ ] Export learnings to team wiki
- [ ] Multi-user learning (aggregate across team)
- [ ] Integration with design system tools (Figma, Storybook)
- [ ] Slack notifications for major learnings
- [ ] Visual dashboard for learning progress

---

## Support

- **View learned context:** `/context-5f`
- **Edit manually:** `/context-5f edit`
- **Get help:** `/context-5f debug`
- **Reset if stuck:** `/context-5f reset`

**Documentation:**
- `workflows/` - Detailed workflow specs
- `commands/COMMANDS.md` - All commands reference
- `README.md` - This overview

---

**Version:** 1.0.0
**Status:** Production-ready
**Last Updated:** March 11, 2026
