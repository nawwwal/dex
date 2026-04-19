---
name: diverge
description: Design brainstorming and structural divergence engine. Generates 8-10 radically different product/design concepts using creative provocation techniques, persona lenses, and axis-based divergence. Concepts differ in mechanism, not styling. Outputs an interactive React prototype with a concept picker and per-concept DialKit tuning controls. Triggers on "diverge", "explore directions", "brainstorm directions", "conceptual range", "radically different concepts", "product directions", "divergent prototypes", "explode the solution space", "give me range".
---

# /diverge — Design Brainstorming & Structural Divergence Engine

Generate concepts that differ in *mechanism*, not *styling*. The output is not a moodboard. It is a set of different machines that solve the same problem through fundamentally different operating principles, discovered through structured creative provocation.

## When to Use

- Early-stage product exploration before converging on a direction
- Breaking out of "default SaaS dashboard" gravity
- Generating prototype-worthy concepts that stress-test different interaction models
- When the user says "diverge", "explore directions", "give me range", "brainstorm", "radically different", "product directions"

## Core Rule

Every concept must differ from every other concept on **at least 3** of the divergence axes. If two concepts share the same core mechanic, collapse them into one and generate a replacement.

Read `$CLAUDE_SKILL_DIR/references/divergence-axes.md` for the full axis library (14 axes), prompt frames, and banned patterns.

---

## Workflow: 5-Pass Divergence

```
Pass 0: DECOMPOSE     — first-principles problem breakdown
Pass 1: EXPLODE       — generate 8-10 concepts using axes + provocations + persona lenses
Pass 2: STRESS TEST   — comparison table with failure modes
Pass 2.5: ENRICH      — cross-pollination, narratives, convergence bridge
Pass 3: PROTOTYPE     — interactive React picker with DialKit
```

### Pass 0: DECOMPOSE (understand before diverging)

Before generating concepts, decompose the problem using first-principles.

Read `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` — use only the **First-Principles Decomposition** section.

**Output (150-250 words, tight):**
- 3 JTBD statements: obvious, emotional, surprising
- The real constraint (time / knowledge / access / trust / motivation / coordination / attention)
- One problem dissolution statement: "What would make this problem not exist?"
- 2 structural siblings from other domains + the mechanism they use

**Do NOT skip this pass.** The decomposition directly shapes which axes and provocations are most relevant in Pass 1.

**Subagent strategy:** Run this pass in the main conversation. It's short and shapes everything after it.

### Pass 1: EXPLODE (generate range)

**Input:** Problem statement from the user + decomposition from Pass 0. If the problem is vague, ask one sharpening question. Do not over-clarify.

**Before generating concepts:**

1. List the 5 most predictable solutions for this problem. **Ban them.**
2. Consult the axis library (`divergence-axes.md`) and select 8-10 axes that apply to this problem space.
3. Assign each concept a different primary axis. No two concepts share the same primary axis.
4. Select **2-3 creative provocation techniques** from `$CLAUDE_SKILL_DIR/references/creative-provocations.md`. Use the Selection Guide at the bottom of that file to match techniques to the problem type. Each selected technique must influence at least 1 concept.
5. Select **1 persona extreme or context shift** from `$CLAUDE_SKILL_DIR/references/persona-lens.md`. At least 1 concept must be designed for this extreme user/context.

**Generate 8-10 concepts. For each, output:**

| Field | What it answers |
|-------|----------------|
| **Name** | Evocative 2-3 word concept name |
| **Premise** | One sentence. What this product *believes* about the problem. |
| **Core mechanic** | The single interaction/system behavior that defines it. Not a feature list. |
| **Interaction model** | Direct manipulation / conversational / ambient / agent-led / game-like / feed / ritual / invisible / collaborative / simulator |
| **What the user no longer has to do** | The effort or decision this concept eliminates. |
| **What it sacrifices** | The tradeoff. What gets worse. Be honest. |
| **Structural difference** | Why this is a different species, not a different skin. Reference which axes it diverges on. |
| **Provocation source** | Which technique or lens generated this concept (axis combination, SCAMPER, assumption reversal, bisociation, persona extreme, emotion-first, etc.) |
| **First prototype scene** | The single screen/moment/interaction to build first to test the concept. |

**Minimum diversity requirements:**
- At least 2 concepts remove the need for a traditional screen
- At least 2 rely heavily on automation or agent behavior
- At least 2 invert the problem (help users avoid/reduce/delegate rather than do)
- At least 1 feels like a game or toy
- At least 1 feels like a serious professional power tool
- At least 1 borrows its operating logic from a non-software domain
- At least 1 generated from a creative provocation technique (not just axis combination)
- At least 1 designed for a non-obvious user persona or context

**Quality gate:** After generating, scan for "fake novelty" — concepts that look different but use the same core mechanic. Replace any duplicates.

**Subagent strategy for Pass 1:** For problems with clear sub-domains, you can spawn **2-3 parallel subagents** to generate concept batches independently, then merge and deduplicate:

