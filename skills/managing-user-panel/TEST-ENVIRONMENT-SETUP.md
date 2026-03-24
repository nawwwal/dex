# Test Environment Setup Guide

**Purpose:** Configure test environment for validating managing-user-panel skill
**Audience:** QA testers, skill maintainers
**Setup Time:** 15-20 minutes

---

## Prerequisites

### Required Access
- [ ] Claude Code installed and configured
- [ ] PM Compass skills loaded (`compass-v0.1.0/`)
- [ ] Slack workspace access (for testing Slack DMs)
- [ ] Google Workspace account (for doc/sheet creation)
- [ ] Skill version v1.3 or higher

### Optional (for complete testing)
- [ ] Test Slack workspace (separate from production)
- [ ] Test Google Sheet (copy of production tracker)
- [ ] Admin access to modify sheet permissions (for error simulation)

---

## Setup Steps

### Step 1: Verify Skill Installation

```bash
# Navigate to skills directory
cd ${CLAUDE_PLUGIN_ROOT}/skills/managing-user-panel

# Check version
grep "Version:" SKILL.md
# Should show: Version: 1.3 or higher

# Verify all files present
ls -la
# Should see: SKILL.md, README.md, TEST-SCRIPT.md, QUICK-TEST-CHECKLIST.md, references/

# Check references
ls -la references/
# Should see: WORKFLOW-DIAGRAM.md, WORKFLOW-STRUCTURE.md, COACHING-SCRIPTS.md,
#             MESSAGE-TEMPLATES.md, MOM-TEST-PRINCIPLES.md
```

**Expected Result:** All files present, version 1.3+

---

### Step 2: Configure Test Slack Workspace (Optional)

