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

## Blade Score Gate (Mode A — always run after implementation)

After all Blade implementation work is done, check coverage and iterate until ≥ 90%.

### 1. Measure

Invoke the `blade-score` skill with the dev server URL:

```
Skill("blade-score", "<dev-server-url-for-this-page> --json --threshold 90")
```

If exit 0 (coverage ≥ 90%) → implementation is complete.

### 2. Identify gaps (if below 90%)

Inspect the component file(s) just written. Find native HTML elements (`<div>`, `<span>`, `<p>`, `<button>`, `<input>`, etc.) that a Blade component could replace.

### 3. Spawn improvement subagents

Spawn one `Agent` per distinct UI area needing improvement. Each subagent receives:
- The component file(s) to fix
- Current blade-score JSON (coverage, totalNodes, bladeNodes)
- Task: replace non-Blade HTML elements with their Blade equivalents

**Subagent workflow:**
1. For each non-Blade element in scope, call `get_blade_component_docs([candidates])` to confirm the right Blade component and its props
2. Call `get_blade_general_docs("box")` for any layout `<div>` (Box replaces most layout divs)
3. Call `get_blade_pattern_docs` if the element is part of a known Blade pattern
4. Replace the element, update imports, remove unused HTML elements
5. No hardcoded hex/spacing — use Blade tokens throughout

### 4. Re-measure and loop

After subagents complete, re-run the blade-score skill. Repeat steps 2–4 until:
- Coverage ≥ 90% (exit 0), or
- Two consecutive runs return the same score (no further Blade improvement possible — log final score and stop)

---

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

### Blade Score (Mode A)
- Final coverage: 93.4% (PASS ≥ 90%)
```
