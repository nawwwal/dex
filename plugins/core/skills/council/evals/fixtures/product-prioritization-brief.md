# Product Prioritization Brief: AI Recommendations vs Onboarding Fix

**Product:** Ledgerly  
**Decision owner:** Head of Product  
**Timeline:** Q2 planning; eng capacity is fixed at 2 squads (8 engineers)  
**Requested output:** Council perspectives on what to ship first and what to defer

## The tradeoff

We have two competing Q2 bets. We can fully staff one; the other gets at most one engineer for maintenance.

### Option A: AI-powered invoice recommendations

**Pitch:** Surface smart line items, due-date suggestions, and client payment-risk hints based on historical invoices and industry benchmarks.

**Expected impact:**
- Differentiation vs Zoho Invoice and Refrens
- Upsell path to "Ledgerly Pro" (₹499/mo tier)
- Demo well in sales calls for accountant channel partners

**Cost:**
- 3 engineers × 10 weeks (ML pipeline, prompt layer, UI surfaces)
- Ongoing inference cost (~₹2.1L/mo at 10k MAU projection)
- Privacy review and DPDP consent copy updates

**Risks:**
- Cold-start problem for new users with no invoice history
- Accuracy complaints if recommendations feel generic
- Distraction from core activation problem

### Option B: Onboarding flow fix

**Pitch:** Redesign three-step onboarding to address 66% drop-off at bank verification and unclear copy.

**Expected impact:**
- Modelled +21pp activation (34% → 55%)
- Direct revenue via faster time-to-first-payout
- Reduces support load (~40 tickets/week tagged onboarding)

**Cost:**
- 2 engineers × 6 weeks (frontend, API tweaks, analytics)
- 1 designer × 4 weeks (already partially done)
- Penny-drop vendor integration unchanged

**Risks:**
- Gains may plateau if underlying trust issue is brand-level, not UX
- Less exciting for fundraising narrative
- Does not help retained users

## Business context

- Runway: 14 months at current burn
- Board wants "AI story" before Series A conversations in August
- Activation is the north-star metric for H1; retention is flat at 62% D30
- Sales pipeline has 3 accountant partnerships waiting on "smart invoicing" demo

## Data we have

| Signal | AI recommendations | Onboarding fix |
|--------|-------------------|----------------|
| User research (n=18) | "Nice to have" (11/18) | "I gave up at bank step" (14/18) |
| Support volume | Low | High |
| Competitive parity | Behind (Zoho launched similar) | Parity issue, not feature gap |
| Revenue attribution | Hypothetical (Pro tier) | Modelled from activation lift |

## Stakeholder positions

CEO favors AI (narrative, partnerships). Eng lead favors onboarding (lower risk). Design says onboarding is ready; AI UX undefined. Growth backs activation funnel math.

## Constraints

- Cannot hire additional squad this quarter
- Must ship something customer-visible by end of May
- DPDP compliance work is non-negotiable background load (~0.5 eng)

## What we need from council

1. Which bet optimizes for 14-month runway and Series A positioning?
2. Is there a credible hybrid (thin AI demo + onboarding fix) or does that fail both?
3. What would change the decision if onboarding A/B shows <10pp lift?
