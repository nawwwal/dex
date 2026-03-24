# 5F Design Review - Core Workflow

**Version:** 1.1
**Last Updated:** 2026-03-16
**Status:** CANONICAL - DO NOT REWRITE THIS FILE

⚠️ **IMPORTANT:** This is the authoritative workflow definition. Only make additive edits, never rewrite from scratch.

---

## Complete Review Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: CONTEXT GATHERING (Max 8 MCQ Questions)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Gather context through MCQs to inform 5F evaluation:          │
│  1. Business problem statement                                 │
│  2. Ideal user journey                                         │
│  3. User stories (if available)                                │
│  4. Target users                                               │
│  5. User's JTBD (Jobs to Be Done)                              │
│  6. Business objectives                                        │
│  7. Specific areas of enquiry/testing                          │
│  8. Design stage (Exploratory/Experimental/Final UI)           │
│                                                                 │
│  Special: If user doesn't know target users well →             │
│           Check Hey Marvin MCP for user research data          │
│           If no data found → Continue review without it        |
|                                                                 |
|   Note: Check the type of design upload. If its Claude make-    |
|    do the review inside agent-browser                            │
│                                                                 │
│  Design stage affects review intensity and scoring strictness  │
│                                                                 │
└────────────────────────┬────────────────────────────────────────
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: SONI MOOD SELECTION (MCQ)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Which perspective do you want?                                │
│                                                                 │
│  [ ] Strategic Soni    - Business impact, metrics, ROI         │
│  [ ] Creative Soni     - Innovation, delight, differentiation  │
│  [ ] Critical Soni     - Usability issues, risks, gaps         │
│  [ ] Balanced (All 3)  - Comprehensive view (default)          │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: VIEW PREFERENCE (MCQ)                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  How detailed should the review be?                            │
│                                                                 │
│  [ ] Simple View       - Quick summary with prioritization     │
│                          (3-5 min read)                         │
│                                                                 │
│  [ ] Advanced View     - Detailed 5F analysis + prioritization │
│                          (15-20 min read)                       │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: RUN REVIEW                                             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────────────────┐
│  SIMPLE VIEW             │  ADVANCED VIEW                       │
├──────────────────────────┼──────────────────────────────────────┤
│                          │                                      │
│  1. Context Summary      │  1. Context Summary                  │
│     (from Step 1)        │     (from Step 1)                    │
│                          │                                      │
│  2. 5F Scorecard         │  2. 5F Detailed Analysis             │
│     (table format)       │     For each F:                      │
│                          │     • Score + justification          │
│  3. Top 3-5 Issues       │     • Sub-principles breakdown       │
│     (most critical)      │     • Specific evidence from design  │
│                          │                                      │
│  4. Top 3-5 Wins         │  3. Strategic Wins                   │
│     (what's working)     │     (what's working well)            │
│                          │                                      │
│  5. Quick Recs           │  4. Critical Gaps                    │
│     (3-5 fixes)          │     (detailed issue breakdown)       │
│                          │                                      │
│  THEN ↓                  │  5. Top 5 Recommendations            │
│                          │     (one per F-principle, if applicable)            │
│  6. Prioritization       │                                      │
│     Framework Summary    │  THEN ↓                              │
│     • P0 (must fix)      │                                      │
│     • P1 (should fix)    │  6. Prioritization Framework Summary │
│     • P2 (nice to have)  │     • P0/P1/P2 breakdown             │
│     • Business impact    │     • Business impact forecast       │
│                          │     • Market-specific insights       │
│                          │                                      │
└──────────────────────────┴──────────────────────────────────────┘

                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: LEARNING SYSTEM (Background Agent - Separate)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Runs AFTER main review completes                              │
│  Does NOT interrupt Steps 1-4                                  │
│  Completely optional - user can skip                           │
│                                                                 │
│  • Mode A: Pattern observation                                 │
│  • Mode B: Context question (if gaps detected)                 │
│  • Feedback: Rating + comments                                 │
│  • Logging: Save to review-sessions.jsonl                      │
│  • Learning: Update memory files (weekly)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## STEP 1: Context Gathering Questions (Max 8 MCQs)

### Question 1: Business Problem Statement

**What problem does this design solve?**

- User activation/onboarding (getting users to first value)
- Conversion optimization (driving purchase/signup)
- Retention improvement (reducing churn)
- Feature adoption (getting users to use new capability)
- Support reduction (reducing confusion/tickets)
- Compliance/regulatory requirement
- Other: [_________]

