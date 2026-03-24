# Phase 2: Building a Feature

The designer is building UI. Do the research automatically before writing any code. Surface decisions that require design judgment.

## Before writing any component

For every new component or page, in this order:

**1. Find what already exists**
Search in this order: (1) the current app itself, (2) libs/shared-ui and libs/shared-utils, (3) apps/shell, (4) web/js/merchant (legacy dashboard components), (5) exemplar apps: money-saver, agentic-dashboard, pos, digital-bills, recon-saas.

If a close match exists:
> "I found something similar — [plain description of what it is, no file path]. Should I start from that and adapt it, or build fresh?"

Only ask this if the match is genuinely usable. If no close match: just proceed.

**2. Check Blade MCP first**
Before writing any UI element, query Blade MCP. Tell the designer in plain terms what you chose and proceed — only pause to ask when there are genuinely two valid UX directions that the designer should decide between:
> "I'm using a Blade [component name] for this — [plain description]. Proceeding."

Only ask "Want me to proceed?" when the Blade component choice requires a real design decision (e.g., card vs. list layout, modal vs. drawer). Don't ask for every routine component selection.

**3. Ask about the data source**
> "Does the backend API for this data already work on devstack, or do you need placeholder data while it's being built?"
- If not ready: automatically set up placeholder data mode (isMockMode pattern). Tell them: "I'll set this up to use placeholder data for now. Before you share with the team, I'll help you switch it to real data."

## Proactive gotcha warnings

Read [gotchas.md](../gotchas.md) at the start of this phase. Before writing any code that matches a known gotcha trigger, warn the designer in plain language and use the correct approach automatically. Never just write the broken version and explain later.

Examples of how to warn:
- About to write a Card with footer content → "A quick note: Blade Cards have a quirk with footer content. I'll use a slightly different approach that looks identical but works reliably."
- About to write dynamic CSS on a Blade component → "Blade components don't support inline CSS the usual way, so I'll use a plain HTML element for this specific style effect."
- About to write a Tab with a link → "Blade tab links need a special wrapper to work correctly in the dashboard without causing a full page reload. I'll handle that."

## During implementation

- Implement one component at a time
- After each component: briefly describe what was built in plain English
- If something doesn't work as expected: describe the problem without technical terms, propose one fix

## Self-updating gotchas

After resolving any unexpected issue:
1. Check if the pattern is already in gotchas.md
2. If not: append it automatically (trigger, symptom, fix)
3. Tell the designer: "I've added this to the shared gotchas library so future designers won't hit the same thing."
