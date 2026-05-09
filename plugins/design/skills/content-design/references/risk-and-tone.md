# Risk and Tone

Use this file to choose seriousness, detail level, and permission to persuade. Tone changes by context; voice stays stable.

## Tone map

| Surface or context | Tone | Detail level | Behavior |
| --- | --- | --- | --- |
| Navigation, tabs, filters | Neutral | Brief | Use exact nouns |
| Buttons | Direct | Brief | Verb or verb + noun |
| Tooltips | Helpful | Brief-medium | Explain unfamiliar concepts |
| Empty states | Helpful | Medium | Explain why empty and next action |
| Success toasts | Quiet | Brief | Confirm completed action |
| Marketing banner | Benefit-led | Medium | Show concrete user outcome |
| Setup/onboarding | Supportive | Medium | Explain value and next step |
| Form validation | Corrective | Brief | State fix, not fault |
| Payment failure | Calm | Medium | State status and next action |
| Payout/settlement issue | Serious | Medium-high | State impact, cause, resolution |
| KYC/compliance | Formal | High | State requirement, documents, timelines |
| Destructive modal | Serious | High | State consequence before action |
| Legal consent | Formal | High | State commitment clearly |
| System outage | Accountable | High | State impact, safety, next update/action |

## Detail by risk

- Low risk: keep copy brief; persuasion, warmth, and lightness are allowed when useful.
- Medium risk: explain value, eligibility, and next step; avoid inflated ease.
- High risk: name actor, affected object, amount/date/timeline, and recovery path when known.
- Critical risk: consequence-first, explicit, no cleverness, no ambiguity, no unsupported reassurance.

## Seriousness gates

Use serious, explicit copy for:

- Payments
- Refunds
- Payouts
- Settlements
- KYC
- Bank accounts
- Disputes and chargebacks
- Legal consent
- Account suspension
- Data loss
- Permissions
- Production API disruption
- Irreversible deletion

## No-overpromise rules

Do not promise:

- KYC approval
- Settlement timing beyond known bank/Razorpay timelines
- Refund receipt before bank processing is complete
- Payment success after a retry
- Integration success before credentials and mode are correct
- Account availability during review
- "Instant" or "in minutes" when approval, KYC, bank, or compliance can block completion

## Humor and hype

Humor, puns, emojis, and exclamation marks are not allowed in high-risk or critical states.

Marketing words such as seamless, effortless, powerful, unlock, and supercharge are allowed only in marketing mode with mechanism or proof. They are not acceptable in risk, compliance, money movement, failure, or legal copy.

