# Harden

Review production readiness for interface edge cases.

## Route Out First

- Razorpay Blade edge-state components, coverage, or component replacement: route to `blade`.
- Performance prefetching, routing architecture, or data-fetching strategy: route to the relevant engineering skill, not this skill.

## Checklist

### Text Overflow
- Long text cannot break layout; flex children use `min-width: 0` where needed.
- Truncation is intentional and has a tooltip or accessible full value.
- URLs and long IDs wrap or truncate deliberately.
- Numeric columns align consistently.
- Native browser wrapping is preserved unless truncation is a deliberate product choice.

### Forms And Native Controls
- Inputs, selects, buttons, links, dialogs, and media controls keep native behavior unless a full replacement is justified.
- Validation appears inline near the relevant field and does not depend only on toast feedback.
- Autocomplete, input modes, keyboard behavior, and submit behavior match the field's job.

### Internationalization
- Translations have 30-40% length budget when i18n is in scope.
- RTL-sensitive spacing uses logical properties.
- Number, currency, and date formatting uses `Intl` or project helpers.
- User-visible strings are localization-ready when the product requires it.

### Error Handling
- 4xx errors explain what the user can do.
- 5xx errors give a retry or recovery path.
- Offline/network failures have a visible state.
- Form validation appears inline near the relevant field.

### Empty And Loading States
- Empty table/list states are designed, not blank.
- Zero-result search shows the query and a clear reset action.
- Loading uses skeletons, spinners, or existing project patterns.
- Partial data states explain what is missing.

### Large Data
- Long lists use pagination or virtualization.
- Tables remain usable on narrow widths.
- Dense surfaces preserve row scan speed.

### Asset And Runtime Cost
- Critical content is not blocked by non-critical scripts or heavy style sheets.
- Imports are scanned before component internals; one-method third-party helpers are flagged as import/dependency findings when a platform API or small local helper can do the job.
- Images and media are sized, compressed, and lazy-loaded when they are not needed for first paint.
- Layout and animation avoid repeated DOM reflow from measuring and mutating in the same loop.
- New dependencies are justified by complexity, maintenance, accessibility, or browser support.

### Actions
- Submit buttons are disabled while requests are in flight.
- Optimistic updates have rollback or correction behavior.
- Destructive actions require confirmation or undo when appropriate.

## Output

```text
## Harden: {target}

### Critical
- [file:line] - [edge case] - Fix: [specific change]

### Warnings
- ...

### Not checked
- ...
```
