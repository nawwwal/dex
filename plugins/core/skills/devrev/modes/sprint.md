# Sprint Mode

Goal: Sprint management. Auto-detects sub-mode (planning vs check-in) from state.
Override: `/devrev sprint plan` or `/devrev sprint checkin`.

## Sub-mode detection

**Step 0.5 — Light MCP fetch (1 agent):**
`list_issues(owned_by=[$USER_DON], sprint=[$ACTIVE_SPRINT_DON])` → JSON array.

```bash
echo '<issues_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/sprint_state.py" submode \
  --today "$(date +%Y-%m-%d)" \
  --start "$ACTIVE_SPRINT_START" \
  --end "$ACTIVE_SPRINT_END"
```

Returns `{"submode": "planning" | "checkin" | "refresh"}`. User arg overrides.

---

## Planning sub-mode

### Phase 1 — Parallel fetchers (2 MCP agents + scripts)

**A (Fetcher):** `list_issues(owned_by=[$USER_DON], state=["open"])` → JSON array.

**B (Fetcher):** `slack_search_public_and_private("priority OR roadmap after:<7d>")` → priority signals.

**Scripts (after A):**
```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/filter_issues.py" no_sprint
```
Returns issues where `sprint == null`. Client-side filter — do NOT pass `sprint=null` to `list_issues`.

**C-MCP (Fetcher):** `list_issues(owned_by=[$USER_DON], state=["closed"], sprint=[<prev_sprint_don>])` → closed issues from previous sprint for velocity.

```bash
echo '<C_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/sprint_health.py" velocity
```
Returns `{"velocity_days": 7.5, "issues_completed": 5}`.

### Phase 2 — Main thread + user Q&A

