# 5F Learning System - Cheat Sheet

**One-liner:** Your design reviewer learns your business rules, users, and quality bar through optional feedback.

---

## 📋 Quick Reference

### What It Learns

| From Your... | It Learns... | Impact |
|--------------|--------------|--------|
| Context answers | User personas, business model, mobile strategy | Sets scoring context forever |
| Feedback comments | Business rules, compliance requirements | Auto-checks in all future reviews |
| Score adjustments | Your quality thresholds | Calibrates 5F scoring automatically |
| Pattern validations | Your design standards | Flags deviations as risks |

### Three Learning Modes

| Mode | What | When | Takes |
|------|------|------|-------|
| **🧪 Mode A** | Pattern observations | Every review | 5 sec to validate |
| **❓ Mode B** | Context questions | 50% → 5% (decreases) | 15 sec to answer |
| **📊 Feedback** | Rate + comments | Every review (optional) | 10 sec |

---

## ⚡ Quick Wins

```
Week 1: Answer "Who are your users?" → Sets Focused/Fluent scoring forever
Week 2: Mention "RBI compliance required" → Auto-checks forever
Week 3: Adjust Fair score 5x → System learns your threshold
Month 1: Run /context-5f report → Validate all learnings
```

---

## 🎯 Best Practices

### ✅ DO
- Answer first 5 context questions (builds 80% of context)
- Be specific: "RBI requires 2FA for >₹50k" not "missed compliance"
- Validate patterns: "Is X our standard?" → Yes/No
- Check monthly: `/context-5f report`

### ❌ DON'T
- Skip ALL feedback (aim for >70% response rate)
- Ignore context questions (they appear when system is uncertain)
- Let wrong learnings sit (edit immediately: `/context-5f edit`)

---

## 🛠️ Commands

```bash
/context-5f                 # What was learned?
/context-5f edit            # Fix wrong learnings
/context-5f answer          # Answer skipped questions
/context-5f report          # Monthly summary
/context-5f reset           # Start fresh
```

---

## 📊 Time Investment

| Phase | Time/Review | Total | Result |
|-------|-------------|-------|--------|
| Reviews 1-5 | 5 min | 25 min | 80% context built |
| Reviews 6-20 | 3 min | 45 min | Patterns validated |
| Reviews 21+ | 2 min | Minimal | Near-perfect accuracy |

**ROI:** 2 hours → Permanently smarter reviews

---

## 🔢 Confidence Thresholds

| Learning | Data Points | Action |
|----------|-------------|--------|
| Context answer | 1 | Use immediately ✅ |
| Business rule | 5+ | Add to auto-checks ✅ |
| Score calibration | 5+ consistent | Adjust threshold ✅ |
| Design pattern | 3+ | Recognize pattern ✅ |

---

## 🚦 What to Expect

### Review #1 (No Context)
- Many questions (50% rate)
- Generic scoring
- Missing your specific rules

### Review #10 (Some Context)
- Fewer questions (20% rate)
- Uses your user personas
- Checks your business rules

### Review #30 (Well-Calibrated)
- Minimal questions (5% rate)
- Perfect scoring (0 overrides)
- Auto-checks everything

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Too many questions | Normal for first 5 reviews, drops to 5% by review 21 |
| Wrong learning | `/context-5f edit` to fix immediately |
| No questions appearing | System has context, working as designed |
| Scores still off | Adjust 5x to calibrate, or manually edit thresholds |

---

## 💡 Pro Tips

1. **Front-load effort:** Answer all questions in first 5 reviews = 80% of context
2. **Be specific:** "RBI requires X" > "compliance issue"
3. **Validate early:** Confirm patterns when asked, prevents wrong learnings
4. **Monthly audit:** `/context-5f report` catches errors before they compound
5. **Share context:** Export → share with team → everyone benefits

---

## 🎓 Learning Curve

```
Day 1:     "Lots of questions, what is this?"
Week 1:    "Ah, it's learning my context"
Week 3:    "Reviews are getting more accurate"
Month 2:   "It knows my product better than I documented it"
Month 6:   "Zero overrides needed, perfect auto-checks"
```

---

**Get Started:** Just run `reviewing-designs-5f [design]` and answer the first question you see.

**Full Guide:** See `HOW-TO-USE.md`
**Quick Start:** See `QUICKSTART.md`
**Full Docs:** See `README.md`
