---
name: diverge
description: Brainstorm radically different concepts for a design problem. Extracts a Brief from the user (main thing, references, constraints), surfaces real-world vocabulary, generates concepts anchored to specific named references across video games, arts, history, music, sport, and craft, runs them through a kill ledger, then outputs the survivors as either an interactive React prototype or a Paper canvas. Triggers on "diverge", "explore directions", "brainstorm directions", "conceptual range", "radically different concepts", "product directions", "divergent prototypes", "give me range".
---

# /diverge — Brainstorm Radically Different Concepts

Generate concepts that differ in *mechanism*, not *styling*. The output is not a moodboard. It is a set of different machines that solve the same problem through fundamentally different operating principles, each anchored to a real-world thing the user can Google.

The skill does two things v2.7.x didn't: it **extracts a Brief** from the user before generating anything (so concepts target real taste, not generic divergence), and it **runs a kill ledger** before the user sees the concepts (so weak concepts get cut, not delivered).

## When to Use

- Early-stage product exploration before converging on a direction
- Breaking out of "default SaaS dashboard" gravity
- Generating prototype-worthy concepts that stress-test different interaction models
- When the user says "diverge", "explore directions", "give me range", "brainstorm", "radically different", "product directions"

## Core Rule

Every concept must differ from every other concept on **at least 3** of the divergence axes. Concepts whose Structural thesis sentences can be swapped without changing meaning are layout variations, not concepts — kill the weaker.

Read `$CLAUDE_SKILL_DIR/references/divergence-axes.md` for the full axis library (14 axes), prompt frames, and banned patterns.

---

## Workflow: 7 steps

```
Step 1: Brief + Break down the problem    — interview, infer, decompose
Step 2: Surface vocabulary                 — name real concepts the user is reaching for
Step 3: Generate concepts                  — 8-10 concepts using axes + provocations + lenses + Brief-targeted anchors
Step 4: Kill ledger                        — Keep / Rewrite / Kill before user sees the set
Step 5: Compare and pick                   — comparison table on the survivors
Step 6: Deepen the picks                   — hybrids, narratives, simplicity pass, real-world states
Step 7: Build it                           — React prototype OR Paper canvas
```

### Step 1: Brief + Break down the problem

Phase 1.A is an interview. The skill posts ONE message with three required questions and waits.

```
Before I diverge, three quick things. Answer in any format — bullets, fragments, vibes.

1. The main thing — if you could only get ONE thing right about this, what is it? (one sentence)
2. References — name 3-5 products / installations / games / films / artworks you admire. Anything that raises your bar; doesn't have to relate to this problem.
3. Constraints and anti-patterns — what cannot change (design system, brand, downstream consumers) and what's already been tried that didn't work / what would feel deeply wrong.

Reply 'go' once done.
```

If the user replies with `skip brief`, the skill self-generates a degraded Brief from the prompt alone and marks the run as DEGRADED at the top of the output.

Phase 1.B — emit the Brief block. Skill drafts the inferred fields:

```
Brief

Main thing: <one sentence>
References: <3-5 named works>
Constraints: <list>
Anti-patterns: <list>
Audience (inferred): <one line, mark if uncertain>
Consistency contract (inferred): <list of familiar things every concept must keep>
Altitude (inferred): <surface | underlying issue | both>
Rave-tweet (drafted): "<20-word tweet a happy user would post>"

Reply 'go' to lock, or correct any line.
```

The skill drafts the rave-tweet given Main thing + References. The Audience comes from constraints (e.g., "Razorpay merchants in India"). The Consistency contract lists what must stay familiar (e.g., "Blade components, dashboard navigation, login state"). The Altitude is inferred from how the prompt is framed.

The Brief becomes load-bearing. Every downstream step references it.

Phase 1.C — Break down the problem (per `references/concept-enrichment.md` "Break down the problem" section).

**Output (150-200 words, tight):**
- 3 JTBD statements: obvious, emotional, surprising — each must serve the Main thing
- The real constraint (time / knowledge / access / trust / motivation / coordination / attention)
- One problem-elimination statement: "What would make this problem not exist?"
- 2 similar problems in other fields + the mechanism they use

