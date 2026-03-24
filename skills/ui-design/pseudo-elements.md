# CSS Pseudo-elements

## ::before and ::after Basics

- Both require the `content` property (even `content: ""` for decorative use)
- Parent element needs `position: relative` for z-index stacking to work
- `z-index: -1` to place pseudo behind text or content

Use pseudo-elements for decoration over extra DOM nodes — they keep markup clean and don't affect accessibility trees.

## Negative Inset for Hit Target Expansion

Expand the clickable area of small elements without changing visual size:

```css
.small-button {
  position: relative;
}
.small-button::before {
  content: "";
  position: absolute;
  inset: -8px; /* expands hit target 8px in all directions */
}
```

This satisfies Fitts's Law (44px WCAG target) without inflating the visual design.

---

## View Transitions API

### view-transition-name Is Required

Every element you want to animate across a page transition needs a unique `view-transition-name`:

```css
.hero-image {
  view-transition-name: hero;
}
```

### Names Must Be Unique During Transition

Two elements cannot share the same `view-transition-name` at the same time. Use unique IDs in dynamic lists:

```css
.card {
  view-transition-name: var(--card-id); /* e.g. card-42 */
}
```

### Clean Up After Transition

Remove `view-transition-name` after the transition completes — stale names can cause layout issues on subsequent navigations:

```js
document.startViewTransition(() => {
  // swap DOM
}).finished.then(() => {
  el.style.viewTransitionName = 'none';
});
```

### Prefer View Transitions API Over JS Libraries

For page-to-page transitions (router navigation, tab switches), View Transitions API outperforms JS-based libraries: it's hardware-accelerated, handles screenshot capture automatically, and requires no third-party dependencies.

### Style ::view-transition-group for Custom Animations

```css
::view-transition-group(hero) {
  animation-duration: 0.5s;
  animation-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
}
```

---

## ::backdrop for Dialog Backgrounds

Use `::backdrop` instead of a custom overlay div for native dialog and popover elements:

```css
dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}
```

## ::placeholder for Input Styling

```css
input::placeholder {
  color: var(--text-subtle);
  font-style: italic;
}
```

## ::selection for Text Selection

```css
::selection {
  background: var(--brand-primary);
  color: white;
}
```

## ::marker for List Bullets

```css
li::marker {
  color: var(--brand-primary);
  font-size: 1.2em;
}
```

## ::first-line for Typographic Treatments

```css
p::first-line {
  font-variant: small-caps;
  letter-spacing: 0.05em;
}
```
