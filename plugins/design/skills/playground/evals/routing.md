# Playground Routing Evals

These cases protect the rename from `visual` to `playground` and ensure the skill produces source-grounded interactive artifacts rather than generic static visuals.

| # | Prompt | Expected behavior |
|---|---|---|
| 1 | "Use playground to explore layout changes to this question tool." | Builds an artifact editor with live preview, meaningful presets, stateful controls, and export prompt. |
| 2 | "Show how this email agent codebase works and let me comment on nodes." | Builds a canvas/node map with click-to-comment, layer filters, inspector, and export feedback. |
| 3 | "Review my SKILL.md and give inline suggestions I can approve, reject, or comment." | Builds a review surface with anchored suggestions, approve/reject/comment states, filters, and approved-change export. |
| 4 | "Help me balance the Inferno hero deck." | Builds a simulator with coupled variables, derived metrics, warnings, and recommended patch output. |
| 5 | "Turn this design review narrative into interactive HTML." | Routes through `design:present`, then creates a narrative walkthrough playground. |
| 6 | "Make the copy sharper and show it as an interactive state explorer." | Routes through `design:content-design`, then creates a copy/state playground. |
| 7 | "Generate visual inspiration first for this architecture playground." | Routes through `imagegen`, then extracts or embeds visual grammar without using the image as wallpaper. |
| 8 | "Create a static diagram of this API flow." | Static output is valid only if the response explicitly states why interaction adds no value. |
| 9 | "Show three different visual concepts." | Routes to `design:diverge`, not playground. |
| 10 | "Build this as production UI." | Routes to `frontend-design` or the app-specific implementation skill, not playground. |
| 11 | "Motion handoff for this drawer." | Creates a motion playground with scrubber, play/pause, speed, reduced-motion behavior, keyframe/state markers, and exportable spec. |
| 12 | "Create this in Paper." | Uses the Paper surface when available; does not call HTML output Paper. |
| 13 | "Create this in Figma." | Uses the Figma surface with editable objects/annotations, not a flattened screenshot. |

## Failure Signals

- Output is static without justification.
- Output uses generic dashboard styling, nested cards, purple gradients, fake metrics, or decorative controls.
- Output lacks a state model or export/paste-back output.
- Output lacks keyboard access, focus states, or reduced-motion handling for interactive artifacts.
- Output depends on external scripts by default.
- Output routes options, production UI, or final hardening through `playground` instead of the owning skill.
