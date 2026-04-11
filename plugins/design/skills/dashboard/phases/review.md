# Phase 4: Opening a PR for Code Review

The designer wants to submit their changes for code review.

## Step 1: Pre-PR check (automatic)

Before generating the PR description, silently check:
1. Are there any obvious issues in the code? (dev-only component left in, wrong header injection)
2. Is placeholder data mode off everywhere?
3. Are any developer log statements still in production paths?

If issues found, fix them silently or ask the designer first depending on severity.

## Step 2: Collect PR info from the designer

Ask only what you can't determine automatically:

1. **Blade Score:** "What's your Blade Score? Run the Blade Coverage extension on devstack and tell me the % — it's shown in the extension panel."
2. **Change summary:** "Describe what changed in 2 sentences — what it does and why it matters."
3. **Screenshots:** "Do you have before/after screenshots? You can paste images here, describe the changes visually, or I can note 'screenshots to follow'."

Everything else (branch name, files changed, testing steps) Claude determines automatically.

## Step 3: Generate PR description

Write the PR description with:
- Summary (2-3 sentences from what designer told you)
- What reviewers should check (based on what changed)
- Testing steps (how to verify the feature on devstack — step by step)
- Blade Score
- Screenshots section
- Pre-merge checklist

## Step 4: Check automated checks status

Check if automated checks are passing. If not:
> "The automated checks are still running / have some issues. I'd recommend waiting until they're green before requesting review. Want me to check again in a few minutes?"

## Step 5: Assign reviewers

Ask: "Who should review this?" If they don't know: suggest their developer buddy as the default technical reviewer, and their EM or design lead for design sign-off.

## What reviewers will look for (know this proactively)

- Blade Score must be 95% or above
- Before/after screenshots for every visual change
- Developer-only headers must not appear in JavaScript code
- Test coverage for new interactive components
- All automated checks green before merging