**Optional details:** [Free text]

---

### Question 2: Ideal User Journey

**What should the user accomplish in this flow?**

- Complete signup/registration
- Make first purchase/transaction
- Set up account/profile
- Discover and use key feature
- Complete task/workflow
- Other: [_________]

**Optional details:** [Free text - describe ideal path]

---

### Question 3: User Stories (Optional)

**Do you have user stories for this design?**

- Yes, I have written user stories → [Paste or describe]
- No, but I can describe goals → [Describe]
- No user stories available
- Skip this question

**User stories:** [Free text - optional]

---

### Question 4: Target Users

**Who are the primary users?**

- First-time users (new to product/domain)
- Repeat/power users (familiar with product)
- Technical users (developers, admins, IT)
- Business users (managers, analysts, decision-makers)
- Non-technical end users (consumers, general public)
- Mixed audience (multiple user types)
- Other: [_________]

**User demographics (optional):** [Age, location, tech proficiency, etc.]

---

### Question 5: Jobs to Be Done (JTBD)

**What job is the user hiring this product to do?**

- Get task done faster (efficiency)
- Learn new capability (education)
- Feel confident/secure (trust)
- Look good to others (social/status)
- Save money (economics)
- Reduce risk (safety)
- Not sure → Check Hey Marvin for user research
- Other: [_________]

**JTBD statement (optional):** [When I ___, I want to ___, so I can ___]

**→ Special: If "Not sure" selected:**

```
Check Hey Marvin MCP:
• Search for user research related to this product/feature
• Extract JTBD, pain points, motivations
• If data found → Use in review context
• If no data → Continue review without JTBD context
```

---

### Question 6: Business Objectives

**What business metrics should this design improve?**

- Activation rate (% completing onboarding)
- Conversion rate (% completing purchase/signup)
- Time to value (how fast users get benefit)
- Task completion rate (% finishing flow)
- Retention/churn reduction
- Support ticket reduction
- Revenue/monetization
- Multiple objectives: [Specify]

**Target metric (optional):** [e.g., "Increase activation from 65% to 80%"]

---

### Question 7: Specific Areas of Enquiry

**What should I focus on? (Select all that apply)**

- Speed & performance (load times, responsiveness)
- Clarity & ease of use (can users understand it?)
- Trust & transparency (do users feel safe?)
- Mobile experience (works on mobile?)
- Accessibility (WCAG compliance, inclusive design)
- Compliance/regulatory (legal requirements)
- Error handling (what if things go wrong?)
- Delight/personality (does it feel good to use?)
- Everything (comprehensive review)

**Specific concerns (optional):** [Free text - e.g., "Worried about jargon for non-technical users"]

---

### Question 8: Design Stage

**Which stage is this design at?**

- **Exploratory** (wireframes, sketches, early ideas - just exploring concepts)
- **Experimental** (testing different iterations, validating approaches)
- **Final UI** (polished, ready to publish/hand off to engineering)

**Why this matters:**
This determines the review intensity and focus areas:


| Design Stage     | Review Style                   | Focus Areas                                                          | 5F Scoring Intensity                                            |
| ---------------- | ------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Exploratory**  | Lenient, encourages bold ideas | User journey, concept validation, innovation opportunities           | Relaxed - focus on F2 (Focused), F4 (Fluent)                    |
| **Experimental** | Balanced, co-creative          | Comparing approaches, identifying best direction, user testing needs | Medium - evaluate all 5Fs, flag critical gaps                   |
| **Final UI**     | Strict, production-ready       | Usability, polish, edge cases, accessibility, user pain points       | Rigorous - strict scoring on F1 (Fast), F2 (Focused), F5 (Fair) |


**Example Review Adjustments:**

**Exploratory Stage:**

- ✅ Encourage: "What if you tried [bold idea]?"
- ✅ Focus on: Big picture user flow, conceptual clarity
- ❌ Don't nitpick: Pixel-perfect spacing, exact copy, visual polish
- Scoring: More forgiving on F3 (Fun) and F1 (Fast) - focus on direction

**Experimental Stage:**

- ✅ Encourage: "Option A vs Option B - here's what each solves"
- ✅ Focus on: Comparing iterations, identifying patterns, user testing priorities
- ⚠️ Flag: Critical usability issues that should be tested
- Scoring: Balanced across all 5Fs, identify which iteration scores better

