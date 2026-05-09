# Arrange

Review layout, spacing, visual rhythm, and alignment.

## Route Out First

- Razorpay Blade spacing props or token replacement: route to `design:blade`.
- Large interaction/motion feel changes: route to `make-interfaces-feel-better` or `web-animation-design`.

## Checks

### Spacing Scale
- Use a consistent 4px-based scale.
- Related items: 8-12px.
- Control groups and form rows: 12-24px.
- Major product sections: usually 24-48px.
- Marketing/content sections can use larger gaps if scan speed is not the main job.

### Density
- Dashboards, tables, forms, and operational tools should preserve scanning density.
- Do not create 100px+ gaps or hero-scale typography inside dense product surfaces.
- If density changes, state the task-speed tradeoff.

### Layout
- Prefer `gap` over margin chains.
- Use Flexbox for one-dimensional layouts and Grid for two-dimensional layouts.
- Add responsive constraints for fixed-format elements: `minmax`, `max-width`, `aspect-ratio`, or container queries.
- Avoid arbitrary one-off values such as 37px or 13px unless there is a measured optical reason.

### Alignment
- Use leading alignment for scannable lists, tables, and forms.
- Center alignment is acceptable for empty states, narrow confirmations, and editorial blocks.
- The squint test should reveal one primary region, one secondary region, and clear supporting content.

## Output

```text
## Arrange: {target}

### Critical
- [file:line] - [layout issue] - Fix: [specific change]

### Warnings
- ...

### Tradeoffs
- ...
```
