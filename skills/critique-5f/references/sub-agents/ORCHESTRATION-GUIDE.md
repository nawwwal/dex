# Sub-Agent Orchestration Guide

**For:** Parent Agent (Main SKILL.md)
**Purpose:** How to coordinate the 3 sub-agents for optimal design reviews

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ PARENT AGENT                                                     │
│ • Soni persona & mood                                           │
│ • 6 clarifying questions                                         │
│ • Figma integration                                             │
│ • Sub-agent orchestration                                       │
│ • Final output assembly                                          │
└─────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌──────────────────┐
│  AGENT 1      │  │   AGENT 2      │  │   AGENT 3        │
│  5F Reviewer  │  │  Prioritizer   │  │ Story Generator  │
│               │  │  & Strategist  │  │                  │
│  ~3KB output  │  │  ~2KB output   │  │  ~2KB output     │
│  ~15KB skill  │  │  ~12KB skill   │  │  ~10KB skill     │
└───────────────┘  └────────────────┘  └──────────────────┘
```

**Total context:** ~37KB skills + ~7KB outputs = ~44KB (well under 50KB limit)

---

## Workflow (Sequential)

### Phase 1: Setup (Parent)
```
1. Introduce as Soni
2. Offer mood selection (Strategic/Creative/Critical/Empathetic)
3. Ask 6 clarifying questions
4. Fetch Figma design (if URL provided) or analyze uploaded images
```

### Phase 2: Analysis (Agent 1)
```
5. Launch Agent 1: 5F Reviewer

   Input:
   - Design images
   - User context (from 6 questions)
   - Selected mood

   Wait for response (~3KB):
   - 5F scores
   - Observations per principle
   - Critical gaps
   - Raw recommendations
   - Strengths
```

### Phase 3: Prioritization (Agent 2)
```
6. Launch Agent 2: Prioritizer & Strategist

   Input:
   - Agent 1's complete output
   - User context

   Wait for response (~2KB):
   - Quick wins (RICE framework)
   - Strategic bets
   - Backlog items
   - 60-second executive summary
   - Brainstorm prompts
   - Impact analysis
```

### Phase 4: Evidence Validation (Agent 3)
```
7. Launch Agent 3: Story Generator

   Input:
   - Agent 1's critical gaps
   - User context

   Wait for response (~2KB):
   - User stories (evidence-backed)
   - Research gaps
   - Validation summary
   - HeyMarvin search log
