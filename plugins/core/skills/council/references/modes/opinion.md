# Opinion Mode

Use when the user wants multiple expert perspectives on a question, decision, or approach. Each agent adopts a specific expert persona and gives their genuine assessment, not a generic review.

## Evidence preference

Prefer:

- the question or decision itself
- context and constraints provided by the user
- relevant code or artifacts
- the agent's domain expertise (persona-driven reasoning)

## How personas work

Each spawned agent is briefed as a specific expert. The persona shapes what they pay attention to, what they consider risky, and what they value.

### Persona assignment rules

- Each agent gets a **distinct persona**. No two agents share the same expertise area.
- Select personas that are **relevant but diverse** for the question. A database migration question benefits from a DBA, a security engineer, and an SRE. It does not benefit from a UX designer.
- Always include at least one persona who would naturally **oppose or be skeptical** of the proposed approach.
- Personas must be specific ("senior security engineer at a fintech") not generic ("technical person").

### Built-in persona library

Select from these or create problem-specific ones:

| Persona | Focuses on | Natural skepticism toward |
|---------|-----------|--------------------------|
| Senior security engineer | Attack surface, auth, data exposure, compliance | Convenience-first decisions, "we'll secure it later" |
| Performance engineer | Latency, throughput, resource usage, scaling | Feature additions without perf testing, N+1 queries |
| Staff frontend engineer | Component architecture, bundle size, UX perf, a11y | Prop drilling, monolith components, ignoring a11y |
| DBA / data engineer | Schema design, query patterns, migration safety, data integrity | Wide tables, missing indices, risky migrations |
| SRE / platform engineer | Operability, observability, failure modes, rollback | Unmonitorable systems, manual deploy steps |
| Product manager | User value, scope, timeline, ROI, adoption risk | Over-engineering, scope creep, features nobody asked for |
| UX designer | User flow, cognitive load, error recovery, consistency | Developer-centric interfaces, exposed implementation details |
| Staff backend engineer | API design, service boundaries, data flow, error handling | Tight coupling, leaky abstractions, missing contracts |
| Tech lead | Architecture fit, team capacity, technical debt, pragmatism | Perfect solutions that take too long, yak shaving |
| QA engineer | Edge cases, error paths, regression risk, testability | Untestable code, missing error states, happy-path-only thinking |

### Custom personas

For domain-specific questions, create personas on the fly:

```
You are a [ROLE] with [N years] experience at [COMPANY TYPE].
You focus on [SPECIALTY] and are naturally skeptical of [ANTI-PATTERN].
Your advice tends to be [ADJECTIVE] — you value [VALUE] over [COUNTER-VALUE].
```

## Debate format (optional)

When the question is a binary decision ("should we do A or B?"), use debate format:

1. Spawn **Agent A** (advocate for option A) and **Agent B** (advocate for option B)
2. Each agent must **steel-man the opposing view** before arguing their own position
3. Each agent states what **evidence would change their mind**
4. Parent synthesizes: where do they actually agree? What's the real crux of the disagreement?

## Mode-specific lenses

Choose from these after the permanent lenses are covered.

### Expert panel

- Focus on: what each expert persona sees from their vantage point
- Do not duplicate: generic analysis without persona commitment

### Stakeholder map

- Focus on: how different organizational roles (user, engineer, PM, leadership) would evaluate this
- Do not duplicate: expert technical assessment

### Pre-mortem

- Focus on: "Imagine we did this and it failed 6 months later. What went wrong?"
- Do not duplicate: devil's advocate (pre-mortem is temporal, devil's advocate is logical)

### Assumption audit

- Focus on: what each expert assumes is true that they haven't verified
- Do not duplicate: blind-spot lens

## Good fit examples

- "should we use X or Y?" decisions
- architecture proposals needing multi-role review
- "give me a second opinion on this approach"
- risk assessment of a proposed change
- "what are we not thinking about?" from specific expert angles
