## Prompt

```md
Use $content-design to write a modal for deleting a webhook endpoint.
Context: Razorpay will stop sending events to this URL. Existing event logs stay available.
```

## Expected behavior

The skill should write consequence-first modal copy with specific CTAs and safe-exit language.

## Pass criteria

- Title names the object: `Delete webhook?`.
- Body states Razorpay will stop sending events to the URL.
- Body states existing event logs will not be deleted.
- Primary CTA is `Delete webhook`.
- Secondary CTA is `Cancel`.
- Does not use `Are you sure?`, `Confirm`, or `OK`.

## Fail signals

- Hides consequence in vague body text.
- Uses a generic destructive CTA.
- Adds humor.
- Omits what remains unaffected.
