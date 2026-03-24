# 5F Design Reviewer - Sub-Agents

**Version:** 2.0 (Hybrid Architecture)
**Created:** 2026-03-09

---

## Overview

This folder contains 3 specialized sub-agents that work together to provide comprehensive, evidence-backed design reviews.

**Why sub-agents?**
- **Reduced verbosity:** Parent skill compressed from 64KB → 8KB
- **Parallel execution:** Agents 2 & 3 can run simultaneously (faster reviews)
- **Reasoning isolation:** Each agent has fresh context, avoiding anchoring bias
- **Clear boundaries:** Each agent has one job, does it well

---

## Architecture

```
PARENT AGENT (8KB)
├── Soni persona & mood
├── 6 clarifying questions
├── Figma integration
└── Orchestration logic
     │
     ├─→ AGENT 1: 5F Reviewer (15KB)
     │   └─→ Returns: Scores, observations, gaps, recs (~3KB)
     │
     ├─→ AGENT 2: Prioritizer (12KB)
     │   └─→ Returns: Quick wins, strategic bets, summary (~2KB)
     │
     └─→ AGENT 3: Story Generator (10KB)
         └─→ Returns: User stories, research gaps (~2KB)
```

**Total context:** ~45KB (well under 50KB limit)
**Total output:** ~7KB (problem-focused, scannable)

---

## The 3 Sub-Agents

### 1. 5F Reviewer (`5f-reviewer.md`)

**Purpose:** Analyze design using 5F Framework
**Size:** 15KB skill, 3KB output
**Tools:** None needed

**Does:**
- Scores all 5 principles (1-5)
- Provides 2-3 observations per principle
- Flags critical gaps (scores ≤2)
- Generates 7-10 raw recommendations
- Identifies 3-5 strengths

**Returns:**
```json
{
  "scores": {"fast": 3, "focused": 4, "fun": 2, "fluent": 3, "fair": 4},
  "observations": {...},
  "critical_gaps": [...],
  "raw_recommendations": [...],
  "strengths": [...]
}
```

---

### 2. Prioritizer & Strategist (`prioritizer-strategist.md`)

**Purpose:** Prioritize recommendations, create action plan
**Size:** 12KB skill, 2KB output
**Tools:** None needed

**Does:**
- Applies RICE framework (Reach × Impact × Confidence / Effort)
- Impact is UX-focused (how much does this improve user experience?)
- Categorizes into Quick Wins / Strategic Bets / Backlog
- Creates 60-second executive summary
- Generates 4-6 brainstorming prompts
- Quantifies UX impact first, then business metrics

**Returns:**
```json
{
  "quick_wins": [...],
  "strategic_bets": [...],
  "backlog": [...],
  "executive_summary": {...},
  "brainstorm_prompts": [...],
  "impact_analysis": {...}
}
```

---

### 3. Story Generator (`story-generator.md`)

**Purpose:** Create evidence-backed user stories
**Size:** 10KB skill, 2KB output
**Tools:** HeyMarvin MCP (required)

**Does:**
- Searches HeyMarvin for behavioral evidence
- Creates user stories ONLY when evidence exists
- Flags research gaps explicitly
- Rates confidence (High/Medium/Low)
- Applies Mom Test framework (no opinions)

**Returns:**
```json
{
  "user_stories": [...],
  "research_gaps": [...],
  "validation_summary": {...},
  "heymarvin_searches_performed": [...]
}
```

**Critical rule:** NO FABRICATION. If no research exists, flag as gap.

---

## Workflow

### Sequential Execution

```
1. PARENT: Introduce + questions + fetch design
2. AGENT 1: Analyze with 5F Framework → wait for response
3. AGENT 2: Prioritize Agent 1's recs → wait for response
4. AGENT 3: Find evidence for gaps → wait for response
5. PARENT: Assemble final output + mood commentary
```

**Time:** ~2-3 minutes total

### Parallel Optimization (Advanced)

```
1. PARENT: Introduce + questions + fetch design
2. AGENT 1: Analyze with 5F Framework → wait
3. LAUNCH PARALLEL:
   - AGENT 2: Prioritize (needs Agent 1 output)
   - AGENT 3: Find evidence (needs Agent 1 gaps)
4. PARENT: Assemble when both complete
```

**Time:** ~1.5-2 minutes (40% faster)

---

## Output Format

### Problem-Focused Template

