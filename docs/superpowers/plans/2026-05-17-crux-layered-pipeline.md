# Crux Layered Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `crux` so it reasons through a fixed, layered dao/qi pipeline with method-specific subagents when available, then renders one cohesive, simple, adaptive answer that exposes the core and gives the user better ways to frame the problem.

**Architecture:** Keep `plugins/design/skills/crux/SKILL.md` as the compact runtime contract. Add one reference file for the fixed pipeline, update examples and evals so they reward cohesive synthesis instead of field completion, and add minimal `agents/openai.yaml` metadata for discoverability. The pipeline is fixed; the visible answer shape is adaptive.

**Tech Stack:** Markdown skill files, Dex skill conventions, `python3`, system `quick_validate.py`, `rtk`, `rg`, YAML metadata.

---

## File Structure

Modify:

- `plugins/design/skills/crux/SKILL.md`
  Replace the worksheet-style visible response contract with a fixed internal pipeline and adaptive rendering contract.

- `plugins/design/skills/crux/references/examples.md`
  Replace the canonical example so it teaches cohesive output, better framing, and idea expansion from the core.

- `plugins/design/skills/crux/evals/core-behavior.md`
  Update pass criteria and cases so evals reject fragmented framework output and reward the layered pipeline.

Create:

- `plugins/design/skills/crux/references/layered-pipeline.md`
  Define the fixed method DAG, method-agent responsibilities, intermediate artifacts, parallel stages, collation, and final adaptive rendering rules.

- `plugins/design/skills/crux/agents/openai.yaml`
  Add minimal UI metadata matching sibling design skills.

Do not create:

- README files
- process notes outside the skill
- executable scripts unless a later eval runner proves the need
- extra reference files for every method; keep the pipeline one hop from `SKILL.md`

---

## Runtime Contract

`crux` should use the fixed layered pipeline for non-trivial crux work. If subagents are available and permitted in the active environment, assign method agents to the fixed DAG. If subagents are unavailable, run the same DAG internally in one thread and preserve the same intermediate artifacts mentally.

The user must not see the pipeline as a report. The final answer should read like one clear diagnosis. It should explain the core in plain language, show what the current frame hides, offer better ways to frame the problem, and leave the user with more useful directions than they had before.

Fixed internal methods:

- intake
- ground truth pass
- naming pressure
- evidence ledger
- context map
- dao extraction
- qi inspection
- reversal / opposite-truth
- crux candidate collation
- weak joint selection
- specific bet formulation
- crude test design
- final question selection
- essence writing
- reframing generation
- opportunity expansion
- cohesion pass

Visible output rules:

- Use adaptive rendering, not a fixed template.
- Do not expose `dao`, `qi`, `evidence type`, or method labels unless the user asks for the method.
- Lead with the biggest flaw or the core insight when critique is requested.
- Keep the answer detailed enough to be useful and simple enough for a non-method reader.
- Give the user better frames, sharper questions, or new product/research/positioning directions when that helps them act.

---

### Task 1: Add the Fixed Layered Pipeline Reference

**Files:**
- Create: `plugins/design/skills/crux/references/layered-pipeline.md`

- [ ] **Step 1: Create the reference file**

Create `plugins/design/skills/crux/references/layered-pipeline.md` with this content:

````markdown
# Layered Pipeline

Use this for non-trivial crux work: strategy, product framing, PRDs, design direction, source artifacts, repo-backed plans, loaded language, emotionally charged claims, or any problem where one quick question would miss the structure.

The pipeline is fixed. The visible answer is adaptive.

## Method Agents

When subagents are available and permitted, use one method agent per method group. When subagents are not available, run the same methods internally in the same order.

Do not show method-agent outputs to the user. Each method produces an intermediate artifact for later stages.

## Fixed DAG

