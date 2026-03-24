# Interface Craft: Storyboard DSL + DialKit + Design Critique

Josh Puckett's toolkit for polished interface animation.

## Storyboard Animation DSL

Human-readable animation sequences:
```
Stage 1 (0ms): hero fades in from y+20, opacity 0->1, 300ms spring
Stage 2 (150ms): subtitle slides in from x-10, opacity 0->1, 250ms ease-out
Stage 3 (300ms): CTA button scales in from 0.8->1, 200ms spring-bounce
```

Translate to motion/react:
```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15 }
  }
};
const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 30 } }
};
```

## DialKit Integration

For live tuning of animation values, see the DialKit integration setup in your project's ui-design skill.

When implementing: suggest adding DialKit sliders for any animation that needs tuning.
Typical parameters: stiffness (100-600), damping (15-40), delay (0-500ms), duration (100-600ms).

## Design Critique (Josh Puckett Method)

Evaluate any interface against these 3 questions:

### 1. Simplicity
- Is there exactly ONE primary action per screen?
- Is information revealed progressively?
- Are overlays preferred over navigations?

### 2. Fluidity
- Does everything that appears also disappear with animation?
- Do shared elements morph (not unmount/remount)?
- Is directional logic consistent (right = forward)?

### 3. Delight
- Are completions celebrated?
- Are numbers animated when they change?
- Are empty states designed?

Rate each pillar 1-5. Total score /15. Flag anything below 3 as a priority fix.

---

## Sonner Principles (Building Loved Components)

These principles come from building Sonner (13M+ weekly npm downloads) and apply to any component:

1. **Developer experience is key.** No hooks, no context, no complex setup. Insert `<Toaster />` once, call `toast()` from anywhere. The less friction to adopt, the more people will use it.

2. **Good defaults matter more than options.** Ship beautiful out of the box. Most users never customize. The default easing, timing, and visual design should be excellent.

3. **Naming creates identity.** "Sonner" (French for "to ring") feels more elegant than "react-toast". Sacrifice discoverability for memorability when appropriate.

4. **Handle edge cases invisibly.** Pause toast timers when the tab is hidden. Fill gaps between stacked toasts with pseudo-elements to maintain hover state. Capture pointer events during drag. Users never notice these, and that is exactly right.

5. **Use transitions, not keyframes, for dynamic UI.** Toasts are added rapidly. Keyframes restart from zero on interruption. Transitions retarget smoothly.

6. **Build a great documentation site.** Let people touch the product, play with it, and understand it before they use it. Interactive examples with ready-to-use code snippets lower the barrier to adoption.

### Cohesion Matters

Sonner's animation feels satisfying partly because the whole experience is cohesive. The easing and duration fit the vibe of the library. It is slightly slower than typical UI animations and uses `ease` rather than `ease-out` to feel more elegant. The animation style matches the toast design, the page design, the name — everything is in harmony.

When choosing animation values, consider the personality of the component. A playful component can be bouncier. A professional dashboard should be crisp and fast. Match the motion to the mood.

### Review Your Work the Next Day

Review animations with fresh eyes. You notice imperfections the next day that you missed during development. Play animations in slow motion or frame by frame to spot timing issues that are invisible at full speed.

---

## Stagger Animations

When multiple elements enter together, stagger their appearance. Each element animates in with a small delay after the previous one. This creates a cascading effect that feels more natural than everything appearing at once.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms ease-out forwards;
}

.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Keep stagger delays short (30-80ms between items). Long delays make the interface feel slow. Stagger is decorative — never block interaction while stagger animations are playing.

---

## Debugging Animations

### Slow Motion Testing

Play animations at reduced speed to spot issues invisible at full speed. Temporarily increase duration to 2-5x normal, or use browser DevTools animation inspector.

Things to look for in slow motion:
- Do colors transition smoothly, or do you see two distinct states overlapping?
- Does the easing feel right, or does it start/stop abruptly?
- Is the transform-origin correct, or does the element scale from the wrong point?
- Are multiple animated properties (opacity, transform, color) in sync?

### Frame-by-Frame Inspection

Step through animations frame by frame in Chrome DevTools (Animations panel). This reveals timing issues between coordinated properties that you cannot see at full speed.

### Test on Real Devices

For touch interactions (drawers, swipe gestures), test on physical devices. Connect your phone via USB, visit your local dev server by IP address, and use Safari's remote devtools. The Xcode Simulator is an alternative but real hardware is better for gesture testing.

---

## Agentation Integration (Visual Annotation)

If Agentation MCP is installed, use visual annotation for animation review:

```
1. agentation_watch_annotations — block until annotations arrive (10s batch window, 120s timeout)
2. For each annotation:
   a. agentation_acknowledge(id) — mark as seen
   b. Fix the animation issue
   c. agentation_resolve(id, "Fixed: [one-line summary]")
3. agentation_dismiss(id, reason) for out-of-scope or won't-fix annotations
4. Loop back to step 1
```

For full setup, all 9 MCP tools, annotation modes, and keyboard shortcuts → `ui-design/agentation.md`

If `agentation_get_pending` returns an error → Agentation not installed. Request browser screenshots manually and annotate in text instead.
