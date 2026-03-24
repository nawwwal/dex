# Quick Test Checklist - Managing User Panel v1.3

**Purpose:** Fast validation of critical bug fixes (15 minutes)
**Use this for:** Quick smoke testing before deployment

---

## ✅ CRITICAL BUGS (Must Pass All 4)

### [ ] Bug #1: "Other" Approver Flow
- Invoke skill → Select "Other" → Prompt appears ✅
- Enter invalid handle → Error shown ✅
- Enter valid handle → Confirmed ✅

### [ ] Bug #2: No Duplicate Messages
- Complete workflow → Simulate sheet error
- Verify: Only 1 message to Saurav (fallback) ✅
- Verify: Step 2 skipped ✅

### [ ] Bug #3: Iteration Counter
- Poor questions → Phase 3 review (iter 1)
- Make Changes → Review again (iter 2)
- Make Changes → Coaching offer appears (iter 3) ✅

### [ ] Bug #4: Screener Format Examples
- Reach Q7 → Format examples visible ✅
- Shows "Q: [question] / Desired Answer: [criteria]" ✅
- 3+ concrete examples shown ✅

---

## ✅ P1 BUGS (Must Pass 5/6)

### [ ] Bug #5: Single Source of Truth (Code Review)
- SKILL.md → References WORKFLOW-STRUCTURE.md ✅
- README.md → References WORKFLOW-STRUCTURE.md ✅
- Only 1 location has full approver list ✅

### [ ] Bug #6: Sheet ID Format (Code Review)
- WORKFLOW-STRUCTURE.md has both formats ✅
- Usage notes provided (API vs docs) ✅

### [ ] Bug #7: Phase 3 Routing
- Q4 issues only → Q4 auto-re-asked ✅
- Multiple issues → User asked to choose ✅

### [ ] Bug #8: Date Format (Code Review)
- Q1 shows DD-MMM-YYYY ✅
- Phase 5 shows DD-MMM-YYYY ✅

### [ ] Bug #9: Q1 Validation
- Empty input → Rejected ✅
- Partial input → Rejected ✅
- Complete input → Accepted ✅

### [ ] Bug #10: README File List (Code Review)
- All 5 reference files listed ✅
- Matches actual directory ✅

---

## PASS/FAIL

**Critical:** ___/4 ✅
**P1:** ___/6 ✅

**Deploy?** [ ] YES [ ] NO

---

**Tester:** _______________
**Date:** _______________
