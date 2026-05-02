---
name: diverge
description: Layered divergence system for product designers. Use when exploring different ways a software product, surface, flow, page, modal, dashboard, component, interaction, state, copy system, visual language, or product direction could work across product mechanics, UX structure, UI presentation, copy, interaction, states, emotion, persuasion, education, accessibility, and implementation handoff.
---

# /diverge - Layered Product Design Divergence

Generate design directions that differ by observable design layers, not by decorative names. The skill supports divergence across product mechanics, UX structure, interaction behavior, information hierarchy, copywriting, layout, visual language, typography, color, motion, emotional design, persuasive design, education, states, accessibility, and implementation handoff.

Replace:

```text
problem -> references -> metaphor-led names -> decorative reward moments -> kill ledger
```

With:

```text
problem -> altitude detection -> product model -> user decision -> state/action map -> divergence layer selection -> layered directions -> execution details -> state matrix -> tradeoff -> prototype slice -> handoff blueprint
```

## Non-negotiable Principle

A direction only counts if it changes a specific design layer and explains the observable outcome.

Every direction must answer:

- What layer changed?
- What stayed constant?
- What does the user see?
- What does the user do?
- What does the system do?
- What information becomes more or less prominent?
- What copy changes?
- What layout/hierarchy changes?
- What state behavior changes?
- What emotional or behavioral effect is intended?
- What tradeoff does this create?

Do not accept "different vibe" as divergence. Do not accept "same screen with different styling" as conceptual divergence. Do not accept metaphor unless it changes product behavior, UI structure, copy, interaction, or visual execution.

## Reference Map

Load only the references needed for the selected altitude:

- `references/divergence-axes.md` - layered axes across product, UX, interaction, UI, copy, visual system, emotional, and persuasive layers.
- `references/concept-enrichment.md` - JTBD, constraints, product model, layer diagnosis, state/action matrix, enrichment passes, kill ledger, narratives, simplicity, and prototype selection.
- `references/creative-provocations.md` - layer-specific provocations.
- `references/persona-lens.md` - persona effects on density, copy, hierarchy, interaction, education, error handling, accessibility, and emotion.
- `references/anchor-library.md` - optional reference-handling rules.
- `references/reference-pattern-library.md` - optional mental library for disciplined reference use.
- `references/copywriting-divergence.md` - copy roles, surfaces, axes, formulas, and gates.
- `references/layout-divergence.md` - layout topologies and quality gates.
- `references/hierarchy-divergence.md` - information hierarchy strategies and squint test.
- `references/interaction-divergence.md` - interaction models and gates.
- `references/typography-divergence.md` - typography strategies and output requirements.
- `references/color-divergence.md` - color roles, strategies, and gates.
- `references/motion-divergence.md` - motion strategy and reduced-motion checks.
- `references/emotional-design.md` - visceral, behavioral, reflective design.
- `references/persuasive-design.md` - ethical persuasive design.
- `references/user-education.md` - education patterns and gates.
- `references/bluff-and-slop-firewall.md` - banned metaphor, visual, and copy slop.
- `references/picker-template.md` - React prototype template.
- `references/paper-canvas-template.md` - Paper canvas template.

## Workflow

### 1. Brief Intake

Ask only what is missing. If the user already gave enough context, infer the rest and show assumptions.

```md
### Brief Intake

1. Surface or flow
   What are we designing?

2. User role
   Who is using it?

3. Core user job
   What is the user trying to decide, understand, complete, avoid, or recover from?

4. Product objects
   What objects exist in this product?

5. Known states
   What states must the design handle?

6. Available actions
   What can the user do?

7. System actions
   What can the system do?

8. Constraints
   What cannot change?

9. Existing anti-patterns
   What has already failed or feels wrong?

10. Register
   Is this a product surface, brand surface, content/editorial surface, or mixed?

11. Emotional target
   What should the user feel?

12. Behavioral target
   What behavior should the interface encourage?

13. Visual system
   What type, color, component, or brand rules already exist?

14. Reference input
   Optional. If provided, I will decompose references into mechanisms and qualities.
```

If only a few fields are missing, ask a narrow question. If missing fields do not block useful output, proceed.

### 2. Assumption Ledger

