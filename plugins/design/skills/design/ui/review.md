# Design Review

Live design review using agent browser and design critique. Chains to a11y automatically.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Step 1: Determine review target

Identify the target: URL, file, screenshot, or Figma link.

## Step 2: Capture (if URL available)

If reviewing a live page:
- Use `agent-browser` to open the page (native mode for authenticated devstack)
- Take a screenshot for visual reference
- Note any obvious layout, contrast, or interaction issues

## Step 3: Code Review (if reviewing code files)

For .tsx/.jsx files:
- Invoke `design-reviewer` agent (it has a full review protocol)
- In Blade mode: also check Blade compliance using `blade-reviewer` agent
- Check WCAG basics (chains to a11y.md automatically in Step 6)

## Step 4: Animation Craft Review

If the component has animations or transitions:
→ Load `motion/craft.md` for Josh Puckett 3-pillar critique (Simplicity / Fluidity / Delight)
→ Load `motion/review.md` if reviewing animation code specifically (Before/After/Why table)
→ If Agentation MCP is installed: `agentation_get_pending` first to check for visual annotations

For non-animated UI, skip this step.

## Step 5: Output Review Report

```
## Design Review: {TARGET}

### Critical (must fix)
- [finding] — [element] — [rule]
  Fix: [concrete change]

### Warning (should fix)
- [finding] — [element]

### Passed
- [what's working]

Score: X/100. Starts at 100, floor is 0. Critical: -15 each. Warning: -8 each.
```

## Step 6: Auto-chain to A11y

"Running accessibility check now..."
→ Read and follow a11y.md
