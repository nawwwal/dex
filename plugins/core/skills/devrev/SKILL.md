---
name: devrev
description: "DevRev sprint management. Modes: morning (default), eod, plan, sprint, groom, enrich. Usage: /devrev [mode] [args]"
argument-hint: "[morning|eod|plan|sprint|groom|enrich] [feature-keyword | URL | doc-name]"
allowed-tools: Bash, Read, Write, Task, mcp__qmd__search, mcp__qmd__get,
  mcp__claude_ai_DevRev__get_tool_metadata, mcp__claude_ai_DevRev__get_self,
  mcp__claude_ai_DevRev__hybrid_search, mcp__claude_ai_DevRev__list_issues,
  mcp__claude_ai_DevRev__get_issue, mcp__claude_ai_DevRev__update_issue,
  mcp__claude_ai_DevRev__create_issue, mcp__claude_ai_DevRev__add_comment,
  mcp__claude_ai_DevRev__list_enhancements, mcp__claude_ai_DevRev__get_enhancement,
  mcp__claude_ai_DevRev__fetch_object_context, mcp__claude_ai_DevRev__link_issue_with_issue,
  mcp__claude_ai_DevRev__list_sprint, mcp__claude_ai_DevRev__get_sprint,
  mcp__claude_ai_DevRev__get_sprint_board, mcp__claude_ai_DevRev__get_valid_stage_transitions,
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

- Every `list_issues` call MUST include `owned_by=[$USER_DON]`. No exceptions.
- Verify `owned_by == $USER_DON` on every `get_issue` result before use.
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

Before every `create_issue`, resolve `applies_to_part`:

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

## list_issues guidance

`list_issues(state=["open"])` on a large org returns 100k+ chars and blows context. Always add at least one of these filters:
- `sprint=[$ACTIVE_SPRINT_DON]` — current sprint only
- `applies_to_part=[specific_enh_don]` — single enhancement
- `target_close_date` range — upcoming issues only

When ISS IDs are already known (from memory or prior fetch), use parallel `get_issue` calls instead of `list_issues`. Never fetch more than 20 issues in a single list call.

## Writing conventions

Always use from `$ISSUE_CONVENTIONS`:
- `target_start_date`: computed via `lib_dates.py schedule_task`, format `YYYY-MM-DDT00:00:00+05:30`
- `target_close_date`: computed via `lib_dates.py schedule_task`, format `YYYY-MM-DDT18:29:59+05:30`
- stage: full DON string from `$ISSUE_CONVENTIONS` (see gotchas.md #3)
- effort: `tnt__remaining_effort` as float days

After any `create_issue` batch → surface gotcha #1 reminder.

## Draft-then-confirm rule (applies to all write modes)

**Never write to DevRev immediately after computing a plan.**

1. Show the user a draft table listing every field that will be written (ISS ID, title, start, close, effort, sprint).
2. Wait for explicit confirmation: "go", "apply", "yes", "looks good", or equivalent.
3. Only then call `update_issue` / `create_issue`.

This prevents half-applied writes caused by the user adjusting the plan mid-stream.

## All-fields rule for sprint date updates

When updating an issue's schedule (start, close, effort), ALL THREE fields must appear in the same `update_issue` call:

```
update_issue:
  id: <DON>
  target_start_date: <from schedule_task — not from chat table>
  target_close_date: <from schedule_task — not from chat table>
  tnt__remaining_effort: <float>
```

Missing any one of these fields is a silent partial update — DevRev will silently keep the old value, causing drift between what the user sees in the plan and what is stored. There are no partial field updates in sprint scheduling.

## Verify-after-write rule (applies to all write modes)

After any batch of `update_issue` or `create_issue` calls, verify every updated field landed correctly by reading the issue back with `get_issue`.

Compare only the fields that were written. For dates, compare the `YYYY-MM-DD` portion only. If any field doesn't match:
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