Always show assumptions when context is incomplete.

```md
### Assumption Ledger

Known:
- ...

Assumed:
- ...

Unknown:
- ...

Risk:
- The output may be weaker around <specific layer> because <missing information>.
```

Do not stall unless a missing fact would make the output unsafe or meaningless.

### 3. Divergence Altitude

Classify the request before ideation:

- Product-level
- UX-level
- UI-level
- Copy-level
- Visual-system-level
- Interaction-level
- State-handling-level
- Mixed

Infer altitude:

- "Diverge on this product idea", "product directions", "what should this be" -> Product-level.
- "Different ways to present this page/layout/modal" -> UX/UI-level.
- "Different copy", labels, CTAs, errors, onboarding text -> Copy-level.
- "Look/feel", typography, color, visual language, design system -> Visual-system-level.
- "How should this interaction work?" -> Interaction-level.
- Dashboards, health, sync, permissions, errors, progress, onboarding, empty states -> State-handling-level.
- If unclear, run Mixed: one product pass, one UX pass, and one UI pass.

### 4. Product Model

Every run extracts a product model before ideation.

```md
### Product Model

Core objects:
- Object:
- Meaning:
- Properties:
- States:
- User actions:
- System actions:
- Dependencies:

Current user decision:
- What is the user trying to decide?
- What information do they need?
- What action follows?
- What can go wrong?

Current surface assumption:
- The current design seems organized around:
- But the user's real decision is about:

Failure modes:
- User cannot tell what matters.
- User cannot tell what changed.
- User cannot tell what to do next.
- User cannot trust the recommendation.
- User cannot recover from failure.
- User fixes the wrong thing first.
- User gets educated instead of guided.
- User sees status but not consequence.
- User sees all information with no priority.
- User gets decorative UI instead of decision support.
```

### 5. State and Action Matrix

For software products, divergence without states is incomplete. Use domain-specific states from the prompt when provided.

```md
| State | User meaning | System meaning | Severity | User action | System action | UI representation | Copy requirement | Edge case |
|---|---|---|---|---|---|---|---|---|
```

Common states: empty, loading, partial loading, error, first-time, returning, long-content, stale data, permission denied, offline, success, undoable success, irreversible success, warning, blocked, degraded, recovering.

### 6. Layer Diagnosis

Diagnose which layers are weak before generating. Only diverge layers that matter.

```md
| Layer | Current weakness | Evidence from prompt | Should diverge? | Why |
|---|---|---|---|---|
| Product mechanics | | | yes/no | |
| UX flow | | | yes/no | |
| Interaction | | | yes/no | |
| Information hierarchy | | | yes/no | |
| Copy | | | yes/no | |
| Layout | | | yes/no | |
| Typography | | | yes/no | |
| Color | | | yes/no | |
| Motion | | | yes/no | |
| Emotional design | | | yes/no | |
| Persuasion | | | yes/no | |
| Education | | | yes/no | |
```

Do not generate typography variants when the real problem is product trust. Do not generate product concepts when the user asked for CTA copy.

### 7. Obvious Baseline

Always include the baseline before divergent directions.

```md
### Obvious Baseline

- What the default sensible solution is:
- Why it might be correct:
- Where it fails:
- What would make it enough:
- What divergence must beat:
```

Novelty is not automatically better. If obvious wins, say so.

### 8. Banned Bad Directions

List predictable weak answers and ban them unless deliberately revived.

Examples:

- Same cards with renamed labels.
- Generic status dashboard.
- Alert carousel.
- Tooltip tour for unclear UI.
- Wizard by default.
- Every button primary.
- Purple-blue gradient "AI" treatment.
- Metaphor name with unchanged mechanics.

### 9. Divergence Strategy

State which layers this run will explore:

```md
### Divergence Strategy

This run will explore:
- Product layers:
- UX layers:
- UI layers:
- Emotional/persuasive layers:
```

### 10. Generate Layered Directions

Default to 5-7 directions. Use the selected mode's output structure. Every direction must use this template unless the user requested a narrower mode such as copy-only.

