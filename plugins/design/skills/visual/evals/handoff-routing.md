# Visual Handoff Evals

These cases protect the handoff merge. `visual` owns handoff artifacts; no standalone handoff skill should be loaded.

| # | User request | Expected route / behavior | Forbidden failure |
|---|---|---|---|
| 1 | "Create engineer handoff with states and edge cases" | Route to `visual`; ask for selected components/screens/states if absent | Loading the deleted standalone skill |
| 2 | "Create a handoff for these React components" | Use `visual`; ask for a target route; render actual source components with layer/property breakdown panels | Static reconstruction that ignores app components |
| 3 | "Break down this card visually" | Preserve exact source styling while separating fills, strokes, shadows, opacity, type, spacing, dimensions, and layer order | Imposing a reference-image palette or generic line-art treatment |
| 4 | "Motion handoff for this drawer" | Use `visual`; include scrubber for code output and keyframe/time-ruler representation for Paper/Figma | Prose-only motion notes |
| 5 | "Create this handoff in Figma" | Use `figma:figma-use`; create editable objects; add native annotations and visible comment pins/callouts | Calling `use_figma` without `figma:figma-use` or claiming native comment threads without support |
| 6 | "Create this handoff in Paper" | Use Paper MCP; if unavailable, fall back to code and state the fallback | Pretending HTML output is Paper |
| 7 | "Make a diagram of this API flow" | Use generic visual diagram behavior only | Triggering component handoff layer breakdown |
