# Implement — Figma to Production Code

Convert a Figma design to production-ready code. Two modes auto-detected per project.

## Mode detection

```bash
# PRIMARY: check package.json for Blade dependency
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")

# SECONDARY: check existing imports if package.json check passes
if [ "$BLADE_MODE" = "yes" ]; then
  BLADE_IMPORTS=$(grep -r "@razorpay/blade" src/ 2>/dev/null | wc -l)
  # Note: only applies when editing existing code — new files in a Blade project have zero imports by definition
  [ "$BLADE_IMPORTS" -eq 0 ] && BLADE_MODE="no"  # Blade listed but not actually used
fi

# User override: "with blade" / "without blade" → respect user intent
```

---

## Mode A: Blade (Razorpay projects)

**Dispatch to `blade-implementer` sub-agent for page/screen-level work.**

Trigger blade-implementer agent when:
- Figma node is a frame (full page or screen-level design)
- Design has multiple interacting components
- Expected output is >50 LOC

**Run inline for component-level work** (single component, <50 LOC expected):

### Inline Blade workflow:
1. Parse Figma URL → extract fileKey + nodeId (convert `-` to `:`)
2. Call `get_screenshot(fileKey, nodeId)` for visual reference
3. Call `get_figma_to_code(fileKey, nodeId, currentProjectRootDirectory)` → get Blade code
4. Call `get_blade_component_docs(componentsList)` to validate variants against screenshot
5. Replace hardcoded values with Blade tokens
6. Validate: no hardcoded hex/spacing, correct Blade imports from `@razorpay/blade/components`
7. Call `publish_lines_of_code_metric` once when done

---

## Mode B: Generic (non-Razorpay / non-Blade projects)

### Generic workflow:
1. Parse Figma URL → extract fileKey + nodeId (convert `-` to `:`)
2. Call `get_design_context(fileKey, nodeId)` + `get_screenshot(fileKey, nodeId)` in parallel
3. Detect existing component library: scan `package.json` for shadcn, radix, mantine, etc.
4. Scan existing components in `src/components/` — reuse before creating new
5. Implement using:
   - Project's existing components first
   - Tailwind CSS + CSS custom properties for tokens (no hardcoded hex/spacing)
6. Data contract check:
   - If existing data hooks/types found for this component → wire to them
   - If no existing contracts → scaffold TypeScript-typed `TODO` placeholders
   - If user said "prototype" or "demo" → can use realistic placeholder data
7. Visual validation against `get_screenshot` output

---

## Common rules (both modes)

- TypeScript types required — no `any`
- File placement: follow existing project structure (scan 2-3 similar components for convention)
- No hardcoded hex colors, pixel spacing, or magic numbers
- Remove unused imports before reporting done

## Output

```
## Implement: {COMPONENT_NAME}
Mode: Blade / Generic

### Files created/modified
- src/components/[ComponentName].tsx — new component
- [any other files]

### Blade components used (Blade mode)
- Button, TextInput, Box, Text

### Data contracts
- Wired to: usePaymentsData hook / TODO placeholders (new feature)

### Visual diff check
- [x] Layout matches Figma
- [x] Spacing correct
- [x] Typography correct
- [ ] Loading state — not in Figma, scaffolded with Spinner
```