```md
## Direction: <plain functional name>

### Altitude
Product-level / UX-level / UI-level / Copy-level / Visual-system-level / Mixed

### Product bet
One sentence explaining the hypothesis.

### Layers changed
- Product mechanics:
- UX structure:
- Interaction:
- Information hierarchy:
- Copy:
- Layout:
- Typography:
- Color:
- Motion:
- Emotional design:
- Persuasive behavior:
- State handling:

Use "unchanged" where a layer is intentionally held constant.

### What stays constant
Name the existing constraints or mechanics preserved.

### User job
When [situation], the user wants to [motivation], so they can [outcome].

### Core mechanic
What makes this direction work structurally.

### Screen anatomy
- Top region:
- Primary region:
- Secondary region:
- Detail region:
- Persistent elements:
- Primary CTA:
- Secondary actions:
- What is hidden by default:
- What appears only after interaction:

### Information hierarchy
1. First thing user should notice:
2. Second thing:
3. Third thing:
4. What is deliberately quiet:
5. What is removed:

### Interaction loop
Trigger -> user action -> system response -> next user decision.

### Copy system
- Page title:
- Section heading:
- Primary CTA:
- Secondary CTA:
- Empty state:
- Loading state:
- Error state:
- Success state:
- Tooltip/helper text only if necessary:
- Confirmation copy if relevant:

### Layout execution
- Layout topology:
- Grid/columns:
- Density:
- Spacing rhythm:
- Grouping logic:
- Scroll behavior:
- Responsive behavior:

### Typography execution
- Font strategy:
- Type scale:
- Weight strategy:
- Line height:
- Line length:
- Numeric/data style:
- Accessibility notes:

### Color execution
- Palette role:
- Semantic colors:
- Accent usage:
- Status usage:
- Contrast requirements:
- Non-color backup signal:

### Motion and feedback
- State transitions:
- Loading:
- Success:
- Error:
- Hover/focus:
- Reduced-motion alternative:

### Emotional design
- Before-use emotional state:
- During-use emotional state:
- After-use emotional state:
- Visceral mechanism:
- Behavioral mechanism:
- Reflective mechanism:

### Persuasive design
- Desired behavior:
- Motivation:
- Ability/friction:
- Prompt:
- Ethical boundary:
- Failure if persuasion goes too far:

### States to design
- Empty:
- Loading:
- Error:
- Permission denied:
- Success:
- Partial failure:
- Stale data:
- Long content:

### Data required

### Component requirements

### Edge cases
List at least 5.

### What the user no longer has to do

### Tradeoff

### How it dies
Specific failure mode: who is affected, what goes wrong, when.

### Prototype slice
Smallest screen or flow that proves the direction.

### Story mode
- Trigger:
- Moment of confusion or need:
- Product response:
- User action:
- Aftermath:

### Handoff notes
- Objects:
- States:
- Events:
- Components:
- Data dependencies:
- Permissions:
- Edge cases:
- Analytics:
- Accessibility:
- Localization:
- QA scenarios:
```

## Output Modes

### Mode 1: Full layered divergence

Use for broad prompts.

Output:
1. Product model
2. State/action matrix
3. Banned obvious bad directions
4. Obvious baseline
5. 5-7 layered directions
6. Comparison table
7. Recommendation
8. Prototype slices
9. Handoff blueprint

### Mode 2: Product mechanics divergence

Use when product behavior is open.

Output:
- 5-7 product directions.
- Each changes at least 2 product layers.
- UI details included but not over-polished.
- Data, trust, and automation tradeoffs included.

### Mode 3: UX structure divergence

Use when the product concept is stable but flow/surface is open.

Output:
- 6-8 UX structures.
- IA, flow, interaction, hierarchy, state handling.
- Rough screen anatomy.
- Typography/color mostly constant unless relevant.

### Mode 4: UI presentation divergence

Use when screen concept is stable.

Output:
- 6-8 UI treatments.
- Vary layout, hierarchy, density, components, copy, type, color, motion.
- Do not change product mechanics.
- Include what each treatment optimizes for.

### Mode 5: Copywriting divergence

Use when words are the design problem. Load `copywriting-divergence.md`.

Output:
- Copy diagnosis.
- User mental state.
- Copy roles.
- 8-12 copy directions grouped by tone/function.
- Labels, CTAs, helper text, errors, empty states, success states.
- Behavioral effect of each.
- "Too clever" and "too vague" kills.

