# Figma -> Interactive Prototype

Converts Figma designs into interactive React prototypes with DialKit controls.

## Step 1: Get Figma Design
Do you have a Figma URL? If yes, use figma:implement-design skill.
If not, ask for the design or use the current code.

## Step 2: Read Figma Context
```
Use the figma:implement-design skill with the provided URL.
Extract: component structure, spacing, colors, interactions, variants.
```

## Step 3: Check Existing Blade Components
Before building from scratch:
- Check Blade MCP for equivalent components
- Check existing project components
- Prefer composition over new components

## Step 4: Build Prototype
Create a Next.js 16+ component with:
- All Figma variants as props or state
- DialKit controls for interactive tuning
- LocalStorage persistence for tuning values
- Geography/locale switching if needed

## Step 5: Add Iteration Controls
```jsx
// DialKit integration for live tuning
import { DialKitPanel } from 'dialkit';
// Add sliders for: spacing, timing, color values
```

## Step 6: Deploy Preview
Suggest: `vercel --prod` or local dev server for stakeholder review.
