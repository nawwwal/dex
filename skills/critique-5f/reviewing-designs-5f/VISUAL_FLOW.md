# 5F Learning System - Visual Flow Diagram

---

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  USER INVOKES SKILL                             │
│                                                                 │
│  User runs: reviewing-designs-5f [design-file]                 │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│             ORCHESTRATOR ACTIVATES                              │
│                                                                 │
│  Step 1: Load Learned Context                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │ • LEARNINGS.md (summary)                 │                  │
│  │ • business-rules.md (compliance)         │                  │
│  │ • user-personas.md (target users)        │                  │
│  │ • design-system.md (patterns)            │                  │
│  │ • product-specifics.md (business model)  │                  │
│  │ • scoring calibrations (adjusted weights)│                  │
│  │ • active hypotheses (patterns to test)   │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│            RUN ORIGINAL SKILL (UNTOUCHED)                       │
│                                                                 │
│  Step 2: Execute reviewing-designs-5f                          │
│  ┌──────────────────────────────────────────┐                  │
│  │  Original skill receives:                │                  │
│  │  - Design file/URL                       │                  │
│  │  + Enhanced context (learned)            │                  │
│  │                                          │                  │
│  │  Original skill generates:               │                  │
│  │  - 5F scores (with learned calibrations) │                  │
│  │  - Issues (checking learned rules)       │                  │
│  │  - Recommendations (context-aware)       │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
│  ✅ Original skill code: UNCHANGED                              │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              APPEND MODE A (Every Review)                       │
│                                                                 │
│  Step 3: Add Experimental Observation                          │
│  ┌──────────────────────────────────────────┐                  │
│  │ 🧪 Learning Mode                         │                  │
│  │                                          │                  │
│  │ Hypothesis: "Users prefer tables for    │                  │
│  │              financial data"             │                  │
│  │                                          │                  │
│  │ Observation: You used tables here.      │                  │
│  │ Competitors (Tally, Zoho) use tables.   │                  │
│  │                                          │                  │
│  │ Quick validation:                        │                  │
│  │ ✅ Yes, our standard                     │                  │
│  │ ❌ No, experimenting                     │                  │
│  │ 🤷 Unsure                                │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
│  Size: 3-5 sentences (5% of review)                            │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│       APPEND MODE B (If Uncertainty Detected)                   │
│                                                                 │
│  Step 4: Add Context Question (5-50% of reviews)               │
│                                                                 │
│  ┌─ Uncertainty Detection ─────────────────┐                   │
│  │ IF high_info_density AND no_user_persona│                   │
│  │ OR forms_detected AND no_compliance_rules│                   │
│  │ OR heavy_media AND no_performance_data   │                   │
│  │ OR ... (10 trigger categories)           │                   │
│  └──────────────────────────────────────────┘                  │
│                   │                                             │
│                   ▼                                             │
│  ┌──────────────────────────────────────────┐                  │
│  │ ❓ Quick Context Question                │                  │
│  │                                          │                  │
│  │ I see 18 data fields. To score          │                  │
│  │ "Focused" accurately:                    │                  │
│  │                                          │                  │
│  │ Your primary users are:                  │                  │
│  │ [ ] Data analysts                        │                  │
│  │ [ ] Business managers ← User selects     │                  │
│  │ [ ] Operations staff                     │                  │
│  │                                          │                  │
│  │ Why: Determines if 18 fields is          │                  │
│  │      "focused" or "overwhelming"         │                  │
│  │                                          │                  │
│  │ [Skip for Now] [Answer]                  │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
│  Frequency: 50% → 20% → 5% (decreases over time)               │
│  Max questions: 2 per review                                   │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│           COLLECT FEEDBACK (Optional)                           │
│                                                                 │
│  Step 5: Prompt User for Feedback                              │
│  ┌──────────────────────────────────────────┐                  │
│  │ 📊 Help This Reviewer Learn (10 sec)     │                  │
│  │                                          │                  │
│  │ How useful: ⭐️⭐️⭐️⭐️⭐️ [1-5]               │                  │
│  │                                          │                  │
│  │ Most helpful:                            │                  │
│  │ [✓] Specific issues                      │                  │
│  │ [✓] Actionable recommendations           │                  │
│  │ [ ] 5F scoring accuracy                  │                  │
│  │                                          │                  │
│  │ What did I miss?                         │                  │
│  │ "Didn't catch our 2FA requirement"       │                  │
│  │                                          │                  │
│  │ Score adjustments:                       │                  │
│  │ Fast: 7 → [8]   (User upgrades)          │                  │
│  │ Fair: 9 → [_]   (User keeps)             │                  │
│  │                                          │                  │
│  │ [Skip Feedback] [Submit]                 │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
│  User can: Skip, disable globally, answer partially            │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              LOG REVIEW SESSION                                 │
│                                                                 │
│  Step 6: Append to review-sessions.jsonl                       │
│  ┌──────────────────────────────────────────┐                  │
│  │ {                                        │                  │
│  │   "review_id": "uuid-1234",              │                  │
│  │   "timestamp": "2026-03-11T14:30:00Z",   │                  │
│  │   "design_type": "dashboard",            │                  │
│  │   "5f_scores_original": {                │                  │
│  │     "fast": 7, "focused": 6, ...         │                  │
│  │   },                                     │                  │
│  │   "feedback": {                          │                  │
│  │     "rating": 4,                         │                  │
│  │     "missed_context": "2FA mandatory",   │                  │
│  │     "score_overrides": {"fast": 8}       │                  │
│  │   },                                     │                  │
│  │   "context_learned": {                   │                  │
│  │     "user_persona": "business_managers"  │                  │
│  │   }                                      │                  │
│  │ }                                        │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│         IMMEDIATE HIGH-CONFIDENCE LEARNING                      │
│                                                                 │
│  Step 7: Process Instant Learnings                             │
│  ┌──────────────────────────────────────────┐                  │
│  │ IF context question answered:            │                  │
│  │   → Update context/user-personas.md NOW  │                  │
│  │   → Summarize in LEARNINGS.md            │                  │
│  │                                          │                  │
│  │ IF new business rule mentioned:          │                  │
│  │   → Add to active-hypotheses.md          │                  │
│  │   → Track for validation (needs 5+ more) │                  │
│  │                                          │                  │
│  │ IF score override pattern (5th time):    │                  │
│  │   → Flag for calibration in weekly cycle │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              USER SEES FINAL OUTPUT                             │
│                                                                 │
│  ┌──────────────────────────────────────────┐                  │
│  │ # 5F Design Review - Payment Dashboard  │                  │
│  │                                          │                  │
│  │ ## Scores                                │                  │
│  │ - Fast: 7/10 (2.5s - meets <3s target)  │                  │
│  │ - Focused: 6/10 (18 fields - high)      │                  │
│  │ - Fun: 8/10 (professional tone)          │                  │
│  │ - Fluent: 7/10 (clear flows)             │                  │
│  │ - Fair: 9/10 (transparent)               │                  │
│  │                                          │                  │
│  │ ## Issues                                │                  │
│  │ 1. Load time 2.5s (target <3s)           │                  │
│  │ 2. 18 data fields (high density)         │                  │
│  │ 3. ...                                   │                  │
│  │                                          │                  │
│  │ ---                                      │                  │
│  │ 🧪 Learning Mode (5%)                    │                  │
│  │ [Experimental observation]               │                  │
│  │                                          │                  │
│  │ ---                                      │                  │
│  │ ❓ Quick Context Question (optional)     │                  │
│  │ [Context question if triggered]          │                  │
│  │                                          │                  │
│  │ ---                                      │                  │
│  │ 📊 Feedback (optional)                   │                  │
│  │ [Feedback prompt]                        │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
│  User can: Read, engage with learning, skip entirely           │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ (Reviews accumulate over time)
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          WEEKLY LEARNING CYCLE (Sundays)                        │
│                                                                 │
│  Step 8: Automated Pattern Analysis (7-day window)             │
│                                                                 │
│  ┌─ Load Feedback ────────────────────────┐                    │
│  │ • review-sessions.jsonl (last 7 days)  │                    │
│  │ • 12 reviews this week                 │                    │
│  │ • 9 with feedback (75% response)       │                    │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Analyze Patterns ─────────────────────┐                    │
│  │ • Missed context: "2FA" mentioned 6x   │                    │
│  │ • Score overrides: Fast +1 (8 times)   │                    │
│  │ • Design patterns: Tables (9/10 reviews)│                   │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Identify High-Confidence ─────────────┐                    │
│  │ ✅ 2FA rule: 6 mentions → Add rule     │                    │
│  │ ✅ Fast calibration: 8 overrides (85%) │                    │
│  │    → Adjust threshold 3s → 2s          │                    │
│  │ ✅ Table pattern: 9/10 → Validate H001 │                    │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Update Memory Files ──────────────────┐                    │
│  │ • context/business-rules.md            │                    │
│  │   + "2FA mandatory for >₹50k"          │                    │
│  │                                        │                    │
│  │ • Scoring weights (invisible)          │                    │
│  │   Fast: 3s → 2s                        │                    │
│  │                                        │                    │
│  │ • context/design-system.md             │                    │
│  │   + "Table layouts standard"           │                    │
│  │                                        │                    │
│  │ • LEARNINGS.md (summary, <200 lines)   │                    │
│  │   Top 10 rules added                   │                    │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Validate Hypotheses ──────────────────┐                    │
│  │ • H001 (tables): 9/10 data points      │                    │
│  │   90% confidence → PROMOTE to rule ✅   │                    │
│  │                                        │                    │
│  │ • H003 (bottom sheets): 5/10 points    │                    │
│  │   50% confidence → Keep collecting     │                    │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Generate Report ──────────────────────┐                    │
│  │ Week: March 11-17, 2026                │                    │
│  │ • 12 reviews, 9 feedback (75%)         │                    │
│  │ • 1 new business rule                  │                    │
│  │ • 1 scoring calibration                │                    │
│  │ • 1 hypothesis validated               │                    │
│  │                                        │                    │
│  │ Saved to: improvement-tracker.md       │                    │
│  └────────────────────────────────────────┘                    │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Check for Major Changes ──────────────┐                    │
│  │ IF new_rules > 2 OR calibrations > 1:  │                    │
│  │   → Notify user:                       │                    │
│  │   "📚 5F reviewer learned new context" │                    │
│  │   "Review changes: /context-5f report" │                    │
│  └────────────────────────────────────────┘                    │
│                                                                 │
│  Duration: ~5-10 seconds                                       │
│  User impact: Minimal (background process)                     │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │
                       └────────────► LOOP BACK TO NEXT REVIEW
                                      (Now with improved context)


