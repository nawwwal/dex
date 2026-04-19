# Performance Rules & Accessibility

## Never Use `transition: all`

Always specify the exact properties that change.

```css
.button {
  transition-property: transform, opacity;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}
```

Tailwind note:
- `transition-transform` covers transform-related properties only
- For multiple explicit properties, use bracket syntax such as `transition-[scale,opacity,filter]`
- Do not use Tailwind's bare `transition` utility when you need strict control

## Prefer transform and opacity

These properties skip layout and paint, running on the GPU. Animating `padding`, `margin`, `height`, or `width` triggers all three rendering steps and causes jank. Subtle `filter` effects like blur are acceptable for polish when used sparingly, but they are still more expensive than plain `transform` and `opacity`.

## CSS Variables Are Inheritable — Be Careful

Changing a CSS variable on a parent recalculates styles for all children. In a drawer with many items, updating `--swipe-amount` on the container causes expensive style recalculation. Update `transform` directly on the element instead.

```js
// Bad: triggers recalc on all children
element.style.setProperty('--swipe-amount', `${distance}px`);

// Good: only affects this element
element.style.transform = `translateY(${distance}px)`;
```

## Framer Motion Hardware Acceleration Caveat

Framer Motion's shorthand properties (`x`, `y`, `scale`) are NOT hardware-accelerated. They use `requestAnimationFrame` on the main thread. For hardware acceleration, use the full `transform` string:

```jsx
// NOT hardware accelerated (convenient but drops frames under load)
<motion.div animate={{ x: 100 }} />

// Hardware accelerated (stays smooth even when main thread is busy)
<motion.div animate={{ transform: "translateX(100px)" }} />
```

This matters when the browser is simultaneously loading content, running scripts, or painting. At Vercel, the dashboard tab animation used Shared Layout Animations and dropped frames during page loads. Switching to CSS animations (off main thread) fixed it.

## CSS Animations Beat JS Under Load

CSS animations run off the main thread. When the browser is busy loading a new page, Framer Motion animations (using `requestAnimationFrame`) drop frames. CSS animations remain smooth. Use CSS for predetermined animations; JS for dynamic, interruptible ones.

## Use `will-change` Sparingly

`will-change` is a last-mile performance hint, not a default styling tool.

- Use it only when you notice first-frame stutter
- Limit it to compositor-friendly properties such as `transform`, `opacity`, and `filter`
- Never use `will-change: all`
- Prefer applying it only around the animation window instead of permanently across the app

```css
.animated-card {
  will-change: transform, opacity;
}
```

```css
.animated-card {
  will-change: all; /* never */
}
```

## Use WAAPI for Programmatic CSS Animations

The Web Animations API gives you JavaScript control with CSS performance. Hardware-accelerated, interruptible, and no library needed.

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  {
    duration: 1000,
    fill: 'forwards',
    easing: 'cubic-bezier(0.77, 0, 0.175, 1)',
  }
);
```

---

## Accessibility

### prefers-reduced-motion

Animations can cause motion sickness. Reduced motion means fewer and gentler animations, not zero. Keep opacity and color transitions that aid comprehension. Remove movement and position animations.

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: fade 0.2s ease;
    /* No transform-based motion */
  }
}
```

```jsx
const shouldReduceMotion = useReducedMotion();
const closedX = shouldReduceMotion ? 0 : '-100%';
```

### Touch Device Hover States

Touch devices trigger hover on tap, causing false positives. Gate hover animations behind this media query:

```css
@media (hover: hover) and (pointer: fine) {
  .element:hover {
    transform: scale(1.05);
  }
}
```

---

## Audio and prefers-reduced-motion

prefers-reduced-motion has three dimensions — each owned by a different file:

1. **CSS animation** (this file) — transform-based motion, position animations
2. **Audio/sound** → `motion/audio.md` — suppress audio playback when PRM is enabled
3. **Accessibility checklist** → `ui/a11y.md` — pointer to both

When `prefers-reduced-motion: reduce` is active, suppress audio feedback alongside visual motion. Motion-sensitive users frequently have auditory sensitivity as well.
