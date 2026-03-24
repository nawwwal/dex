# Managing User Panel - Test Script

**Version:** 1.0
**Created:** 2026-03-18
**Purpose:** Validate bug fixes for v1.3 release
**Total Tests:** 10 test cases covering 10 bug fixes
**Estimated Time:** 45-60 minutes

---

## Test Environment Setup

### Prerequisites
- [ ] Claude Code with managing-user-panel skill loaded
- [ ] Access to test Slack workspace
- [ ] Access to tracking sheet (view permissions minimum)
- [ ] Test Google account for doc creation
- [ ] Skill version: v1.3 or higher

### How to Run Tests
1. Start each test case with a fresh skill invocation
2. Follow steps exactly as written
3. Mark ✅ PASS or ❌ FAIL for each test
4. Document any failures in "Actual Result" section
5. If any test fails, file a bug report

---

## CRITICAL BUG TESTS (4 tests)

### Test Case 1: "Other" Approver Flow
**Bug:** #1 - Missing "Other" approver flow template
**Priority:** Critical
**Estimated Time:** 5 minutes

#### Test Steps
1. Invoke skill: "I need user panel"
2. When prompted for approver, select: **"6. Other"**
3. Verify prompt appears asking for Slack handle with format example
4. Enter **invalid handle**: `@nonexistent.user`
5. Verify error message with options to retry or provide User ID
6. Enter **valid handle** (use real team member or test account)
7. Verify confirmation message with name and User ID

#### Expected Results
- [ ] Step 2: "Other" option available in approver list
- [ ] Step 3: Prompt shows format example: `@firstname.lastname`
- [ ] Step 5: Error message includes:
  - "Could not find Slack user"
  - Option to retry
  - Option to provide User ID directly
- [ ] Step 7: Shows "✅ Found: [Name] (User ID: [ID])"

#### Pass Criteria
✅ All prompts appear correctly
✅ Error handling works for invalid handle
✅ Valid handle is accepted and confirmed

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 2: Sheet Fallback - No Duplicate Messages
**Bug:** #2 - Sheet fallback creates duplicate messages to Saurav
**Priority:** Critical
**Estimated Time:** 10 minutes (requires simulating permission error)

#### Test Steps
1. Complete full brief workflow through Phase 4 (approval)
2. Get approval from manager
3. Reach Phase 5 Step 1 (Log to Tracking Sheet)
4. **Simulate:** Sheet write permission denied (test environment should have restricted permissions, OR review code logic)
5. Verify fallback message sent to Saurav with manual logging request
6. **Verify:** Step 2 (Status Summary) is SKIPPED
7. Confirm user receives message about fallback

#### Expected Results
- [ ] Step 5: Fallback message sent to Saurav with all 7 column values
- [ ] Step 6: NO additional Status Summary message sent to Saurav
- [ ] Step 7: User informed about fallback: "Sent details to coordination team for manual logging"

#### Pass Criteria
✅ Only ONE message sent to Saurav (fallback)
✅ Step 2 skipped (no duplicate status summary)
✅ User notified about fallback

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 3: Iteration Counter Tracking
**Bug:** #3 - Iteration counter not tracked, coaching intervention doesn't trigger
**Priority:** Critical
**Estimated Time:** 15 minutes

#### Test Steps
1. Start workflow and reach Q4 (Research Questions)
2. **Intentionally provide poor questions** with leading language:
   - "Do you like the new dashboard?"
   - "Would you use this feature?"
   - "Is this button clear?"
3. Continue through Q5-Q8
4. Reach Phase 3 Quality Review
5. Verify issues flagged in Criterion 2 (Discussion Guide Quality)
6. Select **"Make Changes"** → iteration_count = 2
7. Revise Q4 but still use 1-2 leading questions
8. Phase 3 review again → Select **"Make Changes"** again → iteration_count = 3
9. **Verify:** Coaching intervention offer appears

