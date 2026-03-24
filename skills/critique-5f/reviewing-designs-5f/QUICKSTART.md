# 5F Learning System - Quick Start Guide

**Get started in 2 minutes**

---

## What This Does

Makes your `reviewing-designs-5f` skill **self-improving** by learning:
- Your business rules (compliance, regulations)
- Your users (personas, environment, behaviors)
- Your quality bar (auto-calibrates 5F scoring)
- Your design patterns (what's standard vs. deviation)

**Without modifying the original skill.**

---

## How It Works (Simple Version)

```
You run: reviewing-designs-5f [design]
         ↓
You get: 5F Review + Learning Prompt
         ↓
You provide (optional): Feedback + Context answers
         ↓
System learns: Patterns, rules, calibrations
         ↓
Next review: Smarter, more accurate scores
```

---

## What You'll See

### 1. Normal Review (Untouched)

```markdown
# 5F Design Review - Payment Dashboard

## Scores
- Fast: 7/10
- Focused: 6/10
- Fun: 8/10
- Fluent: 7/10
- Fair: 9/10

## Issues
1. Load time 2.5s (target <3s)
2. 18 data fields (high density)
...
```

### 2. Learning Mode (5% extra)

```markdown
---
## 🧪 Learning Mode

**Testing:** "Do your users prefer table layouts for financial data?"
**Observation:** You used tables here. Competitors (Tally, Zoho) also use tables.

Is this your standard?
- ✅ Yes
- ❌ No
- 🤷 Unsure
```

### 3. Context Question (Sometimes)

```markdown
---
## ❓ Quick Question (15 sec)

I see 18 fields. Are your users:
- [ ] Data analysts (dense tables OK)
- [ ] Business managers (need simpler views)

[Skip] [Answer]
```

### 4. Feedback Prompt (Optional)

```markdown
---
## 📊 Feedback (10 sec)

Rate this review: ⭐️ [1-5]
What did I miss? [Free text]
Adjust scores? Fast: 7 → [___]

[Skip] [Submit]
```

---

## What Happens Next

### Immediate (Same Session)
- If you answered a context question → Updates context file
- If you mentioned a new rule → Adds to hypotheses

### Weekly (Sundays)
- Analyzes all feedback from last 7 days
- Detects patterns (5+ mentions = new rule)
- Updates memory files
- Validates hypotheses

### Next Review
- Uses learned context automatically
- Gives more accurate scores
- Catches issues specific to your product

---

## Examples of Learning

### After 5 Reviews

**System learned:**
- "Primary users are business managers" (from question)
- "2FA is mandatory" (from 3 feedback mentions → hypothesis)
- "Fast threshold is 2s" (from 2 score overrides → collecting data)

**Next review will:**
- Score "Focused" for business managers (not data analysts)
- Flag missing 2FA as critical issue
- Still learning performance threshold (needs 3 more data points)

### After 20 Reviews

**System learned:**
- 3 business rules (2FA, RBI consent, security indicators)
- 3 scoring calibrations (Fast <2s, Focused OK up to 15 fields, Fair requires explicit consent)
- 2 design patterns (tables for financial data, modals for forms)

**Next review will:**
- Automatically check compliance (2FA, RBI, security)
- Use calibrated thresholds (2s for Fast)
- Recognize your standard patterns
- Only ask about genuinely new things (5% question rate)

---

## Quick Commands

```bash
/context-5f               # What has it learned?
/context-5f edit          # Fix wrong learnings
/context-5f answer        # Answer skipped questions
/context-5f report        # Monthly summary
/context-5f reset         # Start over
```

---

## Control Learning

### Disable All Learning
```bash
export SKIP_5F_LEARNING=true
```

### Disable Only Feedback
```bash
export SKIP_5F_FEEDBACK=true
```

### Edit What It Learned
```bash
/context-5f edit
# Opens LEARNINGS.md for manual editing
```

### Reset Everything
```bash
/context-5f reset
# Deletes learned context (with backup)
```

---

## What Gets Learned

### Business Rules (from feedback)

**User mentions:** "Didn't catch that 2FA is mandatory for us (RBI requirement)"

**After 5 mentions:**
- Added to `context/business-rules.md`
- Future reviews will check for 2FA automatically

### Scoring Calibrations (from overrides)

**User adjusts:** Fast score from 7 → 8 (load time 2.5s)

**After 5 consistent adjustments:**
- System learns: "User's Fast threshold is 2s (not default 3s)"
- Future reviews use stricter threshold

### Design Patterns (from observations)

**User confirms:** "Yes, tables are our standard for financial data"

**After 10 confirmations:**
- System learns: "Table layouts are standard, cards are deviation"
- Future reviews will flag card layouts as potential UX risk

### User Personas (from questions)

**User answers:** "Primary users are business managers"

**Immediately:**
- Added to `context/user-personas.md`
- Future "Focused" scoring adjusted for business managers (not data analysts)

---

## Confidence Levels

| Data Points | Status | Action |
|-------------|--------|--------|
| 1-2 | Low | Just tracking, not learning yet |
| 3-4 | Medium | Added to hypotheses, needs validation |
| 5+ | High | Promoted to business rule, used in reviews |

**You control the thresholds** via `/context-5f config`

---

## Troubleshooting

### "It's not learning anything"

Check feedback response rate:
```bash
/context-5f stats
# Should be >70% response rate
```

If low, learning is slow (needs feedback data).

### "It learned something wrong"

Edit immediately:
```bash
/context-5f edit
# Remove incorrect learning from LEARNINGS.md
```

Or reset specific type:
```bash
/context-5f reset --keep-rules    # Reset scores, keep business rules
```

### "Too many questions"

Questions decrease over time:
- Reviews 1-5: 50% chance of question
- Reviews 6-20: 20% chance
- Reviews 21+: 5% chance

Or disable:
```bash
export SKIP_5F_MODE_B=true   # No more questions
```

### "I want to review what changed"

```bash
/context-5f report
# Shows monthly learning summary

cat skill-memory/reviewing-designs-5f/feedback/improvement-tracker.md
# Shows detailed changelog
```

---

## Files You Care About

```
skill-memory/reviewing-designs-5f/
├── LEARNINGS.md              ← Main memory (view with /context-5f)
├── context/
│   ├── business-rules.md     ← Compliance, regulations
│   ├── user-personas.md      ← Your users
│   └── product-specifics.md  ← Business model, mobile, etc.
└── feedback/
    ├── review-sessions.jsonl ← All feedback log
    └── improvement-tracker.md ← What changed when
```

**Edit anytime:** `/context-5f edit`

---

## Privacy & Data

### What's Stored Locally

- Your feedback (ratings, comments)
- Score overrides
- Context answers
- Design types reviewed (e.g., "dashboard", "checkout")

### What's NOT Stored

- Actual design files
- Figma URLs (unless you put them in feedback)
- User names or personal info

### Where It's Stored

```
$HOME/.claude/memory/reviewing-designs-5f/
```

All files are local, plain text (markdown/JSON).

### How to Delete

```bash
/context-5f reset    # With backup
rm -rf skill-memory/reviewing-designs-5f/    # Permanent delete
```

---

## Next Steps

### First 5 Reviews

**Goal:** Build foundational context

**What to do:**
- Answer context questions (builds user personas, business rules)
- Provide feedback (helps calibrate scoring)
- Be specific about misses ("We require 2FA", not just "missed compliance")

**Expect:** Lots of questions (50% rate)

### Reviews 6-20

**Goal:** Refine and validate

**What to do:**
- Answer remaining questions
- Adjust scores if needed (teaches calibration)
- Validate Mode A observations

**Expect:** Fewer questions (20% rate), smarter reviews

### Reviews 21+

**Goal:** Maintenance mode

**What to do:**
- Minimal feedback needed (system is well-calibrated)
- Answer new questions only (5% rate)
- Review monthly learning report

**Expect:** Highly accurate reviews, minimal learning overhead

---

## Monthly Ritual

**First week of each month:**

1. Review learning report
   ```bash
   /context-5f report
   ```

2. Check what changed
   ```bash
   cat skill-memory/reviewing-designs-5f/feedback/improvement-tracker.md
   ```

3. Validate learnings
   ```bash
   /context-5f validate
   ```

4. Answer pending questions
   ```bash
   /context-5f answer
   ```

5. Edit if needed
   ```bash
   /context-5f edit
   ```

**Takes:** ~5 minutes
**Impact:** Keeps system accurate and up-to-date

---

## Advanced Usage

### Share Context with Team

```bash
/context-5f export team-context.md
# Share file with teammates

# Teammates import:
/context-5f import team-context.md
```

### Backup Before Experiments

```bash
/context-5f export backup-2026-03-11.json
# Try new things

# Restore if needed:
/context-5f import backup-2026-03-11.json
```

### Custom Thresholds

```bash
/context-5f config --edit

# Change:
business_rule_min_data_points: 3    # Learn faster (default: 5)
scoring_calibration_min_consistency: 0.9  # Be stricter (default: 0.8)
```

---

## Support

**Commands:**
- `/context-5f` - View learned context
- `/context-5f debug` - System diagnostics
- `/context-5f help` - This guide

**Files:**
- `README.md` - Full documentation
- `workflows/` - Technical specs
- `commands/COMMANDS.md` - All commands

**Stuck?**
```bash
/context-5f debug
# Shows system health and recommendations
```

---

## Key Takeaway

**You don't have to do anything.**

Just use `reviewing-designs-5f` normally:
- Learning happens automatically in the background
- Feedback is optional (but helps)
- System gets smarter over time
- You can view/edit/reset anytime

**The original skill never changes. Learning is a parallel, optional layer.**

---

**Ready to start?** Just run your next `reviewing-designs-5f` review. The system will handle the rest.
