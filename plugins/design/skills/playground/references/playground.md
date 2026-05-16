# Playground Contract

A playground is an interactive visual artifact that helps the user understand, manipulate, annotate, decide, and export feedback back to the agent.

It is not just a diagram, dashboard, mockup, or HTML page with controls. It is a workbench: the user can inspect the topic, change something meaningful, see immediate feedback, and leave with an agent-ready next prompt or handoff.

## Default Anatomy

- Main visual surface: the primary artifact, map, simulator, review surface, editor, state model, walkthrough, or handoff.
- Interaction surface: direct manipulation, controls, filters, scrubbers, triggers, comments, or selection states that change the artifact.
- Inspector/details panel: selected object details, assumptions, source notes, state explanation, warnings, or derived metrics.
- Annotation/comment system when useful: anchored comments, approve/reject state, node comments, decision notes, or bookmarks.
- Export/paste-back output: a natural-language prompt or handoff packet that the user can paste into the agent.
- Source notes and assumptions: what source material was used, what was inferred, and what is unknown.

## Required Behavior

- Non-static by default. Static output is valid only when interaction would not improve understanding, and the artifact must say why.
- Useful first render before interaction. The first screen must teach something before the user touches controls.
- Immediate feedback after interaction. State changes must visibly affect the surface, inspector, export, or event log.
- Topic-specific visual language. Layout, material, density, color, type, and motion must come from the topic's mechanics.
- Agent-ready export. The output must include enough context to act without seeing the playground.

## Playground Modes

- Map: relationships, ownership, dependency, sequence, or spatial thinking.
- Review: anchored critique, approve/reject/comment, severity, and selected-change export.
- Simulator: coupled variables, derived metrics, warnings, and recommended tuning.
- Editor: direct manipulation, presets, live preview, undo/reset, and implementation/config export.
- State machine: active state, triggers, guards, event log, and blocked-action explanations.
- Scrubber: timeline, play/pause, step, speed, bookmarks, and selected-range export.
- Walkthrough: narrative rail, objections, decision checkpoints, appendix, and meeting script export.
- Handoff: source-faithful layers, states, properties, motion, responsive notes, and implementation handoff.

## Done State

Return the artifact path, open method, what the artifact proves, what it does not prove, and how the user should copy or export feedback back into the agent.
