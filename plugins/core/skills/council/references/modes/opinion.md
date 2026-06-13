# Opinion Mode

Use when the user wants multiple expert perspectives on a question, decision, or approach. Each agent adopts a **derived lens** (archetype + instantiation) and gives their genuine assessment, not a generic review.

## Required references

Before spawning opinion agents, load:

1. `$CLAUDE_SKILL_DIR/references/lens-composer.md`
2. `$CLAUDE_SKILL_DIR/references/domain-overlays.md` when domain signals match

## Evidence preference

Prefer:

- the question or decision itself
- context and constraints provided by the user
- relevant code or artifacts
- lens-driven reasoning grounded in `domain`, `stakes`, `decision_shape`, `evidence_available`, and `cost_bearer`

## How lenses work

Each spawned agent is briefed via the lens composer. The derived lens shapes what they pay attention to, what they consider risky, and what they value.

### Lens assignment rules

- Compose lenses from inputs — **do not** pick from a fixed persona table.
- Each agent gets a **distinct expertise area**. No two agents share the same focus.
- Select archetypes and overlays that are **relevant but diverse** for the question.
- Always include at least one skeptic lens (`devil's advocate`, `skeptic` archetype, or pre-mortem).
- Every derived lens includes a one-line rationale: `chosen because [reason from inputs]`.
- Instantiations must be specific ("onboarding flow advocate for first-time merchants") not generic ("technical person").

### Example library (deprecated as default)

The fixed persona table moved to `$CLAUDE_SKILL_DIR/references/lens-archetypes.md` as **examples only**. Consult it when engineering-heavy instantiation patterns help — never as the default assignment path.

### Custom lenses

For domain-specific questions, derive via lens composer:

```text
Archetype: [from lens-composer.md]
Instantiated as: [ROLE FOR THIS TOPIC]
Chosen because: [stakes / cost_bearer / decision_shape]
Overlay: [from domain-overlays.md if applicable]
Focus: [SPECIALTY]
Skeptical of: [ANTI-PATTERN]
Values: [VALUE] over [COUNTER-VALUE]
```

## Debate format (binary decisions)

When `decision_shape` is binary ("should we do A or B?"), use debate format:

1. Spawn **advocate-for-A** and **advocate-for-B** lenses derived from `cost_bearer` and `stakes`
2. Each agent must **steel-man the opposing view** before arguing their own position
3. Each agent states what **evidence would change their mind**
4. Parent synthesizes: where do they agree? What's the real crux of the disagreement?

## Mode-specific lenses

Choose from these after permanent lenses and composed archetypes are covered.

### Expert panel

- Focus on: what each derived lens sees from its vantage point
- Do not duplicate: generic analysis without lens commitment

### Stakeholder map

- Focus on: how different organizational roles (user, engineer, PM, leadership) would evaluate this
- Do not duplicate: expert technical assessment

### Pre-mortem

- Focus on: "Imagine we did this and it failed 6 months later. What went wrong?"
- Do not duplicate: devil's advocate (pre-mortem is temporal, devil's advocate is logical)

### Assumption audit

- Focus on: what each lens assumes is true that they haven't verified
- Do not duplicate: blind-spot lens

## Good fit examples

- "should we use X or Y?" decisions
- architecture proposals needing multi-role review
- "give me a second opinion on this approach"
- risk assessment of a proposed change
- design critique needing UX, copy, and hierarchy lenses
- "what are we not thinking about?" from distinct derived angles
