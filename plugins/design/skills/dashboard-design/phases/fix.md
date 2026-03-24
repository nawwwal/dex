# Phase: Fixing or Improving Something Existing

The designer wants to fix a bug, improve a page, or add something to a feature that already exists. Find the code automatically — don't ask them for file names.

## Step 1: Understand what needs to change

Ask:
> "What page or feature are you working on?" (e.g. "the Payments home page", "the Agent Studio install flow", "the navigation bar")

Then:
> "What's wrong with it, or what do you want to change?"

Use these descriptions to find the relevant code. Map plain English → file locations:
- "Payments home page" / "payments dashboard" → web/js/merchant/
- "Agent Studio" / "agent marketplace" → apps/agent-marketplace/
- "Navigation" / "sidebar" / "menu" → web/js/merchant/components/NavigationLayout/ or SidebarV2/
- "Header" → apps/shell/src/client/components/Navigation/
- Any other app name → apps/[name]/

## Step 2: Read before changing

Always read the current implementation first. Understand:
- What the code currently does
- What is actually broken or suboptimal
- Whether the change is a small fix or requires structural work

## Step 3: Confirm with the designer

> "I found the relevant code for [what they described]. Here's what I'm going to change: [plain English description of the change — no file names]. Does that sound right?"

If the fix involves a design decision (two valid approaches), ask:
> "There are two ways to do this — [A in plain English] or [B in plain English]. Which fits better?"

## Step 4: Apply the change

Make the minimal, targeted change. Don't refactor unrelated code.

After applying:
> "Done. Here's what changed: [plain English summary]. [If relevant: You can verify this by doing X]"

Never surface:
- File paths
- Component internal details
- Raw error messages — translate them: "The Blade Card's footer doesn't support custom content the standard way. I used a slightly different approach that achieves the same visual result."

## Proactive gotcha warnings

Read [gotchas.md](../gotchas.md) before writing any code. When about to write something that matches a known gotcha trigger, warn in plain language and use the correct approach automatically.

## Self-updating gotchas

After resolving any unexpected issue:
1. Check if the pattern is already in gotchas.md
2. If not: append it automatically under the relevant group
3. Tell the designer: "I've added this to the shared library so future designers won't hit the same thing."
