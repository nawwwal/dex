# Managing User Panel - Skill Documentation

**Version:** 1.0
**Created:** 2026-03-17
**Owner:** Caren J, Senior User Researcher @ Razorpay

---

## What This Skill Does

Automates the Razorpay user panel request workflow while acting as a research quality consultant. Helps designers:

1. **Write high-quality research briefs** with Mom Test coaching
2. **Get cross-design manager approval** via Slack DM
3. **Log studies** to tracking sheet automatically
4. **Notify coordination team** with formatted status summary

**Time saved:** 2-3 hours → 10-15 minutes per request

---

## When to Use This Skill

Use this skill when you:
- Need to recruit participants from Razorpay's user panel
- Want research quality coaching (Mom Test principles)
- Need to submit a research brief for approval
- Are a designer, PM, or researcher requesting user panel access

**Trigger phrases:**
- "I need user panel"
- "Can I use the research panel?"
- "How do I request participants?"
- "/user-panel"

---

## How It Works (5-Phase Workflow)

### Phase 1: Approval Stakeholder Selection
Asks you to select which cross-design manager should approve your brief.

**Approvers:** (See `references/WORKFLOW-STRUCTURE.md` → Quick Reference → Approvers table for complete list)

---

### Phase 2: Brief Creation (Guided Questions)
Asks 8 questions with research coaching:

1. **Requestor Details** - Name, team
2. **Problem Statement** - What user problem are you solving?
   - *Coaching: Problem-first, not solution-first*
3. **Research Goals** - What will you test/show?
4. **Research Questions** - Top 3-5 questions (How/Why, not Would you)
   - *Coaching: Non-leading, open-ended, Mom Test principles*
5. **Methodology** - Interview, usability test, etc.
6. **Session Details** - Duration (min 30 mins), tools
7. **Screener Questions** - How to filter participants
   - *Coaching: Behavioral, not hypothetical*
8. **No. of Participants** - 5-7 recommended for qualitative

---

### Phase 3: Research Quality Review
Evaluates your brief against:

✅ **Problem-first analysis** - User-centered problem statement
✅ **Discussion guide quality** - Non-leading, open-ended questions
✅ **Screener quality** - Behavioral, specific
✅ **Sampling strategy** - Right size for methodology
✅ **Outcome alignment** - Questions match hypothesis

**Review mode:** Balanced (flags critical issues, suggests improvements)

**If issues found:** Provides specific rewrites, iterates with you until quality-approved.

---

### Phase 4: Approval Workflow
1. Creates Google Doc with formatted brief
2. Sends Slack DM to selected approver with brief link
3. Waits for approval or change requests
4. If changes needed → Iterates with you → Re-submits

---

### Phase 5: Logging & Notification
1. **Logs to tracking sheet:**
   - https://docs.google.com/spreadsheets/d/1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro/edit?usp=sharing
   - Appends row with: Date, Designer, Study type, Participants, Status, Brief link

2. **Sends status summary to coordination team:**
   - Slack DM to Saurav Rastogi (User ID: U014YNNNQ2V)
   - Includes brief link, screener criteria, tracker row number
   - Coordination team then contacts panel agency

---

## Research Quality Guardrails

This skill enforces Mom Test principles:

### Rule 1: Problem-First
❌ "We want to test if users like the new design"
✅ "Users abandon checkout. We hypothesize it's due to unclear pricing."

### Rule 2: Non-Leading Questions
❌ "Do you like this feature?"
✅ "How do you currently solve [problem]?"

### Rule 3: Behavioral Screeners
❌ "Would you be interested in..."
✅ "How often in the last 30 days did you..."

**See:** `references/MOM-TEST-PRINCIPLES.md` for full guidelines

---

## Example Usage

**Designer:** "I need user panel for my reports dashboard research"

**Skill:**
```
Hi! I'm your research consultant. I'll help you write a great brief.

Who should approve this?
1. Soni
2. Ankit Punia
...
```

**Designer:** "2 - Ankit Punia"

**Skill:** "Great! Let's start. What's your name and team?"

**Designer:** "Caren, Design Principles team"

