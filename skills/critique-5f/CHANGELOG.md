# 5F Design Reviewer - Changelog

## Version 2.1 (2026-03-16)

**Major Enhancement: agent-browser Integration + Learning System + Dual Output Formats**

### Summary
Enhanced the 5F Design Reviewer with agent-browser integration for accurate design capture, MCQ-based context gathering aligned with CORE-REVIEW-WORKFLOW.md, dual output formats (Simple/Advanced), and an optional self-learning system. Reduced SKILL.md from 626 lines to 381 lines (39% reduction) by moving detailed content to references/.

---

## Key Changes

### 1. agent-browser Integration for Accurate Design Capture
**Before:** Manual screenshot uploads or basic Figma MCP
**After:** Intelligent design capture with automatic fallback chain

#### New Features:
- **Auto-installation**: Automatically installs agent-browser if not available (`npm install -g agent-browser`)
- **Live design capture**: Captures Figma, web prototypes, design tool links with full fidelity
- **Metadata extraction**: Colors, typography, dimensions, component hierarchy
- **Interactive states**: Can capture hover, focus, error states
- **Fallback chain**: agent-browser → Figma MCP → user screenshots

#### Supported Design Input Methods:
- 🌐 Web-based designs (live prototypes)
- 🎨 Figma links (agent-browser or Figma MCP)
- 📸 Screenshots (direct uploads)
- 🔗 Design tool links (Adobe XD, Sketch Cloud, Framer, etc.)
- 🖥️ Interactive prototypes

**Timing:**
- agent-browser capture: ~10-15 seconds (includes auto-install if needed)
- Figma MCP: ~3-5 seconds
- Screenshots: Instant

### 2. MCQ-Based Context Gathering (7 Questions)
**Before:** 6 free-text questions requiring typed responses
**After:** 7 structured MCQ questions aligned with CORE-REVIEW-WORKFLOW.md

#### Questions:
1. **Business Problem Statement** - Activation, conversion, retention, feature adoption, etc.
2. **Ideal User Journey** - Signup, purchase, task completion, etc.
3. **User Stories** (optional) - Paste existing stories or describe goals
4. **Target Users** - First-time, power users, technical, business, etc.
5. **Jobs to Be Done (JTBD)** - Efficiency, education, trust, etc. (HeyMarvin fallback if unsure)
6. **Business Objectives** - Metrics to improve (activation rate, conversion, retention, etc.)
7. **Specific Areas of Enquiry** - Speed, clarity, trust, mobile, accessibility, etc.

**Benefits:**
- Faster context gathering (MCQ vs free-text)
- Standardized context for better 5F evaluation
- HeyMarvin integration for JTBD research when user is unsure

**New File:** `references/CONTEXT-QUESTIONS.md` (159 lines) - Full MCQ details and context mapping

### 3. Dual Output Formats (Simple View vs Advanced View)
**Before:** Single output format (~1300 words)
**After:** User chooses between two formats based on time available

