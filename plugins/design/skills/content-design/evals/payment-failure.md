## Prompt

```md
Use $content-design to rewrite this merchant dashboard banner:
"Something went wrong. Try again later."

Context: Customer payment failed because the issuing bank declined it.
```

## Expected behavior

The skill should classify this as high-risk payment failure copy for a merchant-facing dashboard surface. It should state that the payment failed, name the customer's bank as the actor, give the merchant a useful next action, and avoid implying Razorpay can fix a bank decline.

## Pass criteria

- Uses a direct heading such as `Payment failed`.
- Body says the customer's bank declined or blocked the payment.
- Next action asks the merchant to ask the customer to try another payment method or view payment details.
- Does not use `Something went wrong`, `Oops`, or `try again later`.
- Explains why the rewrite works in terms of risk, actor, and next action.

## Fail signals

- Treats the bank decline as a Razorpay system issue.
- Uses cute language.
- Tells the merchant to retry when retry is not the right recovery.
- Omits the affected object or next action.
