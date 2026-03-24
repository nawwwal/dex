# Harden — Edge Cases & Production Readiness

Make the UI production-ready by handling overflow, i18n, errors, and edge states.

## Mode Detection

```bash
BLADE_MODE=$(grep -q '"@razorpay/blade"' package.json 2>/dev/null && echo "yes" || echo "no")
```

## Checklist (all modes)

### Text overflow
- [ ] Long text doesn't break layout — add `overflow-wrap: break-word` and `min-width: 0`
- [ ] Truncation with ellipsis is intentional and has a tooltip: `title` attribute or `<Tooltip>`
- [ ] Numbers in tables have fixed width: `font-variant-numeric: tabular-nums`
- [ ] URLs and long strings don't overflow: `word-break: break-all` where appropriate

### i18n / Internationalization
_(Apply to Generic mode or explicitly international Blade projects. Skip for India-only Razorpay apps unless i18n is in scope.)_
- [ ] 30–40% space budget for translations (German, Arabic are longer than English)
- [ ] RTL support: use CSS logical properties (`margin-inline-start` not `margin-left`, `padding-block` not `padding-top/bottom`)
- [ ] `Intl` API for number, currency, date formatting — never hardcode `₹`, `$`, or date format
- [ ] No hardcoded English in JSX — all strings should be localization-ready

### Error handling
- [ ] HTTP 4xx → user-friendly message + action (not raw status code)
- [ ] HTTP 5xx → "Something went wrong" + retry button
- [ ] Network offline → offline indicator
- [ ] Form validation → inline error messages, not just console logs

### Empty states
- [ ] Empty table/list has a designed empty state (not a blank screen)
- [ ] Zero result searches have "No results found" + search term + clear filter CTA
- [ ] Loading states: skeleton or spinner (not blank screen)

### Large datasets
- [ ] Lists over 100 items: virtual scrolling or pagination
- [ ] Tables: limit visible columns, support horizontal scroll on mobile

### Double-submit prevention
- [ ] Submit buttons disabled while API is in-flight
- [ ] Optimistic updates have rollback on failure

## Blade mode actions

Use Blade components for edge states: `<EmptyState>`, `<Spinner>`, `<Skeleton>`, and `<Text color="feedback.text.negative.intense">` for errors. Check `get_blade_component_docs` for the correct props.

## Generic mode actions

Use the project's existing error/empty/loading patterns. Grep for existing `EmptyState`, `ErrorBoundary`, `Skeleton` components before creating new ones.

## Output

```
## Harden: {TARGET}

### Critical
- [file:line] — No min-width: 0 on flex child — Add min-width: 0 to prevent overflow
- [file:line] — Hardcoded ₹ symbol — Replace with Intl.NumberFormat

### Warnings
- [file:line] — No empty state for this list

### Applied fixes
- [what was changed]
```

## Predictive Prefetching

Start loading resources before the user explicitly requests them — reclaim 100-200ms of latency.

### Trajectory-Based (Recommended)
Use [ForesightJS](https://foresightjs.com/) / `useForesight` — predicts which link the cursor is moving toward based on trajectory, not hover:

```tsx
import { useForesight } from 'foresightjs';

function NavLink({ href, children }) {
  const { elementRef } = useForesight({
    hitSlop: 20, // trigger 20px before cursor reaches element
    callback: () => router.prefetch(href),
  });
  return <a href={href} ref={elementRef}>{children}</a>;
}
```

Reclaims 100-200ms compared to hover-based prefetch. Touch devices fall back automatically — no manual handling needed.

### Intent-Based (Not Viewport)
In Next.js App Router, `<Link>` prefetches automatically on viewport entry (when the router is idle). To disable this and prefetch only on intent:

```tsx
// Opt out of auto-prefetch; prefetch on foresight/hover intent instead
<Link href="/page" prefetch={false}>{label}</Link>
```

### Keyboard Navigation
Prefetch on Tab focus — keyboard users show clear intent:

```tsx
<a href="/page" onFocus={() => router.prefetch('/page')}>Link</a>
```

### Use Selectively
Best for: data-heavy multi-page apps, navigation to pages with API calls.
Avoid on: static sites (wastes bandwidth), low-traffic pages.
