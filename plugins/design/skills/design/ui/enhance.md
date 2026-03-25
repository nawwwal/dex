# Enhance — Visual Enhancement Pass

Directional enhancement: polish, bolder, quieter, colorize, or add delight. Detect which sub-mode from user's intent.

## Sub-mode detection

| User says | Sub-mode |
|-----------|----------|
| "polish", "pre-ship", "final pass", "tighten" | **Polish** |
| "bolder", "more impact", "flat", "boring", "timid" | **Bolder** |
| "quieter", "too loud", "too heavy", "overwhelming" | **Quieter** |
| "colorize", "add color", "monochromatic", "flat colors" | **Colorize** |
| "delight", "personality", "joy", "fun", "celebration" | **Delight** |

## Mode Detection (Blade/Generic)

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

---

## Polish (pre-ship pass)

Apply before shipping. Checks states, transitions, edge cases.

- [ ] All interactive states covered: default / hover / focus / active / disabled / loading / error / success
- For animation timing, easing, and GPU rules — load /design motion
- [ ] No autoplaying media, no janky scroll, no layout shift on load
- [ ] Edge cases: empty, 0 items, 1 item, 100+ items, very long text, very short text

Anti-AI-slop: see anti-patterns.md for the full detection list (glassmorphism, cyan/purple gradients, bounce easing, etc.)

---

## Bolder (amplify hierarchy)

Make the design more distinctive and impactful.

- Scale jumps 3–5x between levels (h1 should be dramatically larger than body)
- Weight contrast: heavy headings (700–900) with light body (300–400)
- One dominant accent color at ~60% of visual weight
- Asymmetric layouts: break grid deliberately, not accidentally
- Generous whitespace 100–200px between major sections
- Blade mode: use `size="xlarge"` or `size="xxlarge"` on Heading components

**Hard anti-pattern**: "bold" ≠ "more effects". See anti-patterns.md for what counts as AI slop.

---

## Quieter (reduce intensity)

Make the design more refined and sophisticated.

- Desaturate accent colors by 20–30%
- Reduce number of color variants in use → 1–2 max
- Softer typography: reduce weight from 700 → 500 for subheadings
- More whitespace, less visual noise
- Remove decorative shadows and borders (use whitespace as separator instead)
- Blade mode: use `color="surface.text.gray.subtle"` for secondary text

**Note**: Quieter ≠ boring. Think luxury, not laziness.

---

## Colorize (strategic color introduction)

Apply color with intent using the 60/30/10 rule:
- 60%: dominant neutral (background, cards)
- 30%: secondary (sidebar, section separators)
- 10%: accent (CTAs, icons, interactive states)

Use OKLCH for perceptually uniform scales. Never pure grays — always tint with hue.

- Blade mode: use Blade semantic color tokens (`surface.action.background.primary.intense`, `feedback.positive.background`)
- Generic mode: define semantic color variables (`--color-brand`, `--color-success`, `--color-surface`)
- Never use color as the ONLY meaning indicator (add icon or label too)

See anti-patterns.md for full detection list (rainbow vomit, AI-default purple-blue gradient, etc.)

---

## Delight (personality and joy)

Add moments that make the product feel alive.

- For micro-interaction animation patterns — load /design motion (components)
- Empty states: illustrated, animated, or with a clever/branded message
- Success celebrations: confetti, checkmark animation, or brand-matched copy ("Payment sent! 🚀" not "Success.")
- Brand-matched copy: error messages and empty states should sound like the brand voice, not generic AI output
  - ❌ "Oops! Something went wrong." → ✅ "We couldn't load this. Refresh or contact support."
- For prefers-reduced-motion implementation — load /design motion (performance)
- Blade mode: use Blade motion tokens for timing; use `<Spinner>` and `<Toast>` for standard feedback

**Anti-pattern**: "herding pixels" or "teaching robots to dance" — if copy sounds like it was written by a chatbot, rewrite it.

---

## Output

```
## Enhance ({sub-mode}): {TARGET}

### Applied
- [file:line] — [what changed]

### Could not apply
- [finding] — needs design direction / needs brand voice input
```

---

## Visual Design — CSS Craft

### Concentric Border Radius
Nested elements: outer-radius = inner-radius + padding. Example: if inner element has 8px border-radius and sits inside a container with 16px padding, the container should have 24px border-radius.

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

### Button Shadow Anatomy (6 layers)
A polished button typically has:
1. Outer cut shadow (creates depth separation)
2. Inner ambient highlight (diffuse inner glow)
3. Inner top highlight (specular, 1px from top)
4. Depth shadow 1 (close, crisp)
5. Depth shadow 2 (medium spread)
6. Depth shadow 3 (atmospheric, blurred)