```text
0. Intake
   ↓
1. Ground Truth Pass
   ↓
2A. Naming Pressure      2B. Evidence Ledger      2C. Context Map
   ↓                     ↓                       ↓
3A. Dao Extraction       3B. Qi Inspection        3C. Reversal / Opposite-Truth
        \                 |                       /
         \                ↓                      /
          → 4. Crux Candidate Collation ←
                         ↓
5A. Weak Joint Selection     5B. Specific Bet Formulation
             \               /
              → 6. Crude Test Design
                         ↓
7. Final Question Selection
                         ↓
8A. Essence Writer
                         ↓
8B. Reframing Generator      8C. Opportunity Expander
             \               /
              → 8D. Final Cohesion Pass
```

## Stage Contracts

### 0. Intake

Input: user request.

Output:

```text
surface claim:
user intent:
stakes:
provided artifacts:
visible decision:
```

Do not solve the problem here. Normalize what kind of crux work this is.

### 1. Ground Truth Pass

Input: intake.

Inspect files, docs, code, screens, pasted text, issue language, or conversation context before reasoning from the user's wording.

Output:

```text
observed facts:
user terms:
artifact terms:
contradictions:
missing evidence:
source reliability:
```

Every later method must use this as source of truth. If no external source exists, say the source is only the user's claim.

### 2A. Naming Pressure

Runs in parallel with `2B` and `2C`.

Input: ground truth pass.

Job: convert loaded nouns and style words into observable behavior.

Examples:

- `deep` → higher retention from one capability
- `wide` → more surface area across adjacent jobs
- `trust` → user delegates a high-risk action or accepts a recommendation
- `premium` → status signal, lower perceived risk, refined hierarchy, or enterprise readiness
- `simple` → fewer steps, fewer choices, lower cognitive load, faster first success, or lower visual density

Output:

```text
loaded terms:
behavior translations:
terms still ambiguous:
```

### 2B. Evidence Ledger

Runs in parallel with `2A` and `2C`.

Input: ground truth pass.

Job: classify each load-bearing claim as perception, inference, analogy, testimony, taste, social proof, memory, or assumption.

Output:

```text
claim evidence:
strongest evidence:
weakest evidence:
claims pretending to know more than they know:
```

Treat frameworks, analogies, market maps, and business-model language as inference unless tied to observed behavior.

### 2C. Context Map

Runs in parallel with `2A` and `2B`.

Input: ground truth pass.

Job: map the system around the claim.

Output:

```text
actors:
incentives:
constraints:
handoffs:
decision rights:
failure points:
feedback loops:
```

This prevents a clever crux from ignoring the real system.

### 3A. Dao Extraction

Runs after `2A`, `2B`, and `2C`.

Input: naming pressure, evidence ledger, and context map.

Job: name the invisible operating principle, invariant, or causal model.

Output:

```text
dao:
what must stay true:
what the current frame hides:
```

Example: "This is not about going wide or deep. It is about whether one capability creates enough customer pull to survive incumbent entry."

### 3B. Qi Inspection

Runs after `3A` and the ground truth pass.

Input: dao and grounded facts.

Job: inspect whether the visible expression carries or contradicts the dao.

Visible expression can mean product shape, feature, interface, workflow, roadmap, strategy phrase, deck slide, or written claim.

Output:

```text
qi:
where qi supports dao:
where qi contradicts dao:
```

### 3C. Reversal / Opposite-Truth

Runs after `2A` and `2C`.

Input: naming pressure and context map.

Job: find where the opposite claim is true, where both claims are true, and what framing makes the original debate irrelevant.

Output:

```text
where original is true:
where opposite is true:
where both are true:
better frame:
```

Use this to dissolve prestige abstractions without making "avoid binaries" the whole answer.

### 4. Crux Candidate Collation

Input: dao extraction, qi inspection, and reversal.

Output:

```text
candidate avoided realities:
candidate weak joints:
candidate specific bets:
candidate tests:
candidate crux questions:
discarded clever lines:
```

Discard anything that sounds elegant but would not change the work.

