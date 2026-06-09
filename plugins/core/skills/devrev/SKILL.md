---
name: devrev
description: "DevRev sprint management. Modes: morning (default), eod, plan, sprint, groom, enrich. Usage: /devrev [mode] [args]"
argument-hint: "[morning|eod|plan|sprint|groom|enrich] [feature-keyword | URL | doc-name]"
allowed-tools: Bash, Read, Write, Task, mcp__qmd__search, mcp__qmd__get,
  mcp__devrev_remote_mcp_server__get_tool_metadata,
  mcp__devrev_remote_mcp_server__discover_schema,
  mcp__devrev_remote_mcp_server__get_self,
  mcp__devrev_remote_mcp_server__hybrid_search,
  mcp__devrev_remote_mcp_server__list_objects,
  mcp__devrev_remote_mcp_server__create_object,
  mcp__devrev_remote_mcp_server__update_object,
  mcp__devrev_remote_mcp_server__link_objects,
  mcp__devrev_remote_mcp_server__fetch_object_context,
  mcp__devrev_remote_mcp_server__add_comment,
  mcp__devrev_remote_mcp_server__get_sprint,
  mcp__devrev_remote_mcp_server__get_sprint_board,
  mcp__devrev_remote_mcp_server__get_valid_stage_transitions,
  mcp__claude_ai_Slack__slack_search_public_and_private,
  mcp__claude_ai_Slack__slack_read_channel, mcp__claude_ai_Slack__slack_read_thread,
  mcp__claude_ai_Google_Drive__read_file_content, mcp__claude_ai_Google_Drive__search_files
---

# DevRev Skill — Generic Sprint Manager

No hardcoded DON IDs. All personal context loaded from memory. Shareable across users.

## Step 0 — Load and validate context

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/lib_memory.py" validate \
  "$HOME/.agents/memory/reference/devrev.md" \
  "$HOME/.agents/memory/records/devrev-sprint.md"
```

If `ok: false` — abort: "DevRev memory incomplete. Run `/devrev init` to set up."

If `ok: true` — extract placeholders from `context`:
- `$USER_DON`, `$SPRINT_BOARD`, `$DEFAULT_PART`, `$SLACK_MENTION`
- `$ACTIVE_SPRINT_DON`, `$ACTIVE_SPRINT_START`, `$ACTIVE_SPRINT_END`
- `$ISSUE_CONVENTIONS`

Load `gotchas.md` (Read tool) for any mode that writes to DevRev. Gotcha #9 (user scoping) applies to every fetch.

## DevRev MCP contract check

At the start of every `/devrev` run, before any DevRev read or write:

1. Call `get_tool_metadata()`.
2. Call `discover_schema()` with no arguments and cache the returned action names.
3. Before any action, call `discover_schema(action_name="<action>")`; for task issues, call `discover_schema(action_name="<action>", subtype="task")`.
4. Use the generic action tools:
   - `list_objects(action_name="list_issues", values={...}, fields=[...])`
   - `create_object(action_name="create_issue", subtype="task", values={...})`
   - `update_object(action_name="update_issue", subtype="task", values={...})`
   - `link_objects(action_name="link_issue_with_issue", ...)`

Do not assume old dedicated tools such as `list_issues`, `create_issue`, `update_issue`, or `get_issue` exist. If a host still exposes dedicated wrappers, use them only after checking their current schema/metadata.

**Sprint action name:** prefer the action name returned by `discover_schema()` for sprints. Current MCP action inventory exposes `list_sprints`; older metadata may still mention `list_sprint`. If the two disagree, use the action inventory, then verify with a one-row read.

**Sprint freshness check:**

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/sprint_state.py" freshness \
  --memory "$HOME/.agents/memory/records/devrev-sprint.md"
```

If stale: prompt user to confirm sprint rollover, then update `devrev-sprint.md`.

## Step 1 — Mode dispatch

