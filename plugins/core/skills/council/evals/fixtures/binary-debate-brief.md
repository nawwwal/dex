# Architecture Decision Brief: Microservices vs Monolith

**Product:** Ledgerly backend (Node.js, PostgreSQL, Redis, deployed on AWS)  
**Team:** 8 engineers, 1 platform contractor  
**Scale:** ~12k MAU, 400k invoices/month, ₹18Cr monthly GMV through platform  
**Requested output:** Multi-perspective debate — should we split the monolith?

## Current architecture

Single `ledgerly-api` Express monolith:

- **Modules (internal packages):** auth, invoices, payments, payouts, kyc, notifications, webhooks
- **Database:** One PostgreSQL cluster, schema per domain loosely namespaced
- **Deploy:** Single ECS service, 4 tasks, rolling deploy ~8 min
- **Observability:** Datadog APM, log correlation via request ID

Pain is increasing in `payments` and `payouts` modules — they change weekly for Razorpay API updates and RBI compliance tweaks. `invoices` is stable. `auth` is touched by every feature.

## Proposal on the table

Split into three services:

1. **ledgerly-core** — auth, users, invoices, notifications
2. **ledgerly-money** — payments, payouts, webhooks, reconciliation
3. **ledgerly-compliance** — kyc, audit logs, regulatory exports

**Interop:** REST + shared Postgres initially (schema split later), SNS/SQS for async events  
**Timeline:** 4–6 months incremental extraction, starting with webhooks worker (already partially separated)

## Arguments for split

- Payments team can deploy without regression-testing invoice PDF generation
- Blast radius containment if payout job goes runaway
- Compliance module may need different access controls and audit retention
- Hiring pitch: "payments engineering" is easier with bounded service
- Razorpay webhook volume spiked 3×; monolith CPU pegged during settlement windows

## Arguments against split

- Team has no production microservices experience; k8s/ECS service mesh is new ops load
- Shared DB means we get distributed monolith worst case without schema split
- Cross-module transactions (invoice paid → payout triggered → notification) become sagas
- 8 engineers already split across frontend-heavy onboarding rewrite
- Current uptime 99.7%; incidents are deploy-related, not module-isolation failures

## Non-negotiables

- DPDP and RBI audit trail must remain queryable across domains
- P99 API latency for invoice read < 200ms cannot regress
- Zero-downtime deploys required during business hours (IST 9am–9pm)

## Incident history (last 6 months)

| Incident | Root cause | Would split have helped? |
|----------|------------|--------------------------|
| Payout double-credit | Idempotency bug in payouts | Maybe — isolated deploy blast |
| API 502 spike | Memory leak in PDF renderer | No — invoices module |
| Webhook backlog | Razorpay burst + sync processing | Yes — independent worker scaling |
| Auth token expiry bug | Shared middleware change | No — made worse if multi-service auth |

## Options beyond binary split

**A.** Status quo monolith + extract webhook worker only (2 weeks)  
**B.** Modular monolith — enforce package boundaries, separate deploy artifacts, shared runtime  
**C.** Full microservices with schema-per-service (6+ months)  
**D.** Buy time — horizontal scale monolith, revisit at 50k MAU

## What we need from council

1. Given team size and incident history, is split justified now or performative?
2. If modular monolith (B), what boundaries matter most?
3. What decision criteria would trigger a revisit in 6 months?
4. Devil's advocate: what is the best argument that splitting now kills the company?

## Artifacts

- Architecture diagram: `docs/architecture-v4.png`
- RFC-017: Microservices extraction (draft, 12 pages)
- Datadog service map (monolith only today)
