# Typeset — Typography Fixes

Fix font choices, hierarchy, sizing, and readability.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Rules (all modes)

### Scale
- Body text minimum `16px` / `1rem` — never use px for font sizes
- Headings: `line-height: 1.1–1.2`
- Body: `line-height: 1.5–1.7`
- Max 2–3 font families
- Max line length: `max-width: 65ch` on text containers

### Scale strategy
- **App UI** (dashboard, forms, tables): fixed `rem`-based scale: `0.75rem, 0.875rem, 1rem, 1.125rem, 1.25rem, 1.5rem, 2rem`
- **Marketing / content pages**: fluid scale with `clamp()`: `clamp(1rem, 2.5vw, 1.5rem)`

### Anti-patterns
- Inter overuse — if Inter is the only font, flag and suggest pairing
- Mixing px and rem in the same component
- `font-size: 0` traps (breaks browser zoom)
- All-caps headers with no `letter-spacing`

## Blade mode actions

Replace raw sizing with Blade Typography component:
```tsx
// Before: <p style={{ fontSize: '16px' }}>Text</p>
// After: <Text size="medium">Text</Text>

// Use Blade's type scale tokens for non-Text elements
// import { theme } from '@razorpay/blade/components';
```

Check `get_blade_component_docs("Text,Heading,Display,Code")` for the correct Blade component per use case.

## Generic mode actions

Replace hardcoded px values with rem-based CSS custom properties matching the scale in "Scale strategy" above:
`--text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem; --text-xl: 1.25rem; --text-2xl: 1.5rem; --text-3xl: 2rem`

## Output

```
## Typeset: {TARGET}

### Critical (must fix)
- [file:line] — hardcoded px font size — Replace with rem/Blade token
- [file:line] — no max-width on paragraph — Add max-width: 65ch

### Warnings
- [finding]

### Applied fixes
- [what was changed]
```

## Advanced OpenType + Variable Font Features

### Numeric Variants
- `font-variant-numeric: tabular-nums` — for data tables, pricing, dashboards (all numbers same width)
- `font-variant-numeric: oldstyle-nums` — for body prose (numbers blend with lowercase text)
- `font-variant-numeric: slashed-zero` — for code UIs (distinguishes 0 from O)
- `font-variant-numeric: diagonal-fractions` — for pricing, recipe fractions (½ renders as proper fraction)

### OpenType Features
- Keep `font-feature-settings: "calt" 1` (contextual alternates) — never disable
- Enable `"ss02"` for code UIs where I/l/1 and 0/O disambiguation matters
- Leave `font-optical-sizing: auto` — never override (browser optimizes for size automatically)

### Rendering
- `-webkit-font-smoothing: antialiased` on retina displays for crisp rendering
- `font-synthesis: none` for display/icon fonts — prevents browser from synthesizing fake bold/italic
- `font-display: swap` for web fonts — text visible during font load

### Line Wrapping
- `text-wrap: balance` on headings — eliminates uneven line breaks in multi-line headings
- `text-wrap: pretty` on body text — eliminates orphaned single words on the last line
- `text-align: justify` requires `hyphens: auto` — without hyphens, creates river spacing

### Variable Fonts
- Use continuous weight values (450, 550) instead of jumps — natural optical weight transitions
- Avoid jumping between 400→700 when variable font supports intermediates

### Other
- `text-underline-offset: 3px` with `text-decoration-skip-ink: auto` — clean underlines
- `letter-spacing: 0.05em` for uppercase text and small-caps — optical compensation
