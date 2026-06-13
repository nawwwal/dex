# Lens Composer

Derive investigation lenses from the topic — do not default to a fixed persona table. Load this file for `opinion` mode and whenever lenses need to be composed beyond permanent coverage.

## Inputs

Extract these from reconnaissance, the user prompt, and any fixtures:

| Input | What to infer |
|---|---|
| `domain` | design, product, engineering, research, workflow, compliance |
| `stakes` | what breaks if wrong: user trust, revenue, security, timeline, legal exposure |
| `decision_shape` | binary, prioritization, audit, open exploration |
| `evidence_available` | fixtures, code, web sources, user opinion only |
| `cost_bearer` | who pays for being wrong: user, eng, business, legal |

Store compact values in `investigation_context` before spawning agents.

## Archetypes (composable, not fixed roles)

Select archetypes that fit the inputs. Combine with domain overlays from `$CLAUDE_SKILL_DIR/references/domain-overlays.md`.

| Archetype | Focuses on | Natural skepticism toward |
|---|---|---|
| `skeptic` | Hidden assumptions, failure modes | "obviously fine" claims |
| `operator` | Day-to-day execution, runbooks | Untestable abstractions |
| `user_advocate` | User job, cognitive load, recovery | Developer-centric defaults |
| `craft_quality` | Visual, copy, interaction craft | Decorative polish without mechanics |
| `cost_complexity` | Scope, timeline, maintenance | Scope creep, yak shaving |
| `risk_compliance` | Legal, security, regulatory surfaces | "We'll fix later" |
| `evidence_mapper` | Source quality, triangulation | Single-source certainty |

An archetype is not a job title. Instantiate it for the topic:

```text
Archetype: user_advocate
Instantiated as: "onboarding flow advocate — focuses on first-time merchant confusion and drop-off at KYC"
Rationale: chosen because stakes include user trust and cost_bearer is the merchant.
```

## Derivation steps

1. **Set permanent lenses first** — `core mapper`, `dependency / blast radius`, `devil's advocate`, `blind-spot` (see `depths.md`). These are not replaced by archetypes.
2. **Pick 2–4 derived lenses** from archetypes + domain overlays for the remaining agent slots.
3. **Apply domain overlay dimensions** — each overlay adds focus areas agents must cover (see `domain-overlays.md`).
4. **Write a one-line rationale per derived lens** — `chosen because [reason from inputs]`.
5. **Brief each agent** with: archetype name, instantiated focus, rationale, overlay dimensions, and `Do not duplicate` boundaries.

## Hard rules

1. Always include at least one skeptic lens (may be `devil's advocate`, `skeptic` archetype, or pre-mortem).
2. No two lenses share the same expertise area.
3. Each derived lens gets a one-line rationale tied to inputs, not generic role labels.
4. Permanent lenses remain: core mapper, dependency/blast radius, devil's advocate, blind-spot.
5. Parent synthesis must include `## Lens Rationale` listing every derived lens and why (see `synthesis.md`).
6. Do not copy example archetypes from `lens-archetypes.md` when inputs point elsewhere.

## Debate format (binary `decision_shape`)

When `decision_shape` is binary ("A or B"):

1. Spawn advocate-for-A and advocate-for-B lenses derived from `cost_bearer` and `stakes` — not generic pro/con roles.
2. Each steel-mans the opposing view before arguing.
3. Each states what evidence would change their mind.
4. Parent synthesizes: agreement, crux of disagreement, and recommendation.

## Custom instantiation template

```text
You are the [ARCHETYPE] lens, instantiated as [ROLE/FOR THIS TOPIC].
Chosen because: [one-line rationale from domain, stakes, decision_shape, evidence, cost_bearer].

Overlay focus: [dimensions from domain-overlays.md if applicable]

You focus on [SPECIALTY] and are naturally skeptical of [ANTI-PATTERN].
You value [VALUE] over [COUNTER-VALUE].

Do not duplicate: [what other lenses own]
```

## Examples library

For worked examples of archetype instantiation (especially engineering-heavy cases), see `$CLAUDE_SKILL_DIR/references/lens-archetypes.md`. Use as inspiration only — derive from inputs first.
