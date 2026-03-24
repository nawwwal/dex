# Component Patterns & CSS Techniques

## Buttons Must Feel Responsive

Add `transform: scale(0.97)` on `:active`. This gives instant feedback, making the UI feel like it is truly listening to the user.

```css
.button {
  transition: transform 160ms ease-out;
}

.button:active {
  transform: scale(0.97);
}
```

This applies to any pressable element. The scale should be subtle (0.95-0.98).

## Never Animate from scale(0)

Nothing in the real world disappears and reappears completely. Elements animating from `scale(0)` look like they come out of nowhere.

Start from `scale(0.9)` or higher, combined with opacity. Even a barely-visible initial scale makes the entrance feel more natural.

```css
/* Bad */
.entering {
  transform: scale(0);
}

/* Good */
.entering {
  transform: scale(0.95);
  opacity: 0;
}
```

## Make Popovers Origin-Aware

Popovers should scale in from their trigger, not from center. The default `transform-origin: center` is wrong for almost every popover.

**Exception: modals.** Modals keep `transform-origin: center` because they are not anchored to a specific trigger — they appear centered in the viewport.

```css
/* Radix UI */
.popover {
  transform-origin: var(--radix-popover-content-transform-origin);
}

/* Base UI */
.popover {
  transform-origin: var(--transform-origin);
}
```

## Tooltips: Skip Delay on Subsequent Hovers

Tooltips should delay before appearing to prevent accidental activation. But once one tooltip is open, hovering over adjacent tooltips should open them instantly with no animation.

```css
.tooltip {
  transition: transform 125ms ease-out, opacity 125ms ease-out;
  transform-origin: var(--transform-origin);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Skip animation on subsequent tooltips */
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

## CSS Transitions Over Keyframes for Interruptible UI

CSS transitions can be interrupted and retargeted mid-animation. Keyframes restart from zero. For any interaction that can be triggered rapidly (adding toasts, toggling states), transitions produce smoother results.

```css
/* Interruptible — good for UI */
.toast {
  transition: transform 400ms ease;
}

