# Interactive HTML

Default playground output is one standalone HTML file. It should open directly in a browser and work without a dev server unless the user or source fidelity requires an app route.

## Required Technical Rules

- Single HTML file by default.
- Inline CSS and JavaScript.
- No CDN, imports, or remote scripts by default.
- One shared state object.
- `DEFAULTS`, `state`, and `updateAll()` or equivalent pattern.
- `updatePrompt()` or equivalent export renderer.
- Copy button with visible success/failure feedback.
- Export state JSON and import state JSON for non-trivial artifacts.
- Reset control.
- Keyboard-accessible controls and direct-manipulation alternatives.
- Visible focus states.
- Reduced-motion handling through `prefers-reduced-motion` and a state toggle when motion is central.
- Responsive behavior at 320px, 390px, and desktop.
- No unsanitized `innerHTML` for user-provided content.
- No secrets, credentials, tokens, or private data in `localStorage`, state, or export.

## Recommended Structure

```html
<script>
const DEFAULTS = {};
let state = structuredClone(DEFAULTS);

function updateAll() {
  renderSurface();
  renderInspector();
  updatePrompt();
}

function updatePrompt() {
  // Render natural-language paste-back output and optional JSON.
}
</script>
```

## Interaction Quality

- Every control must change state or export output.
- The selected object, state, or range must be visible.
- Warnings must explain what changed and why it matters.
- Canvas or drag interactions need keyboard or control-panel equivalents.
- Motion must pause or simplify under reduced motion.

## Security And Privacy

- Do not include credential forms, fake auth flows, payment forms, destructive admin actions, or deceptive login pages unless the artifact is explicitly a local non-deployable mock.
- Treat user-provided text as untrusted. Use `textContent`, attribute setters, or explicit escaping.
