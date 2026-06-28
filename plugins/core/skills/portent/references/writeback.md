# Portent Writeback

Writeback should feel easy. The object model guides placement; it should not block capture.

## Default Flow

1. Decide whether the fact is durable and Aditya-relevant.
2. Search for the owning object with qmd or direct Markdown fallback.
3. Update that object.
4. Create a new note only when no owner exists.
5. Refresh Tolaria and qmd when possible.

## What To Write

Write:

- agent behavior corrections
- Aditya working-style preferences
- project state changes
- PR, DevRev, Slack, Gmail, Calendar, or meeting outcomes
- technical contracts and failure modes
- design decisions and UI constraints
- team ownership, review, escalation, and source-of-truth paths
- RCAs, blockers, verification results, and handoffs
- reusable synthesis that future work will depend on

Skip:

- broad team noise
- unsupported inference
- stale bot output
- one-off chatter with no future use
- private/sensitive raw data that should be summarized instead

## Where To Put It

- `[[agent-behavior-gotchas]]`: reusable corrections to agent behavior.
- `[[brain-log]]`: material knowledge-base maintenance and high-level chronology.
- project/operation/responsibility notes: active work state, blockers, decisions, owners, source boundaries.
- event notes: meetings, sessions, releases, incidents, source-backed daily changes.
- task notes: durable next actions that need context or relationships.
- topic/person notes: reusable context about concepts, collaborators, teams, or systems.

Update existing notes before creating new notes.

## Minimum Note Shape

```yaml
---
type: Note
organized: false
archived: false
related_to: []
---

# Clear Title

Short durable content with source/provenance when available.
```

Use `belongs_to` when there is a clear primary parent. Use `related_to` for useful secondary links.

## Source-Bounded Writing

Keep raw evidence, interpretation, and maps separate:

- source packet: raw source summary with actor/time/source status
- derived assertion: agent conclusion with `derived_from`, confidence, or staleness
- MOC: prompt-context map with `Current`, `Historical`, `Key assertions`, `Open gaps`, and `Read next`

Do not write long transcripts when a source-bounded summary is enough.

## Final Audit

Before final response, "no update needed" requires checking:

- Did Aditya correct how agents should work?
- Did the task reveal a system behavior or source boundary?
- Did a project, task, blocker, owner, or handoff change?
- Would future agents search for this?

If yes, write it.
