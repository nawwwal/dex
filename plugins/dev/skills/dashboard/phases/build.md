# Phase 2: Building a Feature

The designer is building UI. Do the research automatically before writing any code. Surface decisions that require design judgment.

## Before writing any component

For every new component or page, in this order:

**1. Find what already exists**
Search in this order: (1) the current app itself, (2) libs/shared-ui and libs/shared-utils, (3) apps/shell, (4) web/js/merchant (legacy dashboard components), (5) exemplar apps: money-saver, agentic-dashboard, pos, digital-bills, recon-saas.

If a close match exists:
> "I found something similar — [plain description of what it is, no file path]. Should I start from that and adapt it, or build fresh?"

Only ask this if the match is genuinely usable. If no close match: just proceed.

**2. Route Blade checks to design:blade**
Before writing any UI element, use `design:blade` for Blade component choice, Blade coverage, Blade Score, and Razorpay design-system adherence. Tell the designer in plain terms what you chose and proceed — only pause to ask when there are genuinely two valid UX directions that the designer should decide between:
> "I'm using a Blade [component name] for this — [plain description]. Proceeding."

Only ask "Want me to proceed?" when the Blade component choice requires a real design decision (e.g., card vs. list layout, modal vs. drawer). Don't ask for every routine component selection.

**3. Ask about the data source**
> "Does the backend API for this data already work on devstack, or do you need placeholder data while it's being built?"
- If not ready: automatically set up placeholder data mode (isMockMode pattern). Tell them: "I'll set this up to use placeholder data for now. Before you share with the team, I'll help you switch it to real data."

## Proactive gotcha warnings

Read [gotchas.md](../gotchas.md) at the start of this phase. Before writing any code that matches a known gotcha trigger, warn the designer in plain language and use the correct approach automatically. Never just write the broken version and explain later.

Examples of how to warn:
- About to write a known dashboard routing pattern → "A quick note: this screen has a navigation pattern that can reset state if built the usual way. I'll use the stable dashboard pattern."
- About to write a custom backend call → "A quick note: the dashboard's default API helper may not work for this backend. I'll use the app-specific request path."
- About to write tests around authentication state → "A quick note: this check reads the browser state directly in tests. I'll set that state in the test setup."

## During implementation

- Implement one component at a time
- After each component: briefly describe what was built in plain English and include file references for the code changed
- If something doesn't work as expected: describe the problem without technical terms, propose one fix

## Gotcha maintenance

Gotchas are read-only in this phase. Do not append or propose new entries.
