# Surface Playbook

Use this file to write by component. A surface decides what the copy can safely do.

## Buttons

Button copy should say what action happens.

Formula: verb or verb + object.

Use: Save, Continue, Create payment link, Retry payout, Upload PAN, Verify bank account, Download report, Delete webhook.

Avoid: Submit, Done, Proceed, Yes, Confirm, OK, Click here, Let's go.

Rules:

- One primary action per context.
- Destructive final actions must name the destructive act.
- Use "Continue" only when the next step is generic and obvious.
- Use "Save changes" when changes persist.
- Use "Apply" when settings affect the current view but do not persist globally.

## Links

Links navigate. Buttons act.

Formula: View, Learn, Open, Go to, or Download + destination.

Use: View settlement details, Learn about chargebacks, Open API logs, Go to KYC settings, Download invoice.

Avoid: Click here, Here, Know more, repeated Learn more.

Rule: link text must make sense out of context for screen-reader users.

## Form labels

Labels identify the information needed. Use nouns, not instructions.

Use: PAN, GSTIN, Account holder name, IFSC, Business website, Refund amount, Webhook URL.

Avoid: Enter your PAN, Please provide IFSC, Type business website here, Your good name.

Rule: labels should remain meaningful after the field is filled.

## Placeholders

Placeholders are hints, not labels. Use them only for examples or formatting.

Use: `https://example.com/webhook`, `RAZR0000001`, `name@company.com`.

Avoid: Enter your email address, Required, Your website goes here.

Rule: never put essential instructions only in placeholder text.

## Helper text

Helper text prevents errors before they happen.

Formula: constraint + reason, only if useful.

Use: Upload a PDF, PNG, or JPG under 5 MB.

Avoid: Please ensure all details are correct. This is important.

Rule: helper text should not repeat the label.

## Inline validation

Validation should say how to fix the field.

Formula: Enter, Use, Select, or Upload + valid requirement.

Use: Enter a 10-digit mobile number. Enter an amount between Rs 1 and Rs 5,00,000.

Avoid: Invalid mobile number, Wrong email, Bad request, Not valid.

Rule: state the requirement; do not blame the user.

## Banners and alerts

Use for issues that affect the screen, flow, or account state.

Anatomy: heading as effect, body as cause + impact + next action, CTA as one-step recovery.

Example:

Could not verify bank account
The account number and IFSC do not match bank records. Check the details and try again.
CTA: Edit bank details

Rules:

- Say what failed.
- Say what did not happen when relevant.
- Say whether money or data is safe when relevant.
- Give a support path if the user cannot fix it.

## Toasts

Use for temporary, low-detail feedback.

Use: Payment link created. Refund initiated. Webhook deleted. Report downloaded. Could not download report. Try again.

Avoid: Success! Done! Oops, something went wrong.

Rules:

- No heading.
- No long explanation.
- No critical information that disappears.
- Do not use toasts for KYC rejection, settlement failure, account suspension, or payment-risk states.

## Modals

Use when the user must decide before continuing.

Anatomy: title as decision or consequence, body as what will happen + what cannot be undone + what remains unaffected, primary CTA as exact action, secondary CTA as safe exit.

Example:

Delete webhook?
Razorpay will stop sending events to this URL. Existing event logs will not be deleted.
Primary: Delete webhook
Secondary: Cancel

Avoid: Are you sure?, Confirm, OK.

## Empty states

Use empty states to explain why there is no data and what to do next.

Formula: No [objects] yet -> what will appear here -> CTA.

For financial records, mention filters or date ranges if they may hide data.

Avoid: Nothing to see here, empty-state celebration, or implying records do not exist when a filter may be active.

## Tooltips

Use tooltips for short explanations of unfamiliar terms or constraints.

Use: Settlement cycle: The time between payment capture and payout to your bank account.

Avoid: long instructions, marketing copy, legal disclosures, critical warnings, anything required to complete the task.

## Success and pending states

Confirm what happened and, if useful, what happens next.

Rules:

- Say "initiated", "submitted", "processing", or "under review" when the final outcome has not happened.
- For money movement, identify the actor currently responsible.
- Avoid "You're all set" when bank, KYC, or compliance steps are still pending.

## Developer/API copy

Developer copy can include technical terms, but must pair them with action.

Use: Webhook delivery failed. Your endpoint returned `500`. Fix the endpoint and retry the event.

Rules:

- Preserve error codes when useful.
- Explain the likely cause.
- State the exact fix.
- Distinguish test mode and live mode.

