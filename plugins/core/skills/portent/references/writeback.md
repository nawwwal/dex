# Portent Writeback

Writeback should feel easy. The object model guides placement; it should not block capture.

Default to capture for non-trivial work. The agent should not need Aditya to say "remember this" before storing a useful decision, behavior correction, rationale, blocker, handoff, or design/technical constraint.

## Default Flow

1. Assume non-trivial work probably created something worth storing.
2. Search for the owning object with qmd or direct Markdown fallback.
3. Update that object with the smallest source-bounded entry.
4. Create a new note only when no owner exists.
5. If skipping writeback, name the reason: transient, unsupported, unsafe to store, or not Aditya-relevant.
6. Refresh Tolaria and qmd when possible.

## What To Write

Write:

- agent behavior corrections
- Aditya working-style preferences
- project state changes
- PR, DevRev, Slack, Gmail, Calendar, or meeting outcomes
- technical contracts, failure modes, implementation rationale, rejected paths, and source boundaries
- design decisions, why the decision was made, UI constraints, visual direction, interaction rules, and tradeoffs
- team ownership, review, escalation, and source-of-truth paths
- RCAs, blockers, verification results, and handoffs
- reusable synthesis that future work will depend on

Skip:

- broad team noise
- unsupported inference
- stale bot output
- one-off chatter with no future use after the writeback audit
- private/sensitive raw data that should be summarized instead

## Where To Put It

- `[[agent-behavior-gotchas]]`: reusable corrections to agent behavior.
- `[[brain-log]]`: material knowledge-base maintenance and high-level chronology.
- project/operation/responsibility notes: active work state, blockers, decisions, owners, source boundaries.
- event notes: meetings, sessions, releases, incidents, source-backed daily changes.
- task notes: durable next actions that need context or relationships.
- topic/person notes: reusable context about concepts, collaborators, teams, or systems.

Update existing notes before creating new notes.

Avoid tiny, narrow notes for every correction. Prefer adding a dated entry or short subheading to the owning project, operation, responsibility, behavior gotcha, thread map, people map, or `[[brain-log]]`. Create a new object only when the knowledge has its own durable identity.

## Context Hunger

When the source material is missing the why, ask for it. Useful questions are:

- Why are we doing this?
- What decision did we make, and what did we reject?
- Which source, owner, channel, constraint, or metric makes this true?
- What should a future agent do differently?

Ask one or two precise questions, then continue. If the user is frustrated or the task is urgent, write the known correction first and record the missing context as an open gap instead of stalling.

## Corrections Are Writes

When Aditya corrects agent behavior, do not defend the previous behavior and do not stop at an apology. Update the durable rule first:

- behavior correction -> `[[agent-behavior-gotchas]]`
- voice/comms correction -> voice note or comms owner plus gotcha when reusable
- project/source routing correction -> active map, project note, or runbook
- design/technical decision correction -> owning project/design/technical note with rationale

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
- Did a design or technical decision gain rationale, tradeoff, rejected option, owner, or constraint?
- Did the task reveal how Aditya wants agents to ask for context next time?
- Would future agents search for this?

If yes, write it. If no, say the concrete skip reason rather than using "no update needed" as a default.
