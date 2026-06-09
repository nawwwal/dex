# EOD Mode

Goal: Log what happened, clean up DevRev, prep tomorrow. Stateful flow.

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

## Phase 5 — Tomorrow preview (deterministic, script)

```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/filter_issues.py" starts_on \
  --date "$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d tomorrow +%Y-%m-%d)"
```

Script returns issues with `target_start_date == tomorrow`. Skips weekends (Friday's "tomorrow" = Monday). Main thread prints the list.
