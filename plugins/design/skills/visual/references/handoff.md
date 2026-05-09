# Visual Handoff

Use this when the user asks for a handoff, engineer handoff, implementation spec, component inventory, screen inventory, state inventory, visual breakdown, or motion handoff.

## Intake

Before generating, confirm the selected source unless it is already provided:

- Components, screens, routes, Figma nodes, or screenshots to include.
- States to show: default, hover, focus, active, disabled, loading, empty, error, success, permission, offline, or domain-specific states.
- Output medium: code, Paper, or Figma. Default to code when unspecified.
- For React code output: target route/path for the handoff page.
- For motion: trigger, duration, easing, affected properties, interruption behavior, and reduced-motion expectation.

If the user only gives a rough feature description, ask for the selected components/screens/states before producing the artifact. Do not infer a full component inventory from vibes.

## Artifact Contract

Every handoff artifact must include:

- Source preview: real component, actual screen, source-faithful image, or clearly labeled unavailable source.
- Layer breakdown: separated visual layers with exact source styling.
- Property panel: fills, strokes, shadows, opacity, blur, radius, typography, spacing, dimensions, and layer order.
- State board: selected states with user meaning, system meaning, visual difference, copy, action, and edge case.
- Screen map when more than one screen is selected.
- Accessibility notes: focus order, target size, contrast, screen-reader label, keyboard behavior, reduced-motion alternative.
- Open questions: only unresolved facts needed by engineers.

## Stop Rules

- Do not produce a prose-only spec when the user asked for a handoff.
- Do not invent component props, design tokens, or motion-library APIs. Inspect or ask.
- Do not impose a reference-image palette. The sample images define breakdown structure only.
- If Blade mapping is requested, route to `design:blade` first, then include its result in the visual handoff.
