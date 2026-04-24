# DevRev Sync — Source of Truth Automation

Keeps DevRev in perfect sync with reality by scanning Slack, calendar, and conversation context. Runs as part of Morning Mode, EOD Mode, or standalone.

## Trigger Phrases
- "sync devrev", "update devrev", "devrev hygiene"
- Runs automatically inside Morning Mode (Step 7) and EOD Mode (Step 3)

## Identity Constants

```yaml
devrev_user: don:identity:dvrv-in-1:devo/2sRI6Hepzz:devu/11830
slack_user_id: U09KQAFK740
slack_mention_pattern: "<@U09KQAFK740"
default_part: don:core:dvrv-in-1:devo/2sRI6Hepzz:product/31  # PROD-31 "Design" — fallback for unmatched tasks
task_type: Design
timezone: Asia/Kolkata

# Known project parts (high-confidence routing)
agent_studio_design: don:core:dvrv-in-1:devo/2sRI6Hepzz:enhancement/18008  # ENH-18008 "M2: Launch 100 Merchants" — all Agent Studio Phase 2 design issues
```

## Stage IDs

```yaml
to_do: don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/67
in_progress: don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/44
completed: don:core:dvrv-in-1:devo/2sRI6Hepzz:custom_stage/26
```

## Stage Transition Rules

- Cannot jump directly from To Do to completed. Must go: To Do -> In Progress -> completed.
- Pass stage as a DON ID string, never as `{"name": "..."}`.
- When `get_valid_stage_transitions` returns null from In Progress, writing `custom_stage/26` directly still works.

## Step 1: Gather Current DevRev State

```
list_issues owned_by: [self] state: ["open", "in_progress"]
```

Build a mental map:
- For each open issue: note display_id, title, part, sprint, stage, target_start_date, target_close_date, body
- Group by part/enhancement
- Flag: issues with no target dates, issues In Progress for 3+ days with no activity, issues past target_close_date

Store this as `current_issues` for comparison in later steps.

## Step 2: Scan Slack for Action Items

Search Slack for recent threads mentioning you:

```
slack_search_public_and_private: "@nawal" in the last 24 hours
```

Also check key project channels for threads where you're tagged. For each thread found:

1. Read the full thread (not just the mention)
2. Extract action items assigned to you — look for patterns:
   - Your name/mention + verb (review, fix, design, ship, test, merge)
   - Status indicators: "In Review", "In Progress", "PR Review", "Merged", "Deployed", "Blocked", "To be Clarified"
   - Deadlines: "by tomorrow", "EOW", "today", "first half", specific dates
   - Linked docs: Google Docs URLs, GitHub PRs, Figma links
3. For each action item, capture:
   - `title`: concise task name
   - `status`: mapped to DevRev stages (see Status Mapping below)
   - `deadline`: inferred target_close_date
   - `context`: the full thread context, linked docs, who assigned it
   - `channel`: which Slack channel (used for part resolution)
   - `blockers`: anything flagged as blocking you

### Status Mapping (Slack -> DevRev Stage)

| Slack keyword | DevRev stage |
|---|---|
| "To Do", "not started", "to be clarified" | To Do |
| "In Progress", "working on", "WIP" | In Progress |
| "In Review", "PR Review", "under review" | In Progress (add "In Review" to body) |
| "Merged", "Deployed", "Done", "Shipped" | completed |
| "Blocked" | In Progress (add blocker comment) |

## Step 3: Resolve Parts (Critical — Don't Dump Everything in One Bucket)

For each action item from Slack, determine the correct DevRev part:

1. **Channel-based resolution:** Map Slack channels to known parts. Build this mapping from the user's existing issues — check which parts their issues are under and which Slack channels those projects use.

   Known mappings (use these before searching):
   - Agent Studio / Nexus / merchant journey / design sprint → ENH-18008 (`agent_studio_design`)
   - Generic design work, decks, misc → PROD-31 (`default_part`)

2. **Keyword-based resolution:** Use `hybrid_search` with namespace "part" to find matching enhancements:
   ```
   hybrid_search query: "{action item title} {channel context}" namespace: "part"
   ```
   Pick the highest-scoring result that the user already has issues under.

3. **Existing issue matching:** Before creating a new issue, check if any `current_issues` (from Step 1) already cover this work. Match by:
   - Title similarity (>70% overlap in key terms)
   - Same part + similar timeframe
   - If match found: UPDATE the existing issue instead of creating a new one

4. **Fallback:** If no part matches with confidence, use PROD-31 "Design" as the default. Tasks like event presentations, decks, misc design work all go here.

### Part Resolution Confidence Levels

- **HIGH:** Channel directly maps to a known part (e.g., agent marketplace channel -> ENH-17869)
- **MEDIUM:** hybrid_search returns a part where user already has issues, score > 0.5
- **LOW:** No clear match -> use PROD-31

Always tell the user which part you chose and why, so they can correct if wrong.

