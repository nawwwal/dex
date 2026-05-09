# Exact-Style Layer Breakdown

Use exploded technical structure while preserving the selected UI's real visual style.

## Layers To Separate

For each component or screen, separate these layers when present:

| Layer | Show | Capture |
|---|---|---|
| Base surface | Background or container | fill, token/value, opacity, radius |
| Border/stroke | Outline, divider, focus ring | color, width, style, radius alignment |
| Shadow/elevation | Surface depth | offset, blur, spread, color, opacity, token |
| Content | Text and primary data | font family, size, weight, line height, color, truncation |
| Icon/media | Icons, images, illustrations | size, color, stroke/fill, alignment |
| Overlay | badges, menus, scrims, loading layers | z-order, opacity, trigger, dismissal |
| Hit target | interactive area | target size, padding, focus behavior |
| State delta | what changes between states | property changed, before value, after value |

## Visual Mechanics

- Use exploded stacks, callout pins, rulers, measurement rails, and side property panels.
- Keep the original visual treatment on the separated layers. Annotation marks can be neutral, but source layers keep their real fill, stroke, shadow, opacity, and type.
- Label by engineering-relevant terms: surface, stroke, elevation, padding, gap, radius, typography, icon, overlay, focus, hit target.
- Prefer exact values from computed styles, design tokens, Figma properties, or source code. If unavailable, mark as `inspect source` or ask.

## Quality Gates

- A developer can identify what to implement without reading the component internals.
- A designer can verify visual fidelity from the breakdown.
- State differences are visible as property changes, not just labels.
- Layer order and interaction target boundaries are explicit.