```

### Phase 5: Assembly (Parent)
```
8. Combine all outputs into final review
9. Add mood-specific commentary (Strategic/Creative/Critical)
10. Format output using template
11. Offer Round 2 for edge cases
```

---

## Agent 1 Launch: 5F Reviewer

### When to Launch
Right after fetching design and collecting user context.

### Input Preparation
```json
{
  "design_images": [/* Figma screenshots or uploaded images */],
  "user_context": {
    "target_user": "CFO at Indian SME using Razorpay",
    "jtbd": "Generate financial reports for tax filing",
    "product_context": "Razorpay Reports Dashboard",
    "design_stage": "Final UI",
    "market": "Indian B2B SaaS"
  },
  "mood": "Strategic"
}
```

### Expected Output (~3KB)
```json
{
  "scores": {
    "fast": 3, "focused": 4, "fun": 2, "fluent": 3, "fair": 4
  },
  "observations": {
    "fast": ["✅ ...", "❌ ...", "⚠️ ..."],
    /* ... per principle */
  },
  "critical_gaps": [
    "F1 (Fast): No loading feedback",
    "F3 (Fun): No dopamine hits"
  ],
  "raw_recommendations": [
    "Add loading skeleton",
    "Integrate workflow tools",
    /* ... 7-10 items */
  ],
  "strengths": [
    "Strong info hierarchy",
    "AI transparency"
  ]
}
```

### What to Do with Output
- Store for Agent 2 input
- Store for Agent 3 input
- Use scores for final scorecard
- Use strengths for "What's Working" section

---

## Agent 2 Launch: Prioritizer & Strategist

### When to Launch
Immediately after Agent 1 completes.

### Input Preparation
```json
{
  "agent1_output": {/* Full Agent 1 response */},
  "user_context": {/* Same as Agent 1 */}
}
```

### Expected Output (~2KB)
```json
{
  "quick_wins": [
    {
      "recommendation": "Add loading skeleton",
      "impact": 4,
      "effort": 2,
      "business_impact": "Fixes 23% abandonment, 2h eng",
      "f_principle": "F1: Fast",
      "why_quick_win": "High impact, low effort"
    }
  ],
  "strategic_bets": [/* ... */],
  "backlog": [/* ... */],
  "executive_summary": {
    "what_we_reviewed": "...",
    "overall_score": "3.2/5",
    "status": "Ready with fixes",
    "top_strength": "...",
    "critical_gap": "...",
    "top_quick_win": "...",
    "top_strategic_bet": "...",
    "recommended_action": "..."
  },
  "brainstorm_prompts": [
    "What if...",
    "Could we...",
    /* ... 4-6 items */
  ],
  "impact_analysis": {
    "if_quick_wins_shipped": "3.2/5 → 4.1/5",
    "if_all_shipped": "3.2/5 → 4.8/5",
    "key_metrics_improved": [/* ... */]
  }
}
```

### What to Do with Output
- Use for "Prioritized Recommendations" section
- Use executive_summary for top of output
- Use brainstorm_prompts for "Ideas" section
- Use impact_analysis for "What If We Ship" section

---

## Agent 3 Launch: Story Generator

### When to Launch
Immediately after Agent 2 completes (or in parallel with Agent 2 if you want speed).

### Input Preparation
```json
{
  "critical_gaps": [
    "F1 (Fast): No loading feedback",
    "F3 (Fun): No dopamine hits"
  ],
  "raw_recommendations": [/* From Agent 1 */],
  "user_context": {/* Same as Agent 1 */}
}
```

### Expected Output (~2KB)
```json
{
  "user_stories": [
    {
      "story": "As a merchant, I want...",
      "evidence_type": "behavioral",
      "quote": "I uploaded 3 times because...",
      "source": "HeyMarvin - Study Q4'25 - P007",
      "confidence": "High",
      "related_gap": "F1 (Fast): No loading feedback",
      "validates_assumption": "..."
    }
  ],
  "research_gaps": [
    {
      "gap": "No research on gamification",
      "related_to": "F3 (Fun)",
      "impact": "Cannot validate...",
      "recommendation": "Run 5-8 interviews..."
    }
  ],
  "validation_summary": {
    "stories_created": 2,
    "research_backed": 2,
    "coverage": "50%"
  },
  "heymarvin_searches_performed": [/* ... */]
}
```

### What to Do with Output
- Use user_stories for "User Stories" section
- Use research_gaps for "Research Gaps" section
- Use validation_summary to show evidence coverage
- Display search log for transparency

---

## Final Output Assembly

### Template Structure

```markdown
# 5F Design Review: [Product Name]
*Reviewed by Saurabh Soni | [Mood] Mode*

---

## 📊 At a Glance
[Use Agent 1 scores + Agent 2 executive summary]

| Principle | Score | Status |
|-----------|-------|--------|
| ⚡ Fast | 3/5 | ❌ Critical gap |
| 🎯 Focused | 4/5 | ✅ Strong |
| 🎨 Fun | 2/5 | ❌ Critical gap |
| 🔄 Fluent | 3/5 | ⚠️ Needs work |
| ⚖️ Fair | 4/5 | ✅ Strong |

**Overall:** 3.2/5 — Ready with fixes

---

## 🚨 Top 3 Problems to Fix
[Use Agent 2 quick wins - show top 3]

### 1. [Problem title]
**Impact:** [Agent 2 business_impact]
**Evidence:** [Agent 3 quote if available]
**Fix:** [Agent 2 recommendation]
**Effort:** [Agent 2 effort estimate]

---

## ✅ What's Already Working
[Use Agent 1 strengths]

- **[Strength 1]** - [F-principle]
- **[Strength 2]** - [F-principle]

---

## 🎯 Action Plan
[Use Agent 2 prioritization]

### Quick Wins (This Sprint)
1. **[Rec]** - RICE: X.X
   UX impact: [How UX improves] | Business impact: [Metric]

### This Quarter (Strategic Bets)
1. **[Rec]** - RICE: X.X
   UX impact: [How UX improves] | Business impact: [Metric]

### Backlog
1. **[Rec]** - RICE: X.X (Low confidence or reach)

---

## 💡 Brainstorming Ideas
[Use Agent 2 brainstorm prompts]

💡 What if we...
💡 Could we...
💡 How might we...

---

## 📖 User Stories (Evidence-Backed)
[Use Agent 3 user stories]

### High Confidence Stories
1. **As a [user], I want [capability], so [outcome]**
   - Evidence: "[Quote]" - [Source]
   - Validates: [Gap]

### Research Gaps Identified
[Use Agent 3 research gaps]

⚠️ **No research found on:** [Topic]
- **Impact:** Cannot validate [assumption]
- **Recommendation:** [Specific research method]

**Coverage:** [X%] of gaps backed by research

---

## 🎭 Soni's Take
[Add mood-specific commentary based on selected mood]

**Strategic Soni:** "Focus and Fair are strong, but Fun is your differentiator..."

