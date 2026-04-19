# Animation Code Review

## Required Review Format

When reviewing animation code, you MUST output a markdown table with Before/After/Why columns. Do NOT use a list with "Before:" and "After:" on separate lines.

**Correct format:**

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; avoid `all` |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Nothing in the real world appears from nothing |
| `ease-in` on dropdown | `ease-out` with custom curve | `ease-in` feels sluggish; `ease-out` gives instant feedback |
| No `:active` state on button | `transform: scale(0.96)` on `:active` | Buttons must feel responsive to press |
| `transform-origin: center` on popover | `transform-origin: var(--radix-popover-content-transform-origin)` | Popovers should scale from their trigger (not modals — modals stay centered) |
| Default-state element animates on first render | Add `initial={false}` to `AnimatePresence` | Prevent noisy first-paint motion |
| Icon toggles by mount/unmount only | Animate `opacity`, `scale`, and `blur` with both states represented | Icon changes should feel intentional, not abrupt |

**Wrong format (never do this):**

```
Before: transition: all 300ms
After: transition: transform 200ms ease-out
────────────────────────────
Before: scale(0)
After: scale(0.95)
```

Correct format: A single markdown table with | Before | After | Why | columns, one row per issue found.

---

## Review Checklist

When reviewing animation code, check for each of these issues:

| Issue | Fix |
| --- | --- |
| `transition: all` | Specify exact properties: `transition: transform 200ms ease-out` |
| `scale(0)` entry animation | Start from `scale(0.95)` with `opacity: 0` |
| `ease-in` on UI element | Switch to `ease-out` or custom curve |
| No `AnimatePresence initial={false}` for default-state content | Add `initial={false}` unless a first-load entrance is intentional |
| `transform-origin: center` on popover | Set to trigger location or use Radix/Base UI CSS variable (modals are exempt — keep centered) |
| Animation on keyboard action | Remove animation entirely |
| Duration > 300ms on UI element | Reduce to 150-250ms |
| Hover animation without media query | Add `@media (hover: hover) and (pointer: fine)` |
| Keyframes on rapidly-triggered element | Use CSS transitions for interruptibility |
| Framer Motion `x`/`y` props under load | Use `transform: "translateX()"` for hardware acceleration |
| Same enter/exit transition speed | Make exit faster than enter (e.g., enter 300ms, exit 150ms) |
| Elements all appear at once | Add stagger delay (30-80ms between items) — see craft.md |
| Built-in CSS easing on entering/exiting elements | Use custom cubic-bezier, e.g. `cubic-bezier(0.23, 1, 0.32, 1)` — `ease` is acceptable for hover/color changes |
| State icon just appears/disappears | Cross-fade both states with `scale: 0.25 -> 1`, `opacity: 0 -> 1`, `blur: 4px -> 0px` |

---

## Agentation-Driven Animation Review

When running in watch mode (loop on `agentation_watch_annotations`):

- **Blocking** severity → acknowledge → fix → add Before/After/Why table entry → resolve with summary
- **Important** severity → acknowledge → fix → resolve with summary (no table entry required)
- **Suggestion** severity → inline fix only, no acknowledgement needed

```
agentation_resolve(id, "Changed transition: all 300ms → transform 200ms cubic-bezier(0.23,1,0.32,1)")
```
