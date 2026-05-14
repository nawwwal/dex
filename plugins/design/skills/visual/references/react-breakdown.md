# React Component Handoff

Use this when the output medium is code and the source is a React app or React component library.

## Required Flow

1. Inspect the project structure and identify the router/framework before editing.
2. Ask for the target route/path for the handoff page if not provided.
3. Import and render actual selected source components whenever possible.
4. Add a handoff index around the real components; do not replace them with static drawings unless the source cannot run.
5. Capture style facts from real DOM/computed styles when feasible.

## Handoff Page Sections

- Component index: selected components/screens and the states included.
- Live preview: rendered source component in each selected state.
- Exploded layer view: source-faithful layers separated into surface, stroke, shadow, content, icon/media, overlay, focus, and hit target.
- Computed style table: fill, border, shadow, radius, opacity, typography, spacing, dimensions, transforms, and z-order.
- State board: default, hover, focus, active, disabled, loading, empty, error, success, and provided domain states.
- Edge-case board: long text, narrow viewport, RTL, slow/error API, missing data.
- Accessibility panel: focus order, target size, contrast, keyboard path, screen-reader naming, reduced-motion fallback.

## Motion Libraries

If the target app uses Razorpay Blade, route product UI motion to `blade` before approving Framer Motion, React Spring, GSAP, Motion One, CSS transitions, or another motion library. If the app is not Blade-owned, build the handoff inside the app so timing and easing can be inspected from the real implementation. Do not flatten motion into self-contained HTML unless the motion is plain CSS and can be recreated faithfully.

## Source Fidelity Rules

- Use actual components and props when the user provides them.
- Do not guess variants. Ask or inspect available component exports/stories/tests.
- Do not alter product behavior in the handoff page.
- Keep the handoff route clearly dev/documentation-scoped.
