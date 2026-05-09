# Errors and Recovery

Use this file for failures, validation, blocked states, unknown errors, and recovery copy. Error copy is product behavior. If the product knows the cause and the copy hides it, the copy is wrong.

## Error anatomy

A useful error says:

1. What happened.
2. Why it happened, if known.
3. What is affected.
4. What remains safe or unchanged, if relevant.
5. What the user can do next.
6. What to do if the user cannot fix it.

## Generic failure detector

Reject these as final copy unless the system truly has no better context:

- Something went wrong
- Try again later
- Oops
- Uh-oh
- Failed due to technical issue
- Invalid
- Bad request
- Authentication failed

Replace with failed action + recovery.

Unknown fallback pattern:

Could not [action/object]
Refresh the page to try again. If this keeps happening, contact support.

## Missing system context

For high-risk copy, do not invent cause. Ask for or list missing facts:

- Known cause
- Responsible actor
- Affected object
- Affected amount/date/timeline
- User recovery path
- Support/escalation path
- What remains safe

Safe settlement fallback:

Settlement delayed
We could not confirm the reason yet. Check the settlement details for the latest status, or contact support if the expected date has passed.

## Payment failure

Distinguish merchant-facing and payer-facing copy.

Merchant-facing:

Payment failed
The customer's bank declined the payment. Ask the customer to try another payment method.

Payer-facing:

Payment failed
Your bank declined the payment. Try another payment method or contact your bank.

Rules:

- Say who declined or blocked the payment if known.
- Do not imply Razorpay can fix bank-side failures.
- Do not expose gateway jargon unless the user is a developer.

## Refunds

Separate initiation, processing, success, and failure.

- Refund initiated: the refund request started; the customer may not have received money.
- Refund processing: bank or payment network is handling it.
- Refund completed: money reached the final state.
- Refund failed: state cause and recovery.

Use exact amount and date where possible. Avoid "refunded" until the state is final.

## Settlements and payouts

Be operationally precise.

Use:

- Settlement created
- Settlement processing
- Settlement delayed
- Settlement paid
- Payout failed

Rules:

- Mention amount if available.
- Mention expected date if available.
- Distinguish current settlement impact from future settlement setup.
- Identify whether the user, Razorpay, bank, or regulator owns the next step.

## Validation errors

Validation should describe the fix, not the fault.

Use:

- Enter a 10-digit mobile number.
- Use an email address with `@`.
- Upload a file under 5 MB.
- Enter an amount between Rs 1 and Rs 5,00,000.

Avoid:

- Invalid input
- Wrong
- Not valid
- This field has an error