#### Expected Results
- [ ] Step 5: Criterion 2 flagged with suggestions
- [ ] Step 6: Able to revise Q4
- [ ] Step 8: After 2nd revision, iteration counter triggers coaching offer
- [ ] Step 9: Coaching options shown:
  - "1. Schedule 15-min coaching with research team"
  - "2. Review Mom Test principles guide"
  - "3. Submit as-is (not recommended)"

#### Pass Criteria
✅ First iteration (after Q8) = 1
✅ First "Make Changes" = iteration 2
✅ Second "Make Changes" = iteration 3
✅ Coaching intervention appears at iteration 3

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 4: Screener Format Examples
**Bug:** #4 - Screener question format ambiguity
**Priority:** Critical
**Estimated Time:** 5 minutes

#### Test Steps
1. Start workflow and reach Q7 (Screener Questions)
2. **Verify coaching script shows format examples** before user answers
3. Check that examples include:
   - "Q: [question]"
   - "Desired Answer: [criteria]"
4. Verify 3 concrete examples provided

#### Expected Results
- [ ] Step 2: Format examples visible in coaching
- [ ] Step 3: Examples show structure:
  ```
  Q: "How many times in the last 30 days did you download a financial report?"
  Desired Answer: "5+ times" or "Weekly"
  ```
- [ ] Step 4: At least 3 examples provided (reports, payments, onboarding)

#### Pass Criteria
✅ Format examples appear in Q7 coaching
✅ Structure is clear: Q + Desired Answer
✅ Multiple concrete examples provided

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

## P1 BUG TESTS (6 tests)

### Test Case 5: Approver List Single Source of Truth
**Bug:** #5 - Approver list hardcoded in 5+ places
**Priority:** Medium
**Estimated Time:** 5 minutes (code review)

