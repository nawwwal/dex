---
type: design-taste
tags: [blade, design-system, razorpay, components, taste, figma, ui]
updated: 2026-03-23
---

# Blade Design Taste — the user's Opinionated Defaults

> Load before any Blade implementation or design review. Settled decisions — not re-litigated per feature.

## Component Selection

### Layout
- `Box` for spacing containers, not raw div + inline styles
- `Stack` (vertical) / `Inline` (horizontal) for repeated spacing — never manual margin stacking
- `Grid` only for genuinely 2D layouts

### Data Display
- Summary states → `Card` (not raw Box with border)
- Tables → `Table` (never custom table markup — Blade Table handles sorting, empty states, loading)
- Metrics/KPIs → `Amount` + `Badge`
- Lists without actions → `List`; lists with actions → `Table`

### Status & Feedback
- Inline success/error/warning → `Alert` (not colored Box)
- Transient feedback → `Toast` (not Alert — Toasts auto-dismiss)
- Loading → `Spinner` inside loading zone, not page overlay
- Empty states → `EmptyState` with illustrated spot icon at 120px, never plain text

### Forms
- Always `FormLabel` + `FormHint` + `FormError` — never build label/hint/error manually
- `Select` not native `<select>`
- `TextInput` / `TextArea` — never raw `<input>` or `<textarea>`

### Navigation
- Page tabs → `Tabs` (not custom tab UI)
- Contextual actions → `Dropdown` (not raw popover)
- Primary CTA → `Button variant="primary"`, secondary → `variant="secondary"`, destructive → `variant="destructive"`
- Never more than one `primary` button visible at once

## Spacing & Sizing
- Use Blade spacing tokens (`spacing.4`, `spacing.8`, etc.) — never raw px values in styled props
- Icon sizes: small=12px, medium=16px, large=20px, xlarge=24px — match to text size
- Border radius: Blade tokens only — never `borderRadius: "4px"` inline

## Anti-patterns
- Glassmorphism / heavy gradients — not Razorpay's design language
- Custom modals — use `Modal`; never backdrop + positioned div
- Custom tooltips — use `Tooltip` with `TooltipProvider` at layout root
- Placeholder zeros — use `EmptyState`, not `0` or `—`
- Generic "Loading..." text — use `Spinner` inline in loading zone

## Screen Layout Conventions
- Dashboards: Card + Table + Filters — never accordion for primary content
- Checkout flows: single-column, progressive disclosure — no sidebars
- Settings pages: Tabs + Card + Form — destructive actions at bottom with AlertDialog
- Empty state illustrations: Razorpay's illustrated spot icons — never emoji or generic icons

## Blade Score Target: 95%+
Run Blade reviewer after any implementation. Score < 95% means something above was violated.
Known common failures: custom border styling, non-Blade spacing, missing FormLabel, custom modal.