## Step 4: Resolve Sprint

For each part, find the active sprint:

1. Check the user's existing issues under that part — what sprint are they in?
2. Use that sprint ID for new issues under the same part.
3. If no existing issues to reference, check via `list_sprint` or `get_sprint_board`.

Sprint must be active (not planned, not completed).

## Step 5: Create or Update Issues

### For NEW action items (no matching existing issue):

```
create_issue:
  title: {concise title from Slack}
  applies_to_part: {resolved part DON ID}
  owned_by: [self]
  subtype: task                         # always task, not story — gives access to estimated_effort field
  sprint: {resolved sprint ID}
  target_start_date: {ISO 8601 with +05:30 — IST midnight = UTC 18:30 previous day}
  target_close_date: {ISO 8601 with +05:30 — IST end of day = UTC 18:29:59 same day}
  tnt__remaining_effort: {effort in days, float — e.g. 1, 1.5, 2}
  tnt__skills: ["Design"]
  body: |
    {Contextual summary from Slack thread}

    **Source:** {Slack thread link}
    **Status from Slack:** {original status text}
    **Linked docs:**
    - {any Google Docs, GitHub PRs, Figma links from the thread}

    **Blockers:** {if any}
```

**Post-creation note:** `ctype__task_type` defaults to "Engineering" and cannot be set via API. Update it to "Design" in the DevRev UI after bulk creation.

### For EXISTING issues that need updates:

Compare Slack reality against `current_issues`:

1. **Stage changes:** If Slack says "Merged" but DevRev says "In Progress" -> transition to completed
2. **Date shifts:** If Slack mentions a new deadline -> update target_close_date
3. **Context enrichment:** If the Slack thread has new docs/links not in the issue body -> update body
4. **Blocker comments:** If you're blocked on something, add a comment via `add_comment`:
   ```
   add_comment:
     object: {issue DON ID}
     body: "Blocked: {reason from Slack}. Waiting on {person}."
   ```

### For MOVED/RESCHEDULED items:

If an issue's work was pushed (e.g., "doing this next week instead"):
```
add_comment:
  object: {issue DON ID}
  body: "Rescheduled from {old_date} to {new_date}. Reason: {context from Slack or conversation}."
```
Then update target_start_date and target_close_date.

## Step 6: Hygiene Pass

After sync is complete, check for:

1. **Missing dates:** Open/In Progress issues with no target_start_date or target_close_date
2. **Stale In Progress:** Issues in "In Progress" where target_close_date is 2+ days past
3. **Orphan issues:** Open issues not in any sprint
4. **Empty bodies:** Issues with no description — fill from Slack context if available
5. **Completed but not closed:** Issues where Slack shows "Merged/Deployed" but DevRev still shows open

Report findings as a hygiene checklist. For items with clear fixes (dates, stage transitions), apply them automatically. For ambiguous items, ask the user.

## Step 7: Report

Output format:

```
DevRev Sync Complete:
  Created: {N} new issues
  Updated: {N} existing issues
  Completed: {N} issues marked done
  Hygiene: {N} issues flagged

  New:
  - ISS-XXXXX: {title} -> {part name} (Sprint N, due {date})
  - ...

  Updated:
  - ISS-XXXXX: {title} — {what changed}
  - ...

  Completed:
  - ISS-XXXXX: {title}
  - ...

  Hygiene flags:
  - ISS-XXXXX: {issue} — missing target date
  - ...
```

## Date Inference Rules

When Slack doesn't give an explicit deadline:

| Signal | target_start_date | target_close_date |
|---|---|---|
| "today" / "by EOD" | today | today |
| "tomorrow" / "by tomorrow" | today | tomorrow |
| "EOW" / "this week" / "by Friday" | today | Friday |
| "next week" | next Monday | next Friday |
| "first half" (of day) | today | today (morning) |
| No signal, status is "In Progress" | today | today + 1 day |
| No signal, status is "To Do" | tomorrow | tomorrow + 1 day |
| Effort mentioned: "1 day" | start | start + 1 day |
| Effort mentioned: "2 days" | start | start + 2 days |

Skip weekends when calculating dates. Thursday (Builder Day at Razorpay) should be skipped for design work unless explicitly scheduled.

## Contextual Data to Include in Issue Body

Always include in the issue body when available:
- Summary of what the task is about (from Slack thread context)
- Slack thread link (for traceability)
- Google Doc links (PRDs, specs, one-pagers)
- GitHub PR links
- Figma links
- Who assigned it / who's waiting on it
- Any technical context (API changes, dependencies)
- Blockers and their owners

## Error Handling

- If part resolution fails entirely, create under PROD-31 and flag to user
- If sprint can't be found, create without sprint and flag as "no sprint assigned"
- If stage transition fails (e.g., can't go from completed back to To Do), try intermediate transitions
- Never silently skip an action item — always report what was processed and what was skipped
