---
name: html-presentation
description: Create, edit, or review browser-native HTML presentation decks with Reveal.js. Use when Codex needs to build a working Reveal.js deck, convert narrative content into an HTML slide experience, generate slides synthetically from JavaScript data, tune deck theme/motion/configuration, add speaker notes/fragments/media/code/math/export behavior, or prepare a presentation that runs in a browser instead of PowerPoint, Google Slides, or Figma.
---

# HTML Presentation

Build the actual browser deck, not a slide outline. Use Reveal.js when the user wants a presentation that can run locally, ship as static HTML, embed in a site, include custom interaction, or be generated from structured JavaScript content.

## Source Rules

Use current Reveal.js docs before relying on memory for API details:

1. If the user asks about Reveal.js syntax, configuration, plugins, or a version-specific behavior, fetch current docs with Context7 first.
2. For site coverage and feature selection, read `references/revealjs-site-map.md`.
3. For implementation details, load only the reference file needed for the task:
   - `references/deck-workflow.md` for turning a brief into a deck.
   - `references/configuration.md` for setup profiles and config options.
   - `references/theme-and-motion.md` for theme, layout, and motion decisions.
   - `references/style-reference-library.md` for deck art-direction patterns drawn from the provided Figma references and screenshots.
   - `references/razorpay-brand.md` for Razorpay brand tokens, typography, imagery, iconography, and usage rules from the branding PDF.
   - `references/css-theme-recipes.md` for copyable CSS systems and layout classes.
   - `references/synthetic-decks.md` for JavaScript-generated slide decks.
4. When changing theme colors, run `scripts/contrast-check.js` against the foreground/background pairs before handoff.

## Default Workflow

1. Clarify the presentation job in one pass: audience, decision, runtime target, source content, delivery format, and deadline. Ask only if one of these changes the artifact.
2. Choose a deck mode:
   - **Static HTML** for handcrafted slides.
   - **Markdown-backed** for fast narrative decks with simple layouts.
   - **Synthetic JavaScript** for decks generated from structured data, repeated sections, or site-specific templates.
   - **React Reveal** only when the surrounding app is already React or the user asks for component-based slides.
3. Create or adapt a Reveal.js project:
   - Use local npm install when the deck needs plugins, assets, exports, or repeat work.
   - Use CDN/basic setup only for a quick standalone file.
   - Start from `assets/reveal-synthetic-template/` when generating a deck from JavaScript data.
4. Write slide content as a real talk:
   - one idea per slide
   - speaker notes for claims, transitions, and demo instructions
   - fragments only where sequence improves comprehension
   - appendix/uncounted slides for optional depth
5. Choose a visual system before polishing individual slides. Use `references/style-reference-library.md`; do not default to generic cards, soft gradients, or corporate slide templates.
6. Apply brand tokens and CSS recipes. Use `references/razorpay-brand.md` for Razorpay-branded decks and `references/css-theme-recipes.md` for reusable classes.
7. Verify in a browser. Check first slide, last slide, vertical stacks, fragments, keyboard/touch navigation, notes, PDF print mode, and broken assets.

## Deck Quality Bar

Every finished deck must include:

- `index.html` or equivalent entrypoint that opens without hidden build steps.
- A clear Reveal.js initialization block with documented config choices.
- A theme file or theme overrides that define typography, color, spacing, shape language, texture, code, media, and print behavior.
- A named visual system from the style reference library, with the assumption and tradeoff stated.
- Full-viewport backgrounds. Use Reveal.js background attributes or generated equivalents; do not render the deck as a centered slide container inside browser whitespace.
- Verified readable color pairs for body text, muted text, labels, panels, and code.
- Speaker notes for any slide where the visible content is not enough to present.
- Runtime instructions in the final response: local server command, preview URL/path, speaker-view invocation when notes exist, and PDF export route if relevant.

Avoid producing a deck that is only a Markdown outline inside HTML. Reveal.js is valuable because it can choreograph order, scale, media, code, interaction, and export behavior.

## Site-Specific Config

When the deck will live inside a product site, docs site, microsite, or iframe, choose a named profile from `references/configuration.md`:

- **Standalone talk**: full viewport, hash navigation, speaker notes, PDF support.
- **Embedded module**: contained deck, no global keyboard theft, no hash/history ownership.
- **Kiosk/demo loop**: auto-slide, loop, reduced controls, resilient media.
- **Documentation article**: scroll view, anchored sections, lower motion.
- **Generated report**: synthetic JS content, predictable slide IDs, PDF-safe fragments.

State the selected profile and tradeoff before implementing.

## Synthetic Deck Rule

Use JavaScript generation when the deck has repeated structure, data-driven slides, multiple site variants, localization, or needs to be regenerated. Use `references/synthetic-decks.md` and `assets/reveal-synthetic-template/`.

The generator should:

- accept a structured `deckSpec`
- include a mechanical adapter when the source data is not already shaped as slides
- validate required fields before rendering
- create semantic `<section>` elements
- assign stable slide IDs
- add speaker notes as `<aside class="notes">`
- add fragments, backgrounds, code blocks, media, and appendix slides through typed helpers
- call `Reveal.sync()` after dynamic changes if slides are inserted after initialization

## Handoff From `$present`

`$present` owns narrative coaching: problem frame, audience, objections, and meeting flow. This skill owns the deliverable deck. If the user asks to create, build, generate, polish, or export an HTML/browser presentation, use this skill after the narrative is clear.
