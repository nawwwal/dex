# Design-to-Engineering Handoff Brief

**Team:** Ledgerly product trio (1 designer, 2 frontend, 1 backend) + fractional QA  
**Workflow:** Figma → Linear ticket → PR → staging QA → prod  
**Requested output:** Workflow audit — bottlenecks, handoff gaps, repeat churn

## Scenario

The onboarding redesign (three-step wizard) has been "ready for eng" for two weeks. Only step 1 is in staging. Design is frustrated; eng says specs are incomplete. This pattern repeats every sprint.

## Current handoff process

1. Designer completes Figma with `Ready for dev` label
2. Designer writes Linear ticket with Figma link and screen list
3. Eng lead slices tickets; devs implement against Figma inspect
4. Designer reviews staging via Loom or ad-hoc Slack ping
5. QA runs checklist (often written after first dev pass)
6. Fixes loop until designer approves in Slack thread

**Official doc:** Notion page "Design handoff checklist" — last updated 8 months ago  
**Actual behavior:** Slack DMs and Figma comments

## This sprint's friction (onboarding)

| Issue | Design view | Eng view |
|-------|-------------|----------|
| Bank step specs | "All states are in Figma" | Error states missing mobile breakpoints |
| Copy | Final in Figma | Legal strings not in ticket; dev used placeholders |
| Analytics events | "Obvious from flow" | Event schema doc never linked |
| Penny-drop loading | 3s animation designed | API timeout is 10s; no long-wait spec |
| Empty GSTIN path | Shown in user flow diagram | Not in Figma frames |

## Repeat churn patterns

- **Re-explaining interactions:** Designer walks through prototype in 30-min call every sprint
- **Reopened tickets:** "Pixel polish" tickets return after QA because acceptance criteria were visual-only
- **Duplicate comments:** Same spacing fix requested in Figma, Linear, and Slack
- **Late accessibility:** A11y audit happens post-merge; rework on focus order and aria labels
- **Design token drift:** Dev uses Tailwind defaults; design uses Figma variables with no code mapping

## Tooling landscape

| Tool | Purpose | Gap |
|------|---------|-----|
| Figma | Source of truth for UI | No code connect; devs don't use Dev Mode consistently |
| Linear | Tickets | No enforced template for handoff fields |
| Storybook | Component library | 40% coverage; onboarding uses one-off components |
| Chromatic | Visual regression | Not wired to CI for this repo |
| Notion | Process docs | Stale |

## What good looks like (team agreement, informal)

- Eng can implement without a walkthrough call
- All states (loading, empty, error, success) specified per screen
- Copy is in the ticket body, not only Figma
- Analytics event names agreed before PR opens
- Designer review is async with explicit pass/fail criteria

## Constraints

- Cannot hire dedicated design ops
- Designer time is 50% on new work, 50% on support/review
- Two-week sprint cycle; onboarding must ship this quarter
- Backend eng is shared with payments squad

## Metrics (rough)

- Average days from `Ready for dev` → staging: 12 (target: 5)
- Tickets reopened after "done": 34% last sprint
- Designer review cycles per feature: 2.8 average

## Questions for workflow council

1. Where is information lost between Figma → Linear → PR?
2. Which repeat churn steps should become templates, skills, or CI gates?
3. What is the minimum viable handoff artifact set for a squad this size?
4. Should design review move earlier (pre-PR storybook) or later (staging only)?

**Artifacts:** Linear `ONB-2024-redesign`, stale Notion handoff doc, `#eng-design` retro thread
