# Managing User Panel - Workflow Structure Reference

**Quick Reference:** 5-phase workflow from brief creation to study logging

---

## Workflow Overview

```
Phase 1: Introduction & Approver Selection
    └─> Select cross-design manager (5 options)

Phase 2: Brief Creation (8 Sequential Questions)
    ├─> Q1: Requestor details
    ├─> Q2: Problem statement & hypothesis [+ COACHING]
    ├─> Q3: Research goals & areas of inquiry
    ├─> Q4: Key research questions [+ MOM TEST REVIEW]
    ├─> Q5: Methodology selection
    ├─> Q6: Session details [+ VALIDATION: 30+ mins]
    ├─> Q7: Screener questions [+ BEHAVIORAL CHECK]
    └─> Q8: Number of participants [+ SAMPLE SIZE VALIDATION]

Phase 3: Quality Review (Balanced Mode)
    └─> 5 criteria checks → Flag issues → Iterate or Approve

Phase 4: Approval Workflow
    ├─> Generate Google Doc
    ├─> Send Slack DM to approver
    ├─> Wait for approval
    └─> If changes → Re-ask questions → Re-submit

Phase 5: Study Logging & Notification
    ├─> Log to tracking sheet (7 columns)
    └─> Send status summary to coordination team (Saurav)
```

---

## Phase Breakdown

### Phase 1: Introduction & Approver Selection
**Duration:** 2 minutes
**Output:** Selected approver name + Slack user ID

**Approvers:** See "Quick Reference: Key Constants" section below for complete approver list with User IDs

---

### Phase 2: Brief Creation (8 Questions)

Each question has **Ask → Answer → Coach → Validate** pattern.

| # | Question | Coaching Focus | Validation |
|---|----------|----------------|------------|
| Q1 | Requestor details | — | — |
| Q2 | Problem & hypothesis | User-centered vs solution-first | Specific, observable |
| Q3 | Research goals | Areas to show/test | — |
| Q4 | Key research questions | Mom Test: Past behavior, not future | Non-leading, open-ended |
| Q5 | Methodology | Match method to goal | — |
| Q6 | Session details | 30+ minute requirement | Must be ≥30 mins |
| Q7 | Screener questions | Behavioral, not hypothetical | Past behavior questions |
| Q8 | Number of participants | Sample size guidance | 5-7 discovery, 5-8 usability, 8-12 concept |

**Coaching Triggers:**
- Q2: Flag solution-first problems
- Q4: Auto-review for leading questions (e.g., "Do you like...", "Would you use...")
- Q7: Auto-review for future intent (e.g., "Would you be interested...", "Do you plan...")
- Q6, Q8: Hard validation (block if <30 mins or out-of-range sample)

---

### Phase 3: Research Quality Review

**5 Criteria (Balanced Mode):**

1. **Problem-First Analysis**
   - ✅ User-centered problem statement
   - ⚠️ Solution-first language

2. **Discussion Guide Quality**
   - ⚠️ Leading questions ("Do you like...")
   - ⚠️ Yes/no questions
   - ✅ Open-ended "How/Why" questions

3. **Screener Questions**
   - ⚠️ Future intent ("Would you...", "Do you plan...")
   - ✅ Past behavior ("How often did you...", "When was the last time...")

4. **Sampling Strategy**
   - ✅ Within recommended range
   - ⚠️ Too small (<5) or too large (>12 for qualitative)

5. **Outcome-Question Alignment**
   - ⚠️ Missing critical questions for hypothesis

**Output Format:**
```
📊 Research Brief Quality Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Problem-First Analysis
   [Status message]

⚠️ Discussion Guide Quality
   [Flagged issues with suggestions]

[... other criteria ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall: 4/5 areas strong. 2 areas need improvement.

[Make Suggested Changes] [This Looks Good, Submit for Approval]
```

---

### Phase 4: Approval Workflow

**Step 1: Generate Google Doc**