Show: backlog (from A's no-sprint filter), priority signals (B), computed velocity (cap), sprint working days.

Ask:
1. "Non-negotiables for this sprint?"
2. "Hard dependencies or sequence requirements?"
3. "Any ad-hocs to add to the backlog first?"

After user responds, propose a sequenced schedule as a **draft table** — do NOT write to DevRev yet:

| # | ISS | Title | Priority | Start | Close | Effort |
|---|---|---|---|---|---|---|
| 1 | ISS-X | ... | P0 | Tue May 5 | Wed May 6 | 2d |
| 2 | ISS-Y | ... | P1 | Thu May 7 | Thu May 7 | 1d |

The `#` column is the intended work order. The `Priority` column is the DevRev `priority_v2` to assign:
- `#1` (first / non-negotiable) → **P0**
- `#2–3` (core sprint work) → **P1**
- `#4+` (important but secondary) → **P2**
- Stretch / blocked issues → **P3**

Ask the user to confirm or adjust priorities before writing. Priorities can be overridden per-issue ("make the Connectors task P0").

The Start/Close values MUST come from `lib_dates.py schedule_task`. Compute each row:

The Start/Close values in this table MUST come from `lib_dates.py schedule_task`, not from mental calculation. Compute each row:

```bash
# Row 1: first task starts today (or first working day)
python3 "$CLAUDE_SKILL_DIR/scripts/lib_dates.py" schedule_task "$(date +%Y-%m-%d)" <effort>
# Row 2: next task starts the working day after row 1 closes
python3 "$CLAUDE_SKILL_DIR/scripts/lib_dates.py" next_sequential_start <row1_close>
python3 "$CLAUDE_SKILL_DIR/scripts/lib_dates.py" schedule_task <row2_start> <effort>
# ... repeat for each task
```

Present the draft table. Wait for explicit user confirmation ("go", "looks good", "yes", "apply").

### Phase 3 — Commit (only after user confirms the draft table)

For every issue in the confirmed schedule, apply ALL of these fields. Never omit any:

```
update_issue:
  id: <ISS DON>
  sprint: $ACTIVE_SPRINT_DON
  target_start_date: <start_ist from schedule_task output>     ← from script, not from chat table
  target_close_date: <close_ist from schedule_task output>     ← from script, not from chat table
  tnt__remaining_effort: <effort as float>
  priority_v2: <1=P0, 2=P1, 3=P2, 4=P3>                      ← from confirmed draft table
  title: <title, only if changed>
```

**ALL FOUR date/effort/priority fields are required in every update_issue call for sprint planning.** If any field is missing, the update is incomplete. Do not assume a field will be preserved from a previous state.

**Recompute from script, do not copy from chat table.** Before each write, run `schedule_task` again for that row. Chat tables are display artifacts; scripts are ground truth.

Run in parallel when no sequential dependency. Run sequentially only when B depends on A's close date.

### Phase 4 — Verify (mandatory, runs immediately after Phase 3)

After all `update_issue` calls complete, fetch each updated issue and check that every field landed correctly.

For each issue updated in Phase 3, call `get_issue(id)` and compare:

| Field | Expected | DevRev actual | Match? |
|---|---|---|---|
| target_start_date | <start_ist> | <from get_issue> | ✓ / ✗ |
| target_close_date | <close_ist> | <from get_issue> | ✓ / ✗ |
| tnt__remaining_effort | <float> | <from get_issue> | ✓ / ✗ |
| sprint | $ACTIVE_SPRINT_DON | <from get_issue> | ✓ / ✗ |

When comparing dates: extract the date portion only (`YYYY-MM-DD`) — ignore time and timezone offset differences in the display format.

If any field mismatches:
- Report: "ISS-XXXX: `target_close_date` mismatch — expected 2026-05-06, got 2026-05-09 (Sat). Will retry."
- Retry that specific field with a corrected `update_issue` call.
- If retry fails twice, surface to user: "Could not set `target_close_date` on ISS-XXXX. Please update manually in DevRev."

Show a summary at the end:
```
Applied: 7 issues
  ✓ ISS-2145097 — Tue May 5 → Wed May 6 · 1d
  ✓ ISS-2077876 — Thu May 7 → Fri May 8 · 2d
  ✗ ISS-2077875 — target_close_date mismatch (corrected on retry)
  ...
```

### Phase 5 — Update memory (mandatory, immediately after verify)

Apply the update-memory rule from SKILL.md. Read `devrev-sprint.md`, then write back:

1. Set `last_synced` to `<today> (sprint planning)`
2. For every issue in the confirmed schedule, update its `Sprint` column in the Track B table to the active sprint number. If the issue is not yet in the table, append a new row.

This step is not optional. The skill must not exit planning mode without updating the sprint record.

---

## Check-in sub-mode (mid-sprint)

Answers: sprint health, days left, accomplished, at-risk, next up. No writes by default.

### Phase 1 — 1 MCP agent

**A (Fetcher):** `list_issues(owned_by=[$USER_DON], sprint=[$ACTIVE_SPRINT_DON])` → JSON array with stage, target_close_date, target_start_date, tnt__remaining_effort.

**B (Fetcher, lazy — only on 🔴 or "why am I behind?"):**
`slack_search_public_and_private("$SLACK_MENTION (blocked OR delayed OR slipped) after:<sprint_start>")` → blocker context.

### Phase 2 — Deterministic synthesis (script, no agent)

```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/sprint_health.py" checkin \
  --today "$(date +%Y-%m-%d)" \
  --start "$ACTIVE_SPRINT_START" \
  --end "$ACTIVE_SPRINT_END"
```

Script returns full data block including health emoji (🟢/🟡/🔴), effort math, done/in-progress/at-risk/idle lists, next-up candidates.

Health rule (in script): 🟢 if pace >= midpoint, 🟡 if behind <= 1.5d effort, 🔴 if behind > 1.5d OR unresolved blocker > 24h.

### Phase 3 — Probabilistic glue (main thread, no agent)

Render output template from script JSON. Add one-line concrete recommendation (judgment). If 🔴: fire Phase 1B now and weave blocker context into the recommendation.

```
Sprint <name>: day <elapsed> of <total> · <days_left> working days left

Health: <emoji> — <reason>
  <done>/<total> issues done · <burned>/<total>d effort
  <pace_label>

Done:        <list>
In progress: <list>
At risk:     <list>
Idle:        <list>
Blockers:    <only if 🔴>
Next up:     <candidates>

→ <one concrete action>
```

---

## Refresh sub-mode

Sprint has ended. Prompt: "Sprint <old> ended. Promote Sprint <next> to active?"
On yes: update `devrev-sprint.md` with new active sprint data.
