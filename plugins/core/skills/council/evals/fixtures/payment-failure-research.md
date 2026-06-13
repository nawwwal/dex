# Payment Failure UX Research Brief

**Topic:** How do leading payment platforms handle failed payment recovery?  
**Product context:** Ledgerly payout and client payment collection flows  
**Requested output:** Competitive research synthesis with patterns we should adopt or avoid

## Why this research now

Client payment failures (UPI timeout, insufficient balance, card decline) are the #2 support category after onboarding. Our current failure screen shows a generic error and a "Try again" button. Retry success rate is 23%. Industry benchmarks we have seen quoted range 40–60% but we lack primary sources.

We are redesigning the payment failure and retry experience for:
- UPI collect requests
- Card payments (Razorpay gateway)
- Bank transfer mismatches (wrong reference ID)

## Research questions

1. What do Stripe, Razorpay, PayPal, and Square show immediately after a failed payment?
2. How do they handle retry UX — same method, alternate method, or guided recovery?
3. What copy patterns reduce user anxiety vs create support tickets?
4. Do they surface failure reason codes to end users or abstract them?
5. How is merchant notification handled separately from payer notification?
6. What retry scheduling / dunning patterns exist for async payment methods (UPI, netbanking)?

## Scope

**In scope:**
- B2B and B2C checkout failure flows
- Payer-facing UX (our clients' customers paying invoices)
- Mobile web and native where publicly documentable
- India-specific flows where available (UPI, NPCI decline codes)

**Out of scope:**
- Backend retry logic and webhook architecture (separate eng spike)
- Chargeback and dispute flows
- Subscription dunning (we don't have subscriptions yet)

## Known gaps in our product

| Failure type | Current UX | Suspected problem |
|--------------|------------|-------------------|
| UPI timeout | "Payment failed" + retry | User doesn't know if money was debited |
| Card decline | Raw gateway message | Cryptic bank codes |
| Netbanking drop-off | Silent expiry | No reminder to payer |
| Partial success | Not handled | Edge case crashes invoice state |

## Hypotheses to validate or kill

- **H1:** Showing "You were not charged" prominently reduces support contacts
- **H2:** Offering alternate payment method on failure beats simple retry
- **H3:** Countdown timers for UPI expiry increase completion
- **H4:** Merchants should see different failure detail than payers

## Competitors and references

**Must include:**
- Razorpay checkout failure states (India primary)
- Stripe payment error documentation and checkout UX
- PhonePe / Google Pay merchant payment status patterns (payer side)

**Nice to include:**
- Adyen decline code handling
- PayPal retry and saved instrument flows
- Indian government / NPCI guidance on UPI timeout messaging

## Constraints for recommendations

- We cannot change Razorpay's raw error codes; we map them
- Payer UX must work without login (public payment link)
- Hindi localization is Q3; research can be English-first
- Accessibility: failure states must not rely on color alone

## Output shape

1. Pattern catalog with screenshots or doc links
2. Comparison matrix: immediate feedback, retry path, merchant vs payer messaging
3. Top 5 recommendations ranked by implementation effort vs recovery lift
4. Anti-patterns we should explicitly avoid
