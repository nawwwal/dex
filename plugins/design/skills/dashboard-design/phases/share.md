# Phase 3: Sharing with the Team (devstack)

The designer wants to share their feature with the team on devstack so others can review it.

## Step 1: Dead UI audit (automatic, before deploying)

Silently scan all source files for:
1. Hardcoded strings that look like placeholder data (names, emails, example IDs, sample amounts)
2. Placeholder data mode still active (isMockMode returning true anywhere)
3. Developer log messages left in source files
4. Developer-only browser headers injected in JavaScript code (these should only be set in Mod Header, not in code)

**If issues found:**
> "Before I deploy, I found [N] things that need fixing:
> - [plain English description of each issue]
> Want me to fix them now?"

Fix automatically if they say yes. Never describe issues using technical terms — say "placeholder data is still showing" not "isMockMode() is returning true".

**If clean:**
Proceed to deployment without mentioning the audit.

## Step 2: Deploy to devstack

Use the `deploy-to-devstack` skill if available. If the skill is not installed or fails, fall back to the manual flow:
1. Push the branch to GitHub
2. Wait for the automated Docker build to go green (check GitHub Actions)
3. Run: `/deploy-to-devstack {commit-sha} label:{label-name}` in the Slack bot, OR ask your developer buddy to trigger the deployment
4. Wait for the second CI deployment action to complete

Handle the technical flow invisibly:
1. Check automated checks status (CI) — if not green, wait or flag
2. Trigger the deployment
3. Wait for it to complete

Ask only:
> "What label should I use for your test environment?" (used to identify which version to show — e.g. your name, feature name, or any short label)

## Step 3: Share access instructions

After deployment is complete, tell the designer exactly how to access it:

> "Your feature is live on devstack. To see it:
> 1. Open Chrome and go to: [URL]
> 2. Turn on Mod Header and add this header: [key] = [value]
> 3. You should see your feature at [specific path]
>
> To share with someone else, send them the same URL and header setup."

Never mention rzpctx-dev-serve-user by name — just tell them the key and value to enter.

## Step 4: If something doesn't show up

Check what went wrong automatically:
- Mod Header not set / wrong value → tell them what to check
- CI docker build not finished → wait and tell them
- App not connected to shell → check remotes config (invisible, fix silently)

Always give the designer an action, not a technical error.
