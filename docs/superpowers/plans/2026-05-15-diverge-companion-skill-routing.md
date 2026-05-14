# Diverge Companion Skill Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `diverge` so it uses companion design skills at the right moments: `crux` before weak-premise ideation, `content-design` for copy-heavy directions, and 5F-style critique for design-quality review after concepts exist.

**Architecture:** Keep `plugins/design/skills/diverge/SKILL.md` as the runtime orchestrator and avoid turning it into a large doctrine file. Add a small routing section plus one reference file that defines when to hand off, what inputs to pass, and what output to bring back into divergence. Add evals that catch missed companion-skill routing.

**Tech Stack:** Markdown skill files, Dex skill conventions, `rg`, `python3`, system `quick_validate.py`.

---

## File Structure

Modify:

- `plugins/design/skills/diverge/SKILL.md`
  Add companion-skill routing, update compact/deep output expectations, and add quality gates for copy, critique, and premise checks.

Create:

- `plugins/design/skills/diverge/references/companion-skill-routing.md`
  The actual routing contract: when to use `crux`, `content-design`, 5F critique, visual/design-hardening lenses, and when not to route.

- `plugins/design/skills/diverge/evals/companion-skill-routing.md`
  Regression-style examples for missed trigger and over-trigger cases.

Do not create:

- README files
- long process notes outside the skill
- duplicate copies of `content-design`, `crux`, or 5F rules inside `diverge`

---

## Routing Contract

`diverge` should remain the owner of option generation. Companion skills should sharpen a specific phase:

- `crux`: before ideation when the premise, user job, or success criterion is unclear.
- `content-design`: during or after ideation when copy, labels, CTAs, error states, onboarding, empty states, or persuasion materially shape the direction.
- `reviewing-designs-5f`: after concepts exist, when the user asks for critique/review or when choosing between directions needs a quality score across Fast, Focused, Fun, Fluent, and Fair.
- Design hardening / visual lenses: after a direction is selected, when execution quality, accessibility, density, hierarchy, typography, motion, or polish is the core risk.

The skill should not route away just because a direction contains words or UI. Route only when that layer decides whether the concept works.

---

### Task 1: Add Companion Routing Reference

**Files:**
- Create: `plugins/design/skills/diverge/references/companion-skill-routing.md`

- [ ] **Step 1: Create the routing reference**

Create `plugins/design/skills/diverge/references/companion-skill-routing.md` with this content:

````markdown
# Companion Skill Routing

`diverge` owns option generation. Companion skills sharpen specific gates. Do not route for ceremony; route when the companion skill changes the quality of the result.

## Routing Sequence

Use this order:

1. Premise gate
2. Divergence generation
3. Copy/content gate
4. Critique/selection gate
5. Execution-hardening gate

## Premise Gate: Use `crux`

Use `crux` before generating directions when:

- the prompt is mostly a claim, opinion, strategy, or vague product bet
- the user asks what the real problem is
- the surface is not named
- the target user or job is unclear
- success is undefined
- the request asks for "critical thinking", "what's the crux", "is this right", "question this", or "pressure test this"

Bring back into `diverge`:

- surface claim
- hidden premise
- weak joint
- standard of judgment
- crude test
- crux question

Do not use `crux` when the user already gave a concrete surface, user job, constraints, and asks directly for options.

## Copy Gate: Use `content-design`

Use `content-design` when copy materially decides the concept:

- copy-only divergence
- CTAs, labels, helper text, errors, empty states, onboarding, tooltips, confirmation modals, success states, notifications
- risk-sensitive fintech, payments, KYC, refunds, payouts, settlements, API keys, secrets, credentials, tokens, permissions, irreversible actions, save/recovery moments, security, or data loss
- in-product marketing, adoption prompts, upsell prompts, founder/startup-facing aspiration, campaign surfaces
- accessibility labels or localization risk

Bring back into `diverge`:

- surface
- user state
- system state
- risk level
- required next action
- voice lane
- recommended copy
- variants
- do-not-use patterns

Do not rewrite every direction through `content-design`. Use it for the directions where language changes behavior, trust, risk, or conversion.

## Critique Gate: Use 5F Review

Use a 5F-style review after directions exist when:

- the user asks for design review, critique, evaluation, or 5F analysis
- directions need selection pressure beyond personal taste
- the artifact is a B2B SaaS dashboard, workflow, admin surface, analytics page, settings page, operational tool, fintech interface, or prototype
- tradeoffs between clarity, speed, delight, fluency, and fairness are central

Apply:

- Fast: time-to-understand, time-to-act, path length, visual scan
- Focused: primary job clarity, hierarchy, attention control, noise removal
- Fun: useful delight, reward, momentum, emotional relief, not decoration
- Fluent: interaction continuity, state transitions, language consistency, predictable behavior
- Fair: accessibility, localization, permission clarity, error recovery, non-color signals, power-user and novice support

Bring back into `diverge`:

- strongest direction
- weakest direction
- fastest repair
- highest-leverage improvement
- fairness/accessibility risk
- recommendation

Do not run 5F before options exist unless the user explicitly asked to review an existing artifact.

