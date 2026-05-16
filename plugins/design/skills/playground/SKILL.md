---
name: playground
description: Create interactive, visually distinctive HTML, Paper, Figma, or React playgrounds and visual artifacts for topics, systems, code, data, design, presentations, copy, handoffs, state machines, simulations, reviews, and motion.
allowed-tools: Read, Write, Bash, Grep, Glob, Skill
---

# Playground

Use this when the user needs an artifact workbench: a visual surface that helps them understand, manipulate, annotate, compare, simulate, review, or export decisions back to the agent.

Default to standalone interactive HTML. Use Paper, Figma, or React only when the user asks for that medium or source fidelity requires it.

## Operating Model

1. Understand the topic.
Extract objects, relationships, time, states, tensions, variables, decisions, risks, source truth, and user questions.

2. Route companion skills before building.
- Use `design:diverge` only when the user asks for multiple directions, options, or concepts.
- Use `imagegen` when a generated bitmap seed, texture, scene, mockup, or visual reference would materially improve the artifact. When the user asks for visual inspiration first, name `imagegen`, create one `inspiration seed`, extract `visual grammar`, then rebuild the structure in HTML/SVG/canvas. The response must say the generated image is not wallpaper and must keep labels, controls, state, and export outside the bitmap.
- Use `design:present` before interactive presentation walkthroughs, design review narratives, stakeholder walkthroughs, or narrative HTML artifacts.
- Use `design:content-design` before copy, state, tone, or CTA review playgrounds.
- Use `design:crux` when the premise or weak joint is unclear.
- Use `frontend-design` or app-specific dev skills only for production frontend implementation.
- Do not route production UI to `playground` or `impeccable`. The response must route to `frontend-design` or the app-specific dev skill and should use that exact phrase when declining playground ownership.
- For pure skill, document, or code review surfaces, stay in `playground` unless the user asks for strategy, copy, presentation, production UI, or premise critique.
- Do not route generation work to `harden`; hardening is for final implemented UI.
When routing to a companion skill, name the exact skill in the response before describing the playground.

3. Choose the interaction model.
Internally consider at least three models from `references/interaction-models.md`, choose one, and state why. Do not show options unless the user asked for options.
For concrete UI layout changes, component tuning, generated objects, or surface editing, prefer `artifact editor` unless the source clearly requires a map, review surface, state machine, scrubber, or simulator.
For `artifact editor`, explicitly include live preview, reset, and export / paste-back output.

4. Choose the visual language.
Derive composition, material, motion, density, color semantics, typographic behavior, and metaphor from the topic. Every style choice must map to an observable outcome.

5. Build the artifact.
Default to one self-contained HTML file with inline CSS/JS, no remote scripts, instant interaction, export/paste-back output, browser inspection, keyboard access, reduced-motion support, and mobile handling.

6. Return the result.
Return the artifact path, open method, selected interaction model, selected visual grammar, source assumptions, artifact anatomy, what it proves, what it does not prove, and export / paste-back output.

If the user explicitly asks for read-only review, inline suggestions, or no file/artifact creation, do not build a file. Return anchored suggestions in chat and include the same interaction model, visual grammar, source assumptions, and export shape the artifact would have used.

## References

- Main playground contract: `references/playground.md`
- Topic-to-artifact mapping: `references/topic-modeling.md`
- Interaction model selection: `references/interaction-models.md`
- Topic-specific visual grammar: `references/visual-language.md`
- Image generation integration: `references/image-seeding.md`
- Artifact metadata and lifecycle: `references/artifact-contract.md`
- Standalone HTML rules: `references/interactive-html.md`
- Paste-back output formats: `references/export-output.md`
- Handoffs and breakdowns: `references/handoff.md`, `references/layer-breakdown.md`
- React/app route output: `references/react-breakdown.md`
- Motion handoffs: `references/motion-handoff.md`
- Paper/Figma/code routing: `references/output-media.md`

## Stop Rules

- Static output is valid only when interaction would add no understanding; state that reason explicitly.
- Do not make generic dashboards, nested-card pages, purple AI gradients, fake metrics, or decorative controls.
- Do not hide essential information inside generated images.
- Do not create production UI unless explicitly requested.
