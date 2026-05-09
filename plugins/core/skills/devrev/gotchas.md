# DevRev MCP Known Issues

Source: TKT-62791 + operational experience.

## 1. ctype__task_type not API-settable

Defaults to "Engineering" on every create. Cannot be set via `create_issue` or `update_issue`.

Workaround: After bulk create, surface this reminder:
"Update task_type to 'Design' for these N issues in the DevRev UI: [list ISS IDs]"

## 2. estimated_effort drifts

`estimated_effort` is GET-only (hours). Auto-set at creation as `tnt__remaining_effort × 24`. Subsequent `tnt__remaining_effort` updates do NOT propagate back.

Workaround: Always write `tnt__remaining_effort`. Treat `estimated_effort` as derived/stale.

## 3. Stage = full DON ID only

Passing `{name: "Completed"}` fails silently.

Workaround: Always pass full DON string.
Stage DONs (from $ISSUE_CONVENTIONS):
- to_do: `don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/67`
- in_progress: `don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/44`
- completed: `don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/26`
- blocked: `don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/116`

## 4. get_valid_stage_transitions unreliable from In Progress

Returns null even when Completed is reachable.

Workaround: Skip the validation call. Write the target stage DON directly.

## 5. Stage transition rule

Cannot jump To Do → Completed in one call. Must go: To Do → In Progress → Completed.

Workaround: Two sequential `update_issue` calls when source stage is To Do.

## 6. list_issues blows context on large enhancements

No pagination. A large enhancement returns a massive proto blob.

Workaround: When ISS IDs are known, prefer parallel `get_issue` calls. Filter `list_issues` aggressively with `state`, `sprint`, `target_close_date` params. Truncate fetcher returns to top 20.

## 7. Date encoding silently shifts

Naive ISO strings (no offset) are parsed as UTC. IST midnight = UTC 18:30 prev day.

Workaround: ALL dates MUST include `+05:30` offset. Use:
- `target_start_date`: `YYYY-MM-DDT00:00:00+05:30`
- `target_close_date`: `YYYY-MM-DDT18:29:59+05:30`

Reject any date string lacking `+05:30` before sending.

## 8. MCP responses are proto-formatted

`fields:{key:"..." value:{string_value:"..."}}` structure with escaped quotes.

Workaround: Trust the MCP tool wrapper to parse. Don't try to read raw output.

## 9. Issues live in two parallel tracks (PM vs user)

Features like "Connectors" or "My Agents" have both PM PRDs (full bodies, `[J*-S*]` codes, owned by another user) and design tasks (user-owned, often empty bodies). Both share `applies_to_part` and sprint.

Workaround: ALWAYS scope every `list_issues` with `owned_by=[$USER_DON]`. Verify `owned_by` on every `get_issue` result. PM PRDs are read-only context in `enrich` mode; they never enter the user's task surface, agenda, EOD updates, or velocity calculations.

Failure mode if violated: PM's PRDs appear in "today's tasks", inflating apparent backlog and breaking sprint health math.
