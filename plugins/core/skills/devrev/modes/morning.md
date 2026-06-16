# Morning Mode

Goal: Today's attention in 30 seconds. DevRev is the operational anchor; `## Sync State` is the cached operating view.

## Phase 0 — Sync State cache check

Read `references/sync-state.md`.
Read `## Sync State` from `[[DevRev local knowledge]]`.

If all are true, answer from Sync State and skip live fetch:
- `last_synced` is under 4 hours old.
- The user did not ask for refresh.
- The section contains enough Plate and Signals rows to answer the prompt.

When answering from cache, report `source_coverage` exactly as written and say the answer is from Sync State.

If Sync State is stale, missing, incomplete, or refresh is requested, continue to Phase 1.

If the prompt contains an `External evidence` block, carry it into reconciliation. GitHub and Codex evidence are valid only from this supplied block; do not fetch them directly.

## Phase 1 — Parallel fetchers

Run both agents simultaneously:

**A (Fetcher):** `list_objects(action_name="list_issues", values={"owned_by": [$USER_DON], "state": ["open","in_progress"], "limit": 100}, fields=["id","display_id","title","stage","target_close_date","target_start_date","sprint","tnt__remaining_effort"])`
Return JSON array: `[{iss_id, title, stage, target_close_date, target_start_date, sprint, tnt__remaining_effort}]`
Sort by target_close_date ascending.

**B (Fetcher):** `slack_search_public_and_private("$SLACK_MENTION after:<yesterday_date>")`
Return JSON array: `[{text, channel, ts, link}]`
Max 10 results, most recent first.

## Phase 2 — Deterministic filter

```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/filter_issues.py" morning_buckets \
  --today "$(date +%Y-%m-%d)"
```

Script returns:
```json
{
  "due_today": [...],
  "overdue": [...],
  "starts_today": [...],
  "rest": [...]
}
```

## Phase 3 — Probabilistic synthesis (main thread, no agent)

From script output + Slack asks + previous Sync State + any supplied `External evidence`, the LLM:
1. Dedupes Slack asks against DevRev titles by semantic similarity.
2. Reconciles DevRev operational state with supporting evidence from Slack, Tolaria, and supplied external evidence.
3. Separates confirmed work from drift and writeback proposals.
4. Picks one focus recommendation (judgment: highest urgency + momentum).
5. Renders:

```
→ ATTENTION NOW: [ISS-X or signal] — [why it needs attention]
→ ON MY PLATE: [ISS-Y: title] — [state, freshness, next action]
→ I AM BLOCKING: [item/person] — [what they need from me]
→ BLOCKED / WAITING: [item] — [who/what is blocking it]
→ DRIFT DETECTED: [DevRev vs Slack/Tolaria/external mismatch]
→ FOCUS: [the one thing to start with — one sentence why]
→ SOURCE COVERAGE: [DevRev checked; Slack checked; Tolaria checked; GitHub/Codex not provided or supplied]
```

If due_today and overdue are both empty: show starts_today as top item.
If all empty: show first 3 from rest, sorted by target_close_date.

## Phase 4 — Update Sync State

Overwrite only `## Sync State` in `[[DevRev local knowledge]]`.

Use the section shape and source-coverage rules from `references/sync-state.md`. Set `last_mode: morning`; populate Plate from DevRev issues, Signals from supporting evidence, and Proposed writebacks for drift that needs confirmation.
