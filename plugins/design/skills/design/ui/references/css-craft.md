# Visual Design — CSS Craft

### Concentric Border Radius
Nested elements: outer-radius = inner-radius + padding. Example: if inner element has 8px border-radius and sits inside a container with 16px padding, the container should have 24px border-radius.

Use strict concentric math when surfaces are visually nested and close together. If spacing grows beyond roughly `24px`, treat the two layers as separate surfaces instead of forcing radius math that no longer reads as related.

### Optical Alignment
When geometric centering looks off, align optically instead.

- Buttons with text + icon: make the icon-side padding about `2px` tighter than the text side
- Play triangles and asymmetric icons usually need a slight nudge
- Fix the SVG itself when possible; use margin or padding compensation only when the asset cannot be changed

### Shadows Over Borders
For buttons, cards, and containers that are using a border only to simulate elevation, prefer layered transparent shadows. Keep real borders for dividers, table cell boundaries, and form control outlines where separation or accessibility matters.

### Shadow System
Layer 3+ box-shadows with decreasing opacity for realistic depth:

```css
.card {
  box-shadow:
    0 1px 2px rgba(17, 24, 39, 0.12),  /* ambient */
    0 4px 8px rgba(17, 24, 39, 0.08),  /* raised */
    0 12px 24px rgba(17, 24, 39, 0.04); /* atmospheric */
}
```

All shadows must point in the same direction — single consistent light source.

Use `rgba(17, 24, 39, ...)` neutral (warm-tinted near-black), never pure `#000000` — pure black looks flat and artificial.

Define a shadow scale system:
```css
--shadow-1: 0 1px 2px rgba(17,24,39,0.04);      /* ambient, subtle */
--shadow-2: 0 4px 8px rgba(17,24,39,0.08);      /* raised, card */
--shadow-3: 0 12px 24px rgba(17,24,39,0.12);    /* floating, modal — highest opacity = most elevated */
```

### Animate Shadows with Pseudo-elements (GPU Path)
Directly transitioning `box-shadow` forces paint on every frame. Instead, animate the opacity of a pseudo-element that has the shadow:

```css
.card {
  position: relative; /* required */
}
.card::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1; /* render behind card content */
  box-shadow: var(--shadow-3);
  opacity: 0;
  transition: opacity 200ms ease-out;
}
.card:hover::after {
  opacity: 1;
}
```

### Semi-transparent Borders
Use `border: 1px solid var(--gray-a4)` — alpha-channel gray adapts to any background color (light, dark, colored). Pure solid borders need different values per theme.

### Image Outlines
Images should get a subtle outline so they sit cleanly against varied surfaces.

- Light mode: `rgba(0, 0, 0, 0.1)`
- Dark mode: `rgba(255, 255, 255, 0.1)`
- Use pure black or pure white only. Do not use tinted neutrals such as slate, zinc, or project ink colors; they read as dirty edges against photographs

Prefer `outline` with an inset offset so the image dimensions do not change:

```css
img {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px;
}
```

### Hit Areas
Micro-polish never overrides accessibility floors.

- Default target size is `44x44px`
- If the visible affordance is smaller, extend the hit area with a pseudo-element
- A constrained fallback of `40x40px` is acceptable only when layout makes `44x44px` impossible
- Never let two interactive hit areas overlap

### Button Shadow Anatomy (6 layers)
A polished button typically has:
1. Outer cut shadow (creates depth separation)
2. Inner ambient highlight (diffuse inner glow)
3. Inner top highlight (specular, 1px from top)
4. Depth shadow 1 (close, crisp)
5. Depth shadow 2 (medium spread)
6. Depth shadow 3 (atmospheric, blurred)
