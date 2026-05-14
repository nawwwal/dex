# Blade Motion

Use this reference whenever a UI change involves animation, transition, reveal, hover feedback, route transition, or loading/success treatment. For broader craft judgement such as transition mapping, density, typography, hit areas, and Blade-only constraints, read `interaction-quality.md`. Query Blade MCP before choosing a primitive:

```text
get_blade_component_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  componentsList: "AnimateInteractions,Fade,Move,Slide,Scale,Morph,Stagger,Elevate",
  clientName: "cursor"
})
get_blade_pattern_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  patternsList: "SparkAnimation",
  clientName: "cursor"
})
get_blade_component_docs({
  currentProjectRootDirectory: "<absolute consumer app root>",
  componentsList: "RazorSense,RazorSenseGradient",
  clientName: "cursor"
})
```

## Selection Map

Motion ownership rule: the semantic Blade component still owns meaning, disclosure, focus, escape behavior, stacking, and ARIA. A motion primitive owns one physical change: opacity, position, edge entry, shadow, scale, continuity, sequence, or parent-trigger coordination.

| Need | Use | Execution | Avoid |
| --- | --- | --- | --- |
| Soften content appearing or disappearing | `Fade` | Use controlled `isVisible` for state changes, `motionTriggers={['mount']}` for route/content entry, and `shouldUnmountWhenHidden` only when removal is intended. | CSS opacity classes, hiding interactive content without checking focus behavior. |
| Give entering content spatial arrival | `Move` | Use for cards, forms, inline panels, or content that should fade while shifting position. Add stable container height when unmounting. | Large page travel, manual translate keyframes, motion that changes layout after the user starts reading. |
| Bring a surface from an edge | `Slide` | Use for panel/page entrances where direction communicates source: bottom for mobile/action sheets, side for lateral navigation, top for global notices. Prefer `Drawer`, `Modal`, or `BottomSheet` when those semantics fit. | Fixed custom overlays or viewport transforms for existing overlay components. |
| Communicate interaction affordance | `Elevate` first, `Scale` when fixed scale is acceptable | Use `motionTriggers={['hover', 'focus']}` for pointer + keyboard parity. Use `variant="scale-down"` for tap press feedback only when the fixed compression feels right. On large cards, prefer `Elevate` plus a stable width before adding scale. | `Card shouldScaleOnHover` by default, hover-only CSS, scale on dense table rows, interaction feedback without focus state. |
| Coordinate children from one parent interaction | `AnimateInteractions` | Wrap the parent, then give children `motionTriggers={['on-animate-interactions']}` through `Fade`, `Move`, `Scale`, or `Elevate`. | Reimplementing `.parent:hover .child` in CSS or attaching duplicate hover state to each child. |
| Reveal repeated sibling items in order | `Stagger` | Wrap repeated children and combine with `Fade` or `Move` so order is visible without manual delay math. | Per-item timeout chains, hardcoded CSS delay ladders. |
| Preserve object continuity across states | `Morph` | Use a shared `layoutId` for one conceptual object changing shape, position, or component form. Keep the before/after states visually related. | Morphing unrelated objects, using it for simple show/hide, or hiding structural jumps it cannot actually solve. |
| Create branded success/loading moments | `SparkAnimation`, `RazorSense`, `RazorSenseGradient` | Use presets such as `circleSlideUp`, `rippleWave`, `bottomWave`, or `zoomed`; call `preloadRazorSenseAssets(preset)` before mounting; keep SVG mask children filled white for `RazorSenseGradient`. | Decorative WebGL in dense operational pages, unpreloaded shader mounts, hex/CSS color props where docs require RGB arrays. |

## Trigger Rules

- Do not transpose trigger names between primitives. Use only the triggers MCP returns for the exact component.
- Use `mount` for page or route entry when the content is newly rendered.
- Use controlled `isVisible` for UI that toggles after user action.
- Use `in-view` for long scroll surfaces; do not use it for primary dashboard content above the fold.
- Use `hover` only with `focus` when the element is keyboard reachable.
- Use `tap` or `press` only when MCP exposes that trigger for the chosen primitive and the element is genuinely pressable.
- Use `on-animate-interactions` only inside `AnimateInteractions`.
- Use branded/WebGL motion only for branded moments, success/loading treatments, or deliberately expressive surfaces. Do not add it as decoration inside dense operational workflows.

Trigger vocabulary:

| Trigger | Meaning | Guardrail |
| --- | --- | --- |
| `hover` | Pointer hover feedback. | Pair with `focus` for keyboard parity when the object is reachable. |
| `focus` | Keyboard focus feedback. | Do not use it to hide focus rings or replace semantic focus. |
| `tap` / `press` | Press feedback. | Use the exact term MCP documents for that primitive; do not guess. |
| `mount` | First render entry. | Avoid repeated route loops or delayed critical content. |
| `in-view` | Scroll reveal. | Skip for above-the-fold dashboard content. |
| `on-animate-interactions` | Child response to an `AnimateInteractions` parent. | Only valid inside that parent pattern. |

