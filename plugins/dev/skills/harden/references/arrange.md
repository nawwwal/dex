# Arrange

Review layout, spacing, visual rhythm, and alignment.

## Route Out First

- Razorpay Blade spacing props or token replacement: route to `blade`.
- In Blade projects, large interaction/motion feel changes, transition mapping, hover/focus/tap, or Blade-owned surfaces: route to `blade` first. Generic feel/motion skills can critique the mechanic after Blade MCP proves the allowed Blade path.

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
- Keep elements in normal document flow unless overlay behavior requires otherwise.
- Add responsive constraints for fixed-format elements: `minmax`, `max-width`, `aspect-ratio`, or container queries.
- Use `min-width: 0` on flex children that contain long text, tables, URLs, or IDs.
- Avoid arbitrary one-off values such as 37px or 13px unless there is a measured optical reason.
- Avoid `position: absolute`, negative margins, and transform offsets as primary layout tools.

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
