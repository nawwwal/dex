# Reveal.js Configuration

## Setup Choice

### Basic Browser Setup

Use for quick standalone decks where the user can unzip/copy Reveal.js files or load from CDN.

Mechanic: one `index.html` with CSS, theme CSS, `dist/reveal.js`, and `Reveal.initialize()`.

Tradeoff: fastest artifact; weaker dependency management and harder to reuse.

### Full npm Setup

Use for real decks with assets, plugins, exports, or repeat edits.

Mechanic:

```bash
npm install reveal.js
```

Import styles and plugins from `node_modules` or serve/copy the `dist` files. Use a local dev server for ES modules and external Markdown.

Tradeoff: more setup; cleaner asset and plugin management.

### React Setup

Use `@revealjs/react` only when the deck is part of an existing React surface or needs React components.

Tradeoff: component reuse; heavier runtime and different deck authoring model.

## Named Profiles

### Standalone Talk

Use for live presentation.

```js
Reveal.initialize({
  hash: true,
  controls: true,
  progress: true,
  slideNumber: "c/t",
  center: false,
  transition: "slide",
  backgroundTransition: "fade",
  plugins: [RevealMarkdown, RevealHighlight, RevealNotes]
});
```

Reasoning: hashes support direct slide links; controls/progress help live navigation; notes support speaker view.

Speaker-view invocation when notes are present:

```text
1. Serve the deck, for example: npx http-server . -p 8000
2. Open http://localhost:8000/
3. Press S in the presentation window to open presenter view.
```

Programmatic equivalent for custom controls:

```js
Reveal.getPlugin("notes").open();
```

### Embedded Module

Use inside a product page, docs page, iframe, or component preview.

```js
Reveal.initialize({
  embedded: true,
  keyboardCondition: "focused",
  hash: false,
  history: false,
  controls: true,
  progress: false,
  touch: true,
  center: false,
  transition: "fade"
});
```

Reasoning: the deck should not own the whole URL, keyboard, or page scroll.

### Kiosk Or Demo Loop

Use for unattended displays and looping product demos.

```js
Reveal.initialize({
  controls: false,
  progress: false,
  loop: true,
  autoSlide: 8000,
  autoSlideStoppable: false,
  pause: false,
  transition: "fade",
  autoPlayMedia: true
});
```

Reasoning: timed navigation and resilient media matter more than presenter control.

### Documentation Article

Use when the deck should read like an article.

```js
Reveal.initialize({
  view: "scroll",
  scrollLayout: "full",
  controls: false,
  progress: true,
  hash: true,
  center: false,
  transition: "none"
});
```

Reasoning: scroll view reduces presentation mechanics and improves long-form reading.

### Generated Report

Use when content is data-driven and may be exported.

```js
Reveal.initialize({
  hash: true,
  controls: true,
  progress: true,
  slideNumber: "c/t",
  fragments: true,
  center: false,
  transition: "none",
  pdfSeparateFragments: false,
  plugins: [RevealHighlight, RevealNotes]
});
```

Reasoning: stable hashes and low motion make generated decks easier to review and print.

## Core Options To Decide

- `width`, `height`: design canvas. Use 16:9 defaults unless embedding in a fixed panel.
- `margin`: safe area around slides; increase for projector uncertainty.
- `minScale`, `maxScale`: prevent tiny or oversized scaling.
- `controls`: visible arrows; useful for shared decks, optional for talks.
- `progress`: deck progress bar; hide for kiosk or embedded modules.
- `slideNumber`: use `"c/t"` for review/export decks.
- `hash`: enables URL routes per slide; avoid when embedded in pages that own the hash.
- `history`: browser history per slide; useful for hosted decks, noisy in embedded contexts.
- `center`: set `false` for designed layouts with explicit vertical rhythm.
- `touch`: disable only when swipe conflicts with interactive content.
- `fragments`: keep enabled unless exporting a static report.
- `transition`: `none`, `fade`, `slide`, `convex`, `concave`, or `zoom`.
- `transitionSpeed`: `fast`, `default`, or `slow`.
- `backgroundTransition`: usually `fade`; avoid dramatic background movement.
- `autoSlide`: milliseconds between slides; use only for kiosk/timed decks.
- `autoPlayMedia`: true/false/null. Prefer per-element `data-autoplay` unless kiosk.
- `view`: `null`, `scroll`, or `print`.
- `plugins`: include only used plugins.

## Plugins

Common plugin set:

```js
plugins: [RevealMarkdown, RevealHighlight, RevealNotes]
```

Add:

- `RevealMath.KaTeX` or MathJax variant for formulas.
- Search/Zoom only when the deck genuinely needs them.
- Multiplex only when audience devices must follow the presenter.

## Print And PDF

Use Chrome or Chromium for PDF export. Open:

```text
http://localhost:8000/?print-pdf
```

Decide:

- `showNotes: true` overlays notes.
- `showNotes: "separate-page"` prints notes after slides.
- `pdfSeparateFragments: true` creates one page per fragment state.
- `pdfPageHeightOffset` can compensate for browser print rounding issues.

Mechanical export:

```text
1. Start a local server from the deck folder: npx http-server . -p 8000
2. Open http://localhost:8000/?print-pdf in Chrome or Chromium.
3. Press Cmd+P.
4. Destination: Save as PDF.
5. Layout: Landscape.
6. Margins: None.
7. Enable Background graphics.
8. Save.
```

## Runtime Safety

- Avoid remote assets unless the deck will always have internet.
- Use relative local assets for offline decks.
- Use `data-src` for lazy-loaded iframes and media.
- Use `data-prevent-swipe` on scrollable embedded content.
- Use `Reveal.sync()` after dynamically adding/removing slides.
- Use `Reveal.layout()` after changing dimensions or major CSS that affects slide size.
