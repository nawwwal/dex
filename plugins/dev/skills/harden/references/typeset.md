# Typeset

Review typography for hierarchy, readability, rendering, and data alignment.

## Route Out First

- Razorpay Blade typography components or tokens: route to `blade`.

## Checks

### Scale
- Body text should usually be `1rem` / 16px equivalent.
- App UI can use tighter fixed rem steps: `0.75rem`, `0.875rem`, `1rem`, `1.125rem`, `1.25rem`, `1.5rem`, `2rem`.
- Marketing/content can use larger display type, but not inside dense dashboards.
- Do not scale type with viewport width in product UI.

### Readability
- Body line-height: 1.5-1.7.
- Heading line-height: 1.1-1.2.
- Paragraph line length: max around 65ch.
- No negative letter-spacing.
- Uppercase labels need modest positive letter-spacing only when legibility improves.

### Rendering
- Apply font smoothing once at the app/root level if the project uses it.
- Use `text-wrap: balance` for short headings.
- Use `text-wrap: pretty` for short-to-medium body text.
- Avoid both on long prose, code, and preformatted content.

### Data
- Use `font-variant-numeric: tabular-nums` for counters, prices, dashboards, and numeric table columns.
- Skip tabular numerals for prose, phone numbers, zip codes, and decorative display numerals.

## Output

```text
## Typeset: {target}

### Critical
- [file:line] - [typography issue] - Fix: [specific change]

### Warnings
- ...

### Passed
- ...
```