**Creative Visionary:** "Imagine if this dashboard felt like a conversation..."

**Critical Analyst:** "You're assuming users want automation, but where's the evidence?"

---

## 📈 What If We Ship?
[Use Agent 2 impact analysis]

**If quick wins shipped:** 3.2/5 → 4.1/5 (+0.9 points)
**If all shipped:** 3.2/5 → 4.8/5 (+1.6 points)

**Key metrics:**
- Onboarding completion: +15%
- Time-to-first-action: 4min → 1min
- Abandonment: -23%

---

**Want Round 2?** I can review edge cases, mobile experience, or error states.
```

---

## Mood-Specific Commentary Guide

After assembling the main output, add Soni's perspective:

### Strategic Soni
- Connect design to business metrics
- Reference industry benchmarks
- Focus on competitive advantage
- Balanced tone

**Template:**
"[Strength analysis]. But [critical gap] is killing [metric]. Look at [competitor] - they proved [pattern] drives [outcome]. Fix [gap] this quarter."

### Creative Visionary
- Bold, industry-first ideas
- Reference research (DARPA XAI, Duolingo, Intercom)
- Challenge conventions
- Inspiring tone

**Template:**
"Imagine if [bold vision]. [Competitor] did this with [feature] and achieved [outcome]. Don't just fix [gap] - transform it into [competitive moat]."

### Critical Analyst
- Challenge assumptions
- Demand evidence
- Flag validation needs
- Skeptical tone

**Template:**
"You're assuming [assumption], but where's the evidence? [Agent 3 research gap]. Before building [feature], validate if users even want it."

### Empathetic Coach
- Supportive, growth-oriented
- Celebrate progress
- Gentle on gaps
- Encouraging tone

**Template:**
"You've built something genuinely innovative with [strength]. The [gap] is holding you back, but it's fixable. Start with [quick win] - you'll see results immediately."

---

## Error Handling

### If Agent 1 Fails
- Fall back to parent doing 5F analysis directly
- Skip Agent 2 and Agent 3
- Note in output: "Simplified review (sub-agent unavailable)"

### If Agent 2 Fails
- Use Agent 1's raw recommendations without prioritization
- Manually create basic executive summary
- Skip impact analysis

### If Agent 3 Fails (HeyMarvin MCP unavailable)
- Flag all critical gaps as "Research gaps - HeyMarvin unavailable"
- Recommend user testing without specific stories
- Note in output: "Evidence validation unavailable"

### If All Sub-Agents Fail
- Parent performs full analysis (original verbose mode)
- Note: "Full review mode (sub-agents unavailable)"

---

## Optimization Tips

### For Speed
- Launch Agent 2 and Agent 3 in PARALLEL after Agent 1
  - Agent 2 needs Agent 1's output
  - Agent 3 needs Agent 1's critical_gaps
  - They don't depend on each other
  - Saves ~30 seconds

### For Cost
- Use Haiku for Agent 2 and Agent 3 (simple tasks)
- Use Sonnet for Agent 1 (complex 5F analysis)

### For Quality
- Always run all 3 agents (don't skip)
- Validate Agent outputs match expected format
- If output is malformed, retry once before failing

---

## Token Management

**Budget per review:**
- Sub-agent skills: 37KB (loaded once)
- Sub-agent outputs: 7KB (3KB + 2KB + 2KB)
- Parent context: ~15KB (images, questions, assembly)
- **Total: ~59KB** (safe margin under 100KB limit)

**If approaching limits:**
1. Compress Agent 1 observations (2 per principle instead of 3)
2. Reduce Agent 2 brainstorms (4 instead of 6)
3. Reduce Agent 3 user stories (2 instead of 4)

---

## Success Criteria

A well-orchestrated review has:
- ✅ All 3 agents ran successfully
- ✅ Scores from Agent 1
- ✅ Prioritization from Agent 2
- ✅ Evidence from Agent 3 (or explicit research gaps)
- ✅ Mood-specific commentary
- ✅ Scannable in 60 seconds
- ✅ Actionable recommendations
- ✅ Business impact quantified
- ✅ Under 10KB final output

---

## Quick Reference

| What | Who Does It | When |
|------|-------------|------|
| Soni intro + questions | Parent | Phase 1 |
| Fetch Figma | Parent | Phase 1 |
| 5F analysis + scoring | Agent 1 | Phase 2 |
| Prioritization + summary | Agent 2 | Phase 3 |
| User stories + evidence | Agent 3 | Phase 4 |
| Mood commentary | Parent | Phase 5 |
| Final assembly | Parent | Phase 5 |

---

**Ready to orchestrate!** Follow the workflow, trust the agents, assemble the output. 🚀
