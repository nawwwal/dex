# Sync State Reference

PMB Sync State memory is the single DevRev operating cache. Agents may overwrite only the Sync State record.

Do not edit DevRev config, project map, active sprint, Track A, or Track B as part of Sync State updates. If one of those sections appears stale, add a `Proposed writebacks` row.

## Section Shape

```md
## Sync State

last_synced: 2026-06-15T09:00:00+05:30
last_mode: morning
source_coverage: DevRev checked; Slack checked; PMB checked; GitHub not provided; Codex not provided

### Plate
| Item | Area | State | Freshness | Evidence | Next action | Confidence |
|---|---|---|---|---|---|---|

### Signals
| Source | Signal | Related item | Freshness | Evidence | Action |
|---|---|---|---|---|---|

### Proposed writebacks
| Target | Item | Proposed change | Reason |
|---|---|---|---|
```

## Authority

- DevRev: issue ID, owner, sprint, stage, priority, target dates, remaining effort.
- Slack: asks, blockers, decisions, urgency, coordination gaps.
- PMB: durable context, prior decisions, caveats, current Sync State.
- GitHub/Codex: only when supplied in an `External evidence` block. Do not fetch directly in v1.

## Source Coverage

Record exact status for every source:
- `checked`
- `not provided`
- `unavailable: <reason>`
- `supplied in External evidence`

Do not imply a source was checked when it was unavailable or not supplied.

## Freshness

Use short values: `current`, `stale`, `conflicted`, `blocked`, `historical`.

## Write Rules

- Overwrite `## Sync State` as housekeeping after reconciliation.
- Treat `Proposed writebacks` as drafts, not permission to mutate external systems.
- Require explicit confirmation before mutating DevRev, Slack, GitHub, Codex, or non-Sync-State PMB sections.
