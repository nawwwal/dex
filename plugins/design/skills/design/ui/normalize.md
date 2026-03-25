# Normalize — Design System Alignment

Scan and replace ad-hoc values with the established design system. Think of it as "replace custom with canonical."

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Process (all modes)

1. **Discover** — find all ad-hoc values: hardcoded hex colors, px spacing, custom font-size declarations, non-system components, custom animation durations
2. **Plan** — map each ad-hoc value to its canonical system equivalent
3. **Execute** — replace systematically, one category at a time
4. **Clean up** — remove dead CSS/unused vars, run `tsc --noEmit`, run linter

## Blade mode

Replace ad-hoc → Blade equivalents:

| Ad-hoc | Blade replacement |
|--------|------------------|
| `#0066CC`, `rgb(0,102,204)` | On Blade component with `color` prop: use `color="primary"`. In CSS/style context: use `surface.action.icon.default` token |
| `#E5F1FF` | `surface.action.background.primary.subtle` |
| `#333333` | `surface.text.gray.normal` |
| `padding: 16px` | `padding="spacing.4"` (Box prop) |
| `gap: 8px` | `gap="spacing.2"` (Box prop) |
| `<div>text</div>` | `<Text>text</Text>` |
| `<h2>heading</h2>` | `<Heading size="medium">` |
| `<input type="text">` | `<TextInput>` |
| `<select>` | `<SelectInput>` or `<Dropdown>` |
| `<button>` | `<Button>` |

Use `get_blade_component_docs` to verify correct props before replacing.

For each component replaced, check if additional props are needed (label, accessibilityLabel, etc.).

For the full Blade spacing scale (spacing.1–spacing.20), see `$CLAUDE_SKILL_DIR/arrange.md`.

## Generic mode

Replace ad-hoc → project's established system:

1. Scan for CSS custom properties already defined (`:root { --color-* }`)
2. Map hardcoded values to existing tokens
3. If no token exists for a value used 3+ times: create one
4. Replace inline styles with class names where possible

## Output

```
## Normalize: {TARGET}

### Replaced
- [file:line] — #0066CC → color="primary" (Button prop)
- [file:line] — padding: 16px → padding="spacing.4"

### Cannot normalize (needs design decision)
- [file:line] — custom animation timing 750ms (no system equivalent)

### After
Run: tsc --noEmit && eslint .
```