### Step 2: Surface vocabulary

Read the user's prompt for fuzzy descriptions and name the real-world concepts they might be reaching for. The user often knows what they mean but doesn't know the word for it.

**Trigger rules:**
- User mentions a UI element by family ("slider", "tab", "modal", "feed") → name adjacent patterns + real product examples
- User uses fuzzy adjectives ("delightful", "alive", "calm", "fun") → name 2-3 real-world delight patterns by name
- User uses negation ("not a slider", "shouldn't be a stepper") → name the family of alternatives
- Greenfield prompt with no anchorable language → skip; say "no anchor surfaced, going wide"

**Output format (3-6 items max, one line each):**

```
Vocabulary you might be reaching for:

Interaction patterns
- Snap-to-tier (Apple Music EQ, Stripe pricing): discrete steps on a continuous track. Often what people mean by "not a slider."
- Disclosure pattern (Stripe payment methods): collapsed options that reveal on tap.

Real-world references
- GitHub contribution graph (living state for activity).
- Stardew Valley friendship hearts (silent cumulative score).
- Mughal jharokha (ritual at a fixed time).

Reply 'all', a list of which to anchor on, or 'something else' to keep going.
```

User reply: `all` / list / `something else` / `skip`. Selected items become anchor candidates for Step 3.

### Step 3: Generate concepts

**Input:** Problem + Brief + breakdown + vocabulary candidates.

**Before generating:**

1. List the 5 most predictable solutions for this problem. **Ban them.**
2. Consult `divergence-axes.md` and select 8-10 axes that apply. Assign each concept a different primary axis.
3. Select 2-3 provocation techniques from `creative-provocations.md`. Each must influence at least 1 concept.
4. Select 1 extreme user or context from `persona-lens.md`. At least 1 concept designed for this lens.
5. Open `anchor-library.md`. Decompose the Brief's references into qualities (e.g., "Disco Elysium" → fragmented narrative, internalization-as-mechanic, deadpan absurdity). Pick within-bucket anchors whose qualities match — see the "When a Brief is present, taste-profile within bucket" section in that file.

**Generate 8-10 concepts. Each emits:**

| Field | What it answers |
|-------|----------------|
| **Name** | Evocative 2-3 word concept name |
| **What this product believes** | One sentence. What this product *believes* about the problem. |
| **Core mechanic** | The single interaction/system behavior that defines it. |
| **Modality** | Input (how user expresses intent) → Output (what the system shows / does) → Feedback loop (what the user gets back). One line. From doc.cc/syntax/interface — concepts that share all three modalities are usually layout variations. |
| **Structural thesis** | One rigorous sentence stating the structural difference. References the Main thing from the Brief. Example: "Treats agents as a household garden because the Brief said this needs to feel ALIVE not surveilled — gardens reward attention with growth instead of demanding it with metrics." |
| **What the user no longer has to do** | The effort or decision this concept eliminates. |
| **What it gives up** | The tradeoff. Be honest. |
| **Anchor** | A real, named thing this concept's MECHANIC borrows from. Pull from `anchor-library.md` with Brief taste-profiling. Googleable. |
| **Delight moment** | The single sensory instant (≤30s) where the user feels something. Names the real-world reference (parenthetical). Pull from `anchor-library.md`. |
| **Where the idea came from** | Which technique / lens / axis combination generated this. |
| **First scene to build** | The single screen/moment to build first. |

**Anchor and Delight examples (cross-bucket):**

```
- Snap-to-tier (Apple Music EQ)                       — software pattern
- Stardew Valley friendship hearts                    — game mechanic
- Mughal jharokha (daily balcony moment)              — historical ritual
- F1 pit stop choreography                            — sport
- Wes Anderson chapter card                           — cinema
- Disco Elysium Thought Cabinet                       — game (slow internalization)
- Kintsugi gold seams                                 — craft
- Brian Eno's Music for Airports (generative ambient) — music
- Quaker meeting silence                              — ritual
- Borges Library of Babel                             — literature
```