### 5A. Weak Joint Selection

Runs in parallel with `5B`.

Input: collated candidates.

Job: choose the one place the idea is most likely lying to itself.

Output:

```text
weak joint:
why this is the weak joint:
what would change if it fails:
```

### 5B. Specific Bet Formulation

Runs in parallel with `5A`.

Input: collated candidates.

Job: rewrite the strategy as a concrete bet.

Output:

```text
specific bet:
customer:
moment:
capability:
behavior change:
reason:
commitment signal:
```

Use this shape internally:

```text
For [customer], in [moment], [capability] changes [behavior], because [reason]. We know it works if [commitment signal].
```

Do not force this exact sentence into the final answer if another shape reads better.

### 6. Crude Test Design

Input: weak joint and specific bet.

Job: design the smallest test that reduces uncertainty by measuring commitment, not praise.

Output:

```text
test:
success signal:
failure signal:
desirability signal:
feasibility signal:
viability signal:
legibility signal:
time to test:
what it teaches:
```

### 7. Final Question Selection

Input: weak joint, specific bet, and crude test.

Job: choose the one question whose answer changes the direction of the work.

Output:

```text
crux question:
why this question decides the matter:
```

Most responses should end with this question. If the user needs a concrete answer, recommendation, or rewrite more than a question, place the decisive line last instead.

### 8A. Essence Writer

Input: selected weak joint, specific bet, crude test, and final question.

Job: explain the core in simple language.

Output:

```text
essence:
plain-language explanation:
```

The essence should make the user understand what is really at stake.

### 8B. Reframing Generator

Runs after `8A` and in parallel with `8C`.

Input: essence.

Job: give the user better ways to frame the conversation.

Output:

```text
better frames:
questions to ask instead:
terms to replace:
```

A better frame must move the user closer to a customer, moment, behavior, capability, proof, or tradeoff.

### 8C. Opportunity Expander

Runs after `8A` and in parallel with `8B`.

Input: essence.

Job: show the ideas that open up once the core is understood.

Output:

```text
product directions:
research directions:
positioning directions:
roadmap directions:
```

Do not brainstorm from the original bad frame. Expand from the essence.

### 8D. Final Cohesion Pass

Input: essence, reframes, opportunities, test, and final question.

Job: render one human answer.

Rules:

- Use active voice.
- Use concrete nouns.
- Keep related ideas together.
- Omit method labels unless the user asks for the method.
- Use sections only when they improve scanning.
- Make each paragraph cause the next paragraph.
- Lead with the biggest flaw when critiquing.
- Define style or strategy words through observable mechanics.
- Do not fill a fixed template.
- End with the crux question unless a recommendation, rewrite, or next test is more useful.

## Adaptive Rendering

The final answer takes the shape of the topic:

- Strategy: a short memo that refuses the weak frame, states the real bet, names the weak joint, and offers better frames.
- Product idea: a diagnosis of the painful moment, specific bet, crude test, and next questions.
- Design critique: biggest flaw first, weak joint named, mechanics explained, better directions offered.
- Naming or copy: sharper language, why it works, what it replaces, what behavior it should create.
- PRD or repo-backed plan: observed source pressure, contradiction, deciding assumption, test, and crux question.
- Vague style request: translate words into hierarchy, density, contrast, motion, copy, interaction, or behavior.

The final answer should leave the user with more usable ideas because the core is clearer.
````

- [ ] **Step 2: Verify the reference file exists**

Run:

```bash
test -f plugins/design/skills/crux/references/layered-pipeline.md && echo "layered pipeline reference exists"
```

Expected:

```text
layered pipeline reference exists
```

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/crux/references/layered-pipeline.md
git commit -m "docs: add crux layered pipeline"
```

---

### Task 2: Wire the Pipeline Into `crux`

**Files:**
- Modify: `plugins/design/skills/crux/SKILL.md`

- [ ] **Step 1: Add the reference loading entry**

In `plugins/design/skills/crux/SKILL.md`, add this bullet under `## Reference Loading` after `references/protocol.md`:

