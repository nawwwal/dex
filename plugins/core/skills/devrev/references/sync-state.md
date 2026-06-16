# Sync State Reference

`[[DevRev local knowledge]]` is the single DevRev operating note in Tolaria. Agents may overwrite only its `## Sync State` section.

Do not edit DevRev config, project map, active sprint, Track A, or Track B as part of local knowledge sync. If one of those sections appears stale, add a `Proposed writebacks` row.

## Section Shape

```md
## Sync State

last_synced: 2026-06-15T09:00:00+05:30
last_mode: morning
source_coverage: DevRev checked; Slack checked; Tolaria checked; GitHub not provided; Codex not provided

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
- Tolaria: durable context, prior decisions, caveats, current local knowledge.
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
- Require explicit confirmation before mutating DevRev, Slack, GitHub, Codex, or non-Sync-State Tolaria sections.