**Final UI Stage:**

- ✅ Encourage: "This is strong, but here are edge cases to address"
- ✅ Focus on: Production readiness, edge cases, accessibility, error states
- 🚨 Flag: Any usability issues that will cause user abandonment
- Scoring: Strict - production-quality bar, must score 7+/10 on F1, F2, F5 to ship

---

## How Context Informs 5F Evaluation


| Context from Step 1     | Used to Evaluate...                                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Business Problem**    | Overall goal alignment, prioritization of issues                                                            |
| **User Journey**        | Fast (does it match ideal path?), Fluent (flow makes sense?)                                                |
| **User Stories**        | Focused (does design support user goals?)                                                                   |
| **Target Users**        | Fluent (appropriate for user knowledge level), Fun (tone/personality fit)                                   |
| **JTBD**                | All 5Fs (does design help user accomplish their job?)                                                       |
| **Business Objectives** | Prioritization (which issues block objectives most?)                                                        |
| **Areas of Enquiry**    | Focus attention on specific 5F sub-principles                                                               |
| **Design Stage**        | Review intensity and scoring strictness (Exploratory = lenient, Experimental = balanced, Final UI = strict) |


---

## Prioritization Framework (Included in BOTH Views)

**Always ends with this summary:**

```markdown
## Prioritization Summary

### 🔴 P0 - Must Fix (Launch Blockers)
**Criteria:** Blocks >20% of users OR regulatory requirement OR breaks core flow

• [Issue] → Impact: [X]% drop-off / [Y] business metric
• [Issue] → Impact: [Z] regulatory risk

**Est. Fix Effort:** [Hours/Days]
**Business Impact:** [Conversion lift / Risk mitigation]

---

### 🟡 P1 - Should Fix (High Impact)
**Criteria:** Impacts 10-20% of users OR hurts key metric OR trust/satisfaction

• [Issue] → Impact: [X]% improvement potential
• [Issue] → Impact: User trust/satisfaction

**Est. Fix Effort:** [Hours/Days]
**Business Impact:** [Metric improvement]

---

### 🟢 P2 - Nice to Have (Polish)
**Criteria:** <10% impact OR delight factor OR edge cases

• [Issue] → Impact: Polish, edge cases
• [Issue] → Impact: Delight factor

**Est. Fix Effort:** [Hours/Days]
**Business Impact:** Marginal gains

---

### 📊 Business Impact Forecast

**If you fix P0 + P1:**
- [Metric 1]: [Current] → [After Fix] (+[X]%)
- [Metric 2]: [Current] → [After Fix] (+[Y]%)
- **ARR Impact:** [Calculation based on business objectives]

**If you fix only P0:**
- [Metric]: [Current] → [After Fix] (+[X]%)
- **Risk Mitigation:** [Regulatory / User drop-off avoided]
```

---

## Example Review Flow

**User provides context:**

- Problem: User activation for payment gateway
- Journey: Signup → KYC → Bank setup → First payment
- Users: First-time business owners, Tier 2/3 cities
- JTBD: Start accepting payments quickly
- Objective: Increase activation from 65% to 78%
- Focus: Clarity (jargon concerns), Trust (security/compliance)

**Review uses this to:**

- Score Fluent strictly (first-time users = low jargon tolerance)
- Score Fair for trust/transparency (security is key concern)
- Prioritize issues that block activation metric
- Focus on clarity and trust sub-principles

**Output includes:**

- 5F scores informed by user context
- P0: Issues blocking activation (jargon, error recovery)
- P1: Issues hurting trust (missing AI confidence, compliance)
- Business impact: "Fix P0+P1 → 65% to 78% activation = ₹15L ARR"

---

## Adapting Review Style Based on Design Stage

**Use Question 8 (Design Stage) to calibrate review intensity:**

### Exploratory Stage (Wireframes, Early Ideas)

**Review Approach: Lenient + Encouraging**

**Focus on:**

- ✅ Big picture user journey and conceptual clarity
- ✅ Bold ideas and innovation opportunities
- ✅ Direction validation ("Is this solving the right problem?")
- ✅ User flow logic (does the sequence make sense?)

**DON'T nitpick:**

- ❌ Pixel-perfect spacing, exact alignment
- ❌ Final copy, labels, microcopy
- ❌ Visual polish, colors, typography
- ❌ Edge cases, error states (unless critical)

**5F Scoring Intensity:**

