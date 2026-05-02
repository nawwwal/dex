# Diverge Paper Canvas Template

Use this when the user wants visual side-by-side comparison. Each artboard should expose layered decisions, not decorative lore.

## Artboard sections

Each direction artboard contains:

1. Header: direction name, altitude, product bet.
2. Product model panel: user, job, objects, current decision.
3. State matrix panel: state, meaning, action, representation, copy.
4. Screen anatomy panel: top, primary, secondary, detail, CTA, hidden/after-interaction.
5. Copy panel: title, CTA, empty/loading/error/success.
6. Layout panel: topology, density, responsive behavior.
7. Interaction panel: trigger, input, feedback, recovery.
8. Visual system panel: typography, color, motion, shape.
9. Emotional/persuasive rationale.
10. Handoff strip: state machine, events, data, accessibility, QA.

## Required per-artboard questions

- What is the object model?
- What is the primary user decision?
- What changed by layer?
- What stays constant?
- What does the user see first?
- What does the user do?
- What does the system do?
- What state behavior changes?
- What copy changes?
- What layout/hierarchy changes?
- What data must exist?

## Dimensions

- Desktop product: 1440 x 900
- Mobile-first flow: 390 x 844
- Tablet: 768 x 1024

Arrange artboards horizontally with 80px gaps.

## HTML conventions

- Inline styles only.
- Use flex layouts with padding and gap.
- Do not use margin.
- Do not use HTML tables; represent matrices with flex rows.
- Use `layer-name` attributes on major groups.
- Escape user-provided strings.
- Use design-system tokens when the brief provides them.

## Visual guidance

- Product register: familiar components, clear states, restrained color, useful density.
- Brand register: stronger type/color/composition is allowed.
- Mixed register: identify which artboard sections are product and which are brand.

## Legacy output to remove

- Reference cards as mandatory output.
- Reward cards as mandatory output.
- Belief statements as mandatory framing.
- Metaphor-heavy headers.
- Decorative visuals that do not change execution.

## Completion note

```md
Generated <N> layered divergence artboards in Paper. Each artboard includes product model, state matrix, screen anatomy, copy, layout, interaction, visual system, emotional rationale, and handoff notes.
```