````markdown
- `references/layered-pipeline.md` - load for non-trivial crux work that needs the fixed method pipeline, method-agent fan-out, collation, adaptive rendering, or deeper product/strategy/design pressure.
````

- [ ] **Step 2: Replace the operating contract list**

Replace the sentence `For every input, produce the smallest useful version of:` and its bullet list with:

````markdown
For every input, think through the load-bearing methods:

- surface claim: what was said
- hidden premise: what must be true for the claim to hold
- evidence type: perception, inference, analogy, testimony, taste, social proof, memory, or assumption
- standard of judgment: precedent, actual user experience, concrete benefit, and success signal
- dao: invisible operating principle, model, invariant, or causal structure
- qi: visible expression, artifact, feature, interface, workflow, sentence, or opinion
- weak joint: where the idea is most likely lying to itself
- crude test: the smallest experiment that reduces uncertainty
- crux question: the direct question whose answer changes the direction of the work

Do not expose every method as an output section. The methods are internal pressure tools. The visible answer should be cohesive, plain, and adaptive to the topic.
````

- [ ] **Step 3: Add a pipeline mode section after `## Source-Backed Crux`**

Insert this section after the `Source-Backed Crux` section:

````markdown
## Layered Pipeline Mode

For non-trivial crux work, load `references/layered-pipeline.md` and use the fixed method DAG.

Use method subagents when they are available and permitted by the active environment. Assign each subagent one method group, pass only the prior-stage artifact it needs, and ask it for an intermediate artifact, not user-facing prose. If subagents are unavailable, run the same stages internally in one thread.

The pipeline is fixed:

1. intake
2. ground truth pass
3. parallel naming pressure, evidence ledger, and context map
4. dao extraction, qi inspection, and reversal / opposite-truth
5. crux candidate collation
6. parallel weak joint selection and specific bet formulation
7. crude test design
8. final question selection
9. essence writing
10. parallel reframing generation and opportunity expansion
11. final cohesion pass

Do not show the pipeline to the user. Synthesize it into one readable answer.
````

- [ ] **Step 4: Tighten the internal loop**

In `## Internal Loop`, replace item 3 with:

````markdown
3. For non-trivial inputs, run the layered pipeline: ground truth first, parallel naming/evidence/context pressure, dao/qi/reversal, collation, weak-joint selection, specific-bet formulation, crude test, final question, essence, reframing, opportunity expansion, and cohesion.
````

Replace item 4 with:

````markdown
4. Discard anything generic, clever without pressure, disconnected from evidence, or answerable without changing the work.
````

- [ ] **Step 5: Replace `## Response Shape`**

Replace the entire `## Response Shape` section with:

````markdown
## Adaptive Rendering

Do not use one fixed template.

Choose the answer shape that best serves the topic:

- Strategy: refuse the weak frame, name what it avoids, state the real bet, expose the weak joint, offer better frames, and end with the deciding question.
- Product idea: name the painful moment, state the specific bet, show the smallest test, and ask the crux question.
- Design critique: lead with the biggest flaw, name the weak joint, translate style words into mechanics, and offer better directions.
- Naming or copy: give sharper language, explain what behavior it creates, and show what old framing it replaces.
- PRD or source-backed plan: show observed source pressure, contradiction, deciding assumption, test, and crux question.
- Vague style request: convert words like "impactful", "premium", "simple", "bold", or "dynamic" into hierarchy, contrast, density, motion, copy, interaction, or behavior.

Use sections only when they improve scanning. The answer can be detailed, but it must read as one line of thought.

The final answer should usually include:

- the current frame or claim
- what that frame hides
- the core in simple language
- the specific bet or decision pressure
- the weak joint
- a small test when it reduces uncertainty
- better ways to frame the problem when useful
- the crux question or decisive next move

