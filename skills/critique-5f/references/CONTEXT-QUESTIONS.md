# Context Gathering Questions (MCQ Format)

This file contains the detailed MCQ questions for Phase 1, Step 4 of the review workflow.

---

## Question 1: Business Problem Statement

**What problem does this design solve?**

- [ ] User activation/onboarding (getting users to first value)
- [ ] Conversion optimization (driving purchase/signup)
- [ ] Retention improvement (reducing churn)
- [ ] Feature adoption (getting users to use new capability)
- [ ] Support reduction (reducing confusion/tickets)
- [ ] Compliance/regulatory requirement
- [ ] Other: [_________]

**Optional details:** [Free text]

---

## Question 2: Ideal User Journey

**What should the user accomplish in this flow?**

- [ ] Complete signup/registration
- [ ] Make first purchase/transaction
- [ ] Set up account/profile
- [ ] Discover and use key feature
- [ ] Complete task/workflow
- [ ] Other: [_________]

**Optional details:** [Free text - describe ideal path]

---

## Question 3: User Stories (Optional)

**Do you have user stories for this design?**

- [ ] Yes, I have written user stories → [Paste or describe]
- [ ] No, but I can describe goals → [Describe]
- [ ] No user stories available
- [ ] Skip this question

**User stories:** [Free text - optional]

---

## Question 4: Target Users

**Who are the primary users?**

- [ ] First-time users (new to product/domain)
- [ ] Repeat/power users (familiar with product)
- [ ] Technical users (developers, admins, IT)
- [ ] Business users (managers, analysts, decision-makers)
- [ ] Non-technical end users (consumers, general public)
- [ ] Mixed audience (multiple user types)
- [ ] Other: [_________]

**User demographics (optional):** [Age, location, tech proficiency, etc.]

---

## Question 5: Jobs to Be Done (JTBD)

**What job is the user hiring this product to do?**

- [ ] Get task done faster (efficiency)
- [ ] Learn new capability (education)
- [ ] Feel confident/secure (trust)
- [ ] Look good to others (social/status)
- [ ] Save money (economics)
- [ ] Reduce risk (safety)
- [ ] Not sure → Check HeyMarvin for user research
- [ ] Other: [_________]

**JTBD statement (optional):** [When I ___, I want to ___, so I can ___]

**→ Special: If "Not sure" selected:**
```
Check HeyMarvin MCP:
• Search for user research related to this product/feature
• Extract JTBD, pain points, motivations
• If data found → Use in review context
• If no data → Continue review without JTBD context
```

---

## Question 6: Business Objectives

**What business metrics should this design improve?**

- [ ] Activation rate (% completing onboarding)
- [ ] Conversion rate (% completing purchase/signup)
- [ ] Time to value (how fast users get benefit)
- [ ] Task completion rate (% finishing flow)
- [ ] Retention/churn reduction
- [ ] Support ticket reduction
- [ ] Revenue/monetization
- [ ] Multiple objectives: [Specify]

**Target metric (optional):** [e.g., "Increase activation from 65% to 80%"]

---

## Question 7: Specific Areas of Enquiry

**What should I focus on? (Select all that apply)**

- [ ] Speed & performance (load times, responsiveness)
- [ ] Clarity & ease of use (can users understand it?)
- [ ] Trust & transparency (do users feel safe?)
- [ ] Mobile experience (works on mobile?)
- [ ] Accessibility (WCAG compliance, inclusive design)
- [ ] Compliance/regulatory (legal requirements)
- [ ] Error handling (what if things go wrong?)
- [ ] Delight/personality (does it feel good to use?)
- [ ] Everything (comprehensive review)

**Specific concerns (optional):** [Free text - e.g., "Worried about jargon for non-technical users"]

---

## Context Object Format

After collecting responses, store in this format:

```json
{
  "user_context": {
    "business_problem": "...",
    "user_journey": "...",
    "user_stories": "...",
    "target_users": "...",
    "jtbd": "...",
    "business_objectives": "...",
    "focus_areas": [...],
    "market": "Indian B2B SaaS" // Infer from context
  }
}
```

---

## How Context Informs 5F Evaluation

| Context from Step 1 | Used to Evaluate... |
|---------------------|---------------------|
| **Business Problem** | Overall goal alignment, prioritization of issues |
| **User Journey** | Fast (does it match ideal path?), Fluent (flow makes sense?) |
| **User Stories** | Focused (does design support user goals?) |
| **Target Users** | Fluent (appropriate for user knowledge level), Fun (tone/personality fit) |
| **JTBD** | All 5Fs (does design help user accomplish their job?) |
| **Business Objectives** | Prioritization (which issues block objectives most?) |
| **Areas of Enquiry** | Focus attention on specific 5F sub-principles |
