# Blackline Visuals

## Default

Use `$blackline` for visuals whenever it is available. If `$blackline` is unavailable but an image generation tool is available, generate images with these rules. If no image generation is available after a real attempt, omit images from the final HTML without placeholders.

## Visual Purpose

Images are cognitive anchors. Add one when the reader needs to see:

- an analogy made physical
- a hidden system
- a decision split
- a failure mode
- a before/after contrast
- a repeated sequence
- a term distinction
- an operator action

Do not use images as decoration or section dividers.

## Count

Do not hard-code a count.

- Simple brief: a few images.
- Dense explainer: many images.
- Complex topic with layered concepts: 10-15 images is acceptable.

Enough means every hard concept gets a visual anchor and no easy concept gets filler.

## Placement

Place images where comprehension improves:

- after a paragraph introduces a mechanism
- before a dense translation paragraph
- between two ideas when a visual bridge prevents confusion
- after a section if the image acts as the remembered takeaway

Do not enforce "one image per section." Do not leave an image slot empty.

## Terminology

Use the section's conceptual language. Do not use a fixed controlled vocabulary.

Labels should be short, readable English words that belong to the current idea. Good labels come from the mechanism in the prose, such as `metadata`, `trust`, `masked live data`, `search first`, `stale payload`, or `replay risk`.

## Generation Requirements

Each image should be:

- 16:9 horizontal
- pure white background
- black hand-drawn line art
- sparse red/orange/blue handwritten English annotations
- lots of white space
- Xiaohei as the subject performing the core action
- one concept only

Avoid:

- PPT infographics
- formal flowcharts
- top-left titles
- decorative mascot behavior
- non-English text
- dense annotation paragraphs
- screenshots or futuristic UI

## Final Artifact Rule

Never expose image prompts in the delivered report. Never include "image coming soon." Never ship broken image tags. If generation fails, remove that image beat and smooth the surrounding prose.
