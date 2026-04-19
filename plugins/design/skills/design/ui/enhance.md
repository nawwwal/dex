# Enhance — Visual Enhancement Pass

Directional enhancement: polish, bolder, quieter, colorize, or add delight. Detect which sub-mode from user's intent.

## Sub-mode detection

| User says | Sub-mode |
|-----------|----------|
| "polish", "pre-ship", "final pass", "tighten", "make it feel better", "visual polish", "feels off" | **Polish** |
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
- [ ] Nested rounded surfaces use concentric radius math
- [ ] Icons are optically aligned, not just mathematically centered
- [ ] Buttons, cards, and containers use shadows for depth rather than borders where appropriate
- [ ] Images use subtle neutral outlines, not tinted ones
- [ ] Interactive targets meet the hit-area floor from `ui/a11y.md`

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

## CSS Craft Reference

For CSS craft rules (concentric radius, optical alignment, shadows, borders, image outlines, hit areas, button anatomy) → read `$CLAUDE_SKILL_DIR/ui/references/css-craft.md`