Never include every item by default. Select the moves that make this case clearer.
````

- [ ] **Step 6: Add user-summary rules to `## Output Rules`**

Add these bullets near the top of `## Output Rules`:

````markdown
- The final answer must be simple enough for the user to repeat to another person.
- Prefer active voice, concrete nouns, short paragraphs, and direct causal links.
- Do not output a bundle of disconnected framework sections.
- Give better frames, sharper questions, or new directions when the core insight opens them up.
- If the user's frame is prestige abstraction, status-safe strategy language, or a false category debate, refuse the frame and move one level down into customer, moment, capability, behavior, proof, and tradeoff.
````

- [ ] **Step 7: Run text checks**

Run:

```bash
rg -n "Layered Pipeline Mode|Adaptive Rendering|layered-pipeline|method subagents|prestige abstraction|dao|qi" plugins/design/skills/crux/SKILL.md
```

Expected: matches for the new reference, pipeline mode, adaptive rendering, subagent rule, prestige-abstraction rule, and retained dao/qi terms.

- [ ] **Step 8: Commit**

```bash
git add plugins/design/skills/crux/SKILL.md
git commit -m "docs: teach crux layered adaptive reasoning"
```

---

### Task 3: Update Examples to Teach Cohesive Output

**Files:**
- Modify: `plugins/design/skills/crux/references/examples.md`

- [ ] **Step 1: Replace the canonical example**

Replace the existing canonical example block with:

````markdown
## Canonical Example

User: "I want to build an AI writing assistant for designers."

```text
The weak joint is that you have named the AI surface before proving the painful writing moment.

The core is not "designers need writing help." The core is whether designers repeatedly face writing moments where quality changes a real outcome: stakeholder trust, approval speed, reputation, alignment, or confidence to send.

One level down, the bet is: designers will use a dedicated assistant if it helps them handle high-stakes communication better than generic ChatGPT, Grammarly, peer review, or delay. That bet is still mostly assumption until you see past behavior.

A better way to frame it:
- Instead of asking "Should we build an AI writing assistant?", ask "Which writing moment makes designers spend real effort before they send?"
- Instead of debating assistant features, find the last message a designer rewrote, delayed, escalated, or asked someone else to fix.
- Instead of proving that designers like better writing, prove they already pay a cost when writing is risky.

The smallest useful test is to interview 10 designers about the last high-stakes message they sent. Collect the original draft, final draft, time spent, stakes, workaround, and whether generic AI helped. It works if most can name a recent moment with real cost. It fails if examples are hypothetical, low-stakes, or already solved by generic tools.

Crux question: Would this still matter if ChatGPT already wrote clean English perfectly?
```
````

- [ ] **Step 2: Replace the good skeleton**

Replace the `Good:` example with:

````markdown
Good:

```text
The weak joint is that the solution is named before the painful moment is proven.

The real question is not whether designers need an assistant. It is whether there is a recurring writing moment where quality changes the outcome and existing tools do not remove the risk.

Better frame: "Which message did a designer recently rewrite, delay, escalate, or ask someone else to fix?"

Crux question: Would this still matter if generic ChatGPT already wrote clean English perfectly?
```
````

- [ ] **Step 3: Add a strategy-framing example**

Append this section after `## Bad vs Good`:

````markdown
## Strategy Frame Example

User: "Should we go wide or deep now that two incumbents entered our space?"

```text
The weak joint is the altitude of the question. "Wide or deep" lets the room debate product shape before naming the customer pull that would make any shape defensible.

The core is simpler: which specific capability would make a specific customer switch, buy, stay, or expand despite the incumbents?

One level down, the bet should sound like this: for this customer, in this painful moment, this capability changes this behavior, and we know it works if they commit time, money, data, workflow, or reputation to it.

A better way to frame it:
- Instead of asking "wide or deep?", ask "which customer moment can we win so clearly that product shape follows?"
- Instead of debating platform versus point solution, decide what capability creates pull.
- Instead of citing market analogies, look for the last failed sale, retained user, workaround, or support thread that proves the pain.

Crux question: What capability would make one specific customer change behavior enough to buy and stay?
```
````

