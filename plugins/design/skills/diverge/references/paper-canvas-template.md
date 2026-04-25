# Diverge Paper Canvas Template

Paper canvas output for the divergence prototype. One artboard per concept, laid out horizontally so the user can pan across them as a gallery.

Paper is the design app (like Figma); the Paper MCP plugin exposes tools to create artboards, write HTML into them, and capture screenshots. The full Paper MCP guide is loaded at session start — read it once if you haven't.

## When to use this output

Choose Paper canvas when:
- Concepts hinge on visual metaphor, layout, or screen narrative
- The user wants a side-by-side gallery to skim without code
- Prototype interactivity isn't load-bearing (the look + the anchor + the metaphor carry the concept)

Choose React prototype (`picker-template.md`) when:
- Concepts hinge on dial-tunable behavior (autonomy levels, frequencies, thresholds)
- The user wants to *feel* the concept by pulling sliders
- The mechanic only makes sense when something animates / responds

## Order of MCP calls

Run these in order. Don't skip the orientation calls — they're cheap and prevent typography mistakes.

1. `get_basic_info` — confirm artboard root and existing canvas state
2. `get_font_family_info` — once per session, before any typographic decisions
3. For each concept (loop):
   - `create_artboard` — sized per the device defaults below, named after the concept (`Concept 01 — Ghost Agent`)
   - `write_html` — header strip, then the main scene, then the anchor card, then the meta strip (4 calls per artboard, each adds one visual group)
4. `get_screenshot` — one per artboard, for the user's gallery export
5. `finish_working_on_nodes` — at the end, no exceptions

## Artboard dimensions

| Problem context | Dimensions |
|---|---|
| Default (web/desktop product) | 1440 × 900 |
| Mobile-first problem | 390 × 844 (status bar required — see Paper MCP `get_guide({ topic: "mobile-status-bar" })`) |
| Tablet | 768 × 1024 |

Artboards laid out horizontally with **80px gaps** so the user can pan across the gallery without overlap.

## Per-artboard layout

Each artboard contains four sections, top to bottom, written as separate `write_html` calls:

```
┌─────────────────────────────────────────────┐
│ [Header strip]                              │   ← concept name + what this product believes
│                                              │
│  ┌─────────────────────────┐  ┌──────────┐  │
│  │                          │  │          │  │
│  │   [Main scene]           │  │ [Anchor] │  │   ← the first scene to build
│  │                          │  │          │  │      sidebar card with the real-world reference
│  │                          │  │          │  │
│  └─────────────────────────┘  └──────────┘  │
│                                              │
│ [Meta strip — axes · where the idea came]   │
└─────────────────────────────────────────────┘
```

### Header strip (top, ~80px tall)

- Concept number (small, muted): `01`
- Concept name (large, bold): `Ghost Agent`
- What this product believes (one line, italic, muted): `The best interface is one you never see.`

### Main scene (left column, fills remaining space)

The first scene to build, rendered in HTML. This is the actual prototype frame — what the user would see at the moment that proves the concept.

Use realistic mock data, real component shapes, real spacing. Inline styles only. Flex layout. No margins (use padding + gap).

### Anchor card (right sidebar, ~280px wide)

A small card showing the real-world reference the concept borrows from. Contents:

- Section label: `ANCHOR`
- Anchor name: `Snap-to-tier picker`
- Real-world example: `Apple Music EQ · Stripe pricing tiers`
- One-line note on what the concept inherits: `Discrete steps on a continuous track make the tradeoff visible.`

This card is what makes the Paper output uniquely useful — it makes the borrowed-from-real DNA visible at a glance.

### Meta strip (bottom, ~60px tall)

A horizontal row of pills:

- Axes the concept diverges on: `agency:agent-driven` · `surface:off-screen` · `density:minimal`
- Where the idea came from: `Random domain connection: kindergarten teaching`

Pill style: small, rounded, muted background. Same visual language as the React picker's meta tags.

## HTML conventions (Paper-specific)

Paper's `write_html` parses HTML into design nodes. Follow these rules:

- Inline styles only (`style="..."`)
- All Google Fonts work (`font-family: "Inter", sans-serif`)
- Use `display: flex`, padding, and gap. **Never use margin.** Never use `display: grid` or HTML tables.
- Use `border-box` sizing implicitly (it's the default in Paper).
- Use `<pre>` for code blocks or content where whitespace matters.
- Don't use emojis as icons. Use SVG inline or skip the icon.
- For each top-level visual group, use a `layer-name` attribute so the layer tree is readable: `<div layer-name="Header strip" style="...">`

## Gallery layout

After all artboards are created, position them horizontally in a single row with 80px gaps. Paper places artboards at the next free spot by default — for a clean gallery, write them in concept order and rely on the default placement, then visually verify with `get_screenshot` against the canvas root.

## Gallery export

After the loop:
1. `get_screenshot` per artboard — gives the user one image per concept for sharing/Slack
2. `finish_working_on_nodes` to release the working indicators

Don't include node IDs in any user-facing message — show the screenshots and concept names, that's it.

## Output file naming

The Paper canvas lives inside the user's current Paper file. Don't create new files. After the run, tell the user:

> "Generated `{N}` concept artboards in your Paper canvas as a horizontal gallery. Screenshots captured per concept. Pan across the canvas in Paper to compare."
