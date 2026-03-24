# Phase 1: Creating a New App

The designer wants to create a brand new section of the dashboard. Do all the technical work. Surface only decisions that require the designer's input.

## Step 1: Understand where it belongs

Ask only one question at a time. Start with:

> "Where should users find this feature in the dashboard?"
> **A)** It's its own major section — same level as Banking, Payments, or Engage (appears in the top navigation)
> **B)** It lives inside Payments — same area as Agent Studio, Transactions, or Settlements (appears in the left sidebar under Payments)
> **C)** I'm not sure — describe what the feature does and I'll suggest the right placement

If C: ask "In one sentence, what does this feature help the merchant do?" Then decide:
- If it's a standalone product with its own backend → top navigation (Option A)
- If it's a payments-related tool within the existing payments workflow → Payments sidebar (Option B)

## Step 2: Collect the basics

Ask these one at a time, in this order:

1. "What should the menu label say?" (e.g. "Agent Studio", "Tax Reports", "Shipping Hub")
2. "What short word or phrase should go in the URL? Use lowercase, hyphens are fine." (e.g. "agent-studio", "tax-reports")
3. "What's the app's short code name?" (usually the same as the URL, e.g. "agent-marketplace", "tax-reports") — if same as URL, confirm instead of asking

## Step 3: Do the technical work (invisible to designer)

Search the codebase to verify the integration state. Find the relevant files dynamically — don't assume specific file names, as the codebase evolves. Verify by observable behavior, not file paths.

**For Option A (Top navigation):**
Search for and verify:
1. The app has a lazy import in the shell's routing entry point (wherever top-level products like Engage, Banking are imported from)
2. The app's route is registered at the correct top-level URL path
3. The app appears in the shell's federation configuration alongside other top-level apps
4. The app has a port assigned in its build configuration
5. The app appears in the monorepo's lockfile package registry

**For Option B (Payments sidebar):**
Search for and verify:
1. The app has a lazy import in the Payments dashboard routing entry (wherever payments sub-items like Transactions, Settlements are registered)
2. The app's route is registered with the correct URL path and NOT wrapped with a workspace layout component
3. The app's display name appears in the sidebar's navigation constants alongside other Payments sidebar items
4. The app has route pattern matching configured for its URL (so the sidebar highlights the right item when you're on that page)
5. The app appears in the sidebar's product list for rendering (icon + access condition)
6. The app's remotes config includes the Shell

**For both patterns:**
If any of the above is missing: fix it by following the pattern of an adjacent app that's already working correctly. Don't guess — read how Transactions or Agent Studio is wired, then mirror it.

**After checking, run the clean install:**
`pnpm clean:nodemodules && pnpm install --ignore-scripts && pnpm nx reset`

## Step 4: Report back in plain language

Tell the designer what you checked and what the result is:

If everything is correct:
> "Your app is set up and wired into the [Payments sidebar / top navigation]. I verified all the connections and everything looks right. Your app should be reachable at: localhost:8888/app/[read the actual route path from the registered route config — never assume or guess it]"

If something needs fixing:
> "I found an issue: [describe the problem in plain English — never mention the file name]. I fixed it. Here's what was wrong and what I did..."

Never say: "ProductRouter.tsx was missing a lazy import" — say: "Your app wasn't connected to the top navigation. I've connected it now."