Template structure:
```
User Panel Request Brief

Requestor Name: [Name]
Team / Project: [Team]
Date of Request: [Today's date]

1. Problem Statement & Hypothesis
2. Research Goals & Areas of Inquiry
3. Key Research Questions
4. Proposed Methodology
5. Session Details
6. Participant Screener Questions
7. Number of Participants Required
```

**Step 2: Share Doc**
- Set permissions: "Anyone with link can view"
- Get shareable link

**Step 3: Send Slack DM**

To: Selected approver (Phase 1)

Format:
```
──────────────────────────────────
📋 New User Panel Request

**From:** [Designer name]
**Study:** [Problem statement - first 80 chars]
**Participants:** [N users]
**Duration:** [X minutes]

📄 **Full Brief:** [Google Doc link]

──────────────────────────────────
Please review and respond:
✅ Approve - Ready to schedule
💬 Request Changes - Needs revision
──────────────────────────────────
```

**Step 4: Wait for Approval**
- Monitor thread
- If approved → Phase 5
- If changes requested → Re-ask questions → Re-submit

**Error Handling:**
- No response in 24h → Send reminder OR escalate to AD Research

---

### Phase 5: Study Logging & Notification

**Step 1: Log to Tracking Sheet**

Sheet: `https://docs.google.com/spreadsheets/d/1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro/edit?usp=sharing`

Append new row:
| Column | Field | Format |
|--------|-------|--------|
| A | Date | DD-MMM-YYYY (e.g., 17-Mar-2026) |
| B | Designer name | Text |
| C | Study type | Methodology (e.g., Discovery Interview) |
| D | Problem statement | First 100 chars |
| E | No. of participants | Number |
| F | Status | "Pending Scheduling" |
| G | Brief link | Google Doc shareable link |

**Step 2: Send Status Summary**

To: Saurav Rastogi (`U014YNNNQ2V`)

Format:
```
──────────────────────────────────
🎯 User Panel Study Approved & Logged

**Designer:** [Name] ([Team])
**Study:** [Problem statement]
**Methodology:** [Type]
**Participants:** [N users]
**Duration:** [X mins]

**Screener Criteria:**
[Key criteria from screeners]

📄 **Full Brief:** [Google Doc link]
📊 **Tracker:** Row #[N] - [Sheet link]

**Next Step:** Please coordinate with panel agency for scheduling (2-3 business days turnaround).

**Agency POC:**
Phone: 8002734762 (Primary)
Escalation: 8149001986
──────────────────────────────────
```

**Confirmation to User:**
```
✅ Status summary sent to coordination team (@saurav.rastogi)

You're all set! Next steps:
1. Coordination team will email panel agency
2. Expect scheduling within 2-3 business days
3. You'll receive calendar invites once confirmed

Prepare while waiting:
- Create Google Meet links
- Test your prototype/materials
- Review discussion guide
```

---

## Decision Trees

### Q6 Validation: Session Duration
```
User specifies duration
    ├─> ≥30 minutes → ✅ Proceed
    └─> <30 minutes → ⚠️ "User Panel SOP requires 30+ mins"
                      ├─> Adjust to 30+ → Continue
                      └─> Keep short → "Use cold calls instead" → Exit
```

### Q8 Validation: Sample Size
```
User specifies N participants for [methodology]
    ├─> Within range (5-7 discovery, 5-8 usability, 8-12 concept) → ✅ Proceed
    └─> Outside range → ⚠️ "Standard range is [X-Y] for [method]. More rarely yields new insights."
                        ├─> Adjust → Continue
                        └─> Keep as-is → Document reason → Continue
```

### Phase 3: Quality Review Decision
```
Review all 5 criteria
    ├─> All ✅ → Proceed to Phase 4
    ├─> Some ⚠️ → Show flagged issues
    │              ├─> Make Changes → Re-ask specific questions → Re-review
    │              └─> Submit Anyway → Proceed to Phase 4
    └─> Multiple ⚠️ after 3 iterations → Suggest coaching session
```

