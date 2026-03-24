# User Panel Skill v1.3 - Release Announcement

**Release Date:** March 18, 2026
**Version:** 1.3
**Type:** Bug Fixes + Enhancements

---

## 📢 What's New

### ✨ New Features

**1. "Other" Approver Option**
- Can now select any Slack user as your approver
- No longer limited to the pre-defined list
- Just select "Other" and provide their Slack handle

**2. Screener Format Examples**
- Now shows 3 concrete examples when writing screener questions
- Clear format: "Q: [question] / Desired Answer: [criteria]"
- Helps you write better, more specific screeners

**3. Enhanced Validation**
- Name and team are now required (won't accept empty inputs)
- Prevents incomplete data in tracking sheet
- Clearer error messages throughout

---

## 🔧 Improvements

**Behind the Scenes:**
- ✅ Approver list easier to maintain
- ✅ Date format consistent (DD-MMM-YYYY everywhere)
- ✅ Better error handling for edge cases
- ✅ Documentation updated and complete
- ✅ No duplicate notifications

---

## 💡 How to Use

**Nothing changes for you!**

Just invoke the skill as usual:
- Say: **"I need user panel"**
- Or: **"Need participants for research"**

The workflow is the same, just with better guidance and validation.

---

## 📋 Quick Tips

**For Q1 (Name & Team):**
- Both are now required - you'll see an error if you forget one

**For Q7 (Screeners):**
- Look for the format examples (3 shown)
- Structure: Q: [question] / Desired Answer: [criteria]

**For Approver Selection:**
- See option "6. Other" if your manager isn't in the list
- Provide their Slack handle (@firstname.lastname)

---

## 🐛 Bugs Fixed

- Fixed: "Other" approver option now works properly
- Fixed: Empty name/team no longer accepted
- Fixed: Screener format now has clear examples
- Fixed: Better error handling throughout
- Fixed: Documentation accuracy

---

## 📚 Documentation

**Full documentation:**
`${CLAUDE_PLUGIN_ROOT}/skills/managing-user-panel/README.md`

**Test suite (for QA):**
`/skills/managing-user-panel/TEST-SCRIPT.md`

---

## ❓ Questions?

**Contact:** Caren J (@caren.j)

**Report Issues:**
File in skill repository or ping @caren.j directly

---

## 🎯 What's Next

**Coming in future versions:**
- Brief preview before approval
- More context-aware coaching
- Timeline estimates
- Quality score tracking

---

**Happy researching! 🚀**

---

*Version 1.3 deployed on March 18, 2026*
