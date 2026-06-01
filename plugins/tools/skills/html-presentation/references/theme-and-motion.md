# Theme And Motion

Use this as the operating guide for visual direction. For detailed source patterns, read `style-reference-library.md`. For Razorpay tokens, read `razorpay-brand.md`. For copyable CSS, read `css-theme-recipes.md`.

## Core Stance

Do not make a generic Reveal.js deck with cards, soft gradients, and centered bullets. Build a visual system with a surface, object language, type behavior, motion behavior, and content rules.

The default is one deck-wide design system. Do not change fonts, palettes, or object language slide-by-slide to demonstrate variety. Variation belongs in layout and emphasis, not in the foundations.

Term -> meaning -> execution -> avoid

- **Surface** -> the slide's world -> black stage, pale mat, blue blueprint field, atmospheric image field, or product split -> default white page with floating cards.
- **Object language** -> the repeatable things content appears inside -> chips, rails, exhibit panels, footer rules, mono labels, diagram paths, screenshots, symbol tiles -> arbitrary rectangles per slide.
- **Type behavior** -> how hierarchy is created through type -> one large claim, one small eyebrow, body kept compact, mono only for annotations -> multiple similar heading sizes.
- **Motion behavior** -> how the deck reveals meaning -> fragments for dependency order, auto-animate for state change, static title slides -> animation used as decoration.

## Visual System Selection

Choose one primary system before writing CSS:

| System | Use when | Main mechanics | Tradeoff |
|---|---|---|---|
| Black Stage Workshop | internal design session, demo, teaching | black canvas, chunky chips, symbol blocks, mono annotations | less formal; can read as teaching material rather than approval artifact |
| Pale Mat Exhibit | process, systems, diagrams | pale outer page, dark rounded exhibit panel, large caption claim | diagram must be strong enough to carry the slide |
| Graphic Title System | opening and chapter slides | blue technical field, white title plate, serif display title, metadata footer | use sparingly or it overwhelms content slides |
| Event Atmosphere | keynote, conference, launch | huge uppercase headline, pale image field, footer rule | weak for dense explanations |
| Product Split Explainer | product value and walkthroughs | black copy rail, colored artifact rail, screenshot/code evidence | requires real artifact imagery |
| Type And Symbol Bumper | section transitions | centered phrase made from word chips and symbol tiles | not for detailed explanation |
| Domain Cloud | broad category claim | low-opacity orbit labels, one centered claim, one accent word | not a data visualization |

Use a secondary system only for a meaningful section mode change, such as a blueprint opener before a black-stage workshop. Never mix systems inside a single generated sample deck unless the user explicitly asks for a style sampler.

## Theme Mechanics

Define these once:

- design canvas: default 16:9, explicit padding, `center: false`
- full-bleed background: use Reveal.js `data-background-color`, `data-background-gradient`, `data-background-image`, or generated equivalents so the background fills the viewport; do not fake the slide as a centered card
- surface colors: page, stage, panel, text, muted text, line, accent
- type families: display, body, mono
- object radius: chips 10-14px, exhibit panels 10-12px, media frames 8px
- lines: 1px or dotted; use them as structure, not decoration
- media treatment: full artifact rail, exhibit panel, or atmospheric field
- print behavior: reduce padding and remove fragile fixed effects when needed

## Type Rules

- Give each slide one dominant sentence.
- Put the claim in the title, not in body copy.
- Keep body copy to short lines or labeled chunks.
- Use uppercase mono text for labels like `GOOD TO KNOW`, `ALIGNMENT`, `DESIGN FIDELITY`, and small diagram annotations.
- Use display serif only for title plates or special session identity moments.
- Use uppercase geometric sans for event-scale slides.
- Do not scale font size with viewport width.
- Lock one typography stack per deck. A title opener may use a display variant only if the rest of the system still uses the same body and annotation fonts.

## Color Rules

- Use the 60/30/10 split for branded decks: primary brand colors dominate, secondary colors support, tertiary colors punctuate.
- For black-stage decks, use white/pastel chips on black; let colored chips carry navigation or symbols.
- For pale-mat decks, keep the outer page pale and the exhibit panel dark.
- For product split slides, keep one side black and the artifact side one saturated color field.
- Do not use multicolor accents unless each color encodes a category or sequence.
- Check contrast before handoff. Body text must meet at least 4.5:1 contrast against its surface; large display text must meet at least 3:1. If a Reveal theme stylesheet overrides colors, force `color: inherit` on headings, paragraphs, list items, and captions.

## Layout Rules

- Use a grid, but let objects sit with slight offsets when the reference calls for workshop energy.
- Make the slide full-bleed. Avoid outer max-width wrappers that make the deck look like a web card inside the browser.
- Keep screenshots large enough to inspect. Crop to the UI region that proves the claim.
- Place labels near the object they explain. Use dotted leaders only when the label must sit away from the object.
- Put appendix material in uncounted slides. Do not compress backup evidence into main narrative slides.
- Use repeated classes for generated slides: `.slide-title`, `.slide-claim`, `.slide-split`, `.slide-visual`, `.slide-code`, `.slide-comparison`, `.slide-metric`, `.slide-process`, `.slide-appendix`.

## Motion Rules

### Transitions

- `slide`: live talks where sequence matters.
- `fade`: hosted or embedded decks where transitions should recede.
- `none`: reports, docs, PDF-first decks.
- per-slide transition: only for a section or mode change.

### Fragments

Use fragments for order:

- agenda item sequence
- diagram dependency sequence
- reveal annotation after the viewer has seen the artifact
- compare old state -> failure -> new mechanism

Avoid fragmenting every bullet. If the audience needs to inspect all evidence at once, show it at once.

### Auto-Animate

Use `data-auto-animate` only when object identity is stable across slides:

- messy process resolves into clean path
- architecture ownership moves
- product UI progresses across states
- timeline advances

If the viewer cannot tell what stayed the same, auto-animate is not doing its job.

### Media

- Autoplay only when media is the point of the slide.
- Use muted looping video for kiosk/background moments.
- Use `data-src` for heavy iframes and videos.
- Use lightbox for zooming into screenshots or demos.

## Accessibility And Print

- Maintain high contrast.
- Do not encode meaning with color alone.
- Keep text within stable slide bounds.
- Add captions to screenshots and charts.
- Test `?print-pdf`; fixed backgrounds, fragments, and huge images can print differently.

## Review Checklist

- Is there a named visual system?
- Does the slide have one dominant claim?
- Are the objects consistent across the deck?
- Are colors carrying structure instead of decoration?
- Are annotations tied to visible objects?
- Does motion reveal meaning?
- Would the slide still work as a PDF page?
