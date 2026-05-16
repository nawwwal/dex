# Normalize

Review whether a UI uses its local design system instead of ad-hoc values.

## Route Out First

- Razorpay Blade component, token, score, or coverage work: route to `blade`.

## Process

1. Discover hardcoded colors, spacing, font sizes, shadows, radii, durations, high-specificity selectors, inline styles, and custom components.
2. Identify the project's existing tokens, CSS variables, theme files, or component primitives.
3. Map repeated ad-hoc values to existing system values.
4. Flag overrides that fight the system instead of using its token, prop, class, or primitive.
5. Recommend replacements. Only edit if the user explicitly asks to apply/fix.

## Checks

- Colors map to semantic roles such as action, danger, success, warning, neutral, or surface.
- Spacing follows the project's scale.
- Typography uses existing text components or CSS variables.
- Component primitives are reused before custom controls are created.
- Inline styles are removed when a class, token, prop, or primitive exists.
- `!important`, ID selectors, and deep descendant overrides are treated as design-system drift unless the project explicitly requires them.
- New tokens are recommended only when the same value appears repeatedly and has a stable semantic role.

## Output

```text
## Normalize: {target}

### Replace
- [file:line] - [ad-hoc value] -> [existing system value] - Reason: [semantic role]

### Needs decision
- [file:line] - [value] - No existing system equivalent. Decision needed: [choice]

### Not changed
- [why]
```