#### Test Steps
1. Open `SKILL.md` and search for "Soni" or "Ankit Punia"
2. Verify Phase 1 Step 2 **references** WORKFLOW-STRUCTURE.md (doesn't list approvers)
3. Verify footer **references** Quick Reference (doesn't duplicate list)
4. Open `README.md` and search for approver names
5. Verify all locations **reference** WORKFLOW-STRUCTURE.md
6. Open `WORKFLOW-STRUCTURE.md` → Quick Reference
7. Verify **only this location** has the complete approver table

#### Expected Results
- [ ] Step 2: SKILL.md Phase 1 says "See WORKFLOW-STRUCTURE.md for complete list"
- [ ] Step 3: SKILL.md footer says "See WORKFLOW-STRUCTURE.md → Quick Reference"
- [ ] Step 5: README.md references WORKFLOW-STRUCTURE.md (no duplicate)
- [ ] Step 7: WORKFLOW-STRUCTURE.md has complete table with all 5 approvers + User IDs

#### Pass Criteria
✅ Only 1 location has complete approver list (WORKFLOW-STRUCTURE.md)
✅ All other files reference that source
✅ No hardcoded duplicates found

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 6: Tracking Sheet ID Format Standardization
**Bug:** #6 - Tracking sheet ID format inconsistency
**Priority:** Medium
**Estimated Time:** 3 minutes (code review)

#### Test Steps
1. Open `WORKFLOW-STRUCTURE.md` → Quick Reference
2. Verify both formats documented:
   - Sheet ID (for API calls)
   - Full URL (for documentation/links)
3. Check SKILL.md Phase 5 → verify uses Sheet ID with reference note
4. Check if full URL is used anywhere → verify it's in documentation sections only

#### Expected Results
- [ ] Step 2: Quick Reference shows:
  ```markdown
  **Tracking Sheet:**
  - Sheet ID (for API calls): 1UzZ5A2adJ3Or...
  - Full URL (for documentation/links): https://docs.google...
  ```
- [ ] Step 3: SKILL.md Phase 5 uses Sheet ID + reference to Quick Reference
- [ ] Step 4: Clear usage guidance provided

#### Pass Criteria
✅ Both formats documented with usage notes
✅ API sections use Sheet ID
✅ Documentation sections use full URL

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 7: Phase 3 Auto-Detection Routing
**Bug:** #7 - Phase 3 decision logic unclear
**Priority:** Medium
**Estimated Time:** 10 minutes

#### Test Steps
1. Create brief with **only Q4 issues** (leading questions in research questions)
2. Reach Phase 3 → Criterion 2 flagged
3. Select "Make Changes"
4. **Verify:** Q4 is automatically re-asked (not Q2 or Q7)
5. Fix Q4, reach Phase 3 again
6. This time create brief with **both Q2 and Q4 issues**
7. Select "Make Changes"
8. **Verify:** Agent asks "Which would you like to revise first?"

#### Expected Results
- [ ] Step 4: Q4 automatically re-asked based on Criterion 2 flag
- [ ] Step 8: When multiple criteria flagged, user is asked to choose

#### Criterion-to-Question Mapping Verification
- [ ] Criterion 1 flagged → Q2 re-asked
- [ ] Criterion 2 flagged → Q4 re-asked
- [ ] Criterion 3 flagged → Q7 re-asked
- [ ] Criterion 4 flagged → Q8 re-asked

#### Pass Criteria
✅ Single criterion → auto-routes to correct question
✅ Multiple criteria → asks user to choose
✅ Routing logic is explicit and documented

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 8: Date Format in Q1 and Phase 5
**Bug:** #8 - Date format only in Phase 5, missing in Q1
**Priority:** Medium
**Estimated Time:** 3 minutes (code review + workflow test)

#### Test Steps
1. Open `SKILL.md` and navigate to Q1 (around line 76)
2. Verify date format mentioned: "DD-MMM-YYYY format, e.g., 18-Mar-2026"
3. Navigate to Phase 5 Step 1 (around line 209)
4. Verify same format documented: "DD-MMM-YYYY, e.g., 17-Mar-2026"
5. Start workflow and check Q1 → verify today's date auto-fills in correct format

#### Expected Results
- [ ] Step 2: Q1 shows date format in Store instruction
- [ ] Step 4: Phase 5 shows same format in column A description
- [ ] Step 5: Auto-filled date uses DD-MMM-YYYY (e.g., 18-Mar-2026)

#### Pass Criteria
✅ Date format documented in both Q1 and Phase 5
✅ Format is consistent (DD-MMM-YYYY)
✅ Auto-fill uses correct format

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 9: Q1 Validation for Empty Inputs
**Bug:** #9 - No validation for Q1 (Requestor Details)
**Priority:** Medium
**Estimated Time:** 5 minutes

#### Test Steps
1. Start workflow
2. Reach Q1: "What's your name and team?"
3. **Test 1:** Press Enter without typing anything
4. Verify error message: "Name and team cannot be empty. Please provide both."
5. **Test 2:** Type name only: "John Doe" (no team)
6. Verify error message appears
7. **Test 3:** Type both: "John Doe, Design Team"
8. Verify acceptance and continuation to Q2

#### Expected Results
- [ ] Step 4: Error message for completely empty input
- [ ] Step 6: Error message for missing team
- [ ] Step 8: Accepted when both provided

#### Pass Criteria
✅ Empty input rejected
✅ Partial input rejected
✅ Complete input accepted

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

### Test Case 10: README File List Completeness
**Bug:** #10 - README file list incomplete
**Priority:** Low-Medium
**Estimated Time:** 2 minutes (code review)

#### Test Steps
1. Open `README.md` and navigate to "Files in This Skill" section
2. Verify all 5 reference files listed:
   - WORKFLOW-DIAGRAM.md
   - WORKFLOW-STRUCTURE.md
   - COACHING-SCRIPTS.md
   - MESSAGE-TEMPLATES.md
   - MOM-TEST-PRINCIPLES.md
3. Check actual `references/` directory
4. Verify file list matches reality

#### Expected Results
- [ ] Step 2: File tree shows all 5 reference files
- [ ] Step 4: All files in directory are documented

#### File Tree Should Look Like:
```
managing-user-panel/
├── SKILL.md
├── README.md
└── references/
    ├── WORKFLOW-DIAGRAM.md
    ├── WORKFLOW-STRUCTURE.md
    ├── COACHING-SCRIPTS.md
    ├── MESSAGE-TEMPLATES.md
    └── MOM-TEST-PRINCIPLES.md
```

#### Pass Criteria
✅ All 5 reference files documented
✅ File tree structure accurate
✅ No missing or extra files

**Result:** [ ] PASS [ ] FAIL
**Notes:**

---

## TEST SUMMARY

### Results Table

| Test ID | Bug # | Priority | Status | Notes |
|---------|-------|----------|--------|-------|
| TC-1 | #1 | Critical | [ ] P [ ] F | Other approver flow |
| TC-2 | #2 | Critical | [ ] P [ ] F | Sheet fallback |
| TC-3 | #3 | Critical | [ ] P [ ] F | Iteration counter |
| TC-4 | #4 | Critical | [ ] P [ ] F | Screener format |
| TC-5 | #5 | Medium | [ ] P [ ] F | Approver list DRY |
| TC-6 | #6 | Medium | [ ] P [ ] F | Sheet ID format |
| TC-7 | #7 | Medium | [ ] P [ ] F | Phase 3 routing |
| TC-8 | #8 | Medium | [ ] P [ ] F | Date format |
| TC-9 | #9 | Medium | [ ] P [ ] F | Q1 validation |
| TC-10 | #10 | Low-Med | [ ] P [ ] F | README file list |

### Pass Criteria
- **Critical bugs (TC-1 to TC-4):** ALL must pass
- **P1 bugs (TC-5 to TC-10):** 5/6 must pass

### Test Sign-Off

**Tester Name:** _______________
**Date:** _______________
**Overall Status:** [ ] PASS [ ] FAIL

**Critical Bugs Passed:** ___/4
**P1 Bugs Passed:** ___/6
**Total Passed:** ___/10

### Issues Found

| Test ID | Issue Description | Severity | Status |
|---------|------------------|----------|--------|
| | | | |
| | | | |

---

## Regression Testing (Optional)

After fixing bugs, verify these workflows still work:

### Regression Test 1: Happy Path (End-to-End)
- [ ] Complete full workflow from Phase 1 to Phase 5
- [ ] No errors encountered
- [ ] Doc created, approval received, study logged

### Regression Test 2: Mom Test Coaching
- [ ] Q4 coaching flags leading questions correctly
- [ ] Q7 coaching flags future intent correctly
- [ ] Suggestions provided are helpful

### Regression Test 3: MCP Integrations
- [ ] Google Doc created successfully
- [ ] Slack DM sent to approver successfully
- [ ] Tracking sheet updated successfully

---

## Notes for Test Execution

### Simulating Error Conditions
**Sheet Permission Error (TC-2):**
- Option 1: Use test environment with restricted sheet permissions
- Option 2: Review code logic for fallback path
- Option 3: Temporarily change sheet ID to non-existent sheet

**Invalid Slack Handle (TC-1):**
- Use handle format but non-existent user: `@test.nonexistent`
- Verify lookup fails gracefully

### Test Data
**Use these test values for consistency:**
- Requestor Name: "Test User"
- Team: "Design Principles (Test)"
- Problem Statement: "Users abandon reports page after 30s due to unclear navigation"
- Methodology: "Moderated Usability Test"
- Participants: 5-7 users
- Duration: 45 minutes

---

## Bug Report Template

If any test fails, use this template:

```markdown
**Bug ID:** [Auto-generated]
**Test Case:** TC-[#]
**Bug Title:** [Short description]
**Severity:** Critical / Medium / Low
**Status:** New

**Steps to Reproduce:**
1.
2.
3.

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Environment:**
- Skill Version: v1.3
- Claude Code Version:
- Date: 2026-03-18

**Screenshots/Logs:**
[Attach if available]
```

---

**End of Test Script**

**Version History:**
- v1.0 (2026-03-18): Initial test script for v1.3 bug fixes