Parse `$ARGUMENTS`. Apply these rules IN ORDER:

1. If $ARGUMENTS contains "sprint" (anywhere) AND (first token is "plan" OR phrase matches "plan my sprint" / "plan sprint" / "sprint plan") → `modes/sprint.md` (planning sub-mode)
2. If $ARGUMENTS contains "plan" and a feature keyword (not "sprint") → `modes/plan.md`
3. Otherwise match first token:

| Token | Mode file |
|---|---|
| (empty) or `morning` | `modes/morning.md` |
| `eod` | `modes/eod.md` |
| `plan` | `modes/plan.md` |
| `sprint` | `modes/sprint.md` |
| `groom` | `modes/groom.md` |
| `enrich` | `modes/enrich.md` |

Unknown token → list modes and exit.

Read mode file + `gotchas.md`. Substitute Step 0 placeholders into mode logic.

## Subagent rules (applies to all modes)

- Every `list_objects(action_name="list_issues", ...)` call MUST include `owned_by=[$USER_DON]`. No exceptions.
- Always pass a tight `fields` array and `limit <= 100`. Fetch only fields the mode needs.
- Verify `owned_by == $USER_DON` on every `fetch_object_context` or issue read result before use.
- Subagents return structured data only — tables, JSON arrays, bullet lists. No prose.
- No double-fetching: if agent A fetched data, agent B filters it, never re-fetches.
- Token budget per agent: 500 tokens max.
- Parallelize only independent agents. Sequential when B needs A's output.

**Fetcher prompt:** "Call `<tool>(<params>)` and return as markdown table. No analysis. No prose. Just the table."

**Analyzer prompt:** "Given data below, identify `<criterion>`. Return bulleted list with severity. Max 10 bullets, 200 words."

**Drafter prompt:** "Given inputs, draft `<output>`. Return markdown diffs. Max 400 words."

## Determinism rule

Deterministic work → Python script. Probabilistic/judgment work → LLM.

Scripts: date math, sprint health, JSON filtering, regex audits, memory validation.
LLM: semantic dedup, story drafting, focus recommendation, blockers narrative.

**NEVER use inline `python3 -c "..."` for date calculation or JSON parsing.** Always call named scripts. Inline one-liners bypass weekend validation and produce silent errors.

## Part resolution

Before every `create_object(action_name="create_issue")`, resolve `applies_to_part`:

1. Read the project map from `devrev.md` (already loaded in Step 0 context).
2. Match issue title and context keywords against project names:
   - "Dev X" / "dashboard" / "FEAT-301" → FEAT-301 feature DON
   - "Agent Studio" / "connectors" / "My Agents" / "Activity" / "Catalog" / "Install" / "Agent Builder" / "Delights" → matching ENH DON from memory
3. If match found → use that DON.
4. Only if no match → fall back to `$DEFAULT_PART` and warn the user.

## Date computation rules

All date assignments MUST use the scripts. Never compute dates mentally.

```bash
# For a task starting on a given date with N days effort:
python3 "$CLAUDE_SKILL_DIR/scripts/lib_dates.py" schedule_task <start_iso> <effort_days>
# Returns: {"start": "YYYY-MM-DD", "close": "YYYY-MM-DD", "start_ist": "...", "close_ist": "..."}
```

