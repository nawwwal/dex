# Assistant — God Mode Dispatch Table

This file defines the full signal detection and dispatch logic for `/assistant`. Referenced from SKILL.md during signal detection.

## Signal Detection Rules

Examine ALL signals simultaneously. Multiple modes can be active. Run everything that applies (max 3 operations per invocation — pick the highest-priority ones).

### Temporal Signals

| Condition | Weight | What to run |
|---|---|---|
| Sessions today = 0 AND time before 12pm IST | HIGH | Full Morning Mode |
| Sessions today = 0 AND day = Monday | HIGH | Morning Mode + /log plan |
| Sessions today = 0 AND day = Friday | HIGH | Morning Mode + week kickoff reminder |
| Time after 6pm IST OR "wrapping up" / "done for today" | HIGH | /log (eod trigger) |
| Day = Friday + "wrapping up" | HIGH | /log eod + /log week |
| Days to leave ≤ 14 | MANDATORY | Append leave risk to ANY output |
| Days to leave ≤ 3 | MANDATORY | Everything framed around handoff urgency |

### $ARGUMENTS Signals (explicit overrides — highest priority)

If $ARGUMENTS is set, treat it as a direct mode override BEFORE checking other signals.

| $ARGUMENTS contains | Force mode |
|---|---|
| "morning" | Morning Mode |
| "challenge [X]" | Challenge Mode on X |
| "clean up" / "mom" / "housekeeper" | Housekeeper Mode |
| "plan my week" / "7 days" / "7plan" | /log plan |
| "tell [name]" / "message [name]" / "dm [name]" | Communication Mode |
| "trace [X]" / "history of [X]" | /think trace on X |
| "ideas for [X]" | /think leverage on X |
| "map" | /think graph |
| "answer as me" / "ghost write" | Ghost Mode |
| "emerge" / "any patterns" | /think emerge |
| "drift" / "what's quiet" | /think drift |
| "backlinks" | /think graph |

### Conversation Content Signals

Read the conversation for these signals:

| Signal | What to run |
|---|---|
| Google Doc / Sheets URL in message | Read doc + /emerge for connections to current projects |
| Project name mentioned + question | Context Mode (QMD + decisions + sessions for that project) |
| "stuck" / "don't know" + topic | /think challenge + /think leverage on that topic |
| Frustration signal ("annoyed", "ugh", frustrated tone) | Acknowledge + /drift (what's piling up?) |
| Strategy doc discussed | /think emerge (what connects to current work?) + career implications |
| Meeting in next 60 min (from live context) | Meeting Prep: pull project context for that meeting |
| FY27 / growth pod / strategy mentioned | Connect to Agent Marketplace + Growth pod allocation |

### Vault State Signals (from live injected context)

| Signal | What to run |
|---|---|
| Open tasks > 10 | Surface top 3 + flag as "task debt" |
| ANY project 7+ days silent | /think drift is MANDATORY — surface in every mode |
| No session journals today | Morning Mode is the right mode |
| Sessions exist today | Context/EOD mode is likely right |

## Priority Resolution

When multiple operations apply, pick the 3 highest-priority ones:

1. **Communication Mode** always runs first if communication trigger present (people waiting)
2. **/think drift flag** always included if silences exist (can be a one-liner, doesn't need to be the focus)
3. **Temporal mode** (Morning/EOD/Week) next
4. **Content-triggered mode** (Challenge, Ideas, Trace, etc.) last

## Output Format

Always report outcomes, never process:

```
[What time it is, what day, any critical context]
→ [Outcome 1 — most urgent]
→ [Outcome 2]
→ [Outcome 3 if applicable]
→ [Drift flag if any silences — even one line]
→ [Leave risk if ≤ 14 days]
```

One line per finding. No explanations of what tools were used. No "let me check X" — check it and report.