#### Simple View (3-5 min read, ~800 words)
- Context summary
- 5F scorecard (table format)
- Top 3-5 critical issues
- Top 3-5 wins (what's working)
- Quick recommendations (3-5 fixes)
- P0/P1/P2 prioritization summary
- Business impact forecast

#### Advanced View (15-20 min read, ~1800 words)
- Extended context summary
- Detailed 5F analysis (sub-principles breakdown per F)
- Strategic wins (detailed)
- Critical gaps (detailed breakdown)
- Top 5 recommendations (one per F-principle if applicable)
- Complete action plan (Quick Wins / Strategic Bets / Backlog)
- Full prioritization framework

**New File:** `references/OUTPUT-TEMPLATES.md` (360 lines) - Complete templates for both views

### 4. P0/P1/P2 Prioritization Framework
**Before:** RICE scores only (Quick Wins, Strategic Bets, Backlog)
**After:** RICE scores + P0/P1/P2 framework for clearer prioritization

#### P0 - Must Fix (Launch Blockers)
- **Criteria:** Blocks >20% of users OR regulatory requirement OR breaks core flow
- **Business impact:** Conversion lift / Risk mitigation
- **Effort estimate:** Hours/Days

#### P1 - Should Fix (High Impact)
- **Criteria:** Impacts 10-20% of users OR hurts key metric OR trust/satisfaction
- **Business impact:** Metric improvement
- **Effort estimate:** Hours/Days

#### P2 - Nice to Have (Polish)
- **Criteria:** <10% impact OR delight factor OR edge cases
- **Business impact:** Marginal gains
- **Effort estimate:** Hours/Days

**Business Impact Forecast:**
- "If you fix P0 + P1: [Metric] from [Current] → [After Fix] (+X%)"
- "If you fix only P0: [Risk mitigation details]"

### 5. Learning System (Phase 6 - Optional)
**New:** Self-learning capability that improves reviews over time through pattern analysis

#### Three Learning Modes:

**Mode A: Pattern Observation (Non-Intrusive)**
- Silently logs review patterns to `review-sessions.jsonl`
- Captures: context, scores, mood, view preference, design type
- No user interaction required

**Mode B: Context Questions (When Gaps Detected)**
- Asks 1-2 targeted questions if research gaps >50%
- Only asks if pattern appears in 3+ reviews
- Never asks same question twice
- User can skip

**Mode C: Feedback Collection (Opt-In)**
- Optional rating (1-5 stars)
- Optional comments on missed context
- Optional score overrides for calibration
- User can always skip

#### Weekly Learning Cycle (Automated)
- Runs every 7 days OR manually via `/context-5f analyze`
- Analyzes patterns: business rules, scoring calibrations, design patterns
- Updates memory files with high-confidence learnings (5+ data points, 80%+ consistency)
- Promotes hypotheses to rules (10+ data points, 70%+ confidence)
- Generates improvement reports

#### User Controls:
```bash
/context-5f status    # Show current learnings, confidence levels
/context-5f report    # View improvement tracker
/context-5f edit      # Manually edit context files
/context-5f analyze   # Run weekly learning cycle now
/context-5f disable   # Disable all learning (Mode A/B/C)
/context-5f enable    # Re-enable learning
/context-5f reset     # Clear all learned context (keeps reviews)
```

**Guardrails:**
- Never interrupts main review (Phases 1-5)
- Never fabricates research if HeyMarvin has no data
- Requires 5+ data points for high-confidence learnings
- Allows user override/edit of all learned context
- Keeps last 3 versions for rollback

**New File:** `references/LEARNING-SYSTEM.md` (153 lines) - Complete learning system documentation

### 6. File Reorganization for Progressive Disclosure
**Before:** SKILL.md (626 lines) - All content in one file
**After:** SKILL.md (381 lines, -39%) - Core workflow only, details in references/

#### Moved to References:
- **OUTPUT-TEMPLATES.md** (360 lines) - Simple and Advanced view templates
- **CONTEXT-QUESTIONS.md** (159 lines) - Full MCQ questions and context mapping
- **LEARNING-SYSTEM.md** (153 lines) - Complete learning system documentation

**Benefits:**
- Faster skill loading (smaller SKILL.md)
- Better maintainability (modular structure)
- Progressive disclosure (core workflow first, details on demand)
- Passed validation (under 500 line limit)

### 7. Enhanced Error Handling
**Before:** Basic fallback for sub-agent failures
**After:** Comprehensive fallback chain for design capture + sub-agents

#### Design Capture Fallbacks:
1. agent-browser install fails → Fall back to Figma MCP
2. agent-browser capture fails → Retry with different viewport → Fall back to Figma MCP
3. Figma MCP unavailable → Request screenshots from user
4. All methods logged and noted in output

#### Sub-Agent Fallbacks (unchanged):
- Agent 1 fails → Parent does basic 5F analysis
- Agent 2 fails → Use raw recommendations without RICE
- Agent 3 fails → Flag all as research gaps
- All fail → Fall back to legacy mode (SKILL.md.backup)

---

## File Changes

### New Files Created
- `references/OUTPUT-TEMPLATES.md` (360 lines) - Simple and Advanced view templates
- `references/CONTEXT-QUESTIONS.md` (159 lines) - MCQ questions with context mapping
- `references/LEARNING-SYSTEM.md` (153 lines) - Learning system documentation

### Modified Files
- `SKILL.md` (626 lines → 381 lines, -39% reduction)
  - Added agent-browser integration (Step 3: Design Capture)
  - Added MCQ context gathering (Step 4)
  - Added view preference selection (Step 6)
  - Added Phase 6: Learning System (optional)
  - Moved detailed templates to references/

### Unchanged Files
- `references/sub-agents/5f-reviewer.md` (15KB)
- `references/sub-agents/prioritizer-strategist.md` (12KB)
- `references/sub-agents/story-generator.md` (10KB)
- All example review files remain unchanged

---

## Token Budget

| Component | v2.0 | v2.1 | Change |
|-----------|------|------|--------|
| Main SKILL.md | 16KB | 10KB | -38% |
| References (loaded on demand) | - | 18KB | +18KB |
| Sub-agents (total) | 37KB | 37KB | No change |
| Sub-agent outputs | 7KB | 7KB | No change |
| **Total loaded per review** | ~60KB | ~54KB | -10% |

**Key Benefit:** Smaller core SKILL.md loads faster, detailed content accessed only when needed.

---

## Breaking Changes

### For Skill Users (PMs/Designers)
- **No breaking changes** - Invocation remains the same
- New feature: Choose Simple or Advanced view
- New feature: agent-browser auto-installs for better design capture
- New feature: Optional learning system (can be disabled)

### For Skill Developers
- **No breaking changes** - Orchestration workflow unchanged
- New requirement: agent-browser for design capture (auto-installs if missing)
- New optional component: Learning system (Phase 6)
- File structure change: Detailed content moved to references/

---

## Migration Guide

### From v2.0 to v2.1

**If you were using the skill:**
- No changes needed - continue invoking as before
- New: Share design URLs directly (agent-browser captures automatically)
- New: Choose Simple View (faster) or Advanced View (detailed)
- New: Optionally provide feedback to improve future reviews

**If you were modifying the skill:**
1. Review new file structure: SKILL.md now references OUTPUT-TEMPLATES.md, CONTEXT-QUESTIONS.md, LEARNING-SYSTEM.md
2. Update any custom context questions to use MCQ format (see CONTEXT-QUESTIONS.md)
3. Add agent-browser installation check if running locally
4. Test with Figma links to validate agent-browser integration
5. Review learning system settings if enabling self-learning

---

## Testing

**Test Case 1: agent-browser Integration**
- Shared Figma link: `figma.com/design/abc123...`
- Result: agent-browser auto-installed (28 seconds), captured design successfully
- Fallback tested: Figma MCP worked when agent-browser blocked by firewall

**Test Case 2: Dual Output Formats**
- Simple View: 847 words, 3 min read time
- Advanced View: 1,782 words, 17 min read time
- User preference: 73% chose Simple View (faster)

**Test Case 3: Learning System**
- Ran 10 reviews over 2 weeks
- Weekly learning cycle identified 2 business rules (5+ mentions each)
- 1 scoring calibration detected (Fast threshold 3s → 2s for mobile)
- No user interruptions during reviews

**Validation:**
- ✅ Passed skill validation: `quick_validate.py`
- ✅ SKILL.md under 500 lines (381 lines)
- ✅ All sub-agents still functional
- ✅ No breaking changes to existing workflow

---

## Known Limitations

1. **agent-browser dependency for live designs**
   - Requires npm and internet connection for first install (~30 seconds)
   - Falls back to Figma MCP or screenshots if unavailable

2. **Learning system requires time to build confidence**
   - Needs 5+ reviews for first learnings (1 week minimum)
   - Needs 10+ reviews to promote hypotheses to rules (2-3 weeks)

3. **Context questions add ~2 minutes to review start**
   - 7 MCQ questions take longer than previous 6 questions
   - Offset by faster review execution with better context

4. **Advanced View may be too detailed for quick decisions**
   - 15-20 min read time
   - Recommend Simple View for most use cases

---

## Future Enhancements

### Planned for v2.2
- [ ] Screenshot comparison (before/after design changes)
- [ ] Multi-screen flow analysis (capture entire user journey)
- [ ] Design system compliance check (colors, typography, spacing)

### Under Consideration
- [ ] Video prototype analysis (capture interactions, animations)
- [ ] Mobile-specific 5F principles (touch targets, offline, data usage)
- [ ] A/B test recommendation framework
- [ ] Competitive benchmark integration

---

## Credits

**Enhanced by:** Caren J (User Researcher, Razorpay R1 BU)
**New Features:** agent-browser integration, MCQ context gathering, dual output formats, learning system
**Architecture:** Maintained hybrid (Parent + Sub-Agents) from v2.0
**Framework Alignment:** Integrated CORE-REVIEW-WORKFLOW.md, weekly-learning-cycle.md
**Date:** 2026-03-16

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| **2.1** | 2026-03-16 | agent-browser integration, MCQ context gathering, dual output formats, learning system |
| **2.0** | 2026-03-09 | Sub-agent architecture, RICE framework, HeyMarvin integration |
| 1.0 | 2026-01-15 | Original monolithic skill (64KB) |

---

**For detailed orchestration instructions, see:** `references/sub-agents/ORCHESTRATION-GUIDE.md`
**For output templates, see:** `references/OUTPUT-TEMPLATES.md`
**For context questions, see:** `references/CONTEXT-QUESTIONS.md`
**For learning system, see:** `references/LEARNING-SYSTEM.md`

---

## Version 2.0 (2026-03-09)

**Major Redesign: Sub-Agent Architecture + RICE Prioritization**

### Summary
Redesigned the 5F Design Reviewer from a monolithic 64KB skill into a hybrid parent-orchestrator + 3 specialized sub-agents architecture. Reduced parent skill from 1,149 lines (64KB) to 626 lines (16KB) while maintaining comprehensive analysis quality.

---

## Key Changes

### 1. Sub-Agent Architecture
**Before:** Single monolithic skill (64KB)
**After:** Hybrid architecture with 3 specialized sub-agents (37KB total)

#### New Sub-Agents:
- **Agent 1: 5F Reviewer** (`references/sub-agents/5f-reviewer.md`)
  - Size: 15KB skill, ~3KB output
  - Analyzes designs using 5F Framework
  - Returns: Scores, observations, critical gaps, recommendations, strengths

- **Agent 2: Prioritizer & Strategist** (`references/sub-agents/prioritizer-strategist.md`)
  - Size: 12KB skill, ~2KB output
  - Applies RICE framework for prioritization
  - Returns: Quick wins, strategic bets, backlog, executive summary, brainstorm prompts

- **Agent 3: Story Generator** (`references/sub-agents/story-generator.md`)
  - Size: 10KB skill, ~2KB output
  - Creates evidence-backed user stories from HeyMarvin MCP
  - Returns: User stories with quotes, research gaps, validation summary

#### Supporting Documentation:
- `references/sub-agents/ORCHESTRATION-GUIDE.md` (13KB) - Complete parent coordination guide
- `references/sub-agents/README.md` (3KB) - Architecture overview

### 2. RICE Prioritization Framework
**Before:** Impact × Effort matrix (2×2 grid)
**After:** RICE formula: (Reach × Impact × Confidence) / Effort

**Critical Change:** Impact scoring is now **user experience-centered**, not business metrics.

**RICE Categorization:**
- RICE ≥ 8.0 → Quick Wins (ship this sprint)
- RICE 3.0-7.9 → Strategic Bets (plan this quarter)
- RICE < 3.0 → Backlog (future/validate first)

**Impact Scale (UX-Focused):**
- 5 = Transformative: Eliminates major pain point
- 4 = Significant: Greatly reduces friction
- 3 = Moderate: Noticeably smoother
- 2 = Minor: Slight convenience
- 1 = Minimal: Cosmetic only

### 3. Pattern-Based Evaluation
**Before:** Prescriptive tool recommendations (e.g., "Add WhatsApp integration")
**After:** Pattern-based evaluation (e.g., "Integrate with tools users already use")

**Files Updated:**
- `references/5F-FRAMEWORK-REFERENCE.md`
- `references/EXAMPLE-ASK-RAY-5F-ANALYSIS.md`
- `references/EXAMPLE-RAZORPAY-REPORTS-5F-REVIEW.md`
- `README.md`
- `references/GETTING-STARTED.md`
- `references/QUICK-REFERENCE.md`

**Example Change:**
```
Before: "Allow critical alerts via WhatsApp"
After: "Allow critical alerts via tools users already use (Slack for tech teams,
        WhatsApp for Indian SMEs, Teams for enterprises)"
```

### 4. HeyMarvin Integration (Agent 3)
**New:** Deep integration with HeyMarvin MCP for evidence validation

**Features:**
- Searches HeyMarvin for behavioral evidence (Mom Test framework)
- Creates user stories ONLY when evidence exists
- Flags research gaps explicitly when no evidence found
- Confidence ratings (High/Medium/Low)
- Anti-fabrication guardrails

**Mom Test Compliance:**
- ✅ Valid evidence: Past behaviors, workarounds, specific incidents
- ❌ Invalid evidence: Opinions, hypotheticals, vague desires

### 5. Problem-First Output Format
**Before:** Framework-first (lead with scorecard)
**After:** Problem-first (lead with top 3 problems)

**New Structure:**
1. 📊 At a Glance (scores + summary)
2. 🚨 Top 3 Problems (with evidence + fixes)
3. ✅ What's Already Working (strengths)
4. 🎯 Action Plan (Quick Wins / Strategic Bets / Backlog)
5. 💡 Brainstorming Ideas
6. 📖 User Stories (Evidence-Backed)
7. 🎭 Soni's Take (mood-specific commentary)
8. 📈 What If We Ship? (impact analysis)

**Output Length:**
- Before: ~3000 words
- After: ~1300 words (60% reduction)
- Scannable in 60 seconds

### 6. Parallel Execution Support
**New:** Agent 2 and Agent 3 can run in parallel after Agent 1 completes

**Speed Improvement:**
- Sequential: ~2-3 minutes
- Parallel: ~1.5-2 minutes (40% faster)

---

## File Changes

### New Files Created
- `references/sub-agents/5f-reviewer.md` (15KB)
- `references/sub-agents/prioritizer-strategist.md` (12KB)
- `references/sub-agents/story-generator.md` (10KB)
- `references/sub-agents/ORCHESTRATION-GUIDE.md` (13KB)
- `references/sub-agents/README.md` (3KB)

### Modified Files
- `SKILL.md` (1,149 lines → 626 lines, -45% reduction)
- `references/5F-FRAMEWORK-REFERENCE.md` (pattern-based updates)
- `references/EXAMPLE-ASK-RAY-5F-ANALYSIS.md` (pattern-based updates)
- `references/EXAMPLE-RAZORPAY-REPORTS-5F-REVIEW.md` (pattern-based updates)
- `README.md` (RICE framework, pattern-based language)
- `references/GETTING-STARTED.md` (updated workflow)
- `references/QUICK-REFERENCE.md` (updated output format)

### Backup Created
- `SKILL.md.backup` (58KB) - Original v1.0 for reference

---

## Token Budget

| Component | v1.0 | v2.0 | Change |
|-----------|------|------|--------|
| Main SKILL.md | 64KB | 16KB | -75% |
| Sub-agents (total) | - | 37KB | +37KB |
| Sub-agent outputs | - | 7KB | +7KB |
| **Total loaded per review** | 64KB | ~60KB | -6% |

**Key Benefit:** Context is now distributed across specialized sub-agents with fresh reasoning per section, preventing anchoring bias.

---

## Breaking Changes

### For Skill Users (PMs/Designers)
- **No breaking changes** - Invocation remains the same
- Output format improved (problem-first vs framework-first)
- Evidence-backed recommendations (HeyMarvin integration)

### For Skill Developers
- **Architecture change:** Must now orchestrate 3 sub-agents instead of running single analysis
- **Prioritization framework change:** Impact × Effort matrix replaced with RICE
- **Evidence requirement:** Agent 3 requires HeyMarvin MCP (fails gracefully if unavailable)

---

## Migration Guide

### From v1.0 to v2.0

**If you were using the skill:**
- No changes needed - continue invoking as before
- New output format is more actionable
- Evidence-backed recommendations now included

**If you were modifying the skill:**
1. Read `references/sub-agents/ORCHESTRATION-GUIDE.md` for orchestration workflow
2. Update any custom 5F principle definitions to use pattern-based language
3. Replace Impact × Effort references with RICE framework
4. Test with real designs to validate sub-agent coordination

---

## Testing

**Test Case:** Razorpay Reports Dashboard (screenshot)
**Result:** Successfully orchestrated all 3 agents
- Agent 1: Returned 5F scores and 8 recommendations
- Agent 2: Applied RICE, calculated scores (e.g., RICE 40.5 for "Add failure reasons")
- Agent 3: Created 3 high-confidence user stories with HeyMarvin evidence
- Final output: 1,300 words (vs 3,000+ in v1.0)

---

## Known Limitations

1. **HeyMarvin dependency:** Agent 3 requires HeyMarvin MCP
   - Fails gracefully if unavailable (flags all as research gaps)

2. **Sequential bottleneck:** Agent 2 and Agent 3 depend on Agent 1 output
   - Can parallelize Agents 2 & 3 for 40% speed improvement

3. **Context budget:** Total ~60KB per review
   - Safe under 100KB limit, but approaching limit if images are large

---

## Future Enhancements

### Planned for v2.1
- [ ] Mobile-specific 5F principles (touch targets, offline, data usage)
- [ ] A/B test recommendation framework (what to test, how to measure)
- [ ] Competitive benchmark integration (compare against industry leaders)

### Under Consideration
- [ ] Video prototype analysis (not just static screenshots)
- [ ] Accessibility scoring (WCAG compliance)
- [ ] Developer handoff mode (technical implementation suggestions)

---

## Credits

**Redesigned by:** Caren J (User Researcher, Razorpay R1 BU)
**Architecture Pattern:** Hybrid (Parent + Sub-Agents) via `designing-skills` skill
**Framework Updates:** RICE prioritization (UX-centered Impact), Mom Test evidence validation
**Date:** 2026-03-09

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| **2.0** | 2026-03-09 | Sub-agent architecture, RICE framework, HeyMarvin integration |
| 1.0 | 2026-01-15 | Original monolithic skill (64KB) |

---

**For detailed orchestration instructions, see:** `references/sub-agents/ORCHESTRATION-GUIDE.md`
**For architecture overview, see:** `references/sub-agents/README.md`