```
Agent 1: "Generate 4 concepts for [problem] using axes [A, B, C, D] and 
         provocation technique [X]. Each concept must meet the structural 
         fields defined below. [paste concept table format]"

Agent 2: "Generate 4 concepts for [problem] using axes [E, F, G, H] and 
         provocation technique [Y] + persona lens [Z]. Each concept must 
         meet the structural fields defined below. [paste concept table format]"
```

After agents return, **deduplicate in the main conversation**: merge results, run the fake novelty detector, collapse any overlapping concepts, and fill gaps in the diversity requirements.

Only use parallel agents when the problem space is rich enough to warrant it (broad problem, many applicable axes). For focused problems, generate all concepts in the main conversation.

### Pass 2: STRESS TEST (evaluate range)

Present a compact comparison table of all concepts across these dimensions:

| Concept | Interaction Model | User Effort | System Intelligence | Risk Level | Novelty (real/fake) | Death Scenario | Provocation Source |
|---------|-------------------|-------------|---------------------|------------|---------------------|----------------|-------------------|

**Death Scenario:** For each concept, state the single most likely way it fails. Be specific: who is affected, what goes wrong, when it happens. Not "users might not like it." See `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` Failure Mode Analysis section for quality examples.

Then answer:
- Which 3 are most structurally promising and why?
- Which 2 are fake novelty (same sandwich, different lettuce)?
- Which 1 is the "dangerous" idea — the one that's either brilliant or terrible?

Ask the user: **"Which concepts should I prototype? Pick 2-4, or say 'surprise me.'"**

**Subagent strategy:** Run Pass 2 in the main conversation. It requires seeing all concepts together to compare and detect fake novelty. Do not parallelize.

### Pass 2.5: ENRICH (deepen before prototyping)

For the concepts the user selected (or the top 3 if "surprise me"):

Read `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` — use the **Cross-Pollination**, **Day-in-the-Life Narratives**, and **Convergence Bridge** sections.

1. **Cross-pollinate:** From the shortlisted concepts, pick the 3 most structurally different. Attempt 2-3 hybrid combinations. If a hybrid is more interesting than the weakest shortlisted concept, propose the swap.

