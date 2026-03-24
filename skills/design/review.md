# Design Review

Live design review using agent browser and design critique. Chains to a11y automatically.

## Step 1: Get the Target
Is there a URL? A file? A screenshot? Determine what to review.

## Step 2: Run Agentation (if URL available)
If reviewing a live page:
- Use agent-browser to open the page (native mode for authenticated devstack)
- Use agentation-self-driving skill for autonomous annotation
- Capture annotations

## Step 3: Code Review (if reviewing code files)
For .tsx/.jsx files:
- Invoke design-reviewer agent (it has a full review protocol)
- Check Blade compliance
- Check WCAG basics

## Step 4: Interface Craft Critique
Apply Josh Puckett's three-pillar critique from skills/motion/craft.md:
1. Simplicity — one clear primary action per screen?
2. Fluidity — are transitions present and directional?
3. Delight — are states celebrated?

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

Score: X/100 (Critical: -15 each, Warning: -8 each)
```

## Step 6: Auto-chain to A11y
"Running accessibility check now..."
→ Read and follow a11y.md