## Execution-Hardening Gate

Use a design-hardening or visual execution lens after a direction is selected when:

- typography, spacing, layout density, responsive behavior, motion, or accessibility will make or break execution
- the user asks for polish, harden, make it feel better, sophisticated motion, production-ready UI, or implementation-ready design

Bring back into `diverge`:

- concrete layout corrections
- state coverage gaps
- accessibility fixes
- interaction feedback rules
- motion rules
- prototype-ready constraints

## Output Rule

When a companion skill is used or should be used, state the routing decision before the obvious baseline or directions. Mentioning routing only in a self-check is invalid.

```text
### Companion Routing
- crux: used / skipped because ...
- content-design: used / skipped because ...
- 5F review: used / skipped because ...
- execution hardening: used / skipped because ...
```

Keep this short in compact mode. In deep mode, include the inputs and extracted outputs.
````

- [ ] **Step 2: Verify the file exists**

Run:

```bash
test -f plugins/design/skills/diverge/references/companion-skill-routing.md && echo "routing reference exists"
```

Expected:

```text
routing reference exists
```

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/diverge/references/companion-skill-routing.md
git commit -m "docs: add diverge companion skill routing"
```

---

### Task 2: Wire Routing Into `diverge` Runtime

**Files:**
- Modify: `plugins/design/skills/diverge/SKILL.md`

- [ ] **Step 1: Add reference map entry**

In `plugins/design/skills/diverge/SKILL.md`, add this bullet to `## Reference Map` after `concept-enrichment.md`:

````markdown
- `references/companion-skill-routing.md` - companion-skill routing for `crux`, `content-design`, 5F critique, and execution hardening.
````

- [ ] **Step 2: Add companion routing to compact output**

Replace the compact output list with:

```markdown
Compact output:
1. Assumptions, only if needed.
2. Companion routing, only when a companion skill is used or clearly relevant.
3. Obvious baseline.
4. 4-6 directions.
5. For each direction: product bet, layers changed, visible execution, main interaction/state behavior, copy/content implication when relevant, tradeoff, prototype slice.
6. Recommendation.
```

- [ ] **Step 3: Add companion routing to deep output**

Replace the deep output list with:

```markdown
Deep output:
- Use the full workflow below.
- Load the relevant reference files.
- Load `references/companion-skill-routing.md` when the prompt includes weak premise, copy-heavy work, critique/selection pressure, or implementation-quality risk.
- Include companion routing, product model, state/action matrix, layer diagnosis, comparison, prototype slices, and handoff blueprint.
```

- [ ] **Step 4: Add workflow section after Assumption Ledger**

Insert this section after `### 2. Assumption Ledger`:

````markdown
### 2.5 Companion Skill Routing

Load `references/companion-skill-routing.md` when the prompt suggests weak premise, copy-heavy work, critique/selection pressure, or execution-hardening risk.

Decide before ideation:

```md
### Companion Routing

- crux: used/skipped because ...
- content-design: used/skipped because ...
- 5F review: used/skipped because ...
- execution hardening: used/skipped because ...
```

Rules:

- Use `crux` before divergence when the premise, user job, or success criterion is unclear.
- Use `content-design` when copy changes behavior, trust, risk, conversion, accessibility, or localization.
- Use 5F-style review after directions exist when critique, selection, B2B SaaS quality, or design review is central.
- Use execution hardening after a direction is selected when polish, accessibility, density, typography, motion, or implementation readiness is the core risk.
- Do not route for ceremony. Route when the companion skill changes the result.
````

- [ ] **Step 5: Add quality gates**

Append these items to `Universal kill/rewrite triggers`:

```markdown
11. Copy-heavy direction does not define the user's state, system state, next action, and risk level.
12. Risk-sensitive copy is invented without a recovery path or source of truth.
13. Direction selection relies on taste alone when Fast, Focused, Fun, Fluent, or Fair tradeoffs are visible.
14. Weak premise proceeds into ideation without a crux question or crude test.
```

- [ ] **Step 6: Run text checks**

Run:

```bash
rg -n "companion-skill-routing|Companion Skill Routing|content-design|5F|crux" plugins/design/skills/diverge/SKILL.md
```

Expected: matches in the reference map, output structure, workflow section, and quality gates.

- [ ] **Step 7: Commit**

```bash
git add plugins/design/skills/diverge/SKILL.md
git commit -m "docs: route diverge through companion design skills"
```

---

### Task 3: Add Companion Routing Evals

**Files:**
- Create: `plugins/design/skills/diverge/evals/companion-skill-routing.md`

- [ ] **Step 1: Create eval file**

Create `plugins/design/skills/diverge/evals/companion-skill-routing.md` with this content:

````markdown
# Test: Companion skill routing

## Prompt 1: Weak premise before divergence

```md
/diverge "I think our AI dashboard should feel more trustworthy and premium. Give me directions."
```

## Expected behavior

The skill should run a premise gate before ideation.

## Pass criteria

- Mentions `crux` routing or performs an equivalent crux pass.
- Names the hidden premise behind "trustworthy" and "premium".
- Defines a standard of judgment before generating directions.
- Includes a crux question or crude test.
- Does not jump straight into visual treatments.

