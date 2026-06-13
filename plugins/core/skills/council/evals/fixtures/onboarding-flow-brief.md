# Onboarding Flow Design Critique Brief

**Product:** Ledgerly — SMB invoicing and payouts for Indian freelancers  
**Surface:** First-run onboarding (web, mobile web parity required)  
**Stage:** Pre-build critique; Figma flows exist, no code shipped  
**Requested output:** Design critique with prioritized fixes before eng handoff

## Context

We are redesigning onboarding from a single long form into a three-step wizard:

1. **Account basics** — email, business name, GSTIN (optional)
2. **Bank verification** — IFSC + account number, penny-drop confirmation
3. **First invoice** — template picker, one line item, send or save draft

The goal is activation: user reaches "first invoice sent or saved" within one session. Current baseline completion is 34%; target is 55% within 60 days of launch.

## What we need reviewed

- Step order and cognitive load across the three steps
- Trust signals during bank verification (users abandon here most)
- Copy tone: we oscillate between "friendly startup" and "compliance-heavy fintech"
- Error states for failed penny-drop and invalid GSTIN
- Whether step 3 belongs in onboarding or should defer to dashboard empty state

## Known trust issues

- Users ask "why do you need my bank account before I've sent an invoice?" in support tickets
- No visible security badges or regulator mention until step 2 footer
- Penny-drop failure copy says "Verification failed" with no retry guidance
- We show Razorpay partnership logo only on marketing site, not in-product

## Copy problems (current draft)

| Location | Current copy | Concern |
|----------|--------------|---------|
| Step 1 subtitle | "Let's get you paid faster" | Vague; doesn't set expectation for bank step |
| Step 2 headline | "Connect your account" | Sounds like OAuth; users expect UPI linking |
| Step 2 helper | "We use bank-grade encryption" | Generic; no specifics |
| Step 3 CTA | "Finish setup" | Doesn't communicate value of first invoice |
| Global error | "Something went wrong" | Used for network, validation, and KYC reject |

## Constraints

- Cannot remove bank verification from onboarding; payouts require verified account
- GSTIN remains optional but strongly encouraged for B2B users
- Mobile web must work without native app; no biometric shortcuts yet
- Legal has approved penny-drop flow; cannot change verification vendor this quarter

## Artifacts available

- Figma link: `ledgerly-onboarding-v3` (3 frames + mobile variants)
- Support ticket export: 142 tickets tagged `onboarding-abandon` (last 90 days)
- Analytics funnel: step-level drop-off from Mixpanel

## Open questions for reviewers

1. Should bank verification move after first invoice draft to reduce early friction?
2. Is three steps the right mental model, or should we collapse 1+2?
3. What trust pattern (social proof, regulator, explainer video) fits step 2 without clutter?
