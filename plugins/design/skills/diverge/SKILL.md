---
name: diverge
description: Brainstorm radically different concepts for a design problem. Surfaces real-world vocabulary (components, patterns, products, metaphors) so concepts anchor to things that exist instead of inventing fluff. Outputs concepts as either an interactive React prototype or a Paper canvas with one artboard per concept. Triggers on "diverge", "explore directions", "brainstorm directions", "conceptual range", "radically different concepts", "product directions", "divergent prototypes", "give me range".
---

# /diverge — Brainstorm Radically Different Concepts

Generate concepts that differ in *mechanism*, not *styling*. The output is not a moodboard. It is a set of different machines that solve the same problem through fundamentally different operating principles, each anchored to a real-world thing the user can Google.

## When to Use

- Early-stage product exploration before converging on a direction
- Breaking out of "default SaaS dashboard" gravity
- Generating prototype-worthy concepts that stress-test different interaction models
- When the user says "diverge", "explore directions", "give me range", "brainstorm", "radically different", "product directions"

## Core Rule

Every concept must differ from every other concept on **at least 3** of the divergence axes. If two concepts share the same core mechanic, collapse them into one and generate a replacement.

Read `$CLAUDE_SKILL_DIR/references/divergence-axes.md` for the full axis library (14 axes), prompt frames, and banned patterns.

---

## Workflow: 6 steps

```
Step 1: Break down the problem        — first-principles understanding
Step 2: Surface vocabulary             — name the real concepts the user is reaching for
Step 3: Generate concepts              — 8-10 concepts using axes + provocations + lenses
Step 4: Compare and pick               — comparison table with how each concept dies
Step 5: Deepen the picks               — hybrids, narratives, picking what to prototype
Step 6: Build it                       — React prototype OR Paper canvas
```

### Step 1: Break down the problem

Before generating concepts, decompose the problem using first-principles.

Read `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` — use only the **Break down the problem** section.

**Output (150-250 words, tight):**
- 3 JTBD statements: obvious, emotional, surprising
- The real constraint (time / knowledge / access / trust / motivation / coordination / attention)
- One problem-elimination statement: "What would make this problem not exist?"
- 2 similar problems in other fields + the mechanism they use

**Do NOT skip this step.** The breakdown directly shapes which axes and provocations are most relevant in Step 3.

### Step 2: Surface vocabulary

Before generating concepts, read the user's prompt for fuzzy descriptions and surface the real names of what the user might be reaching for. The user often knows what they mean but doesn't know the word for it. Naming the real concept gives the skill (and the user) a real-world handle to anchor on.

**Trigger rules — when to run this step:**
- User mentions a specific UI element by family name ("slider", "tab", "modal", "feed", "score") → name adjacent patterns + real product examples
- User uses fuzzy adjectives ("delightful", "alive", "calm", "fun", "delight") → name 2-3 real-world delight patterns by name + product example
- User uses negation ("not a slider", "shouldn't be a stepper", "we already use Y, what else") → name the family of alternatives
- Greenfield prompt with no anchorable language → **skip this step**, say "no anchor surfaced, going wide" and proceed to Step 3

**Output format (3-6 items max, one line each, grouped by type where useful):**

```
Vocabulary you might be reaching for:

Interaction patterns
- Snap-to-tier (Apple Music EQ, Stripe pricing): discrete steps on a continuous track. Often what people mean by "not a slider."
- Scrubbing (video timeline): continuous preview while dragging.
- Disclosure pattern (Stripe payment methods): collapsed options that reveal on tap.

Components
- Stepper, segmented control, range input, numeric field with nudge.

Real-world references
- GitHub contribution graph (living state for activity).
- Duolingo streak (continuity as motivation).
- Strava personal records (earned reveal on milestones).

Reply 'all', a list of which to anchor on, or 'something else' to keep going.
```

**User reply handling:**
- `all` → all surfaced items become anchor candidates for Step 3
- A list (e.g., `snap-to-tier, disclosure`) → only those become anchor candidates
- `something else` → ask one sharpening question, then re-surface
- `skip` → proceed without anchor candidates (Step 3 still requires Anchor field, but concepts pick anchors freely)

