# Visual Language

## Mandatory Pre-Build Checklist

Complete this before styling. Do not pick fonts, colors, or layout habits until the grammar is written.

1. Name the topic's primary mechanics (objects, relationships, time, states, tensions, variables).
2. Choose one interaction model from `references/interaction-models.md` and state why.
3. Extract visual grammar from the topic, not from a style adjective:
   - composition and hierarchy
   - depth and layering
   - material and inspectability
   - motion and what must stay still
   - information density
   - typographic contrast (claims vs evidence vs labels)
   - color semantics (what color encodes)
   - texture or imagery only when it aids reasoning
4. Write the grammar as `topic mechanic -> observable outcome -> execution rule -> avoid trap`.
5. Map every important style choice to an observable outcome. Ban decorative defaults unless justified by step 3.
6. If using `tools:media-tools`, extract grammar from the seed and rebuild semantics in HTML/SVG/canvas — do not wallpaper with the bitmap.
7. Start from the matching `assets/templates/` scaffold for the chosen interaction model.

If any step is skipped, the artifact will read generic. Fix the grammar before adding polish.

---

Start from the topic's mechanics, not a style adjective. Visual language is the grammar that makes the artifact easier to understand: composition, depth, material, motion, information density, typographic contrast, color semantics, texture, and imagery.

## Extract The Grammar

- Composition: how objects are arranged to reveal hierarchy, sequence, proximity, ownership, or conflict.
- Depth: which layers sit above others and why.
- Material: what surfaces feel inspectable, editable, fragile, stable, mechanical, narrative, or evidentiary.
- Motion: what changes over time, what needs continuity, and what should stay still.
- Information density: how much the user can scan before detail becomes noise.
- Typographic contrast: how claims, evidence, labels, values, and warnings differ.
- Color semantics: what color encodes, such as risk, confidence, ownership, state, source, or change.
- Texture or generated imagery: when texture, scene, specimen, or product image helps the user reason.

## Style Rule Format

terrain -> risk, proximity, elevation, or route choice matters -> encode elevation/route/proximity through layered contours, paths, checkpoints, and friction -> avoid decorative landscapes that do not encode decisions

instrument -> controls/readouts affect an operating model -> pair each control with a readout, warning, or derived metric -> avoid fake gauges and decorative meters

constellation -> relationship strength or conceptual gravity matters -> size, distance, orbit, and edge weight encode importance and dependency -> avoid random star fields

workbench -> user edits, compares, annotates, or exports an artifact -> keep tools close to the surface, show selected state, and expose undo/reset/export -> avoid dashboard shells around an editor

ledger -> evidence, severity, provenance, or approval matters -> use rows, marks, stamps, deltas, and source notes with clear status -> avoid ornamental tables with no action state

stage -> narrative, sequence, or presentation timing matters -> use section rails, lighting/focus, transitions, and objection/appendix drawers -> avoid slide thumbnails that do not change the argument

machine -> triggers, guards, constraints, and state transitions matter -> use ports, valves, paths, logs, locks, and blocked-state explanations -> avoid sci-fi decoration with no behavior

specimen -> source fidelity, texture, product detail, or visual evidence matters -> place the specimen prominently with callouts and zoom/inspect affordances -> avoid using images as wallpaper

## Generic Defaults To Avoid Unless Justified

- Dark SaaS dashboard.
- Nested cards.
- Purple gradient hero.
- Fake metrics.
- Three-column feature grid.
- Inter/system font by habit.
- Decorative controls that do not change state.
- Repeated chips, tags, or pseudo-system labels that do not add meaning.

## Rationale Rule

Every important style choice must map to an observable outcome. Do not say "premium", "bold", "dynamic", "immersive", "tactile", or similar words unless the execution explains what creates that effect.
