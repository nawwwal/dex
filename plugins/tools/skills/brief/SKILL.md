---
name: brief
description: Create browser-native editorial HTML briefs with dynamic sectioning, Blackline-style conceptual visuals, inline sources, read-next links, adaptive color themes, and a floating section switcher. Use when the user wants a polished long-form HTML report or visual explainer, not a slide deck, PowerPoint, Reveal.js presentation, or Figma file.
---

# Brief

Create the actual HTML brief. Do not create a slide deck, Reveal.js project, outline-only narrative, or prompt pack.

The output is a long-form browser-native report in the style of the provided "Between the Lines" examples: specific, direct, readable, visually enriched, and structured around whatever lenses make the topic easiest to understand.

## Source Rules

Load only the reference needed for the job:

- `references/report-workflow.md` for intake, section derivation, links, and generation order.
- `references/editorial-style.md` for copy, titles, tone, and section mechanics.
- `references/blackline-visuals.md` for visual strategy and image generation behavior.
- `references/html-template.md` for template structure, color behavior, and section switcher requirements.
- `references/verification.md` for final checks.

If the user asks for a slide deck, Reveal.js, PowerPoint, Google Slides, or Figma Slides, route away. This skill owns HTML editorial briefs only.

## Default Workflow

1. Clarify only inputs that change the artifact: topic, reader, source material, deadline, output folder, theme preference, privacy limits, and whether external links should be browsed.
2. Build the topic model:
   - what the reader already assumes
   - what is hard to understand
   - what decision or action the brief should unlock
   - which concepts need an analogy, visual, or source
3. Derive a dynamic section spine. Do not hard-code a fixed four-section format.
4. Write section titles as specific claims, not labels.
5. Create a Blackline visual strategy and try hard to generate actual images.
6. Build the HTML artifact from `assets/report-template/`.
7. Add inline links and a final `Read Next` block with one-sentence descriptions.
8. Verify browser rendering, responsive behavior, color contrast, image loading, switcher behavior, and print/PDF styling.

## Required Artifact

Every finished brief must include:

- `index.html` or equivalent static entrypoint.
- CSS that defines the report reading system, light/dark variants, derived readable colors, and print behavior.
- JavaScript only when needed for color derivation, section switcher behavior, or theme controls.
- A dynamic section spine with numbered lens pills.
- Inline source links plus a final `Read Next` section when sources exist.
- Actual generated visuals when image generation is available.
- No empty image slots, prompt placeholders, missing-image cards, or "image coming soon" copy.

## Visual Standard

Always try to use `$blackline` for visuals. If `$blackline` is not callable but image generation is available, follow the Blackline rules in `references/blackline-visuals.md`. If no image generation is available after a real attempt, omit visuals cleanly and do not expose prompts or placeholders in the final HTML.

Visuals are not decoration. Add them where a reader needs a cognitive anchor: hidden mechanism, analogy, before/after, failure mode, sequence, decision split, vocabulary distinction, or operator action.

## Design Standard

The brief should feel like a readable editorial artifact, not a dashboard, landing page, or deck:

- narrow centered measure
- large serif masthead
- italic serif section titles
- small numbered lens pills
- muted body text with generous line height
- sparse panels reserved for final asks or `Read Next`
- bottom floating section switcher that collapses to the current section and expands on hover/focus

Configurable color is allowed, but readability is not optional. Use the template color derivation or run the contrast helper for every theme handed off.
