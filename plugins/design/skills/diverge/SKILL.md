---
name: diverge
description: Generates 8-10 radically different product/design concepts for a problem statement — structurally divergent, not visual remixes. Each concept differs on interaction model, system behavior, user effort, and mental model. Outputs an interactive React prototype with a concept picker and per-concept DialKit tuning controls. Triggers on "diverge", "explore directions", "conceptual range", "radically different concepts", "product directions", "divergent prototypes", "explode the solution space".
---

# /diverge — Structural Divergence Engine

Generate concepts that differ in *mechanism*, not *styling*. The output is not a moodboard — it is a set of different machines that solve the same problem through fundamentally different operating principles.

## When to Use

- Early-stage product exploration before converging on a direction
- Breaking out of "default SaaS dashboard" gravity
- Generating prototype-worthy concepts that stress-test different interaction models
- When the user says "diverge", "explore directions", "give me range", "radically different", "product directions"

## Core Rule

Every concept must differ from every other concept on **at least 3** of the divergence axes. If two concepts share the same core mechanic, collapse them into one and generate a replacement.

Read `$CLAUDE_SKILL_DIR/references/divergence-axes.md` for the full axis library, prompt frames, and banned patterns.

---

## Workflow: 3-Pass Divergence

### Pass 1: EXPLODE (generate range)

**Input:** Problem statement from the user. If vague, ask one sharpening question — do not over-clarify.

**Before generating concepts:**

1. List the 5 most predictable solutions for this problem. **Ban them.**
2. Consult the axis library (`divergence-axes.md`) and select 8-10 axes that apply to this problem space.
3. Assign each concept a different primary axis. No two concepts share the same primary axis.

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
| **First prototype scene** | The single screen/moment/interaction to build first to test the concept. |

**Minimum diversity requirements:**
- At least 2 concepts remove the need for a traditional screen
- At least 2 rely heavily on automation or agent behavior
- At least 2 invert the problem (help users avoid/reduce/delegate rather than do)
- At least 1 feels like a game or toy
- At least 1 feels like a serious professional power tool
- At least 1 borrows its operating logic from a non-software domain

**Quality gate:** After generating, scan for "fake novelty" — concepts that look different but use the same core mechanic. Replace any duplicates.

### Pass 2: STRESS TEST (evaluate range)

Present a compact comparison table of all concepts across these dimensions:

| Concept | Interaction Model | User Effort | System Intelligence | Risk Level | Novelty (real/fake) |
|---------|-------------------|-------------|---------------------|------------|---------------------|

Then answer:
- Which 3 are most structurally promising and why?
- Which 2 are fake novelty (same sandwich, different lettuce)?
- Which 1 is the "dangerous" idea — the one that's either brilliant or terrible?

Ask the user: **"Which concepts should I prototype? Pick 2-4, or say 'surprise me.'"**

### Pass 3: PROTOTYPE (build interactive picker)

Read `$CLAUDE_SKILL_DIR/references/picker-template.md` for the React template.

Scaffold a **Vite + React** app. Read `$CLAUDE_SKILL_DIR/references/picker-template.md` for the full template and scaffolding instructions.

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
- Agent-driven → `autonomy level`, `intervention frequency`, `aggressiveness`
- Game-like → `difficulty`, `reward frequency`, `time pressure`
- Ritual → `session length`, `reminder cadence`, `reflection depth`
- Power-tool → `information density`, `shortcut depth`, `batch size`

**File output:** Save to workspace as `diverge-[problem-slug]/` and start the dev server

---

## Output Format

After Pass 1, output concepts in the structured table format above.
After Pass 2, output the comparison table and recommendations.
After Pass 3, link the prototype file.

```
## Diverge: {PROBLEM}

### Banned directions (predictable solutions removed)
- [5 banned solutions]

### Concepts generated: {N}
[concept tables]

### Stress test
[comparison table + picks]

### Prototype (Vite app)
Location: `diverge-[problem-slug]/`
Dev server: [local URL]
Concepts included: [list]
DialKit controls per concept: [summary]
```

---

## Edge Cases

- **User provides a solution, not a problem** → Reframe: "You've described a solution. The problem underneath seems to be [X]. I'll diverge on the problem, not the solution."
- **User asks for < 5 concepts** → Still generate 8-10 internally, then surface only the requested count, selecting for maximum range.
- **User asks for "variations"** → Redirect: "Variations optimize within one direction. Diverge generates different directions. Want me to diverge first, then you can pick one to create variations of?"
- **Problem is too broad** → Ask one sharpening question. Do not ask more than one.
- **Problem is too narrow** → Widen it one level before diverging. State what you widened and why.

## What This Skill Is NOT

- Not a UI polish tool (use `/design` for that)
- Not a variation generator (same concept, different styling)
- Not a wireframing tool (prototypes test mechanics, not layouts)
- Not converging — this skill explicitly avoids premature optimization
