# Blade Motion

Use this reference whenever a UI change involves animation, transition, reveal, hover feedback, route transition, loading/success treatment, or custom motion code. Query Blade MCP before choosing a primitive:

```text
get_blade_component_docs("AnimateInteractions,Fade,Move,Slide,Scale,Morph,Stagger,Elevate")
get_blade_pattern_docs("SparkAnimation")
get_blade_component_docs("RazorSense,RazorSenseGradient")
```

## Selection Map

| Need | Use | Execution | Avoid |
| --- | --- | --- | --- |
| Soften content appearing or disappearing | `Fade` | Use controlled `isVisible` for state changes, `motionTriggers={['mount']}` for route/content entry, and `shouldUnmountWhenHidden` only when removal is intended. | CSS opacity classes, hiding interactive content without checking focus behavior. |
| Give entering content spatial arrival | `Move` | Use for cards, forms, inline panels, or content that should fade while shifting position. Add stable container height when unmounting. | Large page travel, manual translate keyframes, motion that changes layout after the user starts reading. |
| Bring a surface from an edge | `Slide` | Use for panel/page entrances where direction communicates source: bottom for mobile/action sheets, side for lateral navigation, top for global notices. Prefer `Drawer`, `Modal`, or `BottomSheet` when those semantics fit. | Fixed custom overlays or viewport transforms for existing overlay components. |
| Communicate interaction affordance | `Elevate` or `Scale` | Use `motionTriggers={['hover', 'focus']}` for pointer + keyboard parity. Use `variant="scale-down"` for tap press feedback. | Hover-only CSS, scale on dense table rows, interaction feedback without focus state. |
| Coordinate children from one parent interaction | `AnimateInteractions` | Wrap the parent, then give children `motionTriggers={['on-animate-interactions']}` through `Fade`, `Move`, `Scale`, or `Elevate`. | Reimplementing `.parent:hover .child` in CSS or attaching duplicate hover state to each child. |
| Reveal repeated sibling items in order | `Stagger` | Wrap repeated children and combine with `Fade` or `Move` so order is visible without manual delay math. | Per-item timeout chains, hardcoded CSS delay ladders. |
| Preserve object continuity across states | `Morph` | Use a shared `layoutId` for one conceptual object changing shape, position, or component form. Keep the before/after states visually related. | Morphing unrelated objects, using it for simple show/hide, or hiding structural jumps it cannot actually solve. |
| Create branded success/loading moments | `SparkAnimation`, `RazorSense`, `RazorSenseGradient` | Use presets such as `circleSlideUp`, `rippleWave`, `bottomWave`, or `zoomed`; call `preloadRazorSenseAssets(preset)` before mounting; keep SVG mask children filled white for `RazorSenseGradient`. | Decorative WebGL in dense operational pages, unpreloaded shader mounts, hex/CSS color props where docs require RGB arrays. |

## Trigger Rules

- Use `mount` for page or route entry when the content is newly rendered.
- Use controlled `isVisible` for UI that toggles after user action.
- Use `in-view` for long scroll surfaces; do not use it for primary dashboard content above the fold.
- Use `hover` only with `focus` when the element is keyboard reachable.
- Use `tap` or `press` only for clear press feedback; do not attach tap motion to non-clickable content.
- Use `on-animate-interactions` only inside `AnimateInteractions`.

## Custom Motion Rejection Log

When keeping custom CSS transitions, keyframes, Framer Motion, timers, or WebGL, record the Blade path that was checked:

```text
Blade motion candidate checked: Move, Fade, AnimateInteractions
Rejected because: transition depends on cross-route shared state not expressible with Blade primitives
Custom motion kept: one route-level wrapper using existing app motion dependency
Follow-up risk: verify focus order, reduced-motion behavior, and layout stability in browser
```

## Validation

Validate motion in the browser, not only in code. Use `agent-browser diff` for open/close, hover/focus, and route changes. Check that the animated element does not resize its parent unexpectedly, trap focus, hide active controls while still tabbable, or leave a delayed invisible layer above clickable UI.
