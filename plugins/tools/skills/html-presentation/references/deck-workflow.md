# Deck Workflow

## Intake

Collect only the inputs that change the artifact:

- **Audience**: who sees it and what they already know.
- **Decision**: what the deck should make possible.
- **Runtime**: local talk, hosted page, embedded module, kiosk, article, or export.
- **Source material**: notes, doc, PRD, data, screenshots, code, assets, brand rules.
- **Output**: HTML-only, npm project, static site route, PDF, or both HTML and PDF.
- **Constraints**: time, aspect ratio, offline use, asset privacy, accessibility, motion tolerance.

If narrative is unclear, use `$present` first. If narrative is clear, build.

## Structure Patterns

### Decision Deck

Use when a room needs to approve, reject, or choose.

1. Title with the decision named.
2. Current state and consequence.
3. Evidence.
4. Proposed mechanism.
5. Walkthrough or comparison.
6. Tradeoff slide.
7. Decision request.
8. Appendix with details and objections.

### Product Walkthrough

Use when demonstrating a flow, feature, or prototype.

1. User/job setup.
2. Failure in the old flow.
3. New route map.
4. Step-by-step flow with screenshots or embeds.
5. What changes operationally.
6. Risks and open questions.
7. Next step.

### Technical Explanation

Use when teaching architecture, APIs, algorithms, or migration plans.

1. One-line problem.
2. Existing system map.
3. Constraint or failure mode.
4. Proposed architecture.
5. Code/API example.
6. Runtime or data flow.
7. Migration/rollout path.
8. Observability and rollback.

### Generated Report

Use when slides come from structured data.

1. Summary slide generated from top-level metrics.
2. Repeated section per entity/team/site/customer.
3. Detail slides created only when data crosses a threshold.
4. Uncounted appendix for raw tables, logs, or methodology.

## Content Options

- **HTML slides**: best for precise layout, components, media, and custom interaction.
- **Markdown slides**: best for fast text-heavy decks; weaker for complex layouts.
- **External Markdown**: useful when content is edited by non-engineers.
- **JavaScript-generated slides**: best for repeatable reports, variants, and data-driven decks.
- **React slides**: best when slides reuse existing React components or live inside a React app.

## Slide Mechanics

Use each mechanic for a job:

- **Fragment**: sequence attention within one idea.
- **Vertical stack**: optional detail under one horizontal story beat.
- **Auto-animate**: show a before/after or evolving model without re-explaining the scene.
- **Background**: set context, not decorate. Good for product screenshots, maps, media, or chapter shifts.
- **Lightbox**: let the speaker inspect a visual without leaving the slide.
- **Speaker notes**: hold spoken transitions, claims, caveats, and timing.
- **Uncounted slides**: appendix material that should not affect perceived deck length.
- **Internal links**: jump to appendix, demo branches, or alternate flows.

## Writing Slides

Prefer slide titles that make claims:

- Weak: `Performance`
- Strong: `The slow path is the partner lookup, not rendering`

Prefer body copy that names the mechanism:

- Weak: `Better onboarding experience`
- Strong: `The user chooses a template first, so the form only asks for missing fields`

Keep each slide inspectable at presentation distance:

- one primary claim
- no more than two supporting regions
- no dense paragraphs unless using scroll view
- code blocks with highlighted lines, not full files
- screenshots cropped to the decision area

## Verification

Before final handoff:

1. Run a local server; do not rely on file URLs if modules or external Markdown are used.
2. Navigate all horizontal slides.
3. Navigate at least one vertical stack.
4. Step through all fragments on dense slides.
5. Open speaker view if notes are included.
6. Open print route with `?print-pdf` when PDF export matters.
7. Check mobile/touch if the deck will be opened on phones or tablets.
8. Confirm no console errors for missing assets, plugins, or module imports.

Notes/export verification is mechanical:

```text
Speaker view: serve the deck, open it, press S, and confirm current slide, next slide, timer, and notes render.
PDF: open http://localhost:PORT/?print-pdf in Chrome/Chromium, press Cmd+P, Save as PDF, Landscape, Margins None, Background graphics on.
```
