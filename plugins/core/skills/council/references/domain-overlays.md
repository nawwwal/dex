# Domain Overlays

Overlays add mandatory focus dimensions on top of archetype lenses. Apply when `domain` matches; stack multiple overlays only when the investigation genuinely spans domains.

Load with `$CLAUDE_SKILL_DIR/references/lens-composer.md` during lens composition.

## Design overlay

**Apply when:** design critique, visual direction, UX flow, copy review, brand, onboarding, hierarchy, interaction states.

| Dimension | Agent must examine |
|---|---|
| `visual_hierarchy` | What draws attention first; whether primary action is obvious; density and scan path |
| `copy_tone` | Voice fit, clarity under stress, jargon, trust signals, error/helper copy |
| `state_coverage` | Empty, loading, error, success, partial, edge; recovery paths; dead ends |

**Preferred archetypes:** `craft_quality`, `user_advocate`, `skeptic`  
**Often pairs with:** product overlay when shipping or prioritization is in scope

**Router signals:** design critique, visual, copy, brand, onboarding, UX flow, hierarchy, modal, empty state

## Research overlay

**Apply when:** competitive landscape, best practices, how others solve X, external survey, literature review.

| Dimension | Agent must examine |
|---|---|
| `source_quality` | Primary vs secondary, recency, author bias, sample size, applicability to our context |
| `negative_space` | What is *not* being said; missing segments; outdated patterns still cited; gaps in search |

**Preferred archetypes:** `evidence_mapper`, `skeptic`, `operator`  
**Tooling:** agents get `WebSearch` and `WebFetch`

**Router signals:** how do others, compare, survey, landscape, best practice, state of the art

## Workflow overlay

**Apply when:** handoff friction, process bottlenecks, review flow, repeated churn, operating model, automation gaps.

| Dimension | Agent must examine |
|---|---|
| `handoff_owner` | Who owns the artifact at each transition; where context is lost; explicit vs implicit contracts |
| `repeat_churn` | Why the same issue resurfaces; feedback loops; missing gates; tooling vs people failure |

**Preferred archetypes:** `operator`, `cost_complexity`, `skeptic`  
**Often pairs with:** product overlay when prioritization drives process change

**Router signals:** handoff, process, bottleneck, churn, operating model, review flow, design→eng

## Product overlay

**Apply when:** prioritization, roadmap bets, adoption risk, scope fit, build vs fix tradeoffs, ROI questions.

| Dimension | Agent must examine |
|---|---|
| `adoption_risk` | Who must change behavior; switching cost; education burden; failure modes for non-power users |
| `ROI` | Opportunity cost; what this displaces; time-to-value; measurable outcome if wrong |
| `scope_fit` | Whether the ask matches the wedge; what is explicitly deferred; minimum viable decision |

**Preferred archetypes:** `cost_complexity`, `user_advocate`, `skeptic`  
**Often pairs with:** design overlay for experience-heavy bets

**Router signals:** should we ship, prioritize, roadmap, wedge, adoption, build vs fix, ROI

## Stacking overlays

| Investigation shape | Typical stack |
|---|---|
| Design critique before diverge | design |
| Payment failure UX research | research + design |
| Design→eng handoff breaking | workflow (+ product if prioritization implied) |
| Ship AI vs fix onboarding | product + design |
| KYC copy risk review | design + risk_compliance archetype (compliance dimension) |

When stacking, assign each overlay dimension to a distinct agent. Do not let one agent superficially tick every box.

## Overlay in agent brief

Include in every overlay-backed agent prompt:

```text
Domain overlay: [design|research|workflow|product]
Required dimensions: [list from table above]
For each dimension: one finding, one evidence anchor, confidence rating
```
