# Morning Mode

Goal: Today's agenda in 30 seconds. DevRev is source of truth.

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

From script output + Slack asks, the LLM:
1. Dedupes Slack asks against DevRev titles by semantic similarity.
2. Picks one focus recommendation (judgment: highest urgency + momentum).
3. Renders:

```
→ DUE TODAY: [ISS-X: title] — [remaining effort estimate]
→ OVERDUE: [ISS-Y: title] — [N days overdue]
→ STARTS TODAY: [ISS-Z: title]
→ SLACK ASKS: [N new items not in DevRev — brief list]
→ FOCUS: [the one thing to start with — one sentence why]
```

If due_today and overdue are both empty: show starts_today as top item.
If all empty: show first 3 from rest, sorted by target_close_date.
