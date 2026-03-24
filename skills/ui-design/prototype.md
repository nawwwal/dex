# Figma → Interactive Prototype

Converts Figma designs into interactive React prototypes with DialKit controls for live tuning.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Step 1: Get Figma Design

If Figma URL provided: call `get_screenshot(fileKey, nodeId)` and `get_design_context(fileKey, nodeId)` in parallel.
Otherwise: ask for the design or use current code.

## Step 2: Check Existing Components

Before building from scratch:
- **Blade mode**: check Blade MCP for equivalent components (`hi_blade`, then `get_blade_component_docs`)
- **Generic mode**: scan `src/components/` for existing components to reuse
- Prefer composition over new components

## Step 3: Build Prototype

Create a Next.js 16+ component with:
- All Figma variants as props or state
- DialKit controls for interactive tuning (see Step 4)
- LocalStorage persistence for tuning values
- Geography/locale switching if needed

## Step 4: Add DialKit Controls

Read `$CLAUDE_SKILL_DIR/dialkit.md` for full DialKit integration details.

## Step 5: Deploy Preview

Suggest: `vercel` (preview deployment) or local dev server for stakeholder review.

## Output

```
## Prototype: {COMPONENT_NAME}
Mode: Blade / Generic

### Files created
- [file paths]

### DialKit controls added
- [list of tunable params]

### Deploy
- Preview URL: [vercel preview URL] or local: npm run dev
```
