# CSS Theme Recipes

Use these recipes when implementing Reveal.js decks. Copy selectively; do not load every class into a small deck.

## Implementation Rules

- Set Reveal dimensions to a real 16:9 canvas such as `width: 1920`, `height: 1080`, and `margin: 0` when the user wants a full-bleed deck.
- Use Reveal background attributes for full-viewport backgrounds. CSS on the slide `section` only colors the scaled slide plane and can create a visible container.
- Force inherited text color after importing Reveal themes: `.reveal h1, .reveal h2, .reveal h3, .reveal p, .reveal li { color: inherit; }`.
- Do not change typography stacks per slide. Change scale, weight, and layout within one stack.
- Test contrast on the rendered slide, not in the CSS file.

## Token Layer

```css
:root {
  --rzp-blue-500: #305eff;
  --rzp-blue-400: #5278ff;
  --rzp-logo-blue: #3395ff;
  --rzp-navy: #0c2651;
  --rzp-green-500: #6ed00b;
  --rzp-green-300: #c1ff84;
  --rzp-forest-500: #00be5f;
  --rzp-sea-500: #389494;
  --rzp-clouds-500: #387594;
  --rzp-coral: #ff8a80;
  --rzp-purple: #826dff;
  --rzp-yellow: #fbec51;
  --rzp-sky-blue: #7dd5e9;
  --surface-000: #ffffff;
  --surface-050: #f8fafc;
  --surface-100: #f1f5fa;
  --surface-sea-050: #edf7f7;
  --surface-clouds-050: #edf4f7;
  --surface-dark: #0c1927;
  --surface-ink: #030303;
  --line-soft: rgba(255, 255, 255, 0.26);
  --line-dark: rgba(12, 25, 39, 0.18);
  --font-display: "Tasa Orbiter Display", "Space Grotesk", Inter, ui-sans-serif, system-ui, sans-serif;
  --font-body: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
}
```

## Black Stage

```css
.theme-black-stage {
  background: var(--surface-ink);
  color: #f7f7f2;
}

.stage-panel {
  background: #111;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  padding: 32px;
}

.chip-row {
  align-items: center;
  display: flex;
  gap: 12px;
  margin: 10px 0;
}

.number-chip,
.symbol-chip,
.word-chip {
  align-items: center;
  display: inline-flex;
  font-weight: 750;
  min-height: 56px;
}

.number-chip {
  background: #4b42ff;
  border-radius: 12px;
  color: #fff;
  font-size: 30px;
  justify-content: center;
  min-width: 92px;
}

.word-chip {
  background: #fff;
  border-radius: 10px;
  color: #030303;
  font-size: 28px;
  padding: 0 22px;
}

.symbol-chip {
  background: #4b42ff;
  border-radius: 12px;
  justify-content: center;
  min-width: 84px;
}
```

## Pale Mat Exhibit

```css
.theme-pale-mat {
  background: var(--surface-sea-050);
  color: #101010;
}

.exhibit-panel {
  background: #050505;
  border-radius: 12px;
  color: #fff;
  min-height: 430px;
  padding: 28px;
}

.exhibit-caption {
  font-family: var(--font-display);
  font-size: 36px;
  line-height: 1.05;
  margin: 24px auto 0;
  max-width: 900px;
  text-align: center;
}

.annotation-label {
  color: rgba(255, 255, 255, 0.86);
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
```

## Blueprint Title

```css
.theme-blueprint {
  background:
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.28), transparent 20%),
    linear-gradient(135deg, #013aff 0%, #305eff 52%, #0e54cc 100%);
  color: #fff;
  overflow: hidden;
}

.theme-blueprint::before {
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.22) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.22) 1px, transparent 1px);
  background-size: 96px 96px;
  content: "";
  inset: -2px;
  opacity: 0.34;
  pointer-events: none;
  position: absolute;
}

.title-plate {
  background: #fff;
  color: #0e54cc;
  margin: 0 auto;
  padding: 42px 80px 34px;
  position: relative;
  text-align: center;
  width: min(900px, 78%);
  z-index: 1;
}

.title-plate h1 {
  font-family: "Instrument Serif", Georgia, serif;
  font-size: 96px;
  font-style: italic;
  letter-spacing: -0.02em;
}
```

## Event Atmosphere

```css
.theme-atmosphere {
  background: #f3f8fc;
  color: var(--rzp-navy);
}

.atmosphere-field {
  inset: 0;
  opacity: 0.72;
  position: absolute;
}

.event-title {
  font-family: "Space Grotesk", var(--font-display);
  font-size: 92px;
  letter-spacing: -0.03em;
  line-height: 0.98;
  max-width: 820px;
  text-transform: uppercase;
}

.footer-rule {
  align-items: center;
  border-top: 1px solid rgba(12, 38, 81, 0.45);
  bottom: 28px;
  display: flex;
  font-size: 13px;
  justify-content: space-between;
  left: 40px;
  position: absolute;
  right: 40px;
}
```

## Product Split

```css
.product-split {
  display: grid !important;
  gap: 0;
  grid-template-columns: minmax(0, 0.46fr) minmax(0, 0.54fr);
  padding: 0 !important;
}

.copy-rail {
  background: #050505;
  color: #fff;
  padding: 84px 56px;
}

.artifact-rail {
  align-items: center;
  background: var(--rzp-purple);
  display: grid;
  padding: 56px;
}

.benefit-list {
  display: grid;
  gap: 22px;
  list-style: none;
  margin: 32px 0 0;
  padding: 0;
}

.benefit-list li::before {
  content: "-> ";
}
```

## Domain Cloud

```css
.domain-cloud {
  background: #050505;
  color: #fff;
  overflow: hidden;
}

.domain-cloud .orbit {
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 999px;
  color: rgba(255, 255, 255, 0.2);
  display: grid;
  font-size: 18px;
  height: 118px;
  place-items: center;
  position: absolute;
  text-align: center;
  width: 118px;
}

.domain-claim {
  font-size: 56px;
  line-height: 1.08;
  margin: 0 auto;
  max-width: 760px;
  position: relative;
  text-align: center;
  z-index: 1;
}
```

## Usage Rule

Pick one primary recipe per deck. Mixing black stage, blueprint, atmosphere, and product split on every slide creates a style sampler, not a presentation system. Mix systems across a deck only when the section change is meaningful and the type/color foundations stay coherent.
