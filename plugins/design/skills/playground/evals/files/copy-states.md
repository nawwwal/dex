# Copy State Fixture

Surface: payout setup.

States:
- Empty: no bank account added.
- Pending: bank verification submitted.
- Failed: verification failed because account holder name did not match.
- Success: payouts are ready.

Current copy:
- Empty: "Add bank details to continue."
- Pending: "Verification pending."
- Failed: "Something went wrong. Try again."
- Success: "You're all set."

Risk:
- Failed state must be specific without sounding punitive.
- Pending state must set expectation without promising exact time.
