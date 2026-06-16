# Plan Mode

Goal: Story breakdown for a feature area. No dates assigned yet.

Usage: `/devrev plan <feature_keyword>` — second token of $ARGUMENTS is the feature.

## Phase 1 — Parallel fetchers

**A (Fetcher, user-scoped):**
1. `hybrid_search(query=<feature_keyword>, namespace="enhancement")` → find matching enhancement DON
2. `list_objects(action_name="list_issues", values={"owned_by": [$USER_DON], "applies_to_part": [matched_enh], "limit": 100}, fields=["id","display_id","title","owned_by","subtype","ctype__task_type","tnt__remaining_effort"])` → return MY existing design stories

Per subagent rule: `list_objects(action_name="list_issues")` MUST include `owned_by=[$USER_DON]`. Never list without the filter.

Return: JSON array of existing user-owned issues under that enhancement.

**A2 (Fetcher, optional, read-only PM context):**
Only fires when user explicitly asks "what's the PM spec?" or "show me the PRD".
`list_objects(action_name="list_issues", values={"applies_to_part": [matched_enh], "state": ["open"], "limit": 20}, fields=["id","display_id","title","owned_by","body","stage"])` — label results "PM context, not your tasks".
Default: OFF.

**B (Fetcher):**
`slack_search_public_and_private("<feature_keyword> design brief OR PRD after:<14d>")` → brief mentions, PRD links.
Return: bullets with source links.

## Phase 2 — Drafter (sequential, after Phase 1)

**C (Drafter):** Given (A's existing user-owned stories + B's briefs + user's outline/notes), propose net-new story table:

| Title | Effort (days) | Enhancement DON | Dependencies |
|---|---|---|---|
| ... | ... | ... | ... |

Rules for C:
- Skip any title that overlaps A's existing stories (title similarity > 70%)
- Effort: 0.5d increments, range 0.5–5d
- Flag if a story depends on another user-owned story being complete first

## Phase 3 — Apply

Show table to user. On approval:
- Batch create by `applies_to_part` (one batch per enhancement, sequential not parallel — avoids race on same parent)
- Each issue: call `create_object(action_name="create_issue", subtype="task", values={...})` with `subtype: "task"`, `ctype__task_type: "Design"`, `tnt__skills: ["Design"]`, `owned_by: [$USER_DON]`, and `tnt__remaining_effort` per table
- NO sprint, NO dates
- After creation: verify `ctype__task_type`, `tnt__skills`, owner, part, and effort landed

## Phase 4 — Update Sync State

Read `references/sync-state.md`.
Read `## Sync State` in `[[DevRev local knowledge]]`, then overwrite only that section.

Use the section shape and source-coverage rules from `references/sync-state.md`. Set `last_mode: plan`; populate Plate with created/overlapping issues, Signals with context used in the breakdown, and Proposed writebacks for non-Sync-State changes that need confirmation.
