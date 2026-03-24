# Dashboard Gotchas Library

Internal reference for Claude — not shown to designers. Loaded at the start of build and fix phases.

Use this as a trigger-based warning system. Before writing any code that matches a trigger category below, warn the designer in plain language and use the correct approach automatically.

When you discover a new issue not already here: append it under the relevant group in this format:
```
**[Plain title of the symptom]**
- Symptom: [what the designer sees]
- Cause: [why it happens, 1 sentence]
- Fix: [what to do instead]
```

---

## Group 1 — Blade Card Layout
*Trigger: writing any Card, CardBody, CardFooter component*

**Cards in a grid are different heights — flex layout breaks inside**
- Symptom: Cards in a grid don't match height; content inside jumps around
- Cause: `CardBody` has no default height, breaking percentage-height children
- Fix: Set `height="100%"` explicitly on `Card` → `CardBody` → inner `Box`; use `flexGrow={1}` only on the body region

**Custom content inside CardFooterLeading or CardFooterTrailing is invisible**
- Symptom: Logos, icons, or badges placed inside `CardFooter` slots don't appear
- Cause: These Blade components only accept specific props (`title`, `subtitle`, `actions`) — arbitrary JSX children are silently discarded
- Fix: Remove `CardFooter` entirely. Add a footer strip as a `Box` with `borderTopWidth="thin"` inside `CardBody`, in a flex-column layout

**Footer Box placed after CardBody breaks card layout**
- Symptom: Card visually breaks; footer appears outside or collapses
- Cause: The footer Box was placed after `</CardBody>` — it must be a child of `CardBody`
- Fix: Pattern is `<CardBody><Box flexDirection="column"><Box flexGrow={1}>{body}</Box><Box borderTopWidth="thin">{footer}</Box></Box></CardBody>`

**CardFooter content not rendered in tests**
- Symptom: Test assertions on footer content fail — elements not found
- Cause: Blade's CardFooter doesn't render children in Jest for non-interactive cards
- Fix: Don't test CardFooter content. Test the underlying data flow. Also switch to the in-CardBody footer pattern above.

---

## Group 2 — Blade Style and Component Quirks
*Trigger: writing Blade components with styles or specific quirks*

**Inline styles on a Blade Box have no visible effect**
- Symptom: `style={{ background: 'linear-gradient(...)' }}` on a Blade `Box` — nothing renders
- Cause: Blade `Box` does not forward the React `style` prop to the DOM element
- Fix: Use a plain `<div style={{...}}>` for any CSS values Blade can't express (gradients, computed colors). This is the documented exception.

**CheckCircleIcon causes an import error or is missing at runtime**
- Symptom: Import fails or icon doesn't render
- Cause: `CheckCircleIcon` doesn't exist in the Blade version pinned by this dashboard
- Fix: Use `CheckIcon`. Before using any icon, verify by searching existing usage in the codebase.

**ChipGroup shows no chip selected even when state is set**
- Symptom: State has the right value but no chip appears selected in the UI
- Cause: Passing `value=""` when "all" is selected means no chip's `value` attribute matches
- Fix: Add an explicit `<Chip value="all">All</Chip>` and always pass `value={selectedCategory}` — even when the value is "all"

**Two-column wizard modal has wrong padding / layout misalignment**
- Symptom: CreationView modal sidebar is pushed in or spaced incorrectly
- Cause: Blade `ModalBody` defaults to `padding="spacing.6"` which fights the two-column split layout
- Fix: Always use `ModalBody padding="spacing.0"` for two-column layouts. The split itself is a plain `Box display="flex" height="100%"` — left sidebar (fixed width, `borderRight`) + right content (`flex={1}`, `overflowY="auto"`)

**useToast is undefined when imported from the app's hooks**
- Symptom: `useToast()` throws or is undefined
- Cause: `useToast` lives in Blade itself, not in a local hooks wrapper
- Fix: `import { useToast } from '@razorpay/blade/components'` directly

**Blade Modal content can't be found in tests**
- Symptom: Test assertion on modal content fails — element not found in container
- Cause: Blade Modal portals its DOM to `document.body`, outside the test render container
- Fix: Use `screen.getByText()` or `screen.getByRole()` — these search the full document

---

## Group 3 — Navigation and Routing
*Trigger: writing tab navigation, back buttons, or route handling*

**Back navigation button looks inconsistent with the rest of the dashboard**
- Symptom: A plain button with a chevron icon is used for back navigation
- Cause: The dashboard uses `Breadcrumb` + `BreadcrumbItem` for page-level back navigation, not a button
- Fix: Use `BreadcrumbItem href="#"` with `onClick={(e) => { e.preventDefault(); navigate('...'); }}`. Last item gets `isCurrentPage`.

**Clicking a tab causes a full page reload instead of smooth navigation**
- Symptom: Tab click reloads the entire page instead of just updating the view
- Cause: Blade `TabItem.href` renders a plain `<a>` tag, which triggers a full reload in Module Federation
- Fix: Use a `TabItemRouterLink` wrapper (from recon-saas) with `useLinkClickHandler`

