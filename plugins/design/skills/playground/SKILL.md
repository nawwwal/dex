---
name: visual
description: Use when creating diagrams, visual explanations, system/API/data flows, dense-table explanations, visual handoffs, component/state/screen breakdowns, or motion handoff artifacts.
allowed-tools: Read, Write, Bash, Grep, Glob, Skill
---

# Visual

Use this when a visual artifact will make structure easier to inspect than prose: diagrams, system flows, API/data flows, comparisons, timelines, dense tables, visual handoffs, component/state/screen breakdowns, and motion handoff artifacts.

Default output medium is source-aware code. Use self-contained HTML only when it can faithfully recreate the source component or motion. For React apps, ask for the target route before writing a handoff page.

## Rules

- Generic diagrams, flows, comparisons, timelines, and dense-table explanations: read `references/visual.md`.
- Handoff, engineer handoff, spec, component inventory, state inventory, screen inventory, or visual breakdown: read `references/handoff.md` and `references/layer-breakdown.md`.
- React component handoff or app route output: also read `references/react-breakdown.md`.
- Motion handoff, transition handoff, scrubber, keyframe, easing, or timeline request: also read `references/motion-handoff.md`.
- Paper, Figma, or explicit output medium request: also read `references/output-media.md`.
- Choose styling from the audience and content density. Do not randomize aesthetics.
- Handoff breakdowns must preserve exact source styling for each layer: fills, strokes, shadows, opacity, blur, typography, spacing, dimensions, and layer order.
- Keep visuals inspectable at 320px and 1440px unless the output medium has fixed artboard constraints.
- Do not handle slide-file conversion or deck generation.
