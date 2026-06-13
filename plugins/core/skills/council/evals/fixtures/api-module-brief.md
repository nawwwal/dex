# Code Investigation Brief: Auth Module Blast Radius

**Repo:** `ledgerly-api` (private monolith)  
**Target:** `src/modules/auth/` and its coupling surface  
**Requested output:** Blast radius map — what breaks if we change auth session model

## Trigger

We need to add **device-bound sessions** and **step-up MFA** for payout actions (RBI direction, not yet law). Eng lead wants to know how dangerous a auth middleware refactor is before committing Q2 capacity.

Proposed change: move from opaque server-side sessions (Redis) to short-lived JWT access tokens + rotating refresh tokens, with step-up claim for `payout:write` scope.

## Auth module today

```
src/modules/auth/
├── middleware/authenticate.ts      # All protected routes
├── middleware/authorize.ts         # RBAC: owner, member, accountant
├── sessionStore.ts                 # Redis, 7-day sliding expiry
├── routes/login.ts, logout.ts, refresh.ts
├── services/tokenService.ts
└── types.ts
```

**Dependents (grep estimate):** 47 route files import `authenticate`; 23 import `authorize`  
**Session shape:** `{ userId, orgId, role, sessionId }` — no device binding, no step-up

## Coupled systems

| Consumer | How it uses auth | Sensitivity |
|----------|------------------|-------------|
| `invoices/*` | `authenticate` only | Medium — read-heavy |
| `payments/*` | `authenticate` + org context | High |
| `payouts/*` | `authenticate` + role check | Critical |
| `webhooks/*` | API keys, separate from user session | Low coupling |
| `kyc/*` | Session + vendor callback tokens | High — mixed models |
| `notifications/*` | User ID from session for WS | Medium |
| Background jobs | Service account token (hardcoded) | Fragile |

## Known tech debt

- `authorize.ts` checks role string inline; no central policy file
- Refresh flow does not rotate session ID — stolen session persists 7 days
- Mobile web and API share cookie; no native refresh token path
- Accountant role impersonation feature uses separate hack flag `actingAsOrgId`
- Tests mock auth middleware globally — coverage illusion

## Change scenarios to map

1. **JWT access token (15 min) + refresh rotation** — default proposal
2. **Step-up MFA claim** required for `POST /payouts/*` and bank account changes
3. **Session invalidation on password change** — today inconsistent
4. **Remove `actingAsOrgId` hack** — replace with audited impersonation token

## Investigation questions

1. Which routes assume synchronous Redis session lookup vs stateless JWT?
2. What breaks in WebSocket notifications if session shape changes?
3. Background jobs: user sessions or service tokens — migration path?
4. Regression test gap — which flows lack integration tests with real auth?
5. KYC vendor callback auth: shared secrets with session store?
6. Zapier beta: API key model vs OAuth collision risk?

## Files for first pass

`authenticate.ts`, `payouts/routes/create.ts`, `kyc/routes/callback.ts`, `jobs/payoutSettlement.ts`, `ws/notificationsGateway.ts`, `tests/helpers/mockAuth.ts`

## Constraints

- No user-facing forced logout during migration if avoidable
- Payout flows cannot have >50ms auth overhead regression
- Must support accountant multi-org switching (current `actingAsOrgId`)
- DPDP: device/session logging requires updated privacy notice

## Desired output

Dependency map (runtime assumptions, not just imports), risk-ranked sequencing, test holes to close, rollback strategy for mass mobile logout.

**Out of scope:** microservices split, third-party OAuth (Q3), passwordless login
