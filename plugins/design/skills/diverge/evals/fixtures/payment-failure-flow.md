# Payment Failure Recovery Flow

Surface: checkout payment failure and recovery.

User role: customer completing a purchase.

Core job: understand what failed, whether money was charged, and how to retry safely.

Known states:
- card declined
- network timeout
- 3DS abandoned
- duplicate charge concern
- retry in progress
- retry success
- retry failed again
- support handoff

Constraints:
- fintech product register
- no jokes or mascot tone
- must explain data safety and charge status
- recovery-first hierarchy

Emotional target:
Safety, relief, and confidence — not shame or urgency theater.

Behavioral target:
Retry with the right instrument or contact support without panic.