### Step 3: Generate concepts

**Input:** Problem statement from the user + breakdown from Step 1 + selected vocabulary from Step 2 (if any). If the problem is vague, ask one sharpening question. Do not over-clarify.

**Before generating concepts:**

1. List the 5 most predictable solutions for this problem. **Ban them.**
2. Consult the axis library (`divergence-axes.md`) and select 8-10 axes that apply to this problem space.
3. Assign each concept a different primary axis. No two concepts share the same primary axis.
4. Select **2-3 creative provocation techniques** from `$CLAUDE_SKILL_DIR/references/creative-provocations.md`. Use the Selection Guide at the bottom of that file to match techniques to the problem type. Each selected technique must influence at least 1 concept.
5. Select **1 extreme user or context** from `$CLAUDE_SKILL_DIR/references/persona-lens.md`. At least 1 concept must be designed for this extreme user/context.

**Generate 8-10 concepts. For each, output:**

| Field | What it answers |
|-------|----------------|
| **Name** | Evocative 2-3 word concept name |
| **What this product believes** | One sentence. What this product *believes* about the problem. |
| **Core mechanic** | The single interaction/system behavior that defines it. Not a feature list. |
| **Interaction model** | Direct manipulation / conversational / ambient / agent-led / game-like / feed / ritual / invisible / collaborative / simulator |
| **What the user no longer has to do** | The effort or decision this concept eliminates. |
| **What it gives up** | The tradeoff. What gets worse. Be honest. |
| **What makes it different** | Why this is a different species, not a different skin. Reference which axes it diverges on. |
| **Anchor** | A real, named thing this concept borrows from: a component, an interaction pattern, a real product's mechanic, a real-world metaphor with a proper name. One line. Examples: "Snap-to-tier (Apple Music EQ)", "Living state (GitHub contribution graph)", "Disclosure pattern (Stripe payment methods)". |
| **Where the idea came from** | Which technique or lens generated this concept (axis combination, SCAMPER, assumption reversal, random domain connection, extreme user, start from the emotion, etc.) |
| **First scene to build** | The single screen/moment/interaction to build first to test the concept. |

**Anchor quality gate:**
The Anchor must be Googleable. The user must be able to look it up and find a real artifact (a product, a Wikipedia page, a Material/Apple/iOS HIG entry, a real product feature). If a concept's anchor is "spaceship console" or any invented thing, replace the anchor — but **don't dampen the concept**. "Bloomberg Terminal density on a phone" is a real anchor, "Boeing 737 HUD as approval surface" is a real anchor, "Tamagotchi as inbox" is a real anchor. The gate kills *invented fluff*, not ambition.

**Minimum diversity requirements:**
- At least 2 concepts remove the need for a traditional screen
- At least 2 rely heavily on automation or agent behavior
- At least 2 invert the problem (help users avoid/reduce/delegate rather than do)
- At least 1 feels like a game or toy
- At least 1 feels like a serious professional power tool
- At least 1 borrows its operating logic from a non-software domain
- At least 1 generated from a creative provocation technique (not just axis combination)
- At least 1 designed for a non-obvious user or context

**Quality gate:** After generating, scan for duplicates — concepts that look different but use the same core mechanic. Replace any duplicates.

### Step 4: Compare and pick

Present a compact comparison table of all concepts across these dimensions:

| Concept | Interaction Model | User Effort | System Intelligence | Risk Level | Novelty (real/fake) | How it dies | Where the idea came from |
|---------|-------------------|-------------|---------------------|------------|---------------------|----------------|-------------------|

**How it dies:** For each concept, state the single most likely way it fails. Be specific: who is affected, what goes wrong, when it happens. Not "users might not like it." See `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` "How each concept dies" section for quality examples.

Then answer:
- Which 3 are most structurally promising and why?
- Which 2 are duplicates (same sandwich, different lettuce)?
- Which 1 is the "dangerous" idea — the one that's either brilliant or terrible?

Ask the user: **"Which concepts should I prototype? Pick 2-4, or say 'surprise me.'"**

### Step 5: Deepen the picks