```markdown
# 5F Design Review: [Product]

## 📊 At a Glance
[Agent 1 scores + Agent 2 summary in table]

## 🚨 Top 3 Problems
[Agent 2 quick wins - top 3]
- Problem + Evidence (Agent 3) + Fix + Effort

## ✅ What's Working
[Agent 1 strengths]

## 🎯 Action Plan
### Quick Wins (This Sprint)
[Agent 2: RICE Score ≥ 8.0]

### Strategic Bets (This Quarter)
[Agent 2: RICE Score 3.0 - 7.9]

### Backlog
[Agent 2: RICE Score < 3.0]

## 💡 Brainstorming
[Agent 2: 4-6 "What if..." prompts]

## 📖 User Stories (Evidence-Backed)
[Agent 3: Stories with quotes + sources]

### Research Gaps
[Agent 3: What we don't know]

## 🎭 Soni's Take
[Parent: Mood-specific commentary]

## 📈 What If We Ship?
[Agent 2: Impact analysis]
```

**Key improvements over v1:**
- Lead with problems, not framework
- Scannable in 60 seconds
- Evidence inline (not separate section)
- Action-oriented (effort estimates)
- Progressive disclosure (details on request)

---

## RICE Framework (User Experience-Centered)

Used by Agent 2 to prioritize:

**Formula:** RICE Score = (Reach × Impact × Confidence) / Effort

**Categorization:**
```
RICE ≥ 8.0    → Quick Wins (Ship this sprint)
RICE 3.0-7.9  → Strategic Bets (Plan this quarter)
RICE < 3.0    → Backlog (Future/validate first)
```

**Components:**
- **Reach (1-10):** How many users affected?
- **Impact (1-5):** How much UX improvement per user? (**USER EXPERIENCE FOCUSED**)
- **Confidence (0.0-1.0):** How certain are we? (research-backed = high)
- **Effort (1-5):** How much eng work?

**Critical Principle:** Impact is ALWAYS about user experience improvement, not business metrics. Ask "How much does this improve the user's experience?"

---

## Token Management

### Budget Breakdown

| Component | Size | Notes |
|-----------|------|-------|
| Agent 1 skill | 15KB | Loaded once per review |
| Agent 2 skill | 12KB | Loaded once per review |
| Agent 3 skill | 10KB | Loaded once per review |
| Agent 1 output | ~3KB | JSON response |
| Agent 2 output | ~2KB | JSON response |
| Agent 3 output | ~2KB | JSON response |
| Parent context | ~15KB | Images, questions, assembly |
| **TOTAL** | **~59KB** | Safe under 100KB limit |

### If Approaching Limits

1. Compress Agent 1 observations (2 per principle)
2. Reduce Agent 2 brainstorms (4 instead of 6)
3. Reduce Agent 3 user stories (2 instead of 4)

---

## Error Handling

### If Agent 1 fails
→ Parent does 5F analysis directly (verbose mode)

### If Agent 2 fails
→ Show Agent 1's raw recommendations without prioritization

### If Agent 3 fails (HeyMarvin unavailable)
→ Flag all as research gaps, recommend user testing

### If all fail
→ Original verbose review mode

---

## Key Principles

### 1. Pattern-Based, Not Prescriptive
❌ "Does it have WhatsApp integration?"
✅ "Does it integrate with tools users already use?"

### 2. Evidence-Backed
- Agent 3 searches HeyMarvin for behavioral evidence
- If no evidence → Flag as research gap
- NEVER fabricate user stories

### 3. Problem-First
- Lead with what's broken, not framework scores
- Show top 3 problems immediately
- Scores available on request

### 4. Actionable
- Every problem has fix + RICE score
- Prioritized by RICE framework (UX-centered)
- Clear next steps

### 5. Scannable
- 60-second executive summary
- Visual hierarchy (emoji, tables, bullets)
- Progressive disclosure

---

## Files in This Directory

| File | Purpose | Size |
|------|---------|------|
| `5f-reviewer.md` | Agent 1: 5F Framework analysis | 15KB |
| `prioritizer-strategist.md` | Agent 2: Prioritization + summary | 12KB |
| `story-generator.md` | Agent 3: Evidence-backed stories | 10KB |
| `ORCHESTRATION-GUIDE.md` | How parent coordinates agents | 13KB |
| `README.md` | This file - Overview | 3KB |

---

## Version History

**v2.0 (2026-03-09)**
- Introduced sub-agent architecture
- Reduced parent skill from 64KB → 8KB
- Added RICE framework prioritization (UX-centered)
- Added HeyMarvin evidence validation
- Output format changed to problem-first

**v1.0**
- Original monolithic skill (64KB)
- Framework-first output
- No prioritization
- No evidence validation

---

## Next Steps

To use this architecture:
1. Read `ORCHESTRATION-GUIDE.md` for parent agent instructions
2. Each sub-agent file is self-contained - load when needed
3. Follow sequential workflow (or parallel for speed)
4. Assemble output using template in ORCHESTRATION-GUIDE

**Ready to ship!** 🚀
