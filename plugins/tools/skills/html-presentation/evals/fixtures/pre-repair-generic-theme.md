# Pre-Repair Generic Theme Snapshot

This fixture records the failure mode that the html-presentation skill must not regress to.

Observed problems:

- The deck appeared as a centered black rectangle inside a white browser viewport instead of using a full-viewport Reveal background.
- Slide 2 used black-on-black text because Reveal's theme stylesheet overrode custom foreground colors.
- The sample deck changed visual systems per slide: blueprint opener, black-stage content, pale-mat comparison, event-atmosphere metric.
- Typography and palette were not deck-wide foundations.
- The output looked like a style sampler instead of a coherent presentation system.

Required repair behavior:

- Use one deck-wide visual system by default.
- Use Reveal background attributes or generated equivalents for full-bleed backgrounds.
- Force inherited readable text colors after importing Reveal themes.
- Run contrast checks for the selected foreground/background pairs.
