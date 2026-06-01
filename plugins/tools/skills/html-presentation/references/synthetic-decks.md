# Synthetic JavaScript Decks

Use synthetic generation when presentation structure is repeatable or data-driven. Do not generate HTML strings by concatenating untrusted content. Build DOM nodes and set `textContent` for user-supplied text.

## Data Model

Start with a plain JavaScript object:

```js
const deckSpec = {
  title: "Agent Marketplace Readiness",
  subtitle: "Install flow proof points and remaining risk",
  visualSystem: "black-stage-workshop",
  theme: "razorpay-dark",
  configProfile: "standalone-talk",
  sections: [
    {
      id: "frame",
      title: "What the room needs to decide",
      slides: [
        {
          type: "claim",
          id: "decision",
          eyebrow: "Decision",
          title: "Approve Phase 2 only if install recovery is visible",
          body: [
            "The critical path is not discovery; it is whether users can recover when connector setup fails.",
            "The deck should make recovery states inspectable before success states."
          ],
          notes: "Pause here and ask whether reviewers agree this is the gating risk."
        }
      ]
    }
  ]
};
```

If the source is report data, add an adapter instead of hand-copying fields into slides. Example for data shaped as `{ title, subtitle, sections: [{ id, title, metrics, items }] }`:

```js
function adaptReportData(report) {
  const slides = [
    {
      type: "title",
      id: "summary",
      eyebrow: "Generated report",
      title: report.title,
      subtitle: report.subtitle,
      notes: "Frame the report scope before moving into generated sections."
    }
  ];

  for (const section of report.sections || []) {
    if (section.metrics?.length) {
      slides.push(...section.metrics.map((metric) => ({
        type: "metric",
        id: `${section.id}-${slugify(metric.label)}`,
        eyebrow: section.title,
        title: metric.label,
        value: String(metric.value),
        body: metric.delta ? `Change: ${metric.delta}` : "No delta supplied.",
        notes: `Explain why ${metric.label} changed.`
      })));
    }

    if (section.items?.length) {
      slides.push({
        type: "process",
        id: `${section.id}-items`,
        eyebrow: section.title,
        title: `${section.title}: items to inspect`,
        steps: section.items,
        notes: "Walk the items in order and name the owner for each follow-up."
      });
    }
  }

  return {
    title: report.title,
    subtitle: report.subtitle,
    visualSystem: "black-stage-workshop",
    configProfile: "generated-report",
    slides
  };
}
```

Required adapter checks:

- fail if `report.title` is missing
- fail if any section lacks `id` or `title`
- fail if a section has neither `metrics` nor `items`
- generate stable slide IDs from `section.id` plus `slugify(metric.label)` or a fixed suffix
- pass every string through DOM helpers that use `textContent` or `createTextNode`

Required slide fields:

- `type`
- `id`
- `title`

Recommended fields:

- `eyebrow`
- `visualSystem`
- `layout`
- `body`
- `media`
- `code`
- `fragments`
- `notes`
- `background`
- `visibility`

## Visual System Field

Add `visualSystem` at deck level so generated decks do not collapse into generic cards. Use slide-level overrides only for explicit section-mode changes.

Supported values should map to `style-reference-library.md`:

- `black-stage-workshop`
- `pale-mat-exhibit`
- `graphic-title-system`
- `event-atmosphere`
- `product-split-explainer`
- `type-symbol-bumper`
- `domain-cloud`

At render time, convert the value into a class on the slide:

```js
section.classList.add(`theme-${slide.visualSystem || spec.visualSystem}`);
```

If a deck mixes systems, the section change must explain why. Example: blueprint title opener plus black-stage workshop body. Do not use a generated sample deck to cycle through unrelated fonts, colors, and surfaces.

For full-bleed output, map the deck's visual system to Reveal background attributes during rendering:

```js
const visualSystems = {
  "black-stage-workshop": { backgroundColor: "#030303" }
};

section.dataset.backgroundColor = slide.background?.color || visualSystems[visualSystem].backgroundColor;
```

CSS `background` on `section` alone is not enough because Reveal scales the slide plane inside the viewport.

## Slide Types

Support a small fixed set first:

- `title`: opening or section divider.
- `claim`: title plus body evidence.
- `split`: text plus image/code/video.
- `visual`: large media with caption.
- `code`: code block with line highlights.
- `comparison`: two or three columns.
- `metric`: large number with definition and context.
- `process`: steps/timeline/flow.
- `appendix`: dense support, often `data-visibility="uncounted"`.

## Renderer Shape

The renderer should have three layers:

1. **Validation**: fail early on missing title, IDs, duplicate IDs, unknown slide types, and missing asset paths.
2. **DOM helpers**: `el(tag, attrs, children)`, `notes(text)`, `fragment(child, index)`, `background(section, config)`.
3. **Slide renderers**: one function per slide type.

After rendering:

```js
Reveal.initialize(config).then(() => {
  Reveal.sync();
  Reveal.layout();
});
```

If slides are generated before `Reveal.initialize`, `sync()` is not strictly necessary but is harmless. If slides are inserted after initialization, `Reveal.sync()` is required.

## Stable IDs

Create deterministic IDs:

```js
function slugify(value) {
  return String(value)
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
```

Use IDs for:

- URL hashes.
- internal links.
- appendix jumps.
- test automation.
- regenerating the same deck without broken references.

## Security And Data Handling

- Use `textContent` for plain text.
- Use `innerHTML` only for trusted, authored slide markup.
- Treat external Markdown, JSON, and CSV as untrusted until sanitized.
- Do not render secrets, internal tokens, private URLs, or auth headers into deck source.
- Copy private screenshots into local assets only when the user has asked for a local artifact and the repo/workspace is appropriate for those files.

## Testing Generated Decks

For a generated deck, verify:

- no duplicate slide IDs
- every internal link target exists
- every asset URL/path resolves
- all slide types render at least once in a sample deck
- fragments appear in the intended order
- appendix slides are hidden or uncounted as intended
- PDF mode does not cut off content

## When Not To Generate

Use handwritten HTML or Markdown when:

- the deck has fewer than six slides and no repeated pattern
- layout is highly bespoke per slide
- the user is still exploring narrative order
- a human will edit the deck in raw HTML after handoff
