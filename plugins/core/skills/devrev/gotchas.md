# DevRev MCP Current Gotchas

Source: TKT-62791, operational experience, and live MCP schema checks on 2026-06-09.

`SKILL.md` owns the operating rules. This file records why those rules exist when DevRev behaves unexpectedly.

## 1. Schema discovery is mandatory

The DevRev MCP now routes creates, updates, lists, and links through generic tools. Old dedicated calls like `create_issue`, `update_issue`, `list_issues`, and `get_issue` may not exist in the current host.

Effect: follow the MCP contract in `SKILL.md`; do not use old dedicated issue tools unless the host schema proves they exist.

## 2. ctype__task_type is now schema-backed for task issues

The stock issue schema does not show `ctype__task_type`, but the `subtype="task"` schema does. Current task create/update schemas expose `ctype__task_type` with values including `Design`, `Engineering`, `Product`, `Analytics`, `Tech Debt`, and others.

Workaround: For design tasks, call `discover_schema(..., subtype="task")`, then create/update with:
```
subtype: "task"
ctype__task_type: "Design"
tnt__skills: ["Design"]
```

Do not tell the user to fix task type in the UI unless schema discovery omits the field or verification proves the write failed.

## 3. estimated_effort drifts

`estimated_effort` is GET-only in this workflow. It may be derived from `tnt__remaining_effort`, but later remaining-effort updates do not reliably propagate back.

Workaround: Always write and verify `tnt__remaining_effort`. Treat `estimated_effort` as derived/stale unless schema discovery proves it is writable for the current subtype.

## 4. Stage names exist, but stage IDs are safer

Current update schemas expose both `stage` and `stage_name`. `stage_name` enums vary by subtype and can include duplicates or different casing. Stage IDs are deterministic.

Workaround: Prefer the custom stage DON for writes. Use `stage_name` only when the discovered subtype schema has the exact intended value and verification reads back the intended state.

Resolve stage DONs from PMB DevRev context or current subtype schema. Do not ship user-specific stage IDs in the skill.

## 5. get_valid_stage_transitions is only partially reliable

Live check: To Do returns In Progress, but In Progress can still return `null` even when completion is operationally reachable.

Workaround: Use `get_valid_stage_transitions` as advisory evidence. For known task closure, still apply the two-step transition when closing from To Do: To Do -> In Progress -> Completed. Verify the final stage after the write.

## 6. List calls now support limit and fields

The old no-pagination context blowup is repaired enough for normal use: `list_objects(action_name="list_issues")` supports `limit` with a max of 100 and accepts a `fields` projection.

Effect: keep user-owned filters, `limit`, and `fields` projection from `SKILL.md`; fetch bodies only when a mode needs body text.

## 7. Sprint board IDs are not sprint IDs

Sprint boards are `vista` objects with `flavor="sprint_board"`. Issue `sprint` expects the sprint iteration ID, usually shaped like `vista/<board>:vista_group_item/<item>`.

Workaround:
1. `hybrid_search(namespace="vista", query="<team> sprint board")` to find the board.
2. Use the sprint list action returned by `discover_schema()`; current inventory exposes `list_sprints`.
3. Call `list_objects(action_name="list_sprints", values={"parent_id": [board_id], "state": ["active"]})`.
4. Use the returned sprint iteration DON in issue `sprint`.

## 8. Date writes need IST offsets; reads may come back as UTC

Naive ISO strings are parsed as UTC. IST midnight is the previous UTC date at 18:30. DevRev may read back `Z` timestamps even when the write used `+05:30`.

Effect: use `lib_dates.py` for writes and compare returned timestamps as IST calendar dates. Never compare only the first 10 characters of a DevRev timestamp.

## 9. Issues live in two parallel tracks (PM vs user)

Feature areas can have both PM PRDs (full bodies, planning codes, owned by another user) and design tasks (user-owned, often empty bodies). Both may share `applies_to_part` and sprint.

Effect: user-owned issue filters are not optional. PM PRDs are read-only context in `enrich` mode; they never enter the user's task surface, agenda, EOD updates, or velocity calculations.

Failure mode if violated: PM's PRDs appear in "today's tasks", inflating apparent backlog and breaking sprint health math.
