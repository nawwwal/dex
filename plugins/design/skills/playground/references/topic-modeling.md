# Topic Modeling

Map source material into an artifact structure before choosing a visual treatment. Extract the topic's real objects, relationships, time, states, tensions, variables, decisions, risks, and user questions.

## Mappings

| Topic | Model | Useful artifact structures |
|---|---|---|
| Codebase | Modules, ownership, dependencies, runtime flows, data boundaries, risk areas, change hotspots | Canvas/node map, layered architecture map, dependency explorer, annotated report |
| UI/component | Layout, hierarchy, density, visual variables, states, variants, interactions, responsive behavior | Artifact editor for layout changes and tuning, state board, component inspector, motion scrubber |
| Presentation | Problem, evidence, argument, objections, decision checkpoints, audience risks | Narrative walkthrough, objection drawer, decision rail, appendix explorer |
| Copy | User state, system state, risk, tone, CTA, state variants, error causes, localization constraints | Review surface, copy/state explorer, lens explorer, variant approver |
| Game/balance | Stats, costs, cooldowns, probabilities, deck composition, dominant strategies, failure loops | Simulator, parameter tuner, replay/scrubber, warnings panel |
| Data/table | Groups, outliers, filters, missing values, comparisons, thresholds, confidence | Filterable table, comparison lens, annotated report, outlier map |
| Strategy/problem | Claims, premises, tensions, tradeoffs, confidence, unknowns, decision criteria | Lens explorer, argument map, annotated report, decision walkthrough |

## Extraction Questions

- What can the user change, judge, compare, or annotate?
- What state must be visible for the artifact to be useful?
- What source truth must be preserved?
- What risks or uncertainties must be labeled instead of smoothed over?
- What export would let an agent act without reopening the artifact?

## Stop Rule

Do not start with style. If source material is missing, ask for it or inspect the repo first. Use `design:crux` only when the premise, weak joint, or standard of judgment is unclear.