**Tab switches cause the layout component to flash or lose state**
- Symptom: Layout remounts on every tab switch; local state resets; flicker visible
- Cause: Separate `<Route>` entries per tab cause React Router to unmount and remount the parent
- Fix: Use a single `:tab` param route (e.g. `/agent-marketplace/:tab`). Tab switches are re-renders, not remounts.

**useMatch() returns null inside a micro-app**
- Symptom: `useMatch('/app/agent-marketplace/...')` returns null when it should match
- Cause: The micro-app may not see the full absolute path in Module Federation's routing context
- Fix: Use `useParams()` instead — it reads the matched segment directly and is reliable inside micro-apps

---

## Group 4 — API and Data
*Trigger: writing API calls, data display, or data transformation*

**Shell's API helper goes to the wrong URL for a custom backend**
- Symptom: API calls fail or go to the wrong endpoint when using shell's built-in helper
- Cause: The shell's `rest-fetch` prepends `/merchant/api/{mode}/` — it can't be overridden
- Fix: Create your own axios instance (e.g. `nexus-fetch.ts`). Don't use the shell's helper for custom backends.

**Date comparison or display shows dates in 1970**
- Symptom: Timestamps render as 1970 dates, or comparisons are wildly wrong
- Cause: The API returns Unix timestamps in seconds; JavaScript's Date expects milliseconds
- Fix: Always multiply API timestamps by 1000: `new Date(timestamp * 1000)`

**PATCHing an item's settings removes other settings**
- Symptom: After a PATCH, some fields that weren't part of the update disappear
- Cause: Sending partial metadata clobbers any fields not included in the payload
- Fix: Deep-copy the entire existing metadata object first, then update the specific field, then send the complete copy

**Display name shows the wrong value (slug instead of readable name)**
- Symptom: UI shows `dispute-auto-responder` instead of "Dispute Auto-Responder"
- Cause: `skill.name` is the machine slug, not the human-readable name
- Fix: Always use `skill.metadata.display_name` for any text shown to users

**A feature's action button shows the wrong state**
- Symptom: "Install" button shows for an active feature, or "Manage" shows for a deactivated one
- Cause: CTA state derived only from subscription presence, missing the `is_active` check
- Fix: Three states — Install (no subscription), Reactivate (`is_active === false`), Manage (active subscription). Check `is_active` explicitly.

---

## Group 5 — Testing
*Trigger: writing any test file*

**Blade components throw "Cannot read properties of undefined (reading 'fonts')" in tests**
- Symptom: Tests fail with a Blade provider error on any component using Blade
- Cause: Using `render` from `@testing-library/react` directly — it's not wrapped with BladeProvider, MemoryRouter, or QueryClientProvider
- Fix: Always import `render` from the project's `jest-utils.tsx`, which includes all three providers

**Jest fails to parse ESM module on any Blade import**
- Symptom: "SyntaxError: Cannot use import statement in a module" on any file importing Blade 12.81.1 GenUI
- Cause: `react-markdown` (a Blade dependency) is ESM-only; Jest's transformer can't handle it
- Fix: Add `jest.mock('react-markdown', ...)` in `jest-setup.ts` before any Blade imports

**jest.spyOn on an authentication check function doesn't intercept calls**
- Symptom: Mocking the function doesn't change behavior in tests
- Cause: The function reads `window.is_token_based_authentication` directly; spying the import doesn't intercept that read
- Fix: Set `window.is_token_based_authentication = value` directly in the test setup

**TypeScript errors appear in test fixture files after a change**
- Symptom: `tsc --noEmit` reports errors in test files — `never[]`, type mismatches
- Cause: Pre-existing type errors in test fixtures that Jest ignores (transpiles with Babel/SWC) but `tsc` catches
- Fix: These are pre-existing. Don't treat them as regressions from your change.

---

## Group 6 — Pre-PR Checklist
*Trigger: any session nearing the review/PR stage*

**Dev-only component ships in a PR**
- Symptom: `<Agentation />` appears in `src/App.tsx` — it's marked `// TODO: remove before push`
- Cause: A development-only debugging tool left in production-bound code
- Fix: Remove both the `import { Agentation }` line and the `<Agentation />` JSX before opening any PR

**Developer-only header appears in JavaScript code**
- Symptom: PR review comment: "this header should not be in JS"
- Cause: `rzpctx-dev-serve-user` was injected in the app's API client code
- Fix: This header must only be set by the Mod Header browser extension (local dev) or by the shell server-side. Remove it from application JavaScript entirely.

**Upgrading axios in one app breaks the monorepo**
- Symptom: pnpm version conflicts; CI fails after upgrading axios
- Cause: All apps pin `axios@0.21.1`. A solo per-app upgrade breaks the shared convention
- Fix: Don't upgrade axios in a single app. Security fixes require a coordinated upgrade across the entire monorepo.

---

*This file grows automatically. When Claude discovers a new pattern during a build or fix session, it appends a new entry here and notes: "Added to shared library."*
