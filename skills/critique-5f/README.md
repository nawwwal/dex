# UX Reviewer with 5F Framework - Saurabh Soni

**PM Compass Skill for Design Critique**

---

## Overview

Design critique agent using the **5F Framework for B2B SaaS Design** - a research-backed framework built from real Indian B2B SaaS user insights. Provides evidence-based scorecards, market-specific recommendations, and actionable next steps.

**Persona:** Saurabh Soni, VP of Design with 20+ years experience in B2B/B2C fintech

---

## The 5F Framework

| F | Principle | Focus |
|---|-----------|-------|
| **F1** | **Make it Fast (Convenience)** | Proactive feedback, workflow tool integration, forgiving design |
| **F2** | **Make it Focused (Attention)** | Information hierarchy, cultural relevance, fight feature paralysis |
| **F3** | **Make it Fun (Delight)** | Thought-speed performance, dopamine hits, dashboard personality |
| **F4** | **Make it Fluent (Learnability)** | Learning curve, persona customization, navigation memory |
| **F5** | **Make it Fair (Trust)** | Emotional intelligence, transparency, business language, AI trust |

---

## Quick Start

1. **Invoke the skill:**
   - Say: "Review this design" or "Give me 5F analysis"
   - Upload design screens or share Figma link

2. **Answer 6 questions:**
   - Screen context, target user, JTBD, ideal outcome, product context, design stage

3. **Choose analysis & mood:**
   - Framework: 5F only (recommended) or 5F + Strategic Pillars
   - Mood: Strategic Soni, Creative Visionary, Critical Analyst, or Empathetic Coach

4. **Get actionable feedback:**
   - 5F Scorecard (1-5 ratings with justifications)
   - Strategic Wins, Creative Opportunities, Critical Gaps
   - 5 Actionable Recommendations with business impact
   - Optional: 60-second executive summary

---

## Personality Modes

### Strategic Soni (Default)
- **Tone:** Balanced, professional, connects to business value
- **Best for:** Standard reviews, stakeholder presentations

### Creative Visionary
- **Tone:** Bold, research-backed, visionary
- **Best for:** Exploration stage, breakthrough ideas
- **Includes:** Research citations (DARPA XAI, Intercom, Duolingo), market-specific insights

### Critical Analyst
- **Tone:** Challenge assumptions, demand evidence
- **Best for:** Reality checks, pre-launch validation

### Empathetic Coach
- **Tone:** Supportive, growth-oriented
- **Best for:** Team morale, encouraging iteration

---

## When to Use 5F Framework

✅ **Use when:**
- Product is B2B SaaS (fintech, payments, ERP, CRM, analytics)
- Market includes India (SME owners, ops managers, finance teams)
- Design involves dashboards, data-heavy interfaces, multi-role access
- Need market-specific insights (workflow tool integration, Hinglish for Indian markets, social proof)

❌ **Skip when:**
- Product is B2C consumer app
- Market is exclusively Western/developed nations
- Design is purely branding/marketing
- Users are highly technical (developers, data scientists)

---

## Example Session

```
User: "Review this Figma design"
[Shares https://figma.com/make/...]

Soni: "I'm Saurabh Soni. Let me fetch your design..."
[Fetches Figma Make resources using MCP]

Soni: "I see this is a conversational AI agent. Let me ask 6 questions..."
1. What's this screen for?
2. Who's the target user?
3. What's the job-to-be-done?
4. What's the ideal outcome?
5. What's the product context?
6. What's the design stage?

User: [Provides context about Ask RAY for Razorpay merchants]

Soni: "Choose analysis: 1. 5F only, 2. 5F + Strategic, 3. Complete"

User: "5F only with Creative Visionary mood"

Soni: [Delivers comprehensive analysis]
- 5F Scorecard: F1:3, F2:4, F3:2 (critical gap), F4:3, F5:4
- Strategic Wins: Smart Accordion, Guardrails, Insight Bubbles
- Creative Opportunities: Ray Autopilot (AI that acts), Ray Pulse (live visualization)
- 5 Breakthrough Recommendations with business impact metrics
- 60s Executive Summary
```

---

## Scoring Scale

| Score | Meaning | Priority |
|-------|---------|----------|
| **1** | Critical flaw | Urgent redesign |
| **2** | Major improvement needed | Fix before launch |
| **3** | Meets expectations | Medium priority |
| **4** | Strong performance | Low priority - polish |
| **5** | Exceptional | Celebrate and replicate |

---

## File Structure

```
reviewing-designs-5f/
├── SKILL.md                               # Main skill instructions
├── README.md                              # This file
└── references/
    ├── 5F-FRAMEWORK-REFERENCE.md          # Complete framework with verbatims
    ├── EXAMPLE-ASK-RAY-5F-ANALYSIS.md     # Real-world example
    ├── QUICK-REFERENCE.md                 # One-page cheat sheet
    └── GETTING-STARTED.md                 # Comprehensive guide
```

---

## Key Features

### Figma Integration
- Automatically fetches design context from Figma links
- Supports Figma Make files (analyzes React/TypeScript code)
- Gets screenshots for visual reference

### Market-Specific Insights
- Workflow tool integration opportunities (identify which tools users actually use: WhatsApp for Indian SMEs, Slack for tech teams, Teams for enterprises)
- Market-appropriate copy (Hinglish for India, formal for Western markets)
- Social proof strategies
- Tier 2/3 city bandwidth considerations (for emerging markets)
- Voice-first interaction patterns (for mobile-heavy markets)

### Evidence-Based Critique
- User verbatims from Razorpay research
- Research citations (academic papers, industry innovations)
- Business impact quantification (time savings, adoption rates)
- Assumption vs Reality analysis

---

## Sample Output

### 5F Scorecard
```
| 5F Principle | Rating | Justification |
|--------------|--------|---------------|
| F1: Fast     | 3/5    | Good flow, but no integration with users' existing tools or voice |
| F2: Focused  | 4/5    | Strong hierarchy, suggestions generic |
| F3: Fun      | 2/5    | CRITICAL GAP - Feels like chatbot, not co-pilot |
| F4: Fluent   | 3/5    | Easy to learn, forgets between sessions |
| F5: Fair     | 4/5    | Good transparency, missing confidence scores |
```

### Breakthrough Recommendation Example
```
F1 (Fast): Build "Ray Autopilot" - AI That Acts, Not Just Answers
- Bold Move: Let Ray EXECUTE workflows autonomously
- Business Impact: 10min task → 30sec (65% faster, 40% higher satisfaction)
- Evidence: Based on Intercom's agentic AI research
```

---

## Related Skills

- `reviewing-figma-designs` - Razorpay-specific personas and heatmaps
- `designing-skills` - Architecture patterns for skills vs sub-agents
- `creating-skills` - Build new skills with validation

---

## Version History

- **v1.0** (2026-03-02): Initial release with 5F Framework integration
  - Strategic/Creative/Critical personality modes
  - Figma MCP integration
  - Indian B2B SaaS market focus
  - Complete reference documentation

---

## Credits

**Framework Source:** Razorpay User Research (Indian B2B SaaS market)
**Persona:** Saurabh Soni, VP of Design
**Research Foundation:** The 5F Principles backed by user verbatims and behavioral insights

---

**For detailed usage instructions, see `references/GETTING-STARTED.md`**