/* Not interruptible — avoid for dynamic UI */
@keyframes slideIn {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
```

## Use Blur to Mask Imperfect Transitions

When a crossfade between two states feels off despite trying different easings and durations, add subtle `filter: blur(2px)` during the transition.

**Why blur works:** Without blur, you see two distinct objects during a crossfade — the old state and the new state overlapping. Blur bridges the visual gap by blending the two states together.

```css
.button {
  transition: transform 160ms ease-out;
}

.button:active {
  transform: scale(0.97);
}

.button-content {
  transition: filter 200ms ease, opacity 200ms ease;
}

.button-content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Keep blur under 20px. Heavy blur is expensive, especially in Safari.

## @starting-style for CSS-Native Entry Animation

The modern CSS way to animate element entry without JavaScript:

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

This replaces the common React pattern of using `useEffect` to set `mounted: true` after initial render. Fall back to the `data-mounted` attribute pattern when browser support requires it:

```jsx
// Legacy pattern (works everywhere)
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted}>
```

---

## CSS Transform Mastery

### translateY with Percentages

Percentage values in `translate()` are relative to the element's own size. Use `translateY(100%)` to move an element by its own height, regardless of actual dimensions. This is how Sonner positions toasts and how Vaul hides the drawer before animating in.

```css
/* Works regardless of drawer height */
.drawer-hidden {
  transform: translateY(100%);
}

/* Works regardless of toast height */
.toast-enter {
  transform: translateY(-100%);
}
```

Prefer percentages over hardcoded pixel values.

### scale() Scales Children Too

Unlike `width`/`height`, `scale()` also scales an element's children. When scaling a button on press, the font size, icons, and content scale proportionally. This is a feature, not a bug.

### 3D Transforms for Depth

`rotateX()`, `rotateY()` with `transform-style: preserve-3d` create real 3D effects in CSS. Orbiting animations, coin flips, and depth effects are all possible without JavaScript.

```css
.wrapper {
  transform-style: preserve-3d;
}

@keyframes orbit {
  from {
    transform: translate(-50%, -50%) rotateY(0deg) translateZ(72px) rotateY(360deg);
  }
  to {
    transform: translate(-50%, -50%) rotateY(360deg) translateZ(72px) rotateY(0deg);
  }
}
```

---

## clip-path for Animation

`clip-path` is one of the most powerful animation tools in CSS.

### The inset Shape

`clip-path: inset(top right bottom left)` defines a rectangular clipping region. Each value "eats" into the element from that side.

```css
/* Fully hidden from right */
.hidden {
  clip-path: inset(0 100% 0 0);
}

/* Fully visible */
.visible {
  clip-path: inset(0 0 0 0);
}

/* Reveal from left to right */
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms ease-out;
}
.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;
}
```

### Tabs with Perfect Color Transitions

Duplicate the tab list. Style the copy as "active" (different background, different text color). Clip the copy so only the active tab is visible. Animate the clip on tab change. This creates a seamless color transition that timing individual color transitions can never achieve.

### Hold-to-Delete Pattern

Use `clip-path: inset(0 100% 0 0)` on a colored overlay. On `:active`, transition to `inset(0 0 0 0)` over 2s with linear timing. On release, snap back with 200ms ease-out. Add `scale(0.97)` on the button for press feedback.

### Image Reveals on Scroll

Start with `clip-path: inset(0 0 100% 0)` (hidden from bottom). Animate to `inset(0 0 0 0)` when the element enters the viewport. Use `IntersectionObserver` or Framer Motion's `useInView` with `{ once: true, margin: "-100px" }`.

### Comparison Sliders

Overlay two images. Clip the top one with `clip-path: inset(0 50% 0 0)`. Adjust the right inset value based on drag position. No extra DOM elements needed — fully hardware-accelerated.

---

## Container Height Animation

Animate height changes dynamically without knowing the target height in advance.

**The Two-Div Pattern**

Use two separate elements — NEVER the same element for both measuring and animating (creates a feedback loop):

```jsx
function AnimatedContainer({ children }) {
  const [bounds, setBounds] = useState({ height: 0 });
  const ref = useCallback(node => {
    if (node) setBounds(node.getBoundingClientRect());
  }, []);

  return (
    <motion.div
      animate={{ height: bounds.height || "auto" }}
      style={{ overflow: "hidden" }}
    >
      <div ref={ref}>{children}</div>
    </motion.div>
  );
}
```

**Rules:**
- Guard: when `bounds.height === 0` on first render, fall back to `"auto"` (avoids collapsing to 0)
- Use ResizeObserver for ongoing measurement, not `getBoundingClientRect` on every render
- Add `overflow: hidden` to the animated container
- Use a callback ref (not `useRef`) — guarantees the node is ready before measuring
- Add a small delay (`transition={{ delay: 0.05 }}`) for a natural "catching-up" feel
- Use sparingly: buttons, accordions, expandable panels are appropriate contexts

---

## Morphing Icons

SVG icon morphing system using exactly 3 SVG lines. The constraint system works by collapsing unused lines to a center point.

**Core constraint: exactly 3 `<line>` elements always**

Unused lines use the `collapsed` constant, not null or omission:

```tsx
const collapsed = { x1: 7, y1: 7, x2: 7, y2: 7 }; // collapses to center of 14×14 viewBox

function MenuIcon({ isOpen }) {
  return (
    <svg viewBox="0 0 14 14" strokeLinecap="round" aria-hidden="true">
      <line {...(isOpen ? collapsed : { x1: 1, y1: 3, x2: 13, y2: 3 })} />
      <line {...(isOpen ? { x1: 2, y1: 12, x2: 12, y2: 2 } : { x1: 1, y1: 7, x2: 13, y2: 7 })} />
      <line {...(isOpen ? collapsed : { x1: 1, y1: 11, x2: 13, y2: 11 })} />
    </svg>
  );
}
```

**Rules:**
- Exactly 3 `<line>` elements always — never more, never fewer
- Unused lines use the `collapsed` constant (not null or omission)
- All icons share the same viewBox (14×14 recommended)
- Rotational variants: group lines and rotate the group, sharing base lines
- Use spring physics for rotation (not duration-based)
- Respect `prefers-reduced-motion` via `useReducedMotion()` — jump instead of animate
- Non-grouped icon transitions jump instantly with `rotation.jump()` (no spring)
- `strokeLinecap="round"` on the SVG element
- Icon SVGs are `aria-hidden="true"` (not interactive elements, described by sibling text)