**Anchor / Delight Googleable gate:**
Each Anchor and each Delight moment must name a real, Googleable thing. The user must be able to look it up and find a real artifact. Replace invented fluff. The gate kills "spaceship console" and similar; it does NOT kill ambition. "Bloomberg Terminal density on a phone" is real. "Tamagotchi as inbox" is real. "Mughal jharokha for daily standup" is real.

**Delight moment quality gates:**
- *Load-bearing:* if removed, would the concept still feel novel? If yes, the delight is decorative — replace with one that reinforces the mechanic.
- *No-cringe (4 questions):* (1) Does this reward real behavior, or just decorate it? (2) Would users still value it after week 3? (3) Can it be ignored without breaking the workflow? (4) Does it create pride, not chores? Any "no" → replace. Bribery patterns (XP for opening, badges for reading) fail.

**Cross-bucket diversity quota:**

| Domain bucket | Min anchors | Min delight refs |
|---|---|---|
| Video games (specific titles) | 2 | 1 |
| Arts / cinema / music / literature / mythology | 2 | 2 |
| History / ritual / sport / craft / architecture | 2 | 1 |
| Domestic / social / fashion | 1 | 1 |
| Software / SaaS / consumer app | at most 3 | at most 3 |

**Other diversity requirements:**
- At least 2 concepts remove the need for a traditional screen
- At least 2 rely heavily on automation or agent behavior
- At least 2 invert the problem (avoid/reduce/delegate rather than do)
- At least 1 feels like a serious professional power tool
- At least 1 generated from a creative provocation (not just axis combination)
- At least 1 designed for a non-obvious user or context

### Step 4: Kill ledger (NEW — runs before user sees concepts)

Before showing the comparison table, run the kill ledger from `references/concept-enrichment.md` ("Kill ledger" section). For each concept:

- **Decision:** Keep | Rewrite | Kill
- **Fatal flaw** (if Rewrite or Kill): one specific line
- **Required revision** (if Rewrite): one line of what to change

