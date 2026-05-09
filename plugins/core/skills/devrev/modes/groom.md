# Groom Mode

Goal: Backlog health check. Review all open issues, surface what's unassigned, stale, or missing metadata, then apply sprint assignments and fixes in one confirmed batch.

Run before sprint planning, or any time the backlog feels messy.

---

## Phase 1 — Fetch (1 MCP call)

**A (Fetcher):** `list_issues(owned_by=[$USER_DON], state=["open"])` → JSON array.

Filter via script immediately after:

```bash
echo '<A_json>' | python3 "$CLAUDE_SKILL_DIR/scripts/filter_issues.py" groom_buckets \
  --active-sprint "$ACTIVE_SPRINT_DON" \
  --today "$(date +%Y-%m-%d)"
```

Script returns:
```json
{
  "no_sprint": [...],
  "active_sprint": [...],
  "future_sprint": [...],
  "no_effort": [...],
  "no_body": [...],
  "stale": [...],
  "counts": { "total": N, "no_sprint": N, ... }
}
```

---

## Phase 2 — Show snapshot

Active sprint issues are **in flight — skip them entirely**. Show them as a single line of context only. Focus the output on no-sprint and future-sprint issues.

```
Backlog — <date>

In flight (Sprint <active>, not shown): N issues
Future (Sprint <next>):                 N issues
True backlog (no sprint):               N issues ← focus

Needs attention (future + backlog only):
  No effort estimate: N
  No body/context:    N
  Overdue To Dos:     N

─── True backlog (no sprint) ───
| ISS | Title | ENH | Effort |
|-----|-------|-----|--------|
| ISS-XXXX | ... | ENH-XXXXX | Xd |
...

─── Future sprint issues needing fixes ───
Only show if no_effort or no_body. Skip if clean.
| ISS | Title | Sprint | Effort | Body? |
|-----|-------|--------|--------|-------|
...

─── Stale (overdue To Dos, any sprint) ───
| ISS | Title | Sprint | Due | Days overdue |
|-----|-------|--------|-----|-------------|
...
```

**Overlap check (probabilistic — main thread, no agent):**
Scan no-sprint titles against active-sprint titles for keyword overlap (same feature area). Flag pairs where a backlog issue likely duplicates an in-flight one:
```
Possible duplicates:
  ⚠ ISS-XXXX "Connectors: Setup flow" ← may overlap ISS-YYYY "Connectors: Setup journeys" (Sprint 26)
```
Surface these before Q&A so the user can close them rather than assign them to a sprint.

---

## Phase 3 — Q&A (probabilistic, 3 questions max)

Ask ONLY about no-sprint and future-sprint issues. Never ask about active-sprint issues.

1. **"Any of these look like duplicates of Sprint <active> work? Close them?"**
   Show the overlap pairs flagged above. Example answer: "Yes, close ISS-XXXX."

2. **"Which remaining backlog issues should go to Sprint $NEXT_SPRINT? Which sprint beyond that?"**
   Example answer: "Cards/Inbox/Analytics → Sprint 27. Catalog + Install → Sprint 28."

3. **"Any effort corrections before we apply?"**
   Example: "Catalog Card should be 3d not 2d."

Do NOT ask more than 3 questions. The user has the full table in front of them.

---

## Phase 4 — Draft table (do NOT write yet)

From user answers, generate the proposed changes:

| ISS | Title | Action | Sprint | Effort |
|-----|-------|--------|--------|--------|
| ISS-XXXX | My Agents: Cards | assign sprint | Sprint 27 | 2d |
| ISS-XXXX | Catalog Detail | assign sprint | Sprint 28 | 2d |
| ISS-XXXX | Agent Analytics | close | — | — |
| ISS-XXXX | WhatsApp wizard | fix effort | Sprint 27 | 1d |

**Do NOT write to DevRev until user confirms.**

Wait for: "go", "apply", "yes", "looks good", or equivalent.

---

## Phase 5 — Apply (after user confirms)

For issues being assigned a sprint (no dates — sprint planning does dates):

```
update_issue:
  id: <DON>
  sprint: <target_sprint_don>
  tnt__remaining_effort: <effort as float>
  priority_v2: <1–4 if specified, otherwise omit>
```

For issues being closed (stage must step through In Progress first — gotchas.md #5):

```
update_issue:
  id: <DON>
  stage: don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/44   ← In Progress
```
then:
```
update_issue:
  id: <DON>
  stage: don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/26   ← Completed
```

For effort-only fixes (no sprint change):

```
update_issue:
  id: <DON>
  tnt__remaining_effort: <corrected float>
```

Run updates in parallel where there are no sequential stage dependencies.

---

## Phase 6 — Verify (mandatory)

After all writes, call `get_issue` for each updated issue and compare:

| Field | Expected | Actual | Match? |
|-------|----------|--------|--------|
| sprint | <target DON> | <from get_issue> | ✓ / ✗ |
| tnt__remaining_effort | <float> | <from get_issue> | ✓ / ✗ |
| stage | <target DON> | <from get_issue> | ✓ / ✗ |

Show summary:
```
Groomed: N issues
  ✓ ISS-XXXX — assigned Sprint 27
  ✓ ISS-XXXX — effort 2d → 1d
  ✗ ISS-XXXX — sprint mismatch (retried)
  ✓ ISS-XXXX — closed
```

## Phase 7 — Update memory (mandatory, immediately after verify)

Apply the update-memory rule from SKILL.md. Read `devrev-sprint.md`, then write back:

1. Set `last_synced` to `<today> (groom)`
2. For issues assigned to a sprint: update their `Sprint` column in the Track B table
3. For closed issues: remove their row from the Track B table (or append `closed <date>` to Notes)
4. For new sprint assignments not yet in the table: append a row

---

## Sprint DON lookup

To assign a future sprint, resolve its DON from `devrev-sprint.md` (loaded in Step 0 context):

- If `$ARGUMENTS` names a sprint ("Sprint 27"), match from the upcoming sprints table.
- Never pass sprint names to the API — always pass the full DON string.
