# HTML Template

## Structure

The template is static HTML, CSS, and small vanilla JavaScript. It should open in a browser without a build step.

Required regions:

- masthead
- intro/meta line
- sections
- optional Blackline figures
- final `Read Next`
- floating section switcher

## Typography

Default fonts:

- Display: Gambetta from Fontshare for masthead, metadata, section titles, and final callouts.
- Body/UI: Nunito variable from Google Fonts for paragraphs, pills, captions, and section switcher.

Keep system fallbacks in CSS so the report remains readable offline.

## Theme

Support:

- `data-theme="dark"` or `data-theme="light"`
- `data-bg="#101010"` or another user-selected background

Foreground, muted text, links, borders, and panels must be derived from the background so the report stays readable. Use the bundled template script or equivalent contrast logic.

## Section Switcher

The floating switcher sits at the bottom center.

Behavior:

- collapsed state shows current section number and title
- hover or keyboard focus morphs the collapsed pill into a compact scrollable dropdown
- collapsed state uses the same active row label, centered inside the pill, so hover feels like one text object moving into position
- expanded rows are always left-aligned, including during hover-out collapse
- selection changes move only the highlight layer, not label text, alignment, or font weight
- dropdown corners should be softly rounded, not fully pill-shaped
- clicking a section scrolls to it
- current section updates on scroll
- works without covering body text on small screens

Use CSS for the open/close morph. JavaScript may populate links and update the current label, but must not be required for the dropdown animation itself. Use buttons or anchors with accessible labels. Do not rely only on hover; keyboard focus must reveal the same menu.

## Figure Markup

Only render a figure when the image asset exists.

```html
<figure class="brief-figure">
  <img src="assets/brief-illustrations/01-topic.png" alt="Short useful alt text">
  <figcaption>One sentence that connects the visual to the section.</figcaption>
</figure>
```

## Print

Print mode should:

- remove the floating switcher
- keep links underlined
- avoid clipping images
- keep sections readable on A4/letter
- preserve enough contrast for PDF export
