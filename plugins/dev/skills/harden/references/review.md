# Design Review

Read-only interface critique for static artifacts: screenshots, diffs, local files, Figma frames already available in context, or product descriptions.

## Route Out First

- Live URL, localhost, screenshots, clicking, page state, or authenticated capture: route to `agent-browser`.
- Razorpay Blade score, Blade coverage, Blade component choice, or Blade migration: route to `blade`.
- In Blade projects, motion timing, easing, transitions, hover/focus/tap, or animation implementation: route to `blade` first so Blade MCP and Blade-native motion own the API. Use generic motion guidance only after Blade proves a gap.
- General "make it feel better" polish: route to `make-interfaces-feel-better`.

## Review Checks

- Frontend substrate: native elements, CSS flow, cascade cost, and runtime weight support the interface before polish. Load `references/frontend-foundations.md` when the artifact includes HTML, CSS, JS, or component code.
- Hierarchy: primary action, dominant content, secondary actions, and de-emphasized metadata are visually distinct.
- Density: dashboard/table/form surfaces preserve scan speed; marketing/editorial surfaces can use larger rhythm.
- State coverage: empty, loading, error, disabled, permission, partial-data, and long-content states are represented.
- Layout: spacing is systematic, alignment is consistent, and responsive constraints are explicit.
- Typography: scale, line length, line-height, wrapping, and numeric alignment support the surface.
- Copy: labels, errors, empty states, and CTAs tell the user what happened and what to do next.
- Accessibility: run `references/a11y.md` for WCAG floors.
- Style terms: translate vague words such as `premium`, `clean`, or `modern` into `Term -> meaning -> execution -> avoid`; lead with structural, responsive, or cascade issues before color and decorative finish.

## Output

Lead with the biggest flaw and name the weak joint.

```text
## Harden: {target}

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
