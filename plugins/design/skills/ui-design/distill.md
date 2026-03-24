# Distill — Strip to Essence

Ruthless simplification. Remove everything that isn't carrying weight.

## Principle

Minimalism ≠ removing features. Distilling = revealing the core by removing noise.
"Mystery ≠ minimalism" — never remove content the user needs to make a decision.

## What to remove (all modes)

### Information architecture
- More than one primary action per screen → promote one, demote the rest
- Duplicate navigation paths → pick one canonical path
- Content visible only to satisfy internal stakeholders, not users → hide or remove
- Onboarding tooltips that show up on every visit → show once, then dismiss

### Visual
- 3+ accent colors → 1–2 colors (primary + semantic feedback only)
- 5+ font size variants → 3–4 (body, subheading, heading, display)
- Decorative dividers, borders, shadows used everywhere → use whitespace instead
- Cards nested inside cards → flatten to 1 level
- Icons + labels → labels alone if space allows (icons are ambiguous)

### Layout
- Centering everything → align leading edge (left for LTR) to create scannable columns
- Equal spacing everywhere → generous section breaks, tight item spacing
- Full-width everything → use max-width to keep reading width comfortable

### Interaction
- Multiple ways to do the same action → one canonical path
- Progressive disclosure: hide advanced options under "More options" or secondary navigation
- Smart defaults: pre-fill what you know, don't ask what you can infer

## Hard limits — NEVER remove
- Functionality the user needs (even if rarely used)
- Accessibility labels and focus management
- Error states and empty states
- Legal/compliance information
- Decision-critical information (amounts, dates, account numbers)

## Output

```
## Distill: {TARGET}

### Removed
- Secondary CTA "View all transactions" (low usage, same destination as "Settlements" nav)
- Decorative divider between each row (replaced with whitespace)
- "Advanced filters" shown by default (moved behind "More filters")

### Reduced
- 6 font sizes → 4 (removed 10px and 20px, everything maps to the 4-step scale)

### Could not remove (decision-critical)
- Transaction ID displayed even though it's long — users need it for support tickets
```
