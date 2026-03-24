# Coaching Scripts - Managing User Panel

**Purpose:** Detailed coaching feedback for each question in Phase 2
**Version:** 1.1 | **Last Updated:** 2026-03-18 | **Bug Fix:** Added screener format examples to Q7

---

## Q2: Problem Statement & Hypothesis - Coaching

**After user answers, provide this coaching:**

```
✅ Good problem statements are:
- User-centered (not feature-centered)
- Specific (not vague)
- Observable (you can measure it)

❌ Avoid:
- "We want to test if users like the new design" (solution-first)
- "Users don't understand our product" (too vague)

✅ Better:
- "Users abandon reports dashboard after 30 seconds. We believe it's due to unclear navigation."

Does your problem statement follow this? [Yes, looks good] [Let me revise]
```

If user selects "Let me revise" → re-ask Question 2.

---

## Q3: Research Goals - Coaching

**After user answers:**

```
Be specific about what you'll show/test. This helps with:
- Screener design (recruit right users)
- Session planning (time allocation)
- Analysis (focused insights)
```

---

## Q4: Key Research Questions - Mom Test Coaching

**After user answers, provide this coaching:**

```
🎯 Mom Test Principle: Ask about PAST behavior, not FUTURE intent

❌ Leading/Hypothetical Questions:
- "Would you use this feature?"
- "Do you like this design?"
- "Is this button clear?"

✅ Non-Leading, Open-Ended Questions:
- "How do you currently solve [problem]?"
- "Walk me through the last time you [did task]."
- "What frustrates you most about [current process]?"

Review your questions:
[Question 1] - ✅ Good | ⚠️ Improve
[Question 2] - ⚠️ Leading - Rewrite as: "How do you currently..."
[Question 3] - ✅ Good

[Make Changes] [This Looks Good]
```

If "Make Changes" → re-ask Question 4 with suggestions.

---

## Q5: Methodology - Coaching

**After user answers:**

```
Match method to goal:
- Discovery/Understanding → Interview
- Usability/Task flow → Moderated test
- Concept validation → Concept test
```

---

## Q6: Session Details - Validation Warning

**If duration < 30 minutes:**

```
⚠️ You specified [X minutes].
User Panel SOP requires minimum 30 minutes.

Participants are decision-makers who won't engage with low-impact studies.

Adjust to 30+ minutes? [Yes] [No, I'll use cold calls instead]
```

If "No" → Explain user should use cold calls, not panel. Exit workflow.

---

## Q7: Screener Questions - Behavioral Coaching

**After user answers, provide this coaching:**

```
🎯 Screener Best Practices:

📋 **Format your screeners like this:**

Example 1:
Q: "How many times in the last 30 days did you download a financial report?"
Desired Answer: "5+ times" or "Weekly"

Example 2:
Q: "When was the last time you set up a new payment gateway for your business?"
Desired Answer: "Within last 6 months"

Example 3:
Q: "How often do you manually reconcile payments?"
Desired Answer: "Daily" or "Multiple times per week"

---

❌ Avoid Future Intent:
- "Would you be interested in..."
- "Do you plan to..."

✅ Ask About Past Behavior:
- "How often in the last [timeframe] did you..."
- "When was the last time you..."

❌ Avoid Binary Questions:
- "Are you a business owner?" (too broad)

✅ Be Specific:
- "Do you manage financial reconciliation for your business?" (targeted)

Review your screeners:
[Screener 1] - ⚠️ Future intent - Rewrite as behavioral
[Screener 2] - ✅ Good - Specific and behavioral

[Make Changes] [This Looks Good]
```

If "Make Changes" → re-ask Question 7 with suggestions.

---

## Q8: Number of Participants - Validation

**If outside recommended range:**

```
You requested [N] participants for [methodology].

✅ Standard range: [5-7] for [discovery interviews]
⚠️ Your request: [N]

Reasoning: Qualitative research reaches saturation around 5-7 interviews.
More than 8 rarely yields new insights, costs more time.

Proceed with [N]? [Yes] [Adjust to recommended range]
```

---

## Phase 3: Quality Review - Balanced Mode Criteria

### 1. Problem-First Analysis
- ✅ User-centered problem statement
- ⚠️ Flag if solution-first

### 2. Discussion Guide Quality
- ⚠️ Flag leading questions ("Do you like...")
- ⚠️ Flag yes/no questions
- ✅ Approve open-ended "How/Why" questions

### 3. Screener Questions
- ⚠️ Flag future intent questions
- ✅ Approve behavioral questions

### 4. Sampling Strategy
- ✅ Within recommended range
- ⚠️ Flag if too small (<5) or too large (>12 for qualitative)

### 5. Outcome-Question Alignment
- ⚠️ Flag if missing critical questions for stated hypothesis

---

## Quality Review Output Template

```
📊 Research Brief Quality Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Problem-First Analysis
   Problem statement is user-centered and specific.

⚠️ Discussion Guide Quality
   Question 3: "Do you like the new reports page?"
   → This is leading. Rewrite as:
     "How do you currently access your financial reports?"

✅ Screener Questions
   All screeners ask about past behavior.

✅ Sampling Strategy
   5 participants for discovery interviews (optimal range).

⚠️ Outcome-Question Alignment
   Missing question about current workarounds.
   → Add: "What workarounds have you built to solve this problem?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: 4/5 areas strong. 2 areas need improvement.

[Make Suggested Changes] [This Looks Good, Submit for Approval]
```

---

## 3+ Iterations - Coaching Intervention

**After 3 revision rounds with persistent issues:**

```
After 3 revision rounds, I've noticed:
- Questions still leading
- Problem statement still solution-first

Would you like to:
1. Schedule 15-min coaching session with research team
2. Review Mom Test principles guide
3. Submit as-is (not recommended)

[Select option]
```

---

**This file contains all detailed coaching scripts. SKILL.md should reference this file for coaching logic.**
