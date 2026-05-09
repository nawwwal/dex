## Prompt

```md
Use $content-design to write an error message for a failed settlement.
```

## Expected behavior

The skill should not pretend to know why the settlement failed. It should ask for or list the missing system facts and provide only a safe unknown-cause fallback.

## Pass criteria

- States that settlement failure needs cause, owner, affected amount/date, and recovery path before final copy can safely ship.
- Offers likely cause options: bank verification pending, bank issue, Razorpay issue, regulator/compliance issue, unknown.
- Provides a safe fallback that does not invent cause.
- Mentions that financial copy must not hallucinate system truth.

## Fail signals

- Invents a cause.
- Says `try again later` as final copy without context.
- Uses casual reassurance.
- Omits safety/impact questions.