Rules enforced by the script:
- If `start_date` falls on a weekend → advances to next Monday
- `close_date` = last working day of the task, skipping weekends
- All returned strings include `+05:30` offset (gotchas.md #7)

For sequential task scheduling (sprint planning), chain: next task starts = `add_working_days(prev_close, 1)`.

**Always derive day-of-week from the date object, never assume.** May 5 2026 is Tuesday. Run `lib_dates.py` to get the correct date, then name it from the computed weekday.

## list issue guidance

`list_objects(action_name="list_issues")` now supports `limit` and `fields`. Use both. Always add at least one domain filter:
- `sprint=[$ACTIVE_SPRINT_DON]` — current sprint only
- `applies_to_part=[specific_enh_don]` — single enhancement
- `target_close_date` range — upcoming issues only

When ISS IDs are already known (from memory or prior fetch), use `fetch_object_context` for the specific issues instead of a broad list. For list calls, request only the fields the mode will use, for example `["id","display_id","title","owned_by","stage","subtype","sprint","target_start_date","target_close_date","tnt__remaining_effort","ctype__task_type"]`.

## Writing conventions

Always use from `$ISSUE_CONVENTIONS`:
- `target_start_date`: computed via `lib_dates.py schedule_task`, format `YYYY-MM-DDT00:00:00+05:30`
- `target_close_date`: computed via `lib_dates.py schedule_task`, format `YYYY-MM-DDT18:29:59+05:30`
- stage: use schema-discovered `stage` IDs for deterministic updates; `stage_name` exists but can vary by subtype
- effort: `tnt__remaining_effort` as float days
- task type: for task issues, include `ctype__task_type: "Design"` whenever the `subtype="task"` schema exposes it

Do not surface manual UI reminders for task type unless schema discovery proves `ctype__task_type` is absent or a verified write fails.

## Draft-then-confirm rule (applies to all write modes)

**Never write to DevRev immediately after computing a plan.**

1. Show the user a draft table listing every field that will be written (ISS ID, title, start, close, effort, sprint).
2. Wait for explicit confirmation: "go", "apply", "yes", "looks good", or equivalent.
3. Only then call `update_object` / `create_object`.

This prevents half-applied writes caused by the user adjusting the plan mid-stream.

## All-fields rule for sprint date updates

When updating a task issue's schedule (start, close, effort), all schedule fields plus any schema-required subtype fields must appear in the same `update_object` call:

```
update_object(action_name="update_issue", subtype="task"):
  id: <DON>
  ctype__task_type: "Design"   # include when subtype="task" schema requires it
  target_start_date: <from schedule_task — not from chat table>
  target_close_date: <from schedule_task — not from chat table>
  tnt__remaining_effort: <float>
```

Missing any schedule field is a partial update that creates drift between the draft plan and DevRev. Missing a schema-required subtype field can reject the update.

## Verify-after-write rule (applies to all write modes)

After any batch of `update_object` or `create_object` calls, verify every updated field landed correctly by reading the issue back with `fetch_object_context` or a narrow `list_objects` call by ID.

Compare only the fields that were written. For dates, convert both expected and returned timestamps to IST calendar dates before comparing; DevRev often reads back `Z` timestamps even when writes used `+05:30`. If any field doesn't match:
1. Retry that single field with a corrected call.
2. If retry fails twice, flag it to the user explicitly — never silently skip.

Show a verification summary after every write batch. Format:
```
Applied N issues:
  ✓ ISS-X — <what changed>
  ✗ ISS-Y — <field> mismatch (corrected) / (needs manual fix in DevRev)
```

This prevents the skill from reporting "done" when writes only partially applied.

## Update-memory rule (applies to all write modes)

After verification passes, update `devrev-sprint.md` immediately. Use the Read + Write tools directly — no script, no subagent.

**Always update:**
- `last_synced` → today's date + mode name (e.g. `2026-05-07 (sprint planning)`)

**For sprint assignment or date changes (sprint planning, groom):**
- In the Track B table, update the `Sprint` column for every issue assigned or moved
- Remove rows for closed/deleted issues

**For new issues (plan mode):**
- Append each created issue as a new row to the Track B table
- Include: Issue ID, title, Part DON short-name (e.g. `ENH-18478`), Sprint, any notes

**Format for Track B rows:**
```
| ISS-XXXXX | Title | ENH-XXXXX | Sprint N | Notes |
```

**Never update Track A rows** — those are PM-owned and not the skill's concern.

Do this even if the user doesn't ask. Stale memory causes every subsequent session to re-fetch data that was already known.
