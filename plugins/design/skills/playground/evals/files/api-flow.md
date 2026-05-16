# API Flow Fixture

Flow: create payout.

Actors and services:
- Dashboard client
- API gateway
- Payout service
- Risk service
- Bank adapter

Sequence:
1. Dashboard client sends `POST /payouts`.
2. API gateway validates auth and forwards to payout service.
3. Payout service validates required fields and calls risk service.
4. Risk service returns `approved`, `review`, or `blocked`.
5. If approved, payout service calls bank adapter.
6. Bank adapter returns `accepted` or `failed`.
7. Payout service returns final status to dashboard client.

Branches:
- Missing fields return `400`.
- Blocked risk returns `403`.
- Bank failure returns `502` with retry guidance.