- [ ] **Step 4: Run example checks**

Run:

```bash
rg -n "Canonical Example|Strategy Frame Example|wide or deep|better way to frame|Crux question" plugins/design/skills/crux/references/examples.md
```

Expected: matches for the updated canonical example and new strategy example.

- [ ] **Step 5: Commit**

```bash
git add plugins/design/skills/crux/references/examples.md
git commit -m "docs: update crux examples for cohesive synthesis"
```

---

### Task 4: Update Evals for Pipeline and Adaptive Rendering

**Files:**
- Modify: `plugins/design/skills/crux/evals/core-behavior.md`

- [ ] **Step 1: Replace pass criteria**

Replace the current `## Pass Criteria` list with:

````markdown
## Pass Criteria

- Output reads as one cohesive line of thought, not a worksheet.
- The agent thinks through the crux methods internally without exposing every method as a visible section.
- For non-trivial inputs, behavior reflects the fixed layered pipeline: ground truth, naming pressure, evidence ledger, context map, dao, qi, reversal, collation, weak joint, specific bet, crude test, final question, essence, reframing, opportunity expansion, and cohesion.
- Subagents are used for method groups when they are available and permitted; otherwise the same method DAG is run internally.
- Final answer shape is adaptive to the topic.
- Final answer is detailed enough to teach the core and simple enough for the user to repeat.
- Output has at most two supporting questions plus one final crux question unless the user explicitly asks for deeper interrogation.
- Final move is usually the crux question, but may be a decisive recommendation, rewrite, or next test when that better serves the user.
- No named-lens leakage unless the user asks for the method.
- Evidence type is not inflated; inference and assumption are named plainly when relevant.
- Crude tests measure commitment, not praise.
- Product or design claims include legibility pressure when relevant.
- If the user provides a file/path/artifact, the agent inspects it before questioning it.
- If artifacts contain relevant terminology, output distinguishes user language from artifact language.
- If artifact truth contradicts user framing, the contradiction becomes the weak joint.
- Questions answerable from provided files are replaced with observed facts.
- Scenario wedges are concrete and boundary-forcing, not generic examples.
- Crux does not write or update docs unless explicitly requested.
````

- [ ] **Step 2: Update case 1 expected behavior**

Replace case 1's expected behavior with:

````markdown
Splits `premium` and `simple` internally; visible answer explains what those words could mean in behavior or interface mechanics; final pressure tests whether the issue is status, cognitive load, first success, visual density, or another observable outcome.
````

- [ ] **Step 3: Add strategy frame regression case**

Add this row after case 2:

````markdown
| 3 | "Should we go wide or deep now that incumbents entered our space?" | Refuses the altitude of the frame; moves one level down to customer, moment, capability, behavior, proof, and tradeoff; offers better ways to frame the decision; asks which specific capability would make a specific customer change behavior enough to buy or stay. |
````

Then renumber the existing cases so the table remains sequential.

- [ ] **Step 4: Add fragmented-output regression case**

Add this row near the end of the table:

````markdown
| 18 | "Find the crux of this strategy: platform vs point solution, CAC vs LTV, wide vs deep." | Does not produce disconnected sections for every framework term; names the status-safe abstraction pattern, explains what reality it avoids, translates the issue into a specific bet, and gives better frames for the user to use instead. |
````

- [ ] **Step 5: Replace the good skeleton**

Replace the `Good skeleton` block with:

````markdown
Good skeleton:

```text
The weak joint is [where the claim protects itself].

The core is [plain explanation of what is really at stake].

One level down, the real bet is [customer / moment / capability / behavior / proof].

Better frames:
- [more concrete way to ask the question]
- [more useful decision frame]

Crux question: [what would change the direction]
```
````

