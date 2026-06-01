# Razorpay Brand Guidance

Use this for Razorpay-branded Reveal.js decks. It condenses the provided `Branding Guidelines.pdf` into executable presentation rules.

## Brand Position

Razorpay is framed as an all-in-one finance platform for disruptors across industries. Presentation design should feel precise through sharp type, technical through structured grids and product proof, financially credible through navy/blue restraint, and human through candid imagery. The visual system should not look like a generic SaaS template.

## Logo Rules

- Use the Razorpay wordmark plus glyph as the primary logo lockup.
- Preserve clear space equal to the logo mark height/width.
- Use the logo mark alone only when the full lockup does not fit.
- Use blue logo on light backgrounds; white logo on dark backgrounds.
- Use all-black or all-white only when color is limited.
- Do not distort, rotate, recolor, add gradients, add effects, mask, texture, or separate the wordmark from the glyph in the lockup.

## Color Tokens

### Logo Colors

| Token | Hex | Use |
|---|---:|---|
| logo-light-blue | `#3395ff` | Razorpay logo on light fields |
| logo-navy | `#0c2651` | Deep brand navy |

### Primary Colors

Use roughly 60 percent of the creative.

| Token | Hex | Use |
|---|---:|---|
| brand-blue-500 | `#305eff` | primary action, title fields, brand ownership |
| brand-blue-400 | `#5278ff` | lighter blue surfaces, gradients, highlight chips |
| brand-green-500 | `#6ed00b` | primary green accent |
| brand-green-300 | `#c1ff84` | pale green surfaces and positive highlights |

### Secondary Colors

Use roughly 30 percent of the creative.

| Token | Hex | Use |
|---|---:|---|
| brand-forest-500 | `#00be5f` | growth/action accents |
| brand-sea-500 | `#389494` | calm technical depth |
| brand-clouds-500 | `#387594` | blue-green support color |

### Tertiary Colors

Use roughly 10 percent of the creative.

| Token | Hex | Use |
|---|---:|---|
| brand-coral | `#ff8a80` | attention and warning accents |
| brand-purple | `#826dff` | emphasis, AI, or workshop contrast |
| brand-yellow | `#fbec51` | sparing attention moments |
| brand-sky-blue | `#7dd5e9` | light technical emphasis |

### Surface Colors

| Token | Hex | Use |
|---|---:|---|
| neutral-000 | `#ffffff` | base surface |
| neutral-050 | `#f8fafc` | page surface |
| neutral-100 | `#f1f5fa` | subtle panel |
| sea-050 | `#edf7f7` | pale green-blue mat |
| sea-100 | `#e2f3f3` | slightly stronger mat |
| clouds-050 | `#edf4f7` | pale blue mat |
| clouds-100 | `#e6eff4` | light blue panel |
| neutral-1300 | `#0c1927` | dark surface |
| neutral-1200 | `#192839` | dark panel |
| neutral-1100 | `#243547` | dark border/secondary surface |
| sea-800 | `#145252` | dark sea surface |
| sea-900 | `#033e3e` | deep sea surface |
| clouds-900 | `#032a3e` | deep blue-green surface |
| neutral-blue-500 | `#bad9f7` | card color |
| neutral-green-500 | `#c9e3e8` | card color |

## Typography

- Use Tasa Orbiter Display for headlines, titles, and prominent text.
- Use Inter for body copy and smaller UI-like text.
- Use semibold/medium weight for labels and navigation; regular weight for longer copy.
- Keep display text large and sparse. Razorpay headline styling loses force when used for paragraphs.

Fallback:

```css
--font-display: "Tasa Orbiter Display", "Space Grotesk", Inter, ui-sans-serif, system-ui, sans-serif;
--font-body: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
```

## Imagery

Use candid human scenes, clean backgrounds, and brand-color environments. Imagery should signal trust, warmth, and reliability through authentic work moments.

Execution:

- real people using phones, laptops, payment flows, or merchant tools
- clean pale blue/white/green backgrounds
- minimal office or retail context
- product UI or financial event visible when relevant
- clear crop with one subject/action

Avoid:

- stock-photo smiles with no task
- dark dramatic photography
- collages with too many subjects
- abstract finance imagery without a human or product anchor

## Iconography

- Use 24x24 icons.
- Keep strokes simple, consistent, and legible.
- Icons can be functional navigation aids or emotive symbols.
- For deck symbols, keep icon geometry compatible with the surrounding chips and fields.

## Presentation Translation

For HTML decks:

- Prefer Razorpay blue as a field or structural accent, not as body text everywhere.
- Use green for outcome or positive system movement.
- Use navy for serious/executive text surfaces.
- Use pale surfaces for explainer slides and dark surfaces for technical/product diagrams.
- Keep logos small and placed in persistent footer/header zones.
- Build human/product proof into the deck; do not rely only on abstract shapes.
