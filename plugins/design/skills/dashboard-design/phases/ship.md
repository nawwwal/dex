# Phase 5: Shipping to Real Users

The designer wants their feature to go live. They can't own the canary deployment — that's the developer buddy's job. Claude's role is to prepare everything so the handoff is clean.

## Step 1: Pre-ship gate

Ask the designer to confirm each of these:
> "Before we get to shipping, let's check the gates:
> 1. Has your PM confirmed the feature is ready?
> 2. Has your EM signed off?
> 3. Has your developer buddy reviewed and signed off on devstack?
> 4. Is the PR merged?"

If any gate is not confirmed: don't proceed. Tell them clearly what's missing and who to reach out to.

## Step 2: Rollout plan (for the developer buddy)

First ask: "Is this feature gated behind a Splitz experiment, or does it go directly to all users once it's merged?"

**If Splitz-gated (most common for new features):**
Explain:
> "With Splitz, the feature starts with a small % of users and expands gradually. Your developer buddy owns the Splitz config — you just need to give them the plan."

Ask:
1. "What % of users should it start with? (Usually 1% — your EM can advise if different)"
2. "If something goes wrong, what should trigger a rollback? (e.g. 'users can't complete checkout', 'error alerts fire')"
3. "Who monitors this? (Your developer buddy will watch for errors — ask them what metrics they'll track)"

Generate handoff document:
```
Rollout Plan — [Feature Name]
Mechanism: Splitz experiment
Start: [X]% of merchants
Rollback trigger: [condition the designer provided]
Rollback action: Set Splitz to 0% — developer buddy: [name]
Monitoring: Developer buddy to confirm what metrics they'll watch
When to expand: Check with [designer name] and [PM name] before next cohort
Ops/Support comms: Done (sent by [designer name])
```

**If direct rollout (no Splitz):**
Ask:
1. "If something breaks after it goes live, what would you or support notice first? (e.g. users can't load the page, checkout fails, support tickets spike)"
2. "Who should your developer buddy contact to declare a rollback — just you, or also your PM/EM?"

Then generate the handoff:
```
Rollout — [Feature Name]
Mechanism: Direct (no Splitz gate)
Rollback: Revert the merged PR — developer buddy: [name]
Rollback trigger: [condition the designer gave in question 1]
Alert: [person(s) the designer named in question 2]
Monitoring: Developer buddy to confirm what to watch
```

**If gated/access-restricted feature (not visible with a normal test account):**
Note this explicitly in the handoff:
```
Access note: Feature is gated by [permission/account type/whitelist]
To verify after rollout: Use a test account with [access type] — ask your developer buddy for one
```

## Step 3: Ops comms

Generate the Slack message for Ops and Support:

```
Hey team — [Feature name] is going live today starting with [X]% of merchants.

What it is: [2-sentence description of the feature in user-facing terms]
Who sees it first: [X]% of merchants — starting today
What to watch for: [potential questions or issues support might see]
Who to contact if something's wrong: [developer buddy name] or [designer name]
```

Ask: "Who should I address this to in Slack?" and "Is there a specific Ops/Support channel?" If they don't know, remind them to ask their PM.

## Step 4: Post-launch verification

After the canary starts (developer buddy handles this), verification depends on the rollout type:

**If direct rollout (no gating):**
> "To check if it's live:
> 1. Open the dashboard in a private window (no Mod Header needed)
> 2. Log in with a test account
> 3. Navigate to [feature URL]
> You should see the feature."

**If Splitz-gated (percentage rollout):**
> "With a percentage rollout, not everyone will see the feature yet — your developer buddy is monitoring whether the right % of users are receiving it. To verify yourself, ask your developer buddy for a test account that's in the experiment's treatment group, or for a Splitz override URL that forces the feature on. Opening a random test account may not show the feature."

Ask your developer buddy: "Can you share a test account or a URL override I can use to verify the feature is live for the users who should see it?"

## Step 5: Done criteria

Tell the designer what "done" looks like:
> "You're done when:
> - The feature has rolled out to 100% of the target segment
> - No rollback happened in the first 48 hours
> - Your PM has confirmed
> - You've closed your DevRev issue
> - Support hasn't flagged anything unusual"