- **Relaxed on:** F1 (Fast), F3 (Fun) - can't judge polish yet
- **Focus on:** F2 (Focused) - Is the core concept clear?
- **Focus on:** F4 (Fluent) - Does the flow make sense?
- **Minimum bar:** 5/10 on F2 and F4 to continue exploring

**Tone:**

- "Love the bold direction on [X]!"
- "What if you tried [creative alternative]?"
- "This concept solves [problem], but consider [user scenario]"

---

### Experimental Stage (Testing Iterations)

**Review Approach: Balanced + Co-Creative**

**Focus on:**

- ✅ Comparing iterations ("Option A vs Option B - here's what each solves")
- ✅ Identifying patterns across iterations
- ✅ User testing priorities (what to validate first)
- ✅ Critical usability issues to fix before testing

**DO flag:**

- ⚠️ Critical user pain points that should be tested
- ⚠️ Assumptions that need validation
- ⚠️ Major flow issues that break core experience

**5F Scoring Intensity:**

- **Medium strictness:** Evaluate all 5Fs
- **Identify gaps:** Flag issues that need testing
- **Compare iterations:** Which version scores better and why?
- **Target bar:** 6-7/10 across F1, F2, F4, F5 to proceed to testing

**Tone:**

- "Option A solves [X] better, but Option B handles [Y] case"
- "Both iterations miss [critical scenario] - suggest testing with [user segment]"
- "This approach is working - recommend testing [specific hypothesis]"

---

### Final UI Stage (Polished, Ready to Publish)

**Review Approach: Strict + Production-Ready**

**Focus on:**

- ✅ Production readiness (can this ship as-is?)
- ✅ Edge cases, error states, empty states
- ✅ Accessibility (WCAG compliance, keyboard nav)
- ✅ User pain points that cause abandonment
- ✅ Visual polish and consistency

**FLAG immediately:**

- 🚨 Any usability issues causing user abandonment
- 🚨 Missing error recovery flows
- 🚨 Accessibility violations (blocker for launch)
- 🚨 Trust/transparency gaps (F5 failures)

**5F Scoring Intensity:**

- **Rigorous strictness:** Production-quality bar
- **Must score 7+/10 on:** F1 (Fast), F2 (Focused), F5 (Fair) to ship
- **Must score 6+/10 on:** F3 (Fun), F4 (Fluent)
- **Any score <6:** Classify as P0 (launch blocker)

**Tone:**

- "This is strong overall, but [critical issue] is a launch blocker"
- "Edge case: What happens when [scenario]? No error state shown"
- "Missing accessibility: [specific WCAG violation] - blocks launch"
- "Polish opportunity: [F3 enhancement] - ship without it, add later"

---

### Design Stage Impact on Prioritization


| Priority              | Exploratory                                      | Experimental                       | Final UI                                            |
| --------------------- | ------------------------------------------------ | ---------------------------------- | --------------------------------------------------- |
| **P0 (Must Fix)**     | Conceptual blockers (wrong problem, broken flow) | Critical usability issues to test  | Launch blockers (abandonment, accessibility, trust) |
| **P1 (Should Fix)**   | Major flow improvements                          | Iteration-specific improvements    | High-impact polish, edge cases                      |
| **P2 (Nice to Have)** | Polish ideas for later                           | Alternative approaches to consider | Minor polish, delight enhancements                  |


**Example:**

**Same Issue, Different Stage:**

Issue: "Button label says 'Submit' instead of 'Create Account'"

- **Exploratory:** P2 (Nice to Have) - "Can refine copy later"
- **Experimental:** P1 (Should Fix) - "Test with clearer label"
- **Final UI:** P0 (Must Fix) - "Ambiguous CTA causes confusion - launch blocker"

---

## Key Principles

✅ **Context first:** Always gather context before reviewing (Step 1)
✅ **User-centric:** Evaluate for THEIR users, not generic best practices
✅ **Business-aligned:** Prioritize by impact on THEIR objectives
✅ **Evidence-based:** Cite specific screens, user research (Marvin), industry data
✅ **Actionable:** Always end with prioritized recommendations + business impact
✅ **Stage-adaptive:** Adjust review intensity based on design stage (Q8)

---

**Version History:**

- v1.1 (2026-03-16): Added Question 8 (Design Stage) + stage-adaptive review guidelines
- v1.0 (2026-03-11): Initial workflow with 7 context questions + Hey Marvin integration