### Mode 6: Interaction divergence

Use when the user asks how an interaction should work. Load `interaction-divergence.md`.

Output:
- 6-8 interaction models.
- Input, feedback, states, accessibility, speed, edge cases.
- Power-user path and first-time path.

### Mode 7: Visual-system divergence

Use when look/feel/art direction is requested. Load visual modules.

Output:
- Register decision: product, brand, or mixed.
- 5-7 visual language directions.
- Type, color, layout rhythm, motion, shape, imagery/icon logic.
- Observable user effect for each visual decision.
- Accessibility checks.

### Mode 8: State-handling divergence

Use for dashboards, health, sync, permissions, errors, progress, onboarding, and empty states.

Output:
- State taxonomy.
- Severity model.
- Repair/recovery model.
- User/system action map.
- 5-7 state presentation models.
- Copy for each state.
- Edge-case matrix.

## Register Rule

Every run must choose register.

### Product register

Design serves the task. Default to familiar components, clear states, restrained color, useful density, clear typography, motion for feedback, copy for action and consequence, and delight only at specific moments.

### Brand register

Design is part of the product. Stronger visual expression, distinctive type, memorable composition, voice, motion/story, and atmospheric color are allowed, while preserving accessibility and usability.

### Mixed register

Define which parts behave like product and which behave like brand.

Example:
Agent builder = product. Launch page = brand. First success moment = product with brand expression.

## Speed and Exposure Principle

Favor fast end-to-end exploration before polishing fragments.

- Full-flow sketch first.
- Detail pass second.
- Polish pass last.

For broad tasks, produce multiple end-to-end directions quickly. Do not over-perfect one small component before the whole flow is discussable.

## Obvious-vs-Novel Decision Rule

For every run, ask:

- Does the obvious solution solve the user job?
- Is novelty adding capability, clarity, emotion, or trust?
- Is novelty increasing learning cost?
- Is the product category one where familiarity is valuable?
- Would users punish us for being clever?

If the obvious baseline wins, say so.

## Default Output Structure

```md
# Diverge: <surface/problem>

## 1. Brief
- Surface:
- User:
- Job:
- Objects:
- States:
- Actions:
- Constraints:
- Register:
- Emotional target:
- Behavioral target:
- Anti-patterns:

## 2. Assumption Ledger
Known:
Assumed:
Unknown:
Risk:

## 3. Product Model
Core objects:
State/action matrix:
Current decision:
Current surface assumption:
Product-design tension:

## 4. Layer Diagnosis
<table>

## 5. Obvious Baseline

## 6. Banned Bad Directions

## 7. Divergence Strategy

## 8. Directions
<5-7 layered directions>

## 9. Comparison
| Direction | Altitude | Best for | What changes | Biggest tradeoff | Data needed | Prototype value | How it dies |

## 10. Recommendation
- Prototype first:
- Prototype second:
- Keep as UI treatment:
- Keep as product provocation:
- Kill:
- Obvious baseline verdict:

## 11. Prototype slices
- Screen/flow:
- States:
- Interactions:
- Copy:
- Components:
- Data:
- Success signal:

## 12. Handoff Blueprint
- Components:
- State machine:
- Events:
- API/data requirements:
- Analytics:
- Accessibility:
- Localization:
- QA cases:
```

## Quality Gates

Load `bluff-and-slop-firewall.md` and `concept-enrichment.md` for full gates.

Universal kill/rewrite triggers:

1. Direction does not name altitude.
2. Direction does not say which layers changed.
3. Direction cannot be sketched.
4. Direction cannot be prototyped.
5. Direction does not handle real states.
6. Direction has no clear user action.
7. Direction uses metaphor without execution.
8. Direction ignores constraints.
9. Direction hides complexity users need.
10. Direction is only a different visual treatment but claims product-level divergence.

## Reference Handling

References are optional. They are never required in every output. Every reference must pass:

```md
Reference:
Observed mechanism:
Design layer it informs:
Product translation:
Concrete execution:
What not to copy:
```

Study artists and non-design references for mechanics, not aesthetics. Designers often provide known answers; artists can help question assumptions. Use both, but make every reference pay rent in execution.
