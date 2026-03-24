# Framer Motion / motion/react API Reference

> Package renamed: use `motion/react` not `framer-motion` in new projects.

## Core Import
```tsx
import { motion, AnimatePresence, useAnimation, useMotionValue, useTransform } from 'motion/react';
```

## Basic Animate
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
/>
```

## AnimatePresence (for mount/unmount)
```tsx
<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div key="modal" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      {children}
    </motion.div>
  )}
</AnimatePresence>
```

## Layout Animations (shared elements)
```tsx
// Same layoutId = smooth morph between states
<motion.div layoutId="card-header" />
```

## Gestures
```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: 'spring', stiffness: 400, damping: 25 }}
/>
```

## useMotionValue + useTransform (scroll-linked)
```tsx
const scrollY = useMotionValue(0);
const opacity = useTransform(scrollY, [0, 100], [1, 0]);
```

## Reduced Motion Support
```tsx
import { useReducedMotion } from 'motion/react';
const shouldReduceMotion = useReducedMotion();
const animProps = shouldReduceMotion ? {} : { initial: { opacity: 0 }, animate: { opacity: 1 } };
```

## Common Spring Configs
```tsx
// Snappy interaction
{ type: 'spring', stiffness: 400, damping: 25 }
// Gentle entrance
{ type: 'spring', stiffness: 200, damping: 30 }
// Bouncy
{ type: 'spring', stiffness: 500, damping: 20, mass: 0.8 }
```

---

## Spring Deep-Dive

Springs feel more natural than duration-based animations because they simulate real physics. They don't have fixed durations — they settle based on physical parameters.

### When to Use Springs

- Drag interactions with momentum
- Elements that should feel "alive" (like Apple's Dynamic Island)
- Gestures that can be interrupted mid-animation
- Decorative mouse-tracking interactions

### Spring Configuration Approaches

**Apple's approach (recommended — easier to reason about):**
```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

**Traditional physics (more control):**
```js
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

Keep bounce subtle (0.1-0.3). Avoid bounce in most UI contexts. Use it for drag-to-dismiss and playful interactions.

### Interruptibility Advantage

Springs maintain velocity when interrupted — CSS animations and keyframes restart from zero. This makes springs ideal for gestures users might change mid-motion.

### useSpring for Mouse Interactions

Tying visual changes directly to mouse position feels artificial. Use `useSpring` to interpolate with spring-like behavior:

```jsx
import { useSpring, useTransform, useMotionValue } from 'motion/react';

const mouseX = useMotionValue(0);

// Use useTransform to create a MotionValue first
const rotationValue = useTransform(mouseX, (x) => x * 0.1);

// Then pass the MotionValue to useSpring
const springRotation = useSpring(rotationValue, {
  stiffness: 100,
  damping: 10,
});
```

Note: `useSpring` requires a `MotionValue` as its first argument, not a plain expression. Use `useTransform` to convert a calculation into a `MotionValue` before passing to `useSpring`.

This works best for **decorative** interactions — mouse-tracked rotations, parallax effects, etc. For functional UI (a graph in a banking app), no animation is better than decorative animation.

---

## AnimatePresence Deep Reference

### exit prop must mirror initial
For visual symmetry, exit animations should reverse the entry animation direction.

### useIsPresent in the child, not the parent
```jsx
function Modal({ onClose }) {
  const isPresent = useIsPresent();
  // handle cleanup when isPresent becomes false
}
```

### safeToRemove after async cleanup
Call `safeToRemove()` after any async operations in exit animations (API calls, timers) to signal AnimatePresence the element can be removed.

### Disable pointer events on exiting elements
```css
[data-framer-motion-exit] { pointer-events: none; }
```

### mode="wait" DOUBLES total transition duration
When using `mode="wait"`, halve the individual in/out timings to maintain the same perceived speed.

### mode="sync" causes layout conflicts
Use `mode="popLayout"` instead for list reordering — sync mode computes layout simultaneously and causes visual conflicts.

### Nested AnimatePresence needs propagate prop
```jsx
<AnimatePresence>
  <AnimatePresence propagate>
    {/* child */}
  </AnimatePresence>
</AnimatePresence>
```

### Coordinate parent-child exit durations
Parent exit animations should complete last — children exit first, then the parent container.