## Fail signals

- Produces only style directions.
- Treats "premium" as a palette or spacing style without defining behavior.
- Skips the weak premise.

---

## Prompt 2: Copy-heavy credential modal

```md
/diverge "Give me simple delight ideas for an API key creation modal. The biggest pain point is users forget to save the secret."
```

## Expected behavior

The skill should route through `content-design` or use content-design mechanics because copy, consequence, and user state decide the experience.

## Pass criteria

- Names the user state: anxious after seeing a one-time secret.
- Names the system state: secret visible once, cannot be recovered later.
- Includes concrete copy or CTA variants.
- Includes a saved-confirmation or copy/export mechanic.
- Avoids decorative delight that does not reduce the pain point.

## Fail signals

- Suggests confetti, animations, badges, or mascot language without solving save anxiety.
- Uses vague CTAs like "Done" as the primary path.
- Omits recovery or consequence copy.

---

## Prompt 3: B2B dashboard option selection

```md
/diverge "Review these three connector health dashboard concepts and tell me which one to prototype.

Concept A: Status Grid. Each connector is a card with health status, last sync, auth status, and a fix button. It optimizes quick scanning but can become noisy.

Concept B: Triage Queue. The page starts with the three most urgent connector problems, each with impact, owner, repair action, and affected agents. Healthy connectors move below the fold.

Concept C: System Map. Connectors are shown as dependencies around active agents, with degraded connectors highlighted in the run path. It explains blast radius but may be slower to scan.

Use Fast, Focused, Fun, Fluent, and Fair to choose the prototype direction."
```

## Expected behavior

The skill should use 5F-style review after directions exist.

## Pass criteria

- Scores or compares options across Fast, Focused, Fun, Fluent, and Fair.
- Separates quick wins from strategic bets.
- Calls out accessibility or fairness risks.
- Recommends one prototype direction with a reason beyond taste.

## Fail signals

- Picks the most visually novel option without explaining operational clarity.
- Ignores novice and power-user differences.
- Does not mention speed-to-diagnosis or repair clarity.

---

## Prompt 4: Concrete options request with enough brief

```md
/diverge "Give me 5 layout directions for a settings page with account, billing, team, API keys, and security. Product mechanics must stay unchanged."
```

## Expected behavior

The skill should not over-route.

## Pass criteria

- Skips `crux` because the surface, objects, and constraint are clear.
- Skips `content-design` unless a direction depends on labels or warnings.
- Generates layout divergence directly.
- Keeps product mechanics unchanged.

## Fail signals

- Stalls for broad premise questions.
- Runs a full critique before producing options.
- Changes product mechanics.
````

- [ ] **Step 2: Verify eval sections**

Run:

```bash
rg -n "Prompt 1|Prompt 2|Prompt 3|Prompt 4|Pass criteria|Fail signals" plugins/design/skills/diverge/evals/companion-skill-routing.md
```

Expected: all four prompts, pass criteria, and fail signals appear.

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/diverge/evals/companion-skill-routing.md
git commit -m "test: cover diverge companion skill routing"
```

---

### Task 4: Validate Skill Shape

**Files:**
- Test: `plugins/design/skills/diverge/SKILL.md`
- Test: `plugins/design/skills/diverge/references/companion-skill-routing.md`
- Test: `plugins/design/skills/diverge/evals/companion-skill-routing.md`

- [ ] **Step 1: Validate frontmatter**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/diverge
```

Expected:

```text
Validation passed
```

If the exact success text differs, accept a zero exit code and no reported errors.

- [ ] **Step 2: Check reference is reachable from `SKILL.md`**

Run:

```bash
rg -n "references/companion-skill-routing.md" plugins/design/skills/diverge/SKILL.md
```

Expected: at least one match.

- [ ] **Step 3: Check no duplicate doctrine was copied**

Run:

```bash
wc -l plugins/design/skills/diverge/SKILL.md plugins/design/skills/diverge/references/companion-skill-routing.md
```

Expected: `SKILL.md` remains readable and the new reference stays small. If `SKILL.md` grows by more than roughly 80 lines, move detail from `SKILL.md` into the reference.

- [ ] **Step 4: Final status check**

Run:

```bash
git status --short
```

Expected: clean after commits, or only unrelated user changes.

---

## Self-Review

Spec coverage:

- Triggered-skill problems are covered by companion routing and quality gates.
- Missed-trigger problems are covered by eval prompts for weak premise, copy-heavy modal, and 5F dashboard review.
- Prerequisite problems are covered by premise gate, product model, copy gate, critique gate, and prototype slice expectations.
- The user's added concern about `content-design` and 5F not being used effectively is directly covered by Task 1 and Task 3.

Placeholder scan:

- No `TBD`, `TODO`, "similar to", or undefined implementation steps remain.

Type and path consistency:

- All paths point to `plugins/design/skills/diverge/...`.
- Validation uses the existing system `quick_validate.py`.
- The plan keeps companion-skill details in one direct reference file, matching skill-creator progressive disclosure guidance.