For the concepts the user selected (or the top 3 if "surprise me"):

Read `$CLAUDE_SKILL_DIR/references/concept-enrichment.md` — use the **Hybrid combinations**, **Day-in-the-Life Narratives**, and **Picking what to prototype** sections.

1. **Hybrid combinations:** From the shortlisted concepts, pick the 3 most structurally different. Attempt 2-3 hybrid combinations. If a hybrid is more interesting than the weakest shortlisted concept, propose the swap.

2. **Day-in-the-Life:** For each shortlisted concept, write a 3-paragraph narrative: trigger (what situation brings the user here), interaction (the felt experience, not features), aftermath (what's different now). Quality gate: must sound like a diary entry, not a press release.

3. **Picking what to prototype:** Present the decision framework table (signal strength, feasibility to prototype, risk of skipping, team conviction) so the user knows which concepts are best suited for prototyping.

Ask the user: **"Ready to prototype? Or want to explore any hybrids further?"**

### Step 6: Build it

Ask one question, wait for the answer:

```
Step 6 output:
  (a) React prototype with DialKit (interactive, tunable, ~10 min build)
  (b) Paper canvas with one artboard per concept (visual side-by-side, fast, no code)
  (c) Both — Paper first, React only for the favorites you pick
```

Don't auto-pick. Wait.

#### Option (a): React prototype

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
1. Each concept is a separate file in `src/concepts/` exporting `{ id, name, premise, anchor, mechanic, sacrifices, axes, controls, Scene }`
2. The `Scene` component receives `{ values }` from DialKit and responds in real-time
3. DialKit controls must reflect the concept's *mechanism*, not cosmetics — see control libraries in picker-template.md
4. 3-6 controls per concept, each changing *behavior* not appearance
5. After scaffolding, run `npm install && npm run dev` and give the user the local URL

**File output:** Save to workspace as `diverge-[problem-slug]/` and start the dev server

#### Option (b): Paper canvas

Read `$CLAUDE_SKILL_DIR/references/paper-canvas-template.md` for the per-concept artboard layout, gallery layout, and the order of Paper MCP calls.

**Summary:**
1. `get_basic_info`, `get_font_family_info` (orientation calls)
2. For each concept: `create_artboard` (1440 × 900 default; 390 × 844 if mobile), then `write_html` for header strip / main scene / anchor card / meta strip
3. `get_screenshot` per artboard
4. `finish_working_on_nodes` at the end

Each artboard contains: header strip (concept name + what this product believes), main scene (first scene to build), anchor card (the Anchor with its real-world reference), meta strip (axes + where the idea came from).

#### Option (c): Both

Run option (b) first — Paper gallery for visual range. After the user picks 1-3 favorites in conversation, run option (a) for those concepts only. Saves the time of building 8-10 React scenes when only a few will be tuned.

---

## Output Format

```
## Diverge: {PROBLEM}

### Break down the problem (Step 1)
- JTBD: [3 statements]
- Real constraint: [primary + secondary]
- Eliminate the problem: [statement]
- Similar problems in other fields: [2 domains + mechanisms]

### Vocabulary surfaced (Step 2)
[3-6 named patterns/components/references — or "skipped, going wide"]

### Banned directions (predictable solutions removed)
- [5 banned solutions]

### Provocation techniques selected
- [2-3 techniques from creative-provocations.md]
- Lens: [selected extreme user/context]

### Concepts generated: {N}
[concept tables, each with the Anchor field]

### Compare and pick (Step 4)
[comparison table with "How it dies" + picks]

### Deepen the picks (Step 5)
[hybrid combinations + narratives + decision framework]

### Built (Step 6)
Output type: [React prototype / Paper canvas / Both]
Location: [path or canvas]
Concepts included: [list]
```

---

## Output Budget

Keep output focused. More words does not mean more divergence.

| Step | Budget |
|------|--------|
| Step 1 (Break down) | 150-250 words |
| Step 2 (Surface vocabulary) | 50-100 words |
| Step 3 (Generate concepts) | 8-10 concepts × ~110 words each = 900-1100 words |
| Step 4 (Compare and pick) | Comparison table + 100-150 words commentary |
| Step 5 (Deepen the picks) | 3 narratives × 200 words + decision table = ~750 words |
| Step 6 (Build it) | Code or canvas output (no word budget) |

Total text output before building: ~2300 words. If you're writing more, you're explaining instead of diverging.

## Technique Rotation

Each run of /diverge should use a **different combination** of provocation techniques. If the user runs /diverge twice on related problems, avoid reusing the same techniques. Variety in technique produces variety in output.

Track which techniques were used and select different ones next time. The creative-provocations.md library has 7 techniques and the persona-lens.md has 8 extreme users, 6 time budgets, and 8 contexts. There are enough combinations to never repeat.

---

## When to use parallel agents

For broad problems with rich axis ranges, you can spawn parallel subagents to speed up work. For focused problems, run everything in the main conversation.

| Step | Strategy | Why |
|------|----------|-----|
| Step 1 | Main conversation | Short, shapes all downstream work |
| Step 2 | Main conversation | Quick, depends on user reply |
| Step 3 | Parallel subagents (optional) | When problem space is broad, split axis ranges across 2-3 agents, merge + deduplicate |
| Step 4 | Main conversation | Requires holistic comparison across all concepts |
| Step 5 | Parallel subagents for narratives | Day-in-the-life narratives are independent per concept |
| Step 6 (React) | Parallel subagents for Scene components | Each concept's Scene is self-contained, merge into scaffold |
| Step 6 (Paper) | Main conversation, sequential calls | Paper MCP calls must be sequential to avoid layout overlap |

**When NOT to use subagents:**
- Problem is focused/narrow (fewer than 8 applicable axes) — generate everything in main
- Only 2 concepts shortlisted — not worth the overhead
- User wants a quick brainstorm without prototyping — skip Step 6 entirely

**Subagent briefing rules:**
- Always include the full concept table format in the prompt so agents produce consistent output
- Always include the problem statement and breakdown from Step 1 + vocabulary from Step 2
- Always specify which axes/techniques the agent should use (prevent overlap between agents)
- After agents return, always run the duplicate detector in the main conversation

**Parallel concept generation example (Step 3):**

```
Agent 1: "Generate 4 concepts for [problem] using axes [A, B, C, D] and 
         provocation technique [X]. Each concept must include the Anchor 
         field — a real, Googleable thing it borrows from. Use these 
         vocabulary anchors as candidates: [paste from Step 2].
         [paste concept table format]"

Agent 2: "Generate 4 concepts for [problem] using axes [E, F, G, H] and 
         provocation technique [Y] + lens [Z]. Each concept must include 
         the Anchor field. [paste concept table format]"
```

After agents return, deduplicate in the main conversation: merge results, run the duplicate detector, collapse any overlapping concepts, and fill gaps in the diversity requirements.

---

## Edge Cases

- **User provides a solution, not a problem** — Reframe: "You've described a solution. The problem underneath seems to be [X]. I'll diverge on the problem, not the solution."
- **User asks for < 5 concepts** — Still generate 8-10 internally, then surface only the requested count, selecting for maximum range.
- **User asks for "variations"** — Redirect: "Variations optimize within one direction. Diverge generates different directions. Want me to diverge first, then you can pick one to create variations of?"
- **Problem is too broad** — Ask one sharpening question. Do not ask more than one.
- **Problem is too narrow** — Widen it one level before diverging. State what you widened and why.
- **User says "quick" or "just brainstorm"** — Run Steps 1-4 only, skip 5 and 6. Output concepts + comparison without prototyping.
- **User says "surprise me"** — Select top 3 by maximum structural range (most different from each other), proceed to Step 5 and 6.
- **Vocabulary surface yields nothing useful** — say "no anchor surfaced, going wide" and proceed; Step 3 still requires Anchor on every concept, the skill picks freely.

## What This Skill Is NOT

- Not a UI polish tool (use `/design` for that)
- Not a variation generator (same concept, different styling)
- Not a wireframing tool (prototypes test mechanics, not layouts)
- Not converging — this skill explicitly avoids premature optimization
- Not exhaustive — it selects from technique libraries, not applies all of them
