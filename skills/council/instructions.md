# Council Protocol

## Overview

Council is a 3-phase multi-agent research process. It spawns 10 agents in parallel, each investigating a different angle of the topic, then synthesizes their findings into a structured report.

**Use council when:**
- A topic is too large for a single agent
- Multiple perspectives are needed simultaneously
- You need to surface inconsistencies, gaps, or hidden dependencies
- The user asks for a "full audit", "deep research", or "find inconsistencies"

---

## Phase 1 — Reconnaissance (inline, before spawning)

Before spawning agents, spend 2-3 tool calls to understand the landscape:

1. **Scope the topic.** What directories, files, or systems are involved? Get a rough map.
2. **Identify the 10 best angles.** What are the most important questions to answer about this topic? What would a thorough investigation cover?
3. **Note constraints.** Any files to avoid? Any known context that agents should have?

Do NOT skip this phase. Poorly defined agent tasks produce noise.

---

## Phase 2 — Spawn 10 Agents in Parallel

Send a **single message** with 10 Agent tool calls. All 10 run simultaneously.

### Standard agent roles (adapt to the topic):

| Agent | Role | Focus |
|---|---|---|
| 1 | **Core investigator** | What does `$ARGUMENTS` actually do/contain? Structure, purpose, current state. |
| 2 | **Dependencies** | What depends on this? What does it depend on? Who calls it, what does it call? |
| 3 | **Patterns + conventions** | What patterns, naming conventions, inconsistencies appear? Compared to how similar things are done elsewhere. |
| 4 | **History** | What do session journals (`log/`), `decisions.md`, and `patterns.md` say about this topic? What was tried before? |
| 5 | **Cross-references** | What else in the vault/codebase references this? What wikilinks point here? What would break if this changed? |
| 6 | **Pain points** | Where do errors, corrections, and patterns.md entries cluster around this? What's been fixed repeatedly? |
| 7 | **Gaps** | What's missing, undocumented, or inconsistent? What SHOULD exist but doesn't? |
| 8 | **Wild card — adversarial** | What would break this? What's the most fragile assumption? What happens if this goes wrong? |
| 9 | **Wild card — blind spot** | What is the user probably NOT asking about, but should be? What's the adjacent problem? |
| 10 | **Synthesizer** | *(Runs after others complete)* Read all 9 agent outputs. Synthesize: what do they reveal together that none reveals alone? |

### Agent prompt template:

```
You are the [ROLE] agent for a council research session on: [TOPIC]

Context from reconnaissance:
[paste relevant context from Phase 1]

Your specific focus: [FOCUS]

Research this thoroughly. Be concrete. Return:
- Your findings (bullet list, specific)
- 1-2 highest-signal insights
- Any open questions you couldn't resolve

Do NOT summarize what you'll do. Just do it and return findings.
```

### Adapting for non-code topics (vault audits, skill analysis, etc.):

For vault or system audits, adapt agent roles:
- Replace "Dependencies" with "What references this?"
- Replace "Pain points" with "Where does this cause confusion?"
- Add a "Comparison" agent that benchmarks against similar systems

---

## Phase 3 — Synthesis

After all 10 agents return:

1. Read all outputs
2. Write the council report following `output-template.md`
3. Be concrete — no platitudes, no "it's complex"
4. Lead with the TL;DR — 3 bullets, maximum signal

**If in plan mode:** After synthesis, write findings to the plan file. Council is the research phase. After council, `/writing-plans` takes over for the implementation plan.

---

## Quality bar

A good council output:
- Has a TL;DR that a skimmer can act on
- Surfaces at least one thing the user didn't know to ask about
- Makes clear which findings are high confidence vs. speculative
- Ends with concrete, prioritized recommended actions

A bad council output:
- Just restates what the user already knew
- Has vague recommendations ("consider improving X")
- Buries the insight in prose
