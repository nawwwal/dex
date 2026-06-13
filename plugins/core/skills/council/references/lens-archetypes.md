# Lens Archetypes — Examples Only

**Do not assign lenses from this table by default.** Derive lenses from inputs via `$CLAUDE_SKILL_DIR/references/lens-composer.md` and apply domain overlays from `$CLAUDE_SKILL_DIR/references/domain-overlays.md`.

This file shows how archetypes can be **instantiated** for common engineering and product contexts. Copy the pattern, not the roles, when inputs differ.

## Example instantiations

| Example instantiation | Archetype | Focuses on | Natural skepticism toward |
|---|---|---|---|
| Senior security engineer | `risk_compliance` | Attack surface, auth, data exposure, compliance | Convenience-first decisions, "we'll secure it later" |
| Performance engineer | `operator` | Latency, throughput, resource usage, scaling | Feature additions without perf testing, N+1 queries |
| Staff frontend engineer | `craft_quality` | Component architecture, bundle size, UX perf, a11y | Prop drilling, monolith components, ignoring a11y |
| DBA / data engineer | `operator` | Schema design, query patterns, migration safety, data integrity | Wide tables, missing indices, risky migrations |
| SRE / platform engineer | `operator` | Operability, observability, failure modes, rollback | Unmonitorable systems, manual deploy steps |
| Product manager | `cost_complexity` | User value, scope, timeline, ROI, adoption risk | Over-engineering, scope creep, features nobody asked for |
| UX designer | `user_advocate` | User flow, cognitive load, error recovery, consistency | Developer-centric interfaces, exposed implementation details |
| Staff backend engineer | `operator` | API design, service boundaries, data flow, error handling | Tight coupling, leaky abstractions, missing contracts |
| Tech lead | `cost_complexity` | Architecture fit, team capacity, technical debt, pragmatism | Perfect solutions that take too long, yak shaving |
| QA engineer | `skeptic` | Edge cases, error paths, regression risk, testability | Untestable code, missing error states, happy-path-only thinking |

## When these examples fit

Use table-style engineering roles **only when** reconnaissance confirms:

- `domain` is engineering or system
- `evidence_available` includes code or architecture artifacts
- `stakes` are technical reliability, security, or delivery

For design, product, research, or workflow investigations, prefer overlays and archetypes from `lens-composer.md` even if the topic touches code.

## Custom example pattern

```text
Archetype: [from lens-composer.md]
Instantiated as: [ROLE] with [EXPERIENCE] in [CONTEXT]
Rationale: chosen because [stakes / cost_bearer / decision_shape]
Focus: [SPECIALTY]
Skeptical of: [ANTI-PATTERN]
Values: [VALUE] over [COUNTER-VALUE]
```