**If using production Slack:**
- Use your own user ID for approver selection
- Use real approvers (they'll see test messages)
- Add "[TEST]" prefix to all briefs

**If using test Slack workspace:**
1. Create test workspace at slack.com/create
2. Invite 2-3 test users (simulate approvers)
3. Get test user Slack IDs:
   ```
   - Click user profile → More → Copy member ID
   - Format: U followed by alphanumeric (e.g., U01234ABCD)
   ```
4. Update test data with test user IDs

---

### Step 3: Configure Test Google Sheet

**Option A: Use Production Sheet (Read-Only Test)**
- Sheet ID: `1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro`
- You can test doc creation but NOT sheet writing
- Good for: TC-1, TC-3, TC-4, TC-5, TC-6, TC-7, TC-8, TC-9, TC-10

**Option B: Create Test Sheet (Full Test)**
1. Copy production sheet:
   - Open: https://docs.google.com/spreadsheets/d/1UzZ5A2adJ3OrOCjme6D87jbxtNQZoKJBp_aTkxLjOro/
   - File → Make a copy → Name: "User Panel Tracker - TEST"
2. Set permissions:
   - Share → Anyone with link can EDIT (for normal test)
   - Share → Anyone with link can VIEW (for error test - TC-2)
3. Get new sheet ID from URL:
   - Format: /d/{SHEET_ID}/edit
4. **IMPORTANT:** Restore production sheet ID after testing

**Sheet Structure (7 columns):**
| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Date | Designer | Study Type | Problem | N | Status | Link |
| DD-MMM-YYYY | Text | Text | Text | Number | Text | URL |

---

### Step 4: Prepare Test Data

**Consistent Test Values (use for all tests):**

```yaml
# Q1: Requestor Details
name: "Test User (QA)"
team: "Design Principles - Test Environment"
date: "18-Mar-2026" (auto-filled)

# Q2: Problem Statement
problem: "Users abandon reports page after 30 seconds due to unclear navigation hierarchy and missing search functionality."
hypothesis: "We believe that adding breadcrumbs and a search bar will reduce abandonment by 40%."

# Q3: Research Goals
goals: |
  - Test new reports navigation prototype (Figma link: figma.com/test-123)
  - Validate search functionality placement
  - Identify pain points in current flow

# Q4: Research Questions (with intentional issues for TC-3)
## First attempt (POOR - for testing):
questions_poor:
  - "Do you like the new dashboard design?"
  - "Would you use the search feature?"
  - "Is the navigation clear?"

## Second attempt (BETTER):
questions_better:
  - "How do you currently find reports in the existing system?"
  - "Walk me through the last time you searched for a specific report."
  - "What frustrates you most about the current reports page?"

# Q5: Methodology
methodology: "Moderated Usability Test"

# Q6: Session Details
duration: 45 (minutes)
tools: "Google Meet (link to be created), Figma prototype (figma.com/test-123)"

# Q7: Screener Questions
screeners:
  - question: "How many times in the last 30 days did you access financial reports?"
    desired_answer: "5+ times or Weekly"
  - question: "Do you have decision-making authority for report customization?"
    desired_answer: "Yes - can request changes from finance team"
  - question: "When was the last time you downloaded or exported a report?"
    desired_answer: "Within last 7 days"

# Q8: Participants
participants: 6
```

---

### Step 5: Error Simulation Setup

#### Simulating Sheet Permission Error (TC-2)

**Method 1: Restricted Permissions (Recommended)**
1. Use test sheet from Step 3
2. Set permissions to "Anyone with link can VIEW" (removes write access)
3. Run test → Sheet write will fail
4. Verify fallback triggered

**Method 2: Invalid Sheet ID**
1. Temporarily modify skill to use non-existent sheet ID
2. Run test → Sheet write will fail
3. Restore correct sheet ID after test

**Method 3: Code Review (Fastest)**
1. Review SKILL.md Phase 5 logic
2. Verify fallback logic: "If permission denied → SKIP Step 2"
3. Check MESSAGE-TEMPLATES.md has fallback message template

#### Simulating Invalid Slack Handle (TC-1)

**Test Handles:**
- **Invalid:** `@nonexistent.user` (format correct, user doesn't exist)
- **Malformed:** `nonexistent.user` (missing @)
- **Valid:** Use your own Slack handle or teammate's

---

## Test Execution Order

### Quick Smoke Test (15 min)
Use `QUICK-TEST-CHECKLIST.md`
1. TC-4: Screener format examples (2 min)
2. TC-9: Q1 validation (3 min)
3. TC-1: Other approver flow (5 min)
4. TC-3: Iteration counter (5 min)

### Code Review Tests (10 min)
No skill execution needed:
1. TC-5: Approver list DRY (3 min)
2. TC-6: Sheet ID format (2 min)
3. TC-8: Date format (2 min)
4. TC-10: README file list (1 min)

### Integration Tests (30 min)
Requires full workflow execution:
1. TC-2: Sheet fallback (10 min)
2. TC-7: Phase 3 routing (10 min)
3. Regression: Happy path end-to-end (10 min)

---

## Common Issues & Solutions

### Issue 1: Skill Not Loading
**Symptom:** "I need user panel" doesn't trigger skill
**Solution:**
1. Check skill is in correct directory: `compass-v0.1.0/skills/managing-user-panel/`
2. Verify SKILL.md has YAML frontmatter with `name: managing-user-panel`
3. Restart Claude Code
4. Try full invocation: `/managing-user-panel`

### Issue 2: Slack DM Not Sending
**Symptom:** Error when trying to send DM to approver
**Solution:**
1. Verify Slack MCP configured in `.mcp.json`
2. Check Slack OAuth token is valid
3. Verify user ID format (should start with U)
4. Try with your own user ID first

### Issue 3: Google Doc Creation Fails
**Symptom:** Error creating brief document
**Solution:**
1. Verify Google Workspace MCP configured
2. Check OAuth permissions include Google Docs
3. Try creating doc manually to verify account access
4. Check for API quota limits

### Issue 4: Sheet Write Fails (Not Error Simulation)
**Symptom:** Sheet write fails when it should succeed
**Solution:**
1. Verify sheet ID is correct
2. Check sheet permissions: Anyone with link can EDIT
3. Verify Google Sheets API enabled
4. Try manual write to test access

---

## Test Data Cleanup

After testing, clean up:

### Slack Cleanup
- [ ] Delete test DMs sent to approvers
- [ ] Inform approvers about test messages if using production Slack

### Google Cleanup
- [ ] Delete test briefs created in Google Docs
- [ ] Remove test rows from tracking sheet (if using production)
- [ ] Delete test sheet (if created)

### Skill State
- [ ] Restore production sheet ID if changed
- [ ] Remove any test comments added to code

---

## Pre-Deployment Checklist

Before deploying to production:

- [ ] All critical tests passed (4/4)
- [ ] 5+ P1 tests passed (5/6 or better)
- [ ] Regression tests passed
- [ ] Test data cleaned up
- [ ] Production sheet ID confirmed
- [ ] Production approver list confirmed
- [ ] Changelog updated
- [ ] README version bumped
- [ ] Test results documented

---

## Support

**Questions about test setup?**
- Skill owner: Caren J (@caren.j)
- Test script issues: File bug in skill repository

**Technical issues?**
- Slack MCP: Check `.mcp.json` configuration
- Google MCP: Check OAuth permissions
- Skill loading: Restart Claude Code

---

**Version:** 1.0
**Created:** 2026-03-18
**Last Updated:** 2026-03-18