## Motion fit rules

Blade motion docs answer what the API accepts. The skill must also decide whether the motion fits the product context.

Use this general rule:

| Context | Prefer | Why |
| --- | --- | --- |
| Isolated clickable object with stable bounds | Blade interaction motion such as `Scale` or `Elevate` | The motion stays attached to one object and does not disturb layout. |
| Dense operational surface | `Elevate`, state color, border/selection, or child reveal before transform scale | Dense UI rewards clarity and stability more than object movement. |
| Page, panel, or route transition | `Fade`, `Move`, `Slide`, `Morph`, or existing app-shell transition after MCP lookup | Spatial change needs source/destination meaning, not decorative movement. |
| Parent-child affordance | `AnimateInteractions` with child motion using `on-animate-interactions` | One parent owns the trigger; children only respond. |
| Missing intensity/distance/timing parameter | Choose the nearest Blade primitive, reduce the effect, or skip it | Blade may expose the behavior but not the product-critical value; do not recreate the primitive. |

Do not use a motion prop just because MCP shows it exists. First check: stable bounds, focus parity, no text blur, no overlap, no parent resizing, no delayed invisible layer, and console has no motion/ref warning.

If a Blade primitive exposes behavior but not intensity, distance, or timing, do not invent a prop. Either accept the preset after visual verification, choose a different Blade primitive, or skip the effect.

## Blade-native animation rules

These rules translate general web animation judgement into Blade constraints:

- Use Blade preset timing/easing when Blade owns the motion. Do not override internal duration or easing unless MCP exposes the prop.
- Use web-animation timing judgement to select Blade primitives: entry/exit maps to `Fade`, `Move`, `Slide`, or overlays; on-screen continuity maps to `Move` or `Morph`; hover/focus maps to component state, `Elevate`, `Scale`, or `AnimateInteractions`.
- Avoid `ease-in` for UI feedback because it delays the first visible response.
- Use motion only when it improves continuity, feedback, hierarchy, or rare branded moments. In high-frequency dashboard actions, prefer instant state, elevation, color, or selection.
- Prefer Blade primitives that animate transform/opacity. Treat width/height/margin/padding animation as unsupported unless Blade or the app shell already owns that layout transition.
- Pair timings for elements that read as one object: overlay and surface, trigger and menu, parent and child reveal.
- Respect reduced motion by preferring Blade-owned motion. If Blade cannot safely own it, do not ship the motion.

## Composing motion primitives

Motion primitives need a child that can accept the required motion/ref behavior. If nested motion wrappers produce React ref warnings, do not keep stacking wrappers until the warning disappears.

General pattern:

```tsx
<AnimateInteractions motionTriggers={['hover', 'focus']}>
  <Box display="block">
    <Elevate motionTriggers={['on-animate-interactions']}>
      <Card>...</Card>
    </Elevate>
  </Box>
</AnimateInteractions>
```

```tsx
<Scale variant="scale-down" motionTriggers={['tap']}>
  <Box display="block">
    <Card>...</Card>
  </Box>
</Scale>
```

Rules:
- Prefer one motion owner for one physical property. `Elevate` owns shadow; `Scale` owns transform; `Move` owns position and opacity.
- Put a DOM-capable Blade `Box` boundary between coordinated motion layers when ref warnings appear.
- Do not stack the same primitive to fake a parameter the API does not expose. If two states require different values, choose a different Blade primitive or simplify the interaction.
- Keep dimensions stable around motion. Width, height, overflow, and hit area should be owned by the surrounding layout, not by the animated transform.

## Blade limitation log

When Blade cannot express the exact motion requested, record the Blade path and the Blade-native fallback:

```text
Blade motion candidate checked: Move, Fade, AnimateInteractions
Limitation: requested transition depends on cross-route shared state not exposed by Blade primitives
Blade-native fallback: route changes instantly; local content uses Fade on mount
Not used: custom CSS transitions, undocumented Framer wrappers, timers, keyframes, WebGL
Follow-up risk: verify focus order and layout stability in browser
```

Exception: if MCP docs for a Blade-owned component or pattern explicitly require `framer-motion`, `AnimatePresence`, or a preload helper, use that documented dependency exactly for that Blade path. Do not use it as permission to wrap unrelated Blade components.

## Validation

Validate motion in the browser, not only in code. Use `agent-browser diff` for open/close, hover/focus, and route changes. Check that the animated element does not resize its parent unexpectedly, trap focus, hide active controls while still tabbable, or leave a delayed invisible layer above clickable UI.
