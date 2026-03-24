# Arrange — Layout & Spacing Fixes

Fix whitespace, grid, visual rhythm, and alignment.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Rules (all modes)

### Spacing scale
Use a consistent scale based on 4px units:
- Conceptual: `xs=4px, sm=8px, md=12px, lg=16px, xl=24px, 2xl=32px, 3xl=48px, 4xl=64px, 5xl=96px`
- In Blade: `spacing.1=4px, spacing.2=8px, spacing.3=12px, spacing.4=16px, spacing.6=24px` (see Blade mode below)
- In CSS: `--space-1: 4px, --space-2: 8px...` (see Generic mode below)

### Rhythm
- Tight groupings (related items): 8–12px between elements
- Section breaks: 48–96px between major sections
- "Squint test" — squint at the design: does hierarchy read clearly? If everything looks the same weight, spacing is broken.

### Layout
- **Flexbox** for 1D layouts (row OR column)
- **Grid** for 2D layouts (rows AND columns simultaneously)
- Default: prefer `gap` over margins/padding hacks
- Asymmetric spacing is usually wrong — flag it

### Fluid spacing
For marketing/content: use `clamp()` for responsive spacing: `padding: clamp(16px, 4vw, 48px)`

### Anti-patterns
- Monotonous card grids (equal size = no hierarchy)
- Everything centered (use alignment as a tool, not a default)
- Arbitrary spacing (37px, 13px — should be on-scale)
- Margins fighting `gap`

## Blade mode actions

Replace hardcoded spacing with Blade spacing props:
```tsx
// Before: <div style={{ padding: '16px', gap: '8px' }}>
// After: <Box padding="spacing.4" gap="spacing.2">

// Use Box component padding/margin/gap props with Blade spacing scale
// spacing.1=4px, spacing.2=8px, spacing.3=12px, spacing.4=16px, spacing.5=20px, spacing.6=24px
```

Check `get_blade_general_docs("Usage")` for spacing token reference.

## Generic mode actions

Replace hardcoded values with the spacing scale defined in the "Rules" section above.
Use CSS custom properties: `--space-1` through `--space-16` (1 unit = 4px).

## Output

```
## Arrange: {TARGET}

### Critical (must fix)
- [file:line] — arbitrary spacing 37px — Replace with space-10 (40px)
- [file:line] — margin fighting gap — Remove margin, use gap only

### Warnings
- [finding]

### Applied fixes
- [what was changed]
```