- [ ] **Step 6: Run eval checks**

Run:

```bash
rg -n "cohesive|fixed layered pipeline|wide or deep|fragmented|Better frames|Good skeleton|Subagents" plugins/design/skills/crux/evals/core-behavior.md
```

Expected: matches for cohesive output, pipeline behavior, strategy-frame regression, fragmented-output regression, and better-frame output.

- [ ] **Step 7: Commit**

```bash
git add plugins/design/skills/crux/evals/core-behavior.md
git commit -m "test: cover crux layered cohesive output"
```

---

### Task 5: Add Minimal OpenAI Metadata

**Files:**
- Create: `plugins/design/skills/crux/agents/openai.yaml`

- [ ] **Step 1: Create metadata directory**

Run:

```bash
mkdir -p plugins/design/skills/crux/agents
```

Expected: command exits with status 0.

- [ ] **Step 2: Create `openai.yaml`**

Create `plugins/design/skills/crux/agents/openai.yaml` with:

````yaml
interface:
  display_name: "Crux"
  short_description: "Find the core bet behind a claim"
  default_prompt: "Use $crux to pressure this claim, find the weak joint, and reframe it around the core bet."
````

- [ ] **Step 3: Validate YAML shape**

Run:

```bash
python3 - <<'PY'
import yaml
from pathlib import Path

path = Path("plugins/design/skills/crux/agents/openai.yaml")
data = yaml.safe_load(path.read_text())
assert isinstance(data, dict)
assert "interface" in data
for key in ("display_name", "short_description", "default_prompt"):
    assert key in data["interface"], key
print("openai.yaml valid")
PY
```

Expected:

```text
openai.yaml valid
```

- [ ] **Step 4: Commit**

```bash
git add plugins/design/skills/crux/agents/openai.yaml
git commit -m "docs: add crux skill metadata"
```

---

### Task 6: Validate Skill Shape and Diff Hygiene

**Files:**
- Test: `plugins/design/skills/crux/SKILL.md`
- Test: `plugins/design/skills/crux/references/layered-pipeline.md`
- Test: `plugins/design/skills/crux/references/examples.md`
- Test: `plugins/design/skills/crux/evals/core-behavior.md`
- Test: `plugins/design/skills/crux/agents/openai.yaml`

- [ ] **Step 1: Validate skill frontmatter and naming**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/crux
```

Expected:

```text
Validation passed
```

If the exact success text differs, accept a zero exit code and no reported errors.

- [ ] **Step 2: Check reference reachability**

Run:

```bash
rg -n "references/layered-pipeline.md|references/examples.md|references/protocol.md" plugins/design/skills/crux/SKILL.md
```

Expected: `layered-pipeline.md`, `examples.md`, and `protocol.md` are all referenced from `SKILL.md`.

- [ ] **Step 3: Check no fixed final template leaked back in**

Run:

```bash
rg -n "You are framing this as \\[current frame\\]|One level down, the real bet is: \\[|The weak joint is: \\[" plugins/design/skills/crux
```

Expected: no matches.

- [ ] **Step 4: Check no method-report output contract remains**

Run:

```bash
rg -n "^claim:|^hidden premise:|^evidence type:|^standard of judgment:|^dao:|^qi:|^assumption audit:" plugins/design/skills/crux/SKILL.md plugins/design/skills/crux/references/examples.md
```

Expected: no matches in visible response examples or default output contracts. It is acceptable for method names to appear inside internal pipeline instructions.

- [ ] **Step 5: Check diff whitespace**

Run:

```bash
git diff --check -- plugins/design/skills/crux docs/superpowers/plans/2026-05-17-crux-layered-pipeline.md
```

Expected: no output.

- [ ] **Step 6: Check status**

Run:

```bash
git status --short
```

Expected: only the intended plan or implementation files are changed, plus any unrelated pre-existing user files left untouched.

- [ ] **Step 7: Commit validation cleanup if needed**

If Tasks 1-5 produced follow-up edits during validation, commit only those crux files:

```bash
git add plugins/design/skills/crux
git commit -m "test: validate crux layered pipeline"
```

Skip this commit if there are no follow-up edits.

---

### Task 7: Forward-Test the Updated Skill Behavior

**Files:**
- Test: `plugins/design/skills/crux/SKILL.md`
- Test: `plugins/design/skills/crux/references/layered-pipeline.md`
- Test: `plugins/design/skills/crux/references/examples.md`
- Test: `plugins/design/skills/crux/evals/core-behavior.md`

- [ ] **Step 1: Run a strategy-frame forward test**

Use a fresh agent or fresh session. Prompt:

```text
Use $crux at /Users/aditya.nawal/projects/dex/plugins/design/skills/crux to answer:

