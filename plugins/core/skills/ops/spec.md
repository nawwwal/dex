# Handoff Specification

Creates a comprehensive handoff spec for engineers. Maps all states, edge cases, Blade components.

## Step 1: Understand the Component/Feature
What is being handed off? Ask if unclear.

## Step 2: Map All States
For each interactive element, document:
- Default state
- Hover state
- Active/pressed state
- Focused state
- Loading state
- Error state
- Disabled state
- Empty state
- Success state

## Step 3: Edge Cases
- What happens with very long text?
- What happens on mobile (< 375px)?
- What happens with RTL languages?
- What if the API is slow (>3 seconds)?
- What if the API fails?
- What if the user is offline?

## Step 4: Blade Component Mapping
For each UI element: which Blade component implements it?
```markdown
| UI Element | Blade Component | Props |
|-----------|-----------------|-------|
| Primary button | `<Button variant="primary">` | size="medium" |
| Card | `<Box>` with shadow tokens | elevation="low" |
```

## Step 5: Write Spec

```markdown
---
date: YYYY-MM-DD
project: {project}
type: handoff-spec
feature: {feature name}
---

# Handoff Spec: {Feature Name}

## Overview
[1-2 sentences: what this feature does and where it lives]

## Figma Link
[URL to final designs]

## Component Inventory

### {Component Name}
**Blade:** `<ComponentName prop="value" />`
**States:**
| State | Visual | Notes |
|-------|--------|-------|
| Default | [description] | |
| Hover | [description] | |
| Loading | [description] | Skeleton loader |
| Error | [description] | Show inline error |
| Empty | [description] | Empty state with CTA |

## Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| API timeout | Show retry with error message |
| Long text | Truncate with tooltip |
| Mobile | Stack to single column |

## Accessibility
- Tab order: [describe logical tab sequence]
- Screen reader: [describe what's announced]
- Focus management: [where focus goes after interactions]

## Copy / Strings
All user-visible text strings with their keys:
```
KEY: value
```
```

## Step 6: Auto-run Accessibility Check
After writing the spec: "Running accessibility check on this spec..."
→ Signal to /design review a11y to verify the spec covers all a11y requirements.
