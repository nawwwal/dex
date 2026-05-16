# Email Agent Source Fixture

Modules:
- `inbox-sync`: pulls unread Gmail messages and stores normalized threads.
- `thread-classifier`: classifies each thread as urgent, waiting, FYI, or needs reply.
- `draft-writer`: prepares reply drafts using thread context and user voice notes.
- `approval-gate`: blocks sending until the user approves or edits the draft.
- `send-worker`: sends approved drafts and records delivery status.

Flows:
1. `inbox-sync` writes `ThreadRecord`.
2. `thread-classifier` reads `ThreadRecord` and writes `ThreadPriority`.
3. `draft-writer` reads `ThreadRecord`, `ThreadPriority`, and `VoiceProfile`.
4. `approval-gate` stores `DraftDecision`.
5. `send-worker` sends only when `DraftDecision.status = approved`.

Risks:
- `draft-writer` can hallucinate commitments if source context is thin.
- `send-worker` must never bypass `approval-gate`.
- Priority is unreliable when a thread contains forwarded context.
