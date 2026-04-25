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
   - `write_html` — header strip, then the main scene, then the anchor card, then the delight card, then the meta strip (5 calls per artboard, each adds one visual group)
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

Each artboard contains five sections, written as separate `write_html` calls:

```
┌─────────────────────────────────────────────┐
│ [Header strip]                              │   ← concept name + what this product believes
│                                              │
│  ┌─────────────────────────┐  ┌──────────┐  │
│  │                          │  │ [Anchor] │  │   ← the first scene to build (left)
│  │   [Main scene]           │  ├──────────┤  │     anchor card on top right
│  │                          │  │ [Delight]│  │     delight card on bottom right
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

Keep the header clean. Do NOT put the Structural thesis or Modality on the header strip — they go in the meta strip at the bottom. Visual artifacts read better when the header is short.

### Main scene (left column, fills remaining space)

The first scene to build, rendered in HTML. This is the actual prototype frame — what the user would see at the moment that proves the concept.

Use realistic mock data, real component shapes, real spacing. Inline styles only. Flex layout. No margins (use padding + gap).

### Anchor card (right sidebar top, ~280px wide × ~50% height)

A small card showing the real-world reference the concept's MECHANIC borrows from. Contents:

- Section label: `ANCHOR`
- Anchor name: `Outer Wilds knowledge-as-progression`
- Bucket: `Video games`
- One-line note on what the concept inherits: `The only thing that persists is what the user has now learned.`

### Delight card (right sidebar bottom, ~280px wide × ~50% height)

A small card showing the real-world reference the concept's DELIGHT MOMENT borrows from. Contents:

- Section label: `DELIGHT`
- Delight name: `Quaker meeting silence`
- Bucket: `History / ritual`
- One-line note on the moment the user feels: `The agent only speaks when something genuinely needs attention; the room is otherwise quiet.`

The two cards together make the Paper output uniquely useful — they show the borrowed-from-real DNA for both the mechanic and the emotional peak at a glance, ideally from different domain buckets.

### Meta strip (bottom, ~80px tall)

Two rows of pills + one Structural thesis line.

Top row (pills):
- Modality: `Input: implicit signals → Output: top ribbon → Feedback: dismiss`
- Axes the concept diverges on: `agency:agent-driven` · `surface:off-screen` · `density:minimal`
- Where the idea came from: `Random domain connection: kindergarten teaching`

Bottom line (full width, italic, small):
- Structural thesis: `Treats agents as a Quaker meeting because the Brief said this needs to feel calm not surveilled — silence is the default, only meaningful interruptions speak.`

Pill style: small, rounded, muted background. Same visual language as the React picker's meta tags. The Structural thesis sits below pills as readable prose, not as a pill (too long).

## HTML conventions (Paper-specific)

Paper's `write_html` parses HTML into design nodes. Follow these rules:

- Inline styles only (`style="..."`)
- All Google Fonts work (`font-family: "Inter", sans-serif`)
- Use `display: flex`, padding, and gap. **Never use margin.** Never use `display: grid` or HTML tables.
- Use `border-box` sizing implicitly (it's the default in Paper).
- Use `<pre>` for code blocks or content where whitespace matters.
- Don't use emojis as icons. Use SVG inline or skip the icon.
- For each top-level visual group, use a `layer-name` attribute so the layer tree is readable: `<div layer-name="Header strip" style="...">`

## HTML-escape user-provided strings

Any string sourced from the Brief (References list, Constraints list, Audience line, free-text user replies) must be HTML-escaped before being inserted into a `write_html` call. Use a simple escape: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&#39;`.

Curated strings (Anchor and Delight references pulled from `anchor-library.md`, axes, where-the-idea-came-from labels) are safe and don't need escaping — they are skill-controlled and don't contain hostile input.

## Prototype-output bans (taste guardrails)

Same universal bans as the React picker (see `picker-template.md`):

- No Acme / Nexus / SmartFlow placeholder company names → use Brief product name
- No John Doe / Sarah Chan placeholder users → use realistic names per Brief audience
- No fake round-number metrics → use organic messy data
- No "Elevate / Seamless / Unleash / Next-Gen" copy → concrete verbs
- No three-equal-cards layouts → asymmetric grid or horizontal scroll
- No AI-Purple gradient glows → desaturated singular accent
- No pure black `#000000` → Zinc-950 or Charcoal

Plus Paper-specific:

- **No emojis as icons** — use inline SVG or skip the icon.
- **No fake stock photos** — if a photo is needed, use a placeholder rectangle with a caption describing what should be there. Don't pull random Unsplash URLs into Paper artboards.
- **Font and color** are conditional on the Brief's consistency contract. If the Brief names "Blade design system," use Blade tokens (Wix grey, primary blue). If the Brief names "Inter" as the brand font, use Inter — don't substitute Geist.

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
