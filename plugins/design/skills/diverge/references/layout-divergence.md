# Layout Divergence

Use when the surface concept is stable but arrangement, density, grouping, and responsive behavior are open.

## Layout topology options

- Single column
- Split pane
- List/detail
- Table/detail
- Queue
- Timeline
- Kanban
- Matrix
- Dashboard grid
- Inspector sidebar
- Canvas
- Map
- Step flow
- Comparison table
- Report
- Command palette
- Notification-first
- Modal
- Drawer
- Bottom sheet

## Layout decisions

For each layout direction, specify:

- Primary region
- Secondary region
- Detail region
- Persistent controls
- Scroll behavior
- Empty state location
- Error location
- CTA placement
- Responsive transformation
- Density
- Grouping logic

## Layout quality gates

- Can the user identify the primary action within 2 seconds?
- Does proximity group related items?
- Does spacing separate unrelated items?
- Is density appropriate to usage frequency?
- Does the layout work with real content length?
- Does the layout handle empty/error/loading states?
- Does mobile preserve function rather than amputating it?
- Can a designer sketch it in 5 minutes?

## Layout output

```md
## Layout direction: <functional name>
- Topology:
- Primary region:
- Secondary region:
- Detail region:
- Persistent controls:
- CTA placement:
- Scroll behavior:
- Empty/error/loading placement:
- Responsive behavior:
- Density:
- Tradeoff:
```
