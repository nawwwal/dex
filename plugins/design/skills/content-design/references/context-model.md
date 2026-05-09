# Context Model

Use this file before writing. Classification is part of the work, not setup ceremony. It decides surface pattern, risk level, voice lane, marketing lane, and the amount of detail.

## Required classification

Capture or infer these fields:

- Surface: button, link, label, placeholder, helper text, validation, toast, banner, modal, empty state, tooltip, table, navigation, success, pending, notification, developer/API copy, accessibility label.
- Product area: payments, payment links, payment pages, checkout, refunds, settlements, payouts, KYC, disputes, chargebacks, bank accounts, reports, webhooks, API keys, dashboard, subscriptions.
- User role: founder, merchant, entrepreneur, finance operator, developer, admin, support operator, risk/compliance reviewer, customer, partner.
- Risk level: low, medium, high, critical.
- User state: first time, returning, blocked, reviewing, confirming, recovering, waiting, comparing, taking destructive action.
- System state: success, pending, failed, partially completed, blocked by user, blocked by Razorpay, blocked by bank/network/regulator/third party, unknown.
- Required next action: retry, edit, change, choose, select, upload, verify, contact support, wait, review, confirm, delete, remove, cancel, no action.
- Voice lane: product UI, founder-supportive, operator-clear, high-risk finance, legal/compliance, developer.
- Marketing lane, if any: platform authority, speed to value, scale proof, operational control, growth outcome, trust and compliance.
- Source/proof need: none, bundled reference, current external source, legal/product review.

## Risk tiers

- Low: cosmetic, preference, navigation, discovery, low-stakes education.
- Medium: setup, configuration, reversible changes, onboarding, optional adoption.
- High: payments, payouts, settlements, refunds, KYC, bank accounts, disputes, chargebacks, permissions, customer-visible money movement.
- Critical: money loss, data loss, legal commitment, account suspension, irreversible deletion, production API disruption.

## Actor model

Name the responsible actor when it helps the user understand what can happen next.

- You: the user must act.
- Razorpay: Razorpay is responsible or will act.
- Bank: bank processing, decline, verification, payout, or refund timing.
- Customer: payer action, retry, alternate payment method.
- Regulator/compliance: policy, KYC, account review, legal constraint.
- System/third party: outage, network, provider, integration.

Avoid actor fog: "The payment could not be processed" is weak when the bank declined it.

## State precision

Use the exact state. Do not flatten lifecycle states.

- Refund initiated is not refund completed.
- Settlement delayed is not settlement failed.
- KYC submitted is not KYC approved.
- Payment authorized is not payment captured.
- Webhook delivery failed is not webhook deleted.
- Test mode is not live mode.

## Next-action verbs

- Edit: modify existing details.
- Change: switch from one option or state to another.
- Choose: decide among valid options.
- Select: pick a UI option.
- Verify: confirm through system, document, bank, or identity check.
- Retry: attempt the same action again.
- Remove: detach from context.
- Delete: permanently remove.
- Cancel: stop a scheduled or requested action.
- Deactivate: turn off without deleting.

Use "click" only when the interface is strictly desktop-only. Prefer "select" for UI instructions.