┌─────────────────────────────────────────────────────────────────┐
│                   NEXT REVIEW IS SMARTER                        │
│                                                                 │
│  Orchestrator loads updated context:                           │
│  ✅ Knows: 2FA is mandatory                                     │
│  ✅ Knows: Users are business managers                          │
│  ✅ Knows: Fast threshold is 2s (not 3s)                        │
│  ✅ Knows: Table layouts are standard pattern                   │
│                                                                 │
│  Review output is more accurate:                               │
│  • Fast: 8/10 (2.3s - meets YOUR <2s threshold) ← Calibrated   │
│  • Focused: 7/10 (appropriate for business managers) ← Context │
│  • Fair: 5/10 (❌ Missing 2FA - YOUR requirement) ← Learned rule│
│                                                                 │
│  Fewer questions (system has context):                         │
│  • Mode B trigger rate drops: 50% → 20% → 5%                   │
│  • Only asks about genuinely new uncertainties                 │
│                                                                 │
│  Better experimental observations:                             │
│  • Mode A now validates learned patterns instead of guessing   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mode C: Invisible Scoring Calibration

```
┌─────────────────────────────────────────────────────────────────┐
│           MODE C: SCORING CALIBRATION (Invisible)               │
│                                                                 │
│  Tracks user score overrides continuously                      │
│                                                                 │
│  Review #3:  User changes Fast 7→8 (load time 2.5s)            │
│  Review #7:  User changes Fast 7→8 (load time 2.3s)            │
│  Review #12: User changes Fast 6→8 (load time 2.4s)            │
│  Review #15: User keeps Fast 7      (load time 3.1s)            │
│  Review #18: User changes Fast 7→8 (load time 2.2s)            │
│  Review #21: User changes Fast 7→9 (load time 1.9s)            │
│  Review #24: User changes Fast 7→8 (load time 2.6s)            │
│  Review #28: User changes Fast 7→8 (load time 2.4s)            │
│  Review #31: User changes Fast 7→8 (load time 2.5s)            │
│                                                                 │
│  ┌─ Pattern Detection (Weekly Cycle) ──────────────────────┐   │
│  │ Total overrides: 8/9 reviews (89% consistency)          │   │
│  │ Average delta: +1.3 points                              │   │
│  │ Load times when overridden: 1.9s-2.6s (avg 2.4s)        │   │
│  │ Load time when kept: 3.1s                               │   │
│  │                                                          │   │
│  │ CONCLUSION: User's threshold is ~2s (not default 3s)    │   │
│  │ CONFIDENCE: 89% (high, exceeds 80% threshold)           │   │
│  │ DATA POINTS: 8 (exceeds 5 minimum)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Update Scoring Weights ──────────────────────────────┐     │
│  │ Fast dimension:                                        │     │
│  │ • OLD: <3s = excellent (8+)                            │     │
│  │ • NEW: <2s = excellent (8+)                            │     │
│  │                                                        │     │
│  │ Saved to: internal scoring weights (invisible file)   │     │
│  │ Logged to: improvement-tracker.md (transparent)        │     │
│  └──────────────────────────────────────────────────────────┘   │
│           │                                                     │
│           ▼                                                     │
│  ┌─ Next Review (Automatic Application) ────────────────┐      │
│  │ Design loads in 2.3s                                  │      │
│  │                                                       │      │
│  │ OLD scoring: Fast 7/10 (meets <3s target)             │      │
│  │ NEW scoring: Fast 8/10 (meets <2s target) ← Calibrated│      │
│  │                                                       │      │
│  │ No user override needed - system learned!            │      │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  User sees: More accurate scores automatically                 │
│  User impact: Zero (happens in background)                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## User Control Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER COMMANDS FLOW                           │
│                                                                 │
│  User wants to...                                              │
│                                                                 │
│  ┌─ View what was learned ────────────────────────────┐        │
│  │ Command: /context-5f                               │        │
│  │ Shows: All rules, personas, calibrations, patterns │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Fix wrong learning ────────────────────────────────┐       │
│  │ Command: /context-5f edit                           │       │
│  │ Opens: LEARNINGS.md for manual editing              │       │
│  │ User: Removes incorrect rule, saves                 │       │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Answer skipped questions ──────────────────────────┐       │
│  │ Command: /context-5f answer                         │       │
│  │ Shows: All pending questions from Mode B            │       │
│  │ User: Answers now (updates context immediately)     │       │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Review monthly progress ────────────────────────────┐      │
│  │ Command: /context-5f report                         │      │
│  │ Shows: What learned, scoring changes, hypotheses    │      │
│  │ User: Approves, reverts, or edits                   │      │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Force learning cycle now ──────────────────────────┐       │
│  │ Command: /context-5f analyze                        │       │
│  │ Runs: Weekly cycle immediately (don't wait Sunday)  │       │
│  │ Shows: What was learned from recent feedback        │       │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Start fresh ────────────────────────────────────────┐      │
│  │ Command: /context-5f reset                          │      │
│  │ Options: Full reset, keep rules, keep calibrations  │      │
│  │ Backup: Automatic to backups/ folder                │      │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ Disable learning ────────────────────────────────────┐     │
│  │ Command: export SKIP_5F_LEARNING=true               │     │
│  │ Effect: Skill runs normally, no learning layer      │     │
│  │ Reversible: Unset env var to re-enable              │     │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Original skill never modified** - Learning wraps around it
2. **Learning is optional** - User can skip/disable anytime
3. **Three modes work in parallel** - A (observations), B (questions), C (calibration)
4. **Weekly cycle is automatic** - Runs in background, non-blocking
5. **User has full control** - View, edit, reset, export, import
6. **Confidence-based** - Only learns from consistent patterns (5+ data points)
7. **Transparent** - All changes logged in improvement-tracker.md

**Result:** Skill gets smarter over time without user having to do anything special.