"Should we go wide or deep now that two incumbents entered our space?"
```

Expected:

```text
The answer refuses the altitude of "wide or deep", explains what reality the frame avoids, states a specific customer/capability/behavior bet, offers better frames, and ends with a decisive crux question or next test.
```

- [ ] **Step 2: Run a vague-style forward test**

Use a fresh agent or fresh session. Prompt:

```text
Use $crux at /Users/aditya.nawal/projects/dex/plugins/design/skills/crux to answer:

"This onboarding should feel premium, simple, and more impactful."
```

Expected:

```text
The answer translates style words into observable mechanics, names the weak joint, avoids generic taste advice, and gives better frames for deciding what the onboarding must change.
```

- [ ] **Step 3: Run a source-backed forward test**

Use a fresh agent or fresh session. Prompt:

```text
Use $crux at /Users/aditya.nawal/projects/dex/plugins/design/skills/crux to inspect /Users/aditya.nawal/projects/dex/plugins/design/skills/crux/evals/core-behavior.md and find the crux of whether the evals still reward fragmented output.
```

Expected:

```text
The answer inspects the file first, cites the observed eval behavior in plain language, treats the file as evidence, and does not ask questions answerable from the file.
```

- [ ] **Step 4: Patch any failed behavior**

If a forward test fails, patch the smallest relevant file:

```bash
git add plugins/design/skills/crux/SKILL.md plugins/design/skills/crux/references/layered-pipeline.md plugins/design/skills/crux/references/examples.md plugins/design/skills/crux/evals/core-behavior.md
git commit -m "fix: tighten crux layered pipeline behavior"
```

Skip this step if all forward tests pass.

- [ ] **Step 5: Final validation**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/crux
git diff --check -- plugins/design/skills/crux
```

Expected: validation passes and `git diff --check` prints no whitespace errors.

---

## Self-Review

Spec coverage:

- Fixed, multi-stage pipeline is covered by Tasks 1 and 2.
- Parallel method-agent stages are covered in the DAG and stage contracts.
- Prior-stage inputs and how each method uses them are covered in Task 1.
- Dao and qi stay named internal methods.
- Adaptive, topic-sensitive rendering is covered by Task 2 and Task 3.
- Simple, detailed, human-readable output is covered by Task 2, Task 3, and the final cohesion rules.
- Better frames and idea expansion are covered by `8B. Reframing Generator` and `8C. Opportunity Expander`.
- Evals reject fragmented framework output in Task 4.
- Skill metadata is covered in Task 5.
- Validation and forward testing are covered in Tasks 6 and 7.

Placeholder scan:

- No `TBD`, `TODO`, "similar to", or undefined implementation steps remain.
- Each file creation task includes exact content.
- Each validation step includes an exact command and expected result.

Type and path consistency:

- All skill paths point to `plugins/design/skills/crux/...`.
- The plan uses the existing system `quick_validate.py`.
- The metadata shape matches sibling design skill `agents/openai.yaml` files.
- The pipeline reference stays one hop from `SKILL.md`, matching skill-creator progressive disclosure guidance.
