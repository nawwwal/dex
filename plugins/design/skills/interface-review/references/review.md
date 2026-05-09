# Design Review

Read-only interface critique for static artifacts: screenshots, diffs, local files, Figma frames already available in context, or product descriptions.

## Route Out First

- Live URL, localhost, screenshots, clicking, page state, or authenticated capture: route to `agent-browser`.
- Razorpay Blade score, Blade coverage, Blade component choice, or Blade migration: route to `design:blade`.
- Motion timing, easing, transitions, or animation implementation: route to `web-animation-design`.
- General "make it feel better" polish: route to `make-interfaces-feel-better`.

## Review Checks

- Hierarchy: primary action, dominant content, secondary actions, and de-emphasized metadata are visually distinct.
- Density: dashboard/table/form surfaces preserve scan speed; marketing/editorial surfaces can use larger rhythm.
- State coverage: empty, loading, error, disabled, permission, partial-data, and long-content states are represented.
- Layout: spacing is systematic, alignment is consistent, and responsive constraints are explicit.
- Typography: scale, line length, line-height, wrapping, and numeric alignment support the surface.
- Copy: labels, errors, empty states, and CTAs tell the user what happened and what to do next.
- Accessibility: run `references/a11y.md` for WCAG floors.

## Output

Lead with the biggest flaw and name the weak joint.

```text
## Interface Review: {target}

### Critical
- [area/file] Problem: what breaks. Mechanic: why it breaks. Fix: exact change.

### High
- ...

### Passed
- ...

### Not checked
- [evidence missing, for example live page capture or Blade gate]
```

Do not output a numeric score unless a named rubric or tool produced it.
