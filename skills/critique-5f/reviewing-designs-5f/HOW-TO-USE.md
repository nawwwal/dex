# 5F Learning System - How to Use

**TL;DR:** Your design reviewer gets smarter every time you use it. Just provide optional feedback and it learns your business rules, user needs, and quality bar.

---

## What This Does

🧠 **Self-improving design reviews** that learn:
- Your **business rules** (compliance, regulations, industry standards)
- Your **users** (who they are, what they struggle with, their environment)
- Your **quality bar** (what scores mean "good" vs "great" for YOUR product)
- Your **design patterns** (what's standard vs. deviation in your product)

**Result:** Reviews get more accurate and relevant over time, automatically.

---

## How to Get the Most Out of It

### 1️⃣ First 5 Reviews: Build Foundation (5 mins each)

**What you'll see:**
- Normal 5F review
- Questions about your users/product (50% of reviews)
- Feedback prompts after each review

**What to do:**
✅ **Answer the questions** - Takes 15 seconds, builds critical context
- "Who are your primary users?" → Sets scoring context for life
- "Your regulatory requirements?" → Auto-checks compliance forever
- "Mobile strategy?" → Knows when to flag mobile issues

✅ **Provide specific feedback** - Takes 10 seconds
- What did I miss? → "We require RBI compliance for PAN collection"
- Adjust scores if wrong → Teaches your quality threshold

**Why it matters:** These 5 reviews create 80% of your learned context.

---

### 2️⃣ Reviews 6-20: Refine & Validate (3 mins each)

**What you'll see:**
- Smarter reviews (uses learned context)
- Fewer questions (20% trigger rate, only new uncertainties)
- Experimental observations to validate patterns

**What to do:**
✅ **Validate patterns when asked** - Takes 5 seconds
- "Is table layout your standard?" → Yes/No/Unsure
- Helps distinguish your intentional patterns from deviations

✅ **Correct wrong scores** - Only if needed
- System is learning your thresholds
- Consistent corrections calibrate scoring automatically

✅ **Answer pending questions** - When convenient
- Run `/context-5f answer` to answer questions you skipped earlier

**Why it matters:** System validates hypotheses, promotes patterns to rules.

---

### 3️⃣ Reviews 21+: Maintenance Mode (2 mins each)

**What you'll see:**
- Highly accurate reviews (auto-checks your rules, uses your thresholds)
- Minimal questions (5% trigger rate, only genuinely new things)
- Few to zero score corrections needed

**What to do:**
✅ **Provide feedback only when something is wrong**
- System is well-calibrated, only speak up for misses

✅ **Monthly check-in** (5 mins/month)
- Run `/context-5f report` to see what was learned
- Edit `/context-5f edit` to remove any wrong learnings

**Why it matters:** Keeps system accurate long-term.

---

## What You Control

### View Anytime
```bash
/context-5f                 # See everything the system learned
```

### Edit Anytime
```bash
/context-5f edit            # Fix wrong learnings manually
```

### Disable Anytime
```bash
export SKIP_5F_LEARNING=true    # Turn off learning
export SKIP_5F_FEEDBACK=true    # Turn off only feedback prompts
```

### Reset Anytime
```bash
/context-5f reset           # Start fresh (keeps backup)
```

---

## Best Practices

### ✅ DO

**Be specific in feedback:**
- ❌ Bad: "Missed compliance"
- ✅ Good: "RBI requires explicit consent for PAN collection (mandatory, not optional)"

**Answer context questions early:**
- First 5 reviews build 80% of context
- 15 seconds now saves hours of corrections later

**Validate patterns when shown:**
- "Is X your standard?" → Yes/No tells system what to auto-check

**Check monthly report:**
- Run `/context-5f report` first week of month
- Catch wrong learnings before they compound

### ❌ DON'T

**Don't skip ALL feedback:**
- System needs data to learn
- Aim for >70% feedback response rate
- Even "5/5, no comments" is useful

**Don't ignore context questions:**
- They appear when system is genuinely uncertain
- Skipping delays learning by weeks

**Don't let wrong learnings sit:**
- If you see incorrect context, edit immediately
- Wrong rules compound over time

**Don't expect perfection immediately:**
- First 5 reviews: Building context
- Reviews 6-20: Validating patterns
- Reviews 21+: Well-calibrated

---

## What Gets Learned (Examples)

### Business Rules
**From:** "Didn't catch that 2FA is mandatory for transactions >₹50k"
**Becomes:** Auto-checks for 2FA in all payment flows forever

### User Context
**From:** "Primary users are first-time business owners in Tier 2/3 cities"
**Becomes:** Scores "Focused" and "Fluent" for low-tech-literacy users

### Quality Bar
**From:** You upgrade "Fast" score 5 times when load is 2-2.5s
**Becomes:** System learns your threshold is 2s (not default 3s)

### Design Patterns
**From:** You confirm "table layouts" 7 times for financial data
**Becomes:** Auto-flags card grids as potential UX risk

---

## Quick Wins

### Week 1: Build User Persona
Answer "Who are your primary users?" → Every future "Focused"/"Fluent" score uses this context

### Week 2: Add Business Rules
Mention compliance requirements in feedback → Auto-checks forever

### Week 3: Calibrate Scoring
Adjust scores if too lenient/strict → System learns your quality bar

### Month 1: Review Learning
Run `/context-5f report` → See all learnings, validate quality

---

## Time Investment vs. Payoff

| Phase | Time Per Review | Cumulative Time | Payoff |
|-------|-----------------|-----------------|--------|
| **Reviews 1-5** | 5 mins (with questions/feedback) | 25 mins total | 80% context built |
| **Reviews 6-20** | 3 mins (fewer questions) | 45 mins total | Patterns validated |
| **Reviews 21+** | 2 mins (maintenance) | Minimal | Near-perfect accuracy |
| **Monthly check** | 5 mins/month | 5 mins/month | Quality assurance |

**Total investment:** ~2 hours over first month
**Payoff:** Permanently smarter reviews, saves hours on corrections

---

## Common Questions

**Q: What if I skip feedback entirely?**
A: System still works, but learns 5x slower. Context questions still appear (answer those at minimum).

**Q: What if I give contradictory feedback?**
A: System flags conflicts for manual review. You'll see: "Detected contradictory signals, clarify?"

**Q: Can I share learned context with my team?**
A: Yes! `/context-5f export team-context.json` → Share → `/context-5f import team-context.json`

**Q: How do I know what was learned?**
A: `/context-5f` shows summary, `/context-5f report` shows detailed monthly breakdown

**Q: Can I undo learning?**
A: Yes. `/context-5f edit` to fix specific rules, `/context-5f reset` to start fresh (keeps backup)

**Q: Will it learn wrong things?**
A: Guardrails prevent bad learning:
- Needs 5+ consistent data points before adding rules
- Flags contradictions for review
- Monthly report lets you catch errors
- You can edit/delete anytime

---

## Success Metrics (Your Goals)

🎯 **After 5 reviews:**
- User persona captured
- 1-2 business rules identified
- Feedback response rate >70%

🎯 **After 20 reviews:**
- 3-5 business rules learned
- 2-3 scoring calibrations
- 2-4 design patterns recognized
- Question rate dropped to 5%

🎯 **After 50 reviews:**
- Score override rate <10%
- Auto-checks all your compliance rules
- Recognizes all your standard patterns
- Maintenance mode (minimal input needed)

---

## Get Started

1. **Just use the skill normally** → `reviewing-designs-5f [design]`
2. **Answer the first question you see** → Builds critical context
3. **Provide 10-second feedback** → "5/5" or "Missed: X"
4. **Check what was learned** → `/context-5f` after review 5
5. **Monthly review** → `/context-5f report` first week of each month

**That's it.** The system handles everything else automatically.

---

**Questions?** Run `/context-5f help` or read `QUICKSTART.md`
