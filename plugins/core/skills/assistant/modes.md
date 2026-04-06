# Assistant — Mode Execution Details

Detailed instructions for each mode. Referenced from SKILL.md when a mode is active.

## Morning Mode

**Runs when:** First session of day + morning hours, or $ARGUMENTS = "morning"

**Steps:**
1. Read `memory/goals.md` — surface priorities AND check for promotion case deadline (PD II case)
2. **Read TODAY's session journals first** (`sessions/YYYY-MM-DD-*.md`) — know what's already been done today before suggesting anything. Never re-suggest completed work.
3. Read yesterday's `^carry-forward` sections — what was unfinished
4. Call `get_events` for today — meetings with times and people
5. Search Slack: `from:@nawal.deepakbhai after:{yesterday}` — threads needing follow-up
6. Search Slack for messages TO @nawal — unanswered asks
7. Check DevRev: `list_issues` owned by self — overdue items
8. Inline: run /assistant drift — if silences, surface top one as first action
9. If standup day (Mon–Fri, check `get_events` for recurring standups): draft standup and send to the user's DM (U09KQAFK740) immediately, no asking
10. If meeting in 60 min: pull project context for that meeting inline

**Output format — always end with ONE concrete recommendation, never a question:**
```
{Time of day}. Here's your day:
→ DONE TODAY: [what today's sessions show was already completed]
→ URGENT: [most overdue/blocked item — specific action]
→ Calendar: [next meeting, free blocks]
→ Slack: [unanswered thread or "clear"]
→ [Drift flag if any silences]
→ [Leave risk if ≤ 14 days]

→ Start with: [the ONE thing to do next — concrete, not "what do you want to work on?"]
```

**Critical:** The final line must always be "Start with: [specific action]" — never end with a question.

## EOD Mode

**Runs when:** "wrapping up", "done for today", "eod", time after 6pm

**Invoke /assistant eod directly.** Don't re-implement — just call it.

If Friday: also invoke /assistant week after /assistant eod.
After /assistant eod: offer /assistant emerge (graduation mode) — "Any insights worth keeping from today's sessions?"

## Week Mode

**Runs when:** Friday + "wrapping up", or $ARGUMENTS contains "week"

**Invoke /assistant week directly.** /assistant week already calls /assistant drift at start and /assistant emerge (graduation mode) at end.

## Communication Mode

**Runs when:** "tell X about Y", "message X", "dm X", "email X", "draft for X"

1. Load `memory/voice.md`
2. Resolve recipient from `memory/people.md` — get Slack ID
3. Draft in the user's voice: short, "hey [name]" opener, no sign-off, Hinglish when natural
4. Show draft with recipient + channel context
5. Wait for "send" / "go" / "yep"
6. Send via `slack_send_dm` or `slack_send_message`
7. Confirm: "Sent to [name] in [channel/DM]"

**Sending to self (DM to U09KQAFK740):** Bulletin drafts, standup drafts, EOD recaps — send directly without asking.

## Context Mode

**Runs when:** "what's the status of X", "what did we decide", "when did we last work on X"

1. QMD query across relevant collections
2. Read decisions.md for matching `^dec-` block IDs
3. Read recent sessions mentioning the topic
4. Check DevRev if there's a linked enhancement
5. If topic is a project + "how did it evolve" → run /assistant trace instead

## Ghost Mode

**Runs when:** "answer X as me", "ghost write my answer", "what would I say about X"

1. Load `memory/voice.md` + `memory/goals.md`
2. QMD query for the question topic
3. Synthesize from decisions + patterns + sessions
4. Draft in the user's voice — show draft, never send unseen
5. If nothing in vault: say so, don't fabricate

## Housekeeper Mode

**Runs when:** "clean up", "organize", "mom mode", "housekeeper", "what's messy"

Run `/assistant graph` — it executes as a forked Explore agent and returns a report. Present the report, wait for user to say "do 1, 3" or "do all" before applying changes.

## Meeting Prep Mode

**Runs when:** Meeting detected in next 60 min from `get_events`

1. Identify which project the meeting relates to (read meeting title + attendees)
2. Read `work/{slug}/index.md` for context
3. Read recent sessions mentioning that project
4. Surface: last decision, open carry-forwards, who's in the meeting and their roles (from people.md)
5. One-paragraph brief: "You have [meeting] in [X] min. Context: [2-3 key facts]"

## Plan Mode

**Runs when:** "plan my week", "7 days", "next week", $ARGUMENTS = "plan"

**Invoke /assistant plan directly.**

## Challenge Mode

**Runs when:** "challenge X", "argue against", "pre-mortem"

**Invoke /assistant challenge with the topic from $ARGUMENTS or conversation.**

## Ideas Mode

**Runs when:** "ideas for X", "what could I explore"

**Invoke /assistant leverage with the scope from $ARGUMENTS or conversation.**
