# Dashboard Blade Gotchas

Use when `design:blade` is handling Razorpay Dashboard surfaces. These are implementation traps observed in dashboard apps; keep them inside Blade so other skills route here instead of duplicating Blade rules.

## Card Layout

**Cards in a grid are different heights**
- Symptom: Cards in a grid do not match height; content inside jumps around.
- Cause: `CardBody` has no default height, breaking percentage-height children.
- Fix: Set `height="100%"` on `Card`, `CardBody`, and inner `Box`; use `flexGrow={1}` only on the body region.

**Custom content inside CardFooterLeading or CardFooterTrailing is invisible**
- Symptom: Logos, icons, or badges placed inside `CardFooter` slots do not appear.
- Cause: These Blade components only accept specific props such as `title`, `subtitle`, and `actions`; arbitrary JSX children are discarded.
- Fix: Remove `CardFooter`. Add a footer strip as a `Box` with `borderTopWidth="thin"` inside `CardBody`, in a flex-column layout.

**Footer Box placed after CardBody breaks card layout**
- Symptom: Card visually breaks; footer appears outside or collapses.
- Cause: The footer `Box` was placed after `</CardBody>`; it must be a child of `CardBody`.
- Fix: Use `<CardBody><Box flexDirection="column"><Box flexGrow={1}>{body}</Box><Box borderTopWidth="thin">{footer}</Box></Box></CardBody>`.

**CardFooter content not rendered in tests**
- Symptom: Test assertions on footer content fail because elements are not found.
- Cause: Blade `CardFooter` does not render arbitrary children in Jest for non-interactive cards.
- Fix: Avoid testing `CardFooter` custom content. Test the data flow, or use the in-`CardBody` footer pattern above.

## Component Quirks

**Inline styles on a Blade Box have no visible effect**
- Symptom: `style={{ background: 'linear-gradient(...)' }}` on a Blade `Box` does not render.
- Cause: Blade `Box` does not forward the React `style` prop to the DOM element.
- Fix: Use Blade props when possible. For CSS values Blade cannot express, use a plain DOM element locally and keep the custom CSS minimal.

**CheckCircleIcon causes an import error or is missing at runtime**
- Symptom: Import fails or the icon does not render.
- Cause: `CheckCircleIcon` is not available in the pinned Dashboard Blade version.
- Fix: Use `CheckIcon`. Before using an icon, verify by searching existing usage in the app.

**ChipGroup shows no chip selected even when state is set**
- Symptom: State has the right value but no chip appears selected.
- Cause: Passing `value=""` for an "all" state means no chip's `value` attribute matches.
- Fix: Add an explicit `<Chip value="all">All</Chip>` and always pass `value={selectedCategory}`.

**Two-column wizard modal has wrong padding**
- Symptom: Modal sidebar is pushed in or spaced incorrectly.
- Cause: Blade `ModalBody` defaults to `padding="spacing.6"`, which fights split layouts.
- Fix: Use `ModalBody padding="spacing.0"` for two-column layouts. The split itself is a `Box display="flex" height="100%"` with a fixed left sidebar and flexible right content.

**useToast is undefined when imported from the app's hooks**
- Symptom: `useToast()` throws or is undefined.
- Cause: `useToast` lives in Blade, not a local hooks wrapper.
- Fix: Import `useToast` from `@razorpay/blade/components`.

**Blade Modal content cannot be found in tests**
- Symptom: Test assertion on modal content fails because the element is not found in the render container.
- Cause: Blade Modal portals its DOM to `document.body`.
- Fix: Use `screen.getByText()` or `screen.getByRole()` so the query searches the full document.

## Navigation

**Clicking a Blade tab causes a full page reload**
- Symptom: Tab click reloads the full page instead of updating the view.
- Cause: Blade `TabItem.href` renders a plain anchor, which triggers a full reload in Module Federation.
- Fix: Use the app's router-link wrapper pattern for tabs, such as `TabItemRouterLink` with `useLinkClickHandler`.

## Testing

**Blade components throw `Cannot read properties of undefined (reading 'fonts')` in tests**
- Symptom: Tests fail with a Blade provider error.
- Cause: Rendering with `@testing-library/react` directly skips the app's providers.
- Fix: Import `render` from the project's Jest utilities so BladeProvider, MemoryRouter, and QueryClientProvider are present.

**Jest fails to parse ESM module on Blade import**
- Symptom: `SyntaxError: Cannot use import statement in a module` appears for a Blade dependency.
- Cause: A Blade dependency is ESM-only and the app's Jest transformer cannot parse it.
- Fix: Follow the app's existing Jest setup pattern for mocking/transpiling that dependency before Blade imports.