**Skill:** "What problem are we solving?"

**Designer:** "We want to test the new reports layout"

**Skill:**
```
⚠️ This sounds solution-first.

Better problem statement:
"Users abandon reports page within 30 seconds. We believe it's due to unclear navigation."

Try rephrasing as a user problem, not a solution test.
```

**Designer:** "Users can't find the report they need quickly"

**Skill:** "✅ Much better! User-centered and specific. Next question..."

*(15 minutes later)*

**Skill:**
```
📊 Quality Review Complete

✅ Problem statement: User-centered
⚠️ Question 3 is leading - suggested rewrite provided
✅ Screeners: Behavioral
✅ Sampling: 5 users (optimal)

[Make Changes] [Submit for Approval]
```

**Designer:** "Submit for Approval"

**Skill:**
```
✅ Brief created and sent to Ankit Punia for approval
✅ Logged to tracking sheet (Row #47)
✅ Status summary sent to coordination team

You're all set! Expect scheduling within 2-3 business days.
```

---

## Success Metrics

**Quality indicators:**
- 100% of briefs are problem-first (not solution-first)
- 90%+ of questions are non-leading
- 100% of screeners are behavioral
- 0 briefs approved with hypothetical questions

**Efficiency indicators:**
- Time per brief: 2-3 hours → 10-15 minutes (5-10x faster)
- Approval turnaround: < 24 hours
- Support tickets: "How do I request panel?" → 0

---

## Troubleshooting

### Issue: Approver doesn't respond
**Solution:** Skill auto-escalates after 24 hours to AD Research

### Issue: Can't write to tracking sheet
**Solution:** Skill sends manual logging request via Slack DM to coordination team

### Issue: Brief quality is very poor after 3 iterations
**Solution:** Skill suggests 15-min coaching session with research team

---

## Configuration

**Tracking Sheet:**
https://docs.google.com/spreadsheets/d/1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro/edit?usp=sharing

**Status Summary Recipient:**
- Saurav Rastogi (@saurav.rastogi@razorpay.com) - Slack User ID: U014YNNNQ2V

**Cross-Design Manager Approvers:**
See `references/WORKFLOW-STRUCTURE.md` → Quick Reference: Key Constants → Approvers table for complete list.

**To update approvers:** Edit `references/WORKFLOW-STRUCTURE.md` → Quick Reference → Approvers table (single source of truth)

---

## Files in This Skill

```
managing-user-panel/
├── SKILL.md                          # Main skill workflow
├── README.md                         # This file (documentation)
├── TEST-SCRIPT.md                    # Comprehensive test script (10 test cases, 45-60 min)
├── QUICK-TEST-CHECKLIST.md           # Fast validation checklist (15 min)
├── TEST-ENVIRONMENT-SETUP.md         # Test environment configuration guide
└── references/
    ├── WORKFLOW-DIAGRAM.md           # Visual flowcharts (Mermaid + ASCII)
    ├── WORKFLOW-STRUCTURE.md         # Detailed workflow reference + constants
    ├── COACHING-SCRIPTS.md           # Coaching feedback templates
    ├── MESSAGE-TEMPLATES.md          # Slack/Doc message templates
    └── MOM-TEST-PRINCIPLES.md        # Research quality guidelines
```

---

## Future Enhancements (v2.0)

- **Auto-scheduling integration:** Sync with panel agency calendar
- **HeyMarvin integration:** Auto-log sessions to research repository
- **Quality analytics:** Track brief quality scores over time
- **Designer coaching reports:** "You've improved 40% since first brief!"
- **Screener library:** Reusable screener question templates

---

## Support

**Questions about the skill:**
- Caren J (@caren.j) - Skill owner

**Questions about user panel process:**
- Saurav Rastogi (@saurav.rastogi@razorpay.com) - Coordination lead

**Questions about research quality:**
- Pingal Kakati / Varghese Mathew - AD Research

---

**Last Updated:** 2026-03-18
**Changelog:**
- v1.2 (2026-03-18): Fixed P1 bugs - Updated approver references to single source of truth, completed file list with all reference docs
- v1.0 (2026-03-17): Initial release
