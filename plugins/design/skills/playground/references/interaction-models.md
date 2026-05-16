# Interaction Models

Interaction means user action changes state, reveals consequence, improves judgment, or creates exportable feedback. Controls that do not affect understanding are decoration.

Choose at least three candidate models internally, then select one and state why. Do not show options unless the user asked for options.

## Models

parameter tuner -> bounded visual/system variables -> sliders, toggles, segmented controls, presets, live preview, derived metrics -> prompt with non-default deltas and rationale -> avoid random controls that do not map to real variables

canvas/node map -> relationships and spatial thinking -> draggable nodes, edges, zoom, filters, click-to-comment, inspector/details panel -> annotated map export with selected nodes, comments, and unresolved questions -> avoid graph soup with every node at equal weight

review surface -> critique and decision filtering -> approve, reject, comment, line anchors, status filters, severity, before/after preview -> approved-change prompt with rejected items labeled separately -> avoid passive reports that the user cannot act on

state machine -> hidden behavior and transition rules -> trigger buttons, active state, guards, event log, why-blocked messages, replay path -> reproduction or behavior prompt with state path and expected outcome -> avoid fake flows where triggers do not change real state

replay/scrubber -> time, order, motion, sequence, or narrative pacing -> play, pause, step, speed, bookmarks, timeline markers, selected range -> selected-range summary or motion spec -> avoid flat timelines that cannot be scrubbed or compared

simulator -> cause and effect under changing conditions -> scenario switches, coupled variables, repeated runs, derived metrics, warnings, recommended ranges -> recommended patch output or tuning prompt with evidence and assumptions -> avoid fake dashboards with numbers that do not derive from state

lens explorer -> different interpretations of the same material -> user/system/business/engineering lenses, overlays, filters, confidence markers -> selected-lens notes and decision prompt -> avoid tabs that only swap copy without changing interpretation

narrative walkthrough -> presentation, argument, or story that unfolds over time -> section rail, objection drawer, decision checkpoints, appendix, speaker notes -> meeting prompt, review script, or stakeholder follow-up -> avoid deck clones that only paginate static slides

artifact editor -> concrete generated object, UI layout, component, or surface -> direct manipulation, live preview, undo/redo, reset, presets, import/export config -> implementation prompt or config JSON -> avoid decoration-only editing where controls do not affect the artifact's meaning

annotated report -> evidence review and triage -> filters, sections, comments, severity, source links, export JSON/Markdown -> targeted fix prompt or decision memo -> avoid static reports with no filtering, selection, or feedback path

## Fit Test

- What is the user trying to judge, change, learn, or simulate?
- What is the primary state object?
- What action changes state?
- What feedback appears immediately?
- What export becomes more useful because of the interaction?
- Could a static poster replace this without losing the concept? If yes, choose a different model or justify static output.
