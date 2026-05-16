# Visual Explanation Generator

Creates self-contained HTML visual explanations of systems, code, data, or plans.

## When to Use
- Any table with >3 columns and >4 rows (proactively)
- Architecture diagrams
- Data flows
- System comparisons
- Plan/spec visualizations
- Diff reviews
- Code change explanations

Do not use this generic mode for component handoffs, implementation handoffs, state inventories, screen inventories, or motion handoffs. Those requests use the handoff references from `visual/SKILL.md`.

## Step 1: Understand What to Visualize
What concept needs to be made visual?
- Data/tables → styled HTML table or card grid
- Flows → flowchart (Mermaid or CSS)
- Architecture → system diagram
- Before/after → side-by-side comparison
- Timeline → horizontal timeline component

## Step 2: Choose The Artifact Shape

- Flow: ordered steps, branching decisions, retries, ownership handoffs.
- System: components, data stores, boundaries, dependencies.
- Comparison: side-by-side differences with the decision criteria visible.
- Timeline: phases, dependencies, deadlines, owners.
- Dense table: group columns, freeze key labels, surface exceptions, and separate summary from raw rows.

Choose styling from the audience and content density. Do not randomize themes.

## Step 3: Generate Self-Contained HTML
Write a complete, single-file HTML with all CSS and JS inline.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{TITLE}</title>
<style>
/* Include full CSS — self-contained, no external dependencies */
</style>
</head>
<body>
<!-- Visual content here -->
</body>
</html>
```

Requirements:
- 100% self-contained (no CDN, no imports)
- Works when opened directly in any browser
- Responsive (works at 320px to 1440px)
- Accessible (WCAG AA)
- Copyable: include "Copy as Markdown" or "Copy code" button where applicable

## Step 4: Open in Browser (optional)
Offer to open the file only if a file was created and the user wants to inspect it.