2. **Day-in-the-Life:** For each shortlisted concept, write a 3-paragraph narrative: trigger (what situation brings the user here), interaction (the felt experience, not features), aftermath (what's different now). Quality gate: must sound like a diary entry, not a press release.

3. **Convergence bridge:** Present the decision framework table (signal strength, feasibility to prototype, risk of skipping, team conviction) so the user knows which concepts are best suited for prototyping.

Ask the user: **"Ready to prototype? Or want to explore any hybrids further?"**

**Subagent strategy:** Spawn **parallel subagents for narratives** when 3+ concepts are shortlisted:

```
Agent 1: "Write a day-in-the-life narrative for [Concept A]. 3 paragraphs: 
         trigger (specific situation, time, emotional state), interaction 
         (felt experience, not features), aftermath (what changed). 
         Must sound like a diary entry, not marketing copy. 
         Concept details: [paste concept fields]"

Agent 2: "Write a day-in-the-life narrative for [Concept B]. [same format]"

Agent 3: "Write a day-in-the-life narrative for [Concept C]. [same format]"
```

Run cross-pollination and convergence bridge in the main conversation (requires seeing all concepts together).

### Pass 3: PROTOTYPE (build interactive picker)

Read `$CLAUDE_SKILL_DIR/references/picker-template.md` for the full React template and scaffolding instructions.

**App structure:**
```
diverge-[problem-slug]/
├── index.html
├── package.json          (vite + react deps)
├── vite.config.js
└── src/
    ├── main.jsx          (ReactDOM render)
    ├── App.jsx           (DivergePicker root — concept nav, scene, dialkit)
    ├── concepts/         (one file per concept)
    │   ├── concept-1.jsx (exports: meta + controls + Scene component)
    │   ├── concept-2.jsx
    │   └── ...
    ├── components/
    │   ├── ConceptNav.jsx
    │   ├── ConceptMeta.jsx
    │   └── DialKitPanel.jsx
    └── styles.css        (minimal global reset + dark theme tokens)
```

**Key rules:**
1. Each concept is a separate file in `src/concepts/` exporting `{ id, name, premise, mechanic, sacrifices, axes, controls, Scene }`
2. The `Scene` component receives `{ values }` from DialKit and responds in real-time
3. DialKit controls must reflect the concept's *mechanism*, not cosmetics — see control libraries in picker-template.md
4. 3-6 controls per concept, each changing *behavior* not appearance
5. After scaffolding, run `npm install && npm run dev` and give the user the local URL

**DialKit control examples by concept type:**
- Agent-driven: `autonomy level`, `intervention frequency`, `aggressiveness`
- Game-like: `difficulty`, `reward frequency`, `time pressure`
- Ritual: `session length`, `reminder cadence`, `reflection depth`
- Power-tool: `information density`, `shortcut depth`, `batch size`

**File output:** Save to workspace as `diverge-[problem-slug]/` and start the dev server

**Subagent strategy for Pass 3:** Spawn **parallel subagents for concept scenes** (the most parallelizable part of the entire workflow):

```
Agent 1: "Build the React Scene component for [Concept A]. 
         Export format: { id, name, premise, mechanic, sacrifices, axes, controls, Scene }
         The Scene component receives { values } and responds to DialKit controls in real-time.
         Concept details: [paste concept fields + selected controls]
         Follow the concept file format from picker-template.md. Self-contained, 
         inline styles, mock data, no external dependencies beyond React."

Agent 2: "Build the React Scene component for [Concept B]. [same format]"

Agent 3: "Build the React Scene component for [Concept C]. [same format]"
```

Build the scaffold (App.jsx, ConceptNav, ConceptMeta, DialKitPanel, styles, config) in the main conversation while concept agents run in parallel. Merge concept files when agents return, then run `npm install && npm run dev`.

---

## Output Format

```
## Diverge: {PROBLEM}

### Decomposition (Pass 0)
- JTBD: [3 statements]
- Real constraint: [primary + secondary]
- Problem dissolution: [statement]
- Structural siblings: [2 domains + mechanisms]

### Banned directions (predictable solutions removed)
- [5 banned solutions]

### Provocation techniques selected
- [2-3 techniques from creative-provocations.md]
- Persona lens: [selected persona/context]

### Concepts generated: {N}
[concept tables]

### Stress test (Pass 2)
[comparison table with death scenarios + picks]

### Enrichment (Pass 2.5)
[cross-pollination results + narratives + convergence bridge]

### Prototype (Vite app)
Location: `diverge-[problem-slug]/`
Dev server: [local URL]
Concepts included: [list]
DialKit controls per concept: [summary]
```

---

## Output Budget

Keep output focused. More words does not mean more divergence.

| Pass | Budget |
|------|--------|
| Pass 0 (DECOMPOSE) | 150-250 words |
| Pass 1 (EXPLODE) | 8-10 concepts x ~100 words each = 800-1000 words |
| Pass 2 (STRESS TEST) | Comparison table + 100-150 words commentary |
| Pass 2.5 (ENRICH) | 3 narratives x 200 words + decision table = ~750 words |
| Pass 3 (PROTOTYPE) | Code output (no word budget) |

Total text output before prototyping: ~2200 words. If you're writing more, you're explaining instead of diverging.

## Technique Rotation

Each run of /diverge should use a **different combination** of provocation techniques. If the user runs /diverge twice on related problems, avoid reusing the same techniques. Variety in technique produces variety in output.

Track which techniques were used and select different ones next time. The creative-provocations.md library has 7 techniques and the persona-lens.md has 8 personas, 6 time budgets, and 8 contexts. There are enough combinations to never repeat.

---

## Subagent Orchestration Summary

| Pass | Strategy | Why |
|------|----------|-----|
| Pass 0 | Main conversation | Short, shapes all downstream work |
| Pass 1 | Parallel subagents (optional) | When problem space is broad, split axis ranges across 2-3 agents, merge + deduplicate |
| Pass 2 | Main conversation (read concept-enrichment.md for failure mode examples) | Requires holistic comparison across all concepts |
| Pass 2.5 | Parallel subagents for narratives | Day-in-the-life narratives are independent per concept |
| Pass 3 | Parallel subagents for Scene components | Each concept's Scene is self-contained, merge into scaffold |

**When NOT to use subagents:**
- Problem is focused/narrow (fewer than 8 applicable axes) — generate everything in main
- Only 2 concepts shortlisted — not worth the overhead
- User wants a quick brainstorm without prototyping — skip Pass 3 entirely

**Subagent briefing rules:**
- Always include the full concept table format in the prompt so agents produce consistent output
- Always include the problem statement and decomposition from Pass 0
- Always specify which axes/techniques the agent should use (prevent overlap between agents)
- After agents return, always run the fake novelty detector in the main conversation

---

## Edge Cases

- **User provides a solution, not a problem** — Reframe: "You've described a solution. The problem underneath seems to be [X]. I'll diverge on the problem, not the solution."
- **User asks for < 5 concepts** — Still generate 8-10 internally, then surface only the requested count, selecting for maximum range.
- **User asks for "variations"** — Redirect: "Variations optimize within one direction. Diverge generates different directions. Want me to diverge first, then you can pick one to create variations of?"
- **Problem is too broad** — Ask one sharpening question. Do not ask more than one.
- **Problem is too narrow** — Widen it one level before diverging. State what you widened and why.
- **User says "quick" or "just brainstorm"** — Run Passes 0-2 only, skip 2.5 and 3. Output concepts + stress test without prototyping.
- **User says "surprise me"** — Select top 3 by maximum structural range (most different from each other), proceed to Pass 2.5 and 3.

## What This Skill Is NOT

- Not a UI polish tool (use `/design` for that)
- Not a variation generator (same concept, different styling)
- Not a wireframing tool (prototypes test mechanics, not layouts)
- Not converging — this skill explicitly avoids premature optimization
- Not exhaustive — it selects from technique libraries, not applies all of them
