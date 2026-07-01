# EOD Mode

Goal: Close the day, reconcile active work, update `## Sync State`, and prep tomorrow. DevRev writes stay draft-then-confirm.

## Phase 0 — Read current Sync State

Read `references/sync-state.md`.
Read Sync State from PMB before fetching live data.

If the prompt contains an `External evidence` block, carry it into reconciliation. GitHub and Codex evidence are valid only from this supplied block; do not fetch them directly.

## Phase 1 — Parallel fetchers

Run both simultaneously:

**A (Fetcher):** `list_objects(action_name="list_issues", values={"owned_by": [$USER_DON], "state": ["open","in_progress"], "limit": 100}, fields=["id","display_id","title","stage","target_close_date","target_start_date","tnt__remaining_effort","body"])`
Return JSON array: `[{iss_id, title, stage, target_close_date, target_start_date, tnt__remaining_effort, body_excerpt}]`

**B (Fetcher):** `slack_search_public_and_private("$SLACK_MENTION on:<today_date>")`
Return bullets: one per thread — what was asked/said/decided.

## Phase 2 — Main thread Q&A

Show A's condensed summary (ISS IDs + stages). Results from A and B persist in context.

Ask conversationally:
1. "What did you finish today?"
2. "What's still in progress? Effort remaining?"
3. "Anything new from Slack or meetings not in DevRev yet?"

## Phase 3 — Drafter agent (sequential, after Phase 2)

**C (Drafter):** Given (A's issue list + user's answers from Phase 2), draft for each affected issue:
- Stage change (prefer stage DON; see gotchas.md #4 and #5)
- Body append (append only, never overwrite — use `## EOD Update [date]` section)
- Effort update (`tnt__remaining_effort` as float days)

Return markdown diff per issue. Max 400 words total.

## Phase 4 — Apply updates

Show drafts. On confirm: parallel `update_object(action_name="update_issue", subtype="task")` calls (main thread, not subagents).

For stage transitions involving To Do → Completed: use two sequential calls per gotchas.md #5.

Do not mutate DevRev without confirmation.

## Phase 5 — Update Sync State

Overwrite only Sync State in PMB regardless of whether DevRev writes were applied.

Use the section shape and `source_coverage` rules from `references/sync-state.md`. Set `last_mode: eod`; populate Plate from still-open/completed work and user answers, Signals from supporting evidence, and Proposed writebacks for drafted but unconfirmed DevRev changes.

## Phase 6 — Tomorrow preview (deterministic, script)

```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/filter_issues.py" starts_on \
  --date "$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d tomorrow +%Y-%m-%d)"
```

Script returns issues with `target_start_date == tomorrow`. Skips weekends (Friday's "tomorrow" = Monday). Main thread prints the list.