### Phase 4: Approval Response
```
Monitor Slack thread
    ├─> ✅ Approved → Confirm to user → Phase 5
    ├─> 💬 Changes Requested → Show feedback → Re-ask questions → Re-submit
    └─> No response in 24h → Ask user:
                            ├─> Send reminder
                            ├─> Escalate to AD Research
                            └─> Wait longer
```

---

## Error Recovery Patterns

### Scenario: Sheet Write Permission Denied
```
Try to append row
    └─> Permission denied
        └─> Fallback: Send brief details via Slack DM to Saurav
            ├─> Include all 7 column values for manual logging
            └─> SKIP Step 2 (Status Summary) to avoid duplicate notification
```

### Scenario: Poor Brief Quality After 3 Iterations
```
After 3 revision rounds with persistent issues
    └─> Offer:
        ├─> Schedule 15-min coaching with research team
        ├─> Review Mom Test principles guide (references/MOM-TEST-PRINCIPLES.md)
        └─> Submit as-is (not recommended, but allow)
```

### Scenario: Approver Selection "Other"
```
User selects "Other (specify Slack handle)"
    ├─> Ask: "Please provide Slack handle (e.g., @firstname.lastname)"
    ├─> Look up user ID via Slack API
    │   ├─> Found → Store name + user ID
    │   └─> Not found → Ask for user ID directly or re-select from list
    └─> Proceed to Phase 2
```

---

## Success Metrics

**Quality Indicators:**
- ✅ Problem statement is user-centered (not feature-centered)
- ✅ Research questions are open-ended, non-leading
- ✅ Screener questions ask about past behavior (not future intent)
- ✅ Sampling size matches methodology (5-7 for qualitative)

**Workflow Completion:**
- ✅ Cross-design manager approval received
- ✅ Study logged to tracking sheet
- ✅ Status summary sent to coordination team

**Time Benchmarks:**
- Phase 1-2: 10-15 minutes (brief creation)
- Phase 3: 2-3 minutes (quality review)
- Phase 4: Variable (wait for approval, typically <24h)
- Phase 5: 2 minutes (logging)

---

## Integration Points

### Google Workspace MCP
- Create Doc: Phase 4, Step 1
- Share Doc: Phase 4, Step 2
- Append to Sheet: Phase 5, Step 1

### Slack MCP
- Send DM (Approver): Phase 4, Step 3
- Monitor thread: Phase 4, Step 4
- Send DM (Saurav): Phase 5, Step 2

### HeyMarvin MCP (Optional)
- Not used in core workflow
- Can be referenced in coaching examples

---

## Quick Reference: Key Constants

**Tracking Sheet:**
- **Sheet ID (for API calls):** `1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro`
- **Full URL (for documentation/links):** `https://docs.google.com/spreadsheets/d/1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro/edit?usp=sharing`

**Coordination Team:**
- Saurav Rastogi: `U014YNNNQ2V`

**Approvers:**
| Name | Slack Handle | User ID |
|------|--------------|---------|
| Soni | @soni | U33LQ5Q2X |
| Ankit Punia | @ankit.punia@razorpay.com | U06LJR20NQJ |
| Pingal Kakati | @pingal.kakati@razorpay.com | UBGQDHJV7 |
| Varghese Mathew | @varghese.mathew@razorpay.com | U09P6MDLGPK |
| Abhinav Krishna | @abhinav.krishna@razorpay.com | U013WFYJEUT |

**Panel Agency:**
- Primary: 8002734762
- Escalation: 8149001986

**Timeline SLA:**
- Scheduling turnaround: 2-3 business days

---

## Version Info

**Version:** 1.2
**Created:** 2026-03-17
**Last Updated:** 2026-03-18
**Synced with:** SKILL.md v1.3
**Bug Fixes:**
- Clarified sheet fallback logic (Critical Bug #2)
- Standardized tracking sheet ID format with usage notes (P1 Bug #6)
- Converted approver list references to single source of truth (P1 Bug #5)

---

**This reference is a companion to SKILL.md. For detailed coaching scripts and full message templates, see the main SKILL.md file.**