**Kill criteria (any one is enough):**
1. Interchangeable Structural thesis with another concept → kill the weaker
2. Foundation veto (impossible latency / trust / data / autonomy in user's context) → kill or flag risky
3. Anchor monoculture (3+ concepts in same bucket, no orthogonal axis) → kill weakest
4. Layout variation (only visual / copy / layout differs from another) → kill weaker
5. Off the Main thing in the Brief → kill
6. Anchor or Delight fails Googleable gate → rewrite
7. Conflicts with consistency contract without earning the conflict → rewrite

No praise quota. The ledger is doing one job: thinning the set.

**Honesty gate:** on ordinary non-trivial runs, zero Kill/Rewrite requires explicit justification. Reason out loud why every concept passed.

**User sees only Keep + Rewritten concepts in Step 5.** The Killed list is a one-line summary at the bottom; user can ask to revive any.

### Step 5: Compare and pick

Present a compact comparison table of the surviving concepts (Keep + Rewritten):

| Concept | Modality | User Effort | System Intelligence | Risk Level | How it dies | Where the idea came from |

**How it dies:** see `concept-enrichment.md` "How each concept dies" — be specific about who, what, when.

Then answer:
- Which 3 are most structurally promising and why?
- Which 1 is the "dangerous" idea (brilliant or terrible)?

Ask the user: **"Which concepts should I prototype? Pick 2-4, or say 'surprise me.'"**

(Note: duplicate detection now happens in Step 4's kill ledger, not here.)

### Step 6: Deepen the picks

For shortlisted concepts (or top 3 if "surprise me"):

Read `concept-enrichment.md` — sections **Hybrid combinations**, **Day-in-the-Life Narratives**, **Simplicity pass**, and **Picking what to prototype**.

1. **Hybrid combinations:** From shortlisted, attempt 2-3 hybrids. Swap if more interesting than the weakest pick.
2. **Day-in-the-Life:** 3-paragraph narrative per concept (trigger / interaction / aftermath). Diary-entry tone, not press release.
3. **Simplicity pass:** for each shortlisted concept, write a one-line before/after — what can be removed, combined, or hidden without killing the concept. If identical, the gate failed.
4. **Real-world states:** for each shortlisted concept, describe how it handles the states the Brief named (empty / error / loading / first-time / long-content). Substantively different from happy path. "Loading shows a spinner" is not a state.
5. **Picking what to prototype:** decision framework table (signal strength, feasibility, risk of skipping, team conviction).

Ask: **"Ready to prototype? Or want to explore any hybrids further?"**

### Step 7: Build it

Ask one question, wait:

```
Step 7 output:
  (a) React prototype with DialKit (interactive, tunable, ~10 min build)
  (b) Paper canvas with one artboard per concept (visual side-by-side, fast, no code)
  (c) Both — Paper first, React only for the favorites you pick
```

Don't auto-pick. Wait.

#### Robustness layer (applies to all build paths)

- **Slug sanitization:** convert problem name → `[a-z0-9-]+` only for `diverge-[slug]/` directory naming. Strip apostrophes, punctuation, spaces (replace with `-`), lowercase. Truncate to 40 chars.
- **Overwrite protection:** if `diverge-[slug]/` already exists, append a timestamp suffix `diverge-[slug]-YYYY-MM-DD-HHMM/` to the new run. Don't silently overwrite prior work.
- **Prototype-safe Brief summary:** before writing artifact files, generate a derivative of the Brief that strips PII, customer names, API keys, internal URLs. The full Brief is used in conversation; the prototype-safe summary is what lands in code/artboards.
- **HTML escape:** when writing user-provided strings to Paper artboards via `write_html`, escape `& < > " '`. Curated strings (Anchors, Delight references, axis labels) are skill-controlled and don't need escaping.

#### Option (a): React prototype

Read `references/picker-template.md` for the full template.

**App structure:**
```
diverge-[slug]/
├── index.html
├── package.json          (vite + react deps)
├── vite.config.js
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── concepts/
    │   ├── concept-1.jsx
    │   └── ...
    ├── components/
    │   ├── ConceptNav.jsx
    │   ├── ConceptMeta.jsx
    │   └── DialKitPanel.jsx
    └── styles.css
```

**Key rules:**
1. Each concept exports `{ id, name, premise, modality, structuralThesis, anchor, delight, mechanic, sacrifices, axes, controls, Scene }`
2. Scene receives `{ values }` from DialKit and responds in real-time
3. DialKit controls reflect the *mechanism*, not cosmetics
4. 3-6 controls per concept
5. After scaffolding: `npm install && npm run dev`

Apply the prototype-output bans from `picker-template.md` (universal: no Acme/John Doe/fake metrics/Elevate copy/three-equal-cards/AI-Purple/Pure-Black/emoji-as-icons; conditional on Brief consistency contract: font and color choices match the Brief's named design system).

#### Option (b): Paper canvas

Read `references/paper-canvas-template.md` for the artboard layout, MCP call order, and HTML conventions.

**Summary:**
1. `get_basic_info`, `get_font_family_info`
2. For each concept: `create_artboard` (1440 × 900 default; 390 × 844 mobile), then `write_html` for header strip / main scene / anchor card / delight card / meta strip
3. `get_screenshot` per artboard
4. `finish_working_on_nodes` at the end

Each artboard contains: header strip (concept name + believes), main scene (first scene to build), anchor card, delight card, meta strip (Modality + axes + idea source + Structural thesis as bottom line). Structural thesis stays in meta strip, NOT header — keeps the visual clean.

Apply the same prototype-output bans as the React picker, plus Paper-specific: no emojis as icons, no fake stock photos.

#### Option (c): Both

Run option (b) first — Paper gallery for visual range. After user picks 1-3 favorites, run option (a) for those concepts only. Saves the time of building 8-10 React scenes when only a few will be tuned.

---

## Output Format

```
## Diverge: {PROBLEM}

### Brief
[interview answers + skill-inferred fields]

### Break down the problem (Step 1.C)
- JTBD: [3 statements]
- Real constraint: [primary + secondary]
- Eliminate the problem: [statement]
- Similar problems in other fields: [2 domains + mechanisms]

### Vocabulary surfaced (Step 2)
[3-6 named patterns/components/references — or "skipped, going wide"]

### Banned directions (predictable solutions removed)
- [5 banned solutions]

### Provocation techniques selected
- [2-3 techniques + 1 lens]

### Concepts generated: {N}
[concept tables]

### Kill ledger (Step 4)
[Keep / Rewrite / Kill labels per concept]
Killed: [one-line reason per killed concept]

### Compare and pick (Step 5)
[comparison table on survivors + picks]

### Deepen the picks (Step 6)
[hybrids + narratives + simplicity passes + real-world states + decision table]

### Built (Step 7)
Output type: [React prototype / Paper canvas / Both]
Location: [path or canvas]
Concepts included: [list]
```

---

## Output Budget

| Step | Budget |
|------|--------|
| Step 1 (Brief + breakdown) | 250-350 words |
| Step 2 (Surface vocabulary) | 50-100 words |
| Step 3 (Generate concepts) | 8-10 concepts × ~120 words each = 1000-1200 words |
| Step 4 (Kill ledger) | 1-2 lines per concept × 10 + Killed summary = ~150-200 words |
| Step 5 (Compare and pick) | Comparison table + 100-150 words commentary |
| Step 6 (Deepen the picks) | 3 narratives × 200 + simplicity + states + decision table = ~900 words |
| Step 7 (Build it) | Code or canvas output (no word budget) |

Total text output before building: ~2700 words.

## Technique Rotation

Each run should use a different combination of provocation techniques. The libraries (7 techniques, 8 extreme users, 6 time budgets, 8 contexts) have enough combinations to never repeat.

---

## When to use parallel agents

| Step | Strategy |
|------|----------|
| Step 1 | Main conversation |
| Step 2 | Main conversation |
| Step 3 | Parallel subagents (optional, when problem space is broad) |
| Step 4 | Main conversation (kill ledger requires holistic view) |
| Step 5 | Main conversation |
| Step 6 | Parallel subagents for narratives |
| Step 7 (React) | Parallel subagents for Scene components |
| Step 7 (Paper) | Main conversation (Paper MCP must be sequential) |

**Subagent briefing rules:**
- **Every parallel subagent prompt MUST include the Brief block in full.** Without the Brief, taste calibration vanishes — fall back to single-thread.
- Always include the problem statement, breakdown, vocabulary, and concept table format.
- Always specify which axes/techniques the agent should use.
- After agents return, run the kill ledger in the main conversation on the merged set.

**Parallel concept generation example (Step 3):**

```
Agent 1: "Generate 4 concepts for [problem] using axes [A, B, C, D] and 
         provocation [X]. Each concept must have all required fields including 
         Modality and Structural thesis. Anchor and Delight must be Googleable 
         and pulled with Brief taste-profiling.

         Brief: [paste full Brief block]
         Vocabulary anchors: [paste from Step 2]
         [paste concept table format]"

Agent 2: "Generate 4 concepts for [problem] using axes [E, F, G, H] and 
         provocation [Y] + lens [Z]. [same format + Brief]"
```

---

## Edge Cases

- **User provides a solution, not a problem** — Reframe: "You've described a solution. The problem underneath seems to be [X]. I'll diverge on the problem."
- **User asks for < 5 concepts** — Generate 8-10 internally, surface only the requested count, selecting for maximum range.
- **User asks for "variations"** — Redirect: "Variations optimize within one direction. Diverge generates different directions."
- **Problem is too broad** — Ask one sharpening question. No more.
- **Problem is too narrow** — Widen one level. State what you widened.
- **User says "skip brief"** — Self-generate degraded Brief from prompt; mark output as DEGRADED at top.
- **User says "quick" or "just brainstorm"** — Run Steps 1-5 only, skip 6 and 7.
- **User says "surprise me"** — Top 3 by maximum structural range, proceed to Step 6 and 7.
- **Vocabulary surface yields nothing useful** — say "no anchor surfaced, going wide" and proceed; Step 3 still requires Anchor.

## What This Skill Is NOT

- Not a UI polish tool (use `/design`)
- Not a variation generator
- Not a wireframing tool
- Not converging — explicitly avoids premature optimization
- Not exhaustive — selects from technique libraries, doesn't apply all of them
