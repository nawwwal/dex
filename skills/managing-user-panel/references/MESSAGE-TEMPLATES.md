# Message Templates - Managing User Panel

**Purpose:** All Slack messages and Google Doc templates for the workflow
**Version:** 1.1 | **Last Updated:** 2026-03-18 | **Bug Fix:** Added "Other" approver selection flow

---

## Phase 1: Introduction Message

```
Hi! I'm your research consultant. I'll help you:

1. Write a crisp, user-centered research brief
2. Review it for Mom Test principles (non-leading questions, behavioral screeners)
3. Get cross-design manager approval
4. Log the study and notify the coordination team

This takes ~10-15 minutes. Let's create a great brief together!
```

---

## Phase 1: Approver Selection Prompt

```
Who should approve this research brief?

Please select the cross-design manager for your team:

1. Soni (@soni) - User ID: U33LQ5Q2X
2. Ankit Punia (@ankit.punia@razorpay.com) - User ID: U06LJR20NQJ
3. Pingal Kakati (@pingal.kakati@razorpay.com) - User ID: UBGQDHJV7
4. Varghese Mathew (@varghese.mathew@razorpay.com) - User ID: U09P6MDLGPK
5. Abhinav Krishna (@abhinav.krishna@razorpay.com) - User ID: U013WFYJEUT
6. Other (specify Slack handle)

[Select number or specify handle]
```

---

## Phase 1: Other Approver Selection Flow

**If user selects "6. Other":**

```
You selected "Other". Please provide the Slack handle of your approver.

Format: @firstname.lastname (e.g., @john.doe)

[User inputs handle]
```

**After user inputs handle:**

```
Looking up user ID for [handle]...
```

**If found:**

```
✅ Found: [Full Name] (User ID: [ID])

Great! I'll send the approval request to [Full Name] when the brief is ready.
```

**If not found:**

```
❌ Could not find Slack user with handle [handle].

Please check the handle and try again, or:
1. Select from the pre-defined list (options 1-5)
2. Provide the Slack User ID directly (format: U followed by alphanumeric)

[User choice]
```

**If user provides User ID directly:**

```
You provided User ID: [ID]

Please confirm the name of this person:
[User inputs name]

✅ Stored: [Name] (User ID: [ID])
```

---

## Phase 4: Google Doc Brief Template

```
User Panel Request Brief

Requestor Name: [Name]
Team / Project: [Team]
Date of Request: [Today's date]

1. Problem Statement & Hypothesis
[User's answer from Q2]

2. Research Goals & Areas of Inquiry
[User's answer from Q3]

3. Key Research Questions
[User's answer from Q4]

4. Proposed Methodology
[User's answer from Q5]

5. Session Details
Duration: [X minutes]
Tools: [Google Meet, Figma link, etc.]

6. Participant Screener Questions
[User's answer from Q7 - formatted as list]

7. Number of Participants Required
[User's answer from Q8]
```

---

## Phase 4: Slack DM to Approver

**To:** [Selected approver Slack user ID]

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

---

## Phase 4: Changes Requested - User Notification

```
Your manager requested changes:
"[Feedback text]"

Let's revise the brief. Which section needs updating?
1. Problem Statement
2. Research Questions
3. Screener Questions
4. Other

[Select section to revise]
```

---

## Phase 5: Tracking Sheet - Confirmation Message

```
✅ Study logged to tracking sheet (Row #[N])
📊 View tracker: [Sheet link]
```

---

## Phase 5: Slack DM to Coordination Team (Saurav)

**To:** Saurav Rastogi (U014YNNNQ2V)

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

---

## Phase 5: Final Confirmation to User

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

## Error Handling: No Response from Approver (24h)

```
⏰ No response from [approver] in 24 hours.

Options:
1. Send reminder to approver
2. Escalate to AD Research (Pingal: UBGQDHJV7 or Varghese: U09P6MDLGPK)
3. Wait longer

[Select option]
```

---

## Error Handling: Sheet Write Permission Denied

```
❌ Cannot write to tracking sheet.

Possible causes:
- Sheet permissions restricted
- Incorrect sheet URL

I'll send brief details via Slack DM to Saurav Rastogi (U014YNNNQ2V) for manual logging.

[Confirm]
```

**Fallback Slack Message to Saurav:**

```
⚠️ Unable to write to tracking sheet directly. Please log manually:

**Date:** [DD-MMM-YYYY]
**Designer:** [Name]
**Study Type:** [Methodology]
**Problem:** [First 100 chars]
**Participants:** [N]
**Status:** Pending Scheduling
**Brief Link:** [Google Doc link]
```

---

## Error Handling: Poor Brief Quality After 3 Iterations

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

## Recommended Sample Sizes by Methodology

**For Q8 coaching:**

```
Recommended ranges:
- Discovery interviews: 5-7 users
- Usability testing: 5-8 users
- Concept validation: 8-12 users
```

---

**This file contains all message templates. SKILL.md should reference this file for message content.**
