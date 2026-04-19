# Animation Principles (Emil Kowalski)

## Core Philosophy

### Taste Is Trained, Not Innate

Good taste is not personal preference. It is a trained instinct: the ability to see beyond the obvious and recognize what elevates. Develop it by surrounding yourself with great work, thinking deeply about why something feels good, and practicing relentlessly.

When building UI, don't just make it work. Study why the best interfaces feel the way they do. Reverse engineer animations. Inspect interactions. Be curious.

### Unseen Details Compound

Most details users never consciously notice. That is the point. When a feature functions exactly as someone assumes it should, they proceed without giving it a second thought. That is the goal.

> "All those unseen details combine to produce something that's just stunning, like a thousand barely audible voices all singing in tune." — Paul Graham

Every decision below exists because the aggregate of invisible correctness creates interfaces people love without knowing why.

### Beauty Is Leverage

People select tools based on the overall experience, not just functionality. Good defaults and good animations are real differentiators. Beauty is underutilized in software. Use it as leverage to stand out.

---

## The 3 Pillars

### 1. Simplicity — Gradual Revelation
- One clear primary action per screen
- Progressive disclosure — reveal complexity only when needed
- Context preservation during transitions

### 2. Fluidity — Frequency-Based Animation

**Ask first: How often will users see this?**

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette) | No animation. Ever. |
| Tens of times/day (hover effects, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare/first-time (onboarding, celebrations) | Can add delight |

**Never animate keyboard-initiated actions.** These are repeated hundreds of times daily. Animation makes them feel slow and disconnected. Raycast has no open/close animation — that is the optimal experience for something used hundreds of times a day.

- Shared elements morph between states
- Directional logic: right = forward, left = back, bottom sheet = up from bottom
- Default easing: `cubic-bezier(0.23, 1, 0.32, 1)` for entrances
- Similar elements must use identical timing functions and durations
- One focal point should animate prominently at a time — stagger is sequential, not simultaneous, so only one element is in its prominent entrance at each moment (stagger satisfies this rule)
- Modal backgrounds should dim (opacity 0→0.5) as part of the open transition

### 3. Delight — Selective Emphasis
- Frequent features: subtle micro-interactions (< 150ms)
- Infrequent: memorable moments (celebrations, confetti, success states)
- Numbers animate when they change
- Empty states are designed, not afterthoughts

---

## Core Rules
- NEVER animate `width`, `height`, `top`, `left`, `margin`, `padding` — prefer `transform` and `opacity`; use subtle `filter` effects only when they materially improve the transition
- NEVER exceed 300ms for interaction feedback
- ALWAYS check `prefers-reduced-motion`
- NEVER add `will-change` outside an active animation
- MUST pause looping animations when off-screen
- PREFER custom easing curves for entering/exiting elements — built-in `ease` is acceptable for hover/color transitions; `ease-out` is the minimum for element entrances
- NEVER animate context menu entrances (right-click-initiated, high-frequency equivalent to keyboard actions)

## Anti-Patterns That Kill Animation
1. Linear easing — nothing in the physical world moves linearly
2. Symmetric in/out — entrances should be springy, exits should be crisp
3. Animating layout properties — always use `transform` instead
4. Blocking interactions during animation
5. `setTimeout` for animation — use CSS transitions or animation event listeners

---

## Animation Decision Framework

### Should This Animate?

Use the frequency table above. If it's 100+/day: no animation.

### What Is the Purpose?

Every animation must have a clear answer to "why does this animate?"

Valid purposes:
- **Spatial consistency**: toast enters and exits from the same direction
- **State indication**: a morphing feedback button shows the state change
- **Explanation**: a marketing animation showing how a feature works
- **Feedback**: a button scales down on press, confirming the interface heard the user
- **Preventing jarring changes**: elements appearing without transition feel broken

If the purpose is just "it looks cool" and the user will see it often, don't animate.

### What Easing?

Is the element entering or exiting?
  Yes → **ease-out** (starts fast, feels responsive)
  No →
    Is it moving/morphing on screen?
      Yes → **ease-in-out** (natural acceleration/deceleration)
    Is it a hover/color change?
      Yes → **ease**
    Is it constant motion (marquee, progress bar)?
      Yes → **linear**
    Default → **ease-out**

- View transitions (page-to-page, tab switches): **ease-in-out**

**Never use ease-in for UI animations.** It starts slow, making the interface feel sluggish. A dropdown with `ease-in` at 300ms *feels* slower than `ease-out` at 300ms, because ease-in delays initial movement — the exact moment the user is watching most closely.

### How Fast?

| Element | Duration |
| --- | --- |
| Button press feedback | 100-160ms |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects | 150-250ms |
| Modals, drawers | 200-500ms |
| Small state changes (toggles, chips, badges) | 180-250ms |
| Marketing/explanatory | Can be longer |

**Fix slow feel by shortening duration first** before adjusting the easing curve — duration is the most powerful perception lever.

**Rule: Interaction feedback should stay under 300ms.** Modals and drawers may extend up to 500ms — they are transitions, not feedback. A 180ms dropdown feels more responsive than a 400ms one.

### Perceived Performance

Speed in animation is not just about feeling snappy — it directly affects how users perceive your app's performance:

- A **fast-spinning spinner** makes loading feel faster (same load time, different perception)
- A **180ms select** animation feels more responsive than a **400ms** one
- **Instant tooltips** after the first one is open (skip delay + skip animation) make the whole toolbar feel faster

The perception of speed matters as much as actual speed. Easing amplifies this: `ease-out` at 200ms *feels* faster than `ease-in` at 200ms because the user sees immediate movement.

Note: Decorative mouse-tracking animations (like spring-linked rotations) that add visual interest without serving a function are appropriate only in non-critical UI. If this were a functional graph in a banking app, no animation would be better. Know when decoration helps and when it hinders.

---

## Easing Reference

```css
/* Entrance / exit — spring-like, source: easing.dev */
--ease-spring: cubic-bezier(0.23, 1, 0.32, 1);

/* On-screen movement — balanced */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);

/* Standard — balanced for general use */
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);

/* iOS-like drawer curve */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

**Resources:** Don't create curves from scratch. Use [easing.dev](https://easing.dev/) or [easings.co](https://easings.co/) to find stronger custom variants.

**Note on exit easing:** The wiki rule `easing-exit-ease-in` is explicitly rejected: ease-in for exits means the element lingers at the exact moment the user wants it gone. Use ease-out for both enter and exit.

**Spring stiffness boundary:** The wiki's "balanced" spring config (stiff=500, damp=30) is valid but exceeds Emil's recommended range — use stiff=100-400, damp=10-25 as production defaults. stiff=500 is acceptable for decorative or playful interactions.

**Audio and PRM:** For prefers-reduced-motion applied to audio → motion/audio.md
