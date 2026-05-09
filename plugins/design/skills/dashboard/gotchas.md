# Dashboard Gotchas Library

Internal reference for dashboard workflows. Loaded at the start of build and fix phases.

Use this as a trigger-based warning system for non-Blade dashboard issues. Anything about Blade components, Blade Score, Blade coverage, Blade tokens, or Blade implementation quirks must route to `design:blade`.

This file is read-only during dashboard work. Do not append, propose, or maintain new entries from the dashboard skill.

## Navigation And Routing

*Trigger: writing tab navigation, back buttons, or route handling*

**Back navigation button looks inconsistent with the rest of the dashboard**
- Symptom: A plain button with a chevron icon is used for back navigation.
- Cause: The dashboard uses breadcrumb-style page navigation, not a loose button.
- Fix: Use the existing breadcrumb/back-navigation pattern in the app.

**Tab switches cause the layout component to flash or lose state**
- Symptom: Layout remounts on every tab switch; local state resets; flicker is visible.
- Cause: Separate route entries per tab cause React Router to unmount and remount the parent.
- Fix: Use a single `:tab` param route so tab switches are re-renders, not remounts.

**useMatch() returns null inside a micro-app**
- Symptom: `useMatch('/app/...')` returns null when it should match.
- Cause: The micro-app may not see the full absolute path in Module Federation's routing context.
- Fix: Use `useParams()` for the matched segment.

## API And Data

*Trigger: writing API calls, data display, or data transformation*

**Shell's API helper goes to the wrong URL for a custom backend**
- Symptom: API calls fail or go to the wrong endpoint when using shell's built-in helper.
- Cause: The shell helper prepends a fixed merchant API path.
- Fix: Create the app's own fetch/axios instance for custom backends.

**Date comparison or display shows dates in 1970**
- Symptom: Timestamps render as 1970 dates, or comparisons are wrong.
- Cause: The API returns Unix timestamps in seconds; JavaScript `Date` expects milliseconds.
- Fix: Multiply API timestamps by 1000 before constructing a Date.

**PATCHing an item's settings removes other settings**
- Symptom: After a PATCH, fields not included in the update disappear.
- Cause: Sending partial metadata clobbers omitted fields.
- Fix: Deep-copy the existing metadata object, update the specific field, and send the complete copy.

**Display name shows the wrong value**
- Symptom: UI shows a machine slug instead of a readable name.
- Cause: Code uses the machine `name` instead of display metadata.
- Fix: Use the human-readable display metadata for user-facing text.

**A feature action button shows the wrong state**
- Symptom: "Install" appears for an active feature, or "Manage" appears for a deactivated one.
- Cause: CTA state is derived only from subscription presence.
- Fix: Distinguish no subscription, inactive subscription, and active subscription explicitly.

## Testing

*Trigger: writing any test file*

**jest.spyOn on an authentication check function does not intercept calls**
- Symptom: Mocking the function does not change behavior in tests.
- Cause: The implementation reads a global directly, so spying the import does not intercept the read.
- Fix: Set the relevant global value directly in test setup.

**TypeScript errors appear in test fixture files after a change**
- Symptom: `tsc --noEmit` reports errors in test files that Jest ignored.
- Cause: Pre-existing test fixture types are caught by TypeScript but not by Jest's transpilation path.
- Fix: Confirm whether they are pre-existing before treating them as regressions.

## Pre-PR Checklist

*Trigger: any session nearing the review/PR stage*

**Dev-only component ships in a PR**
- Symptom: A development-only debugging component appears in production-bound app code.
- Cause: Local instrumentation was left mounted.
- Fix: Remove the debug import and JSX before opening any PR. Route Agentation workflows to `agentation`.

**Developer-only header appears in JavaScript code**
- Symptom: PR review flags a local development header inside application JavaScript.
- Cause: The header was injected in app code instead of local tooling.
- Fix: Remove it from application JavaScript; keep it in local browser/server development tooling.

**Upgrading axios in one app breaks the monorepo**
- Symptom: Package version conflicts or CI failures appear after an app-local axios upgrade.
- Cause: The monorepo pins axios consistently across apps.
- Fix: Do not upgrade axios in a single app. Security fixes require coordinated monorepo work.
