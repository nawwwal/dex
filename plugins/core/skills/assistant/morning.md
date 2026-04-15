# Morning Briefing

Start-of-day synthesis. Runs when first session of day + morning hours, or $ARGUMENTS = "morning".

## Steps

1. **Read today's sessions first** (`~/.claude/log/YYYY-MM-DD-*.md`) — know what's already done. Never re-suggest completed work.
2. Read yesterday's `^carry-forward` sections — what was unfinished.
3. Read `~/.claude/TASKS.md` — overdue, due today, quick wins.
4. Read `memory/goals.md` — surface priorities, check promotion case deadline.
5. `get_events` for today — meetings with times and people.
6. Slack: `from:@nawal.deepakbhai after:{yesterday}` — threads needing follow-up.
7. Slack: messages TO @nawal — unanswered asks.
8. DevRev: `list_issues` owned by self — overdue items.
9. **DevRev Sync (MANDATORY):** Read and execute `devrev-sync.md` — auto-apply in morning mode (no approval step). Report delta inline.
10. Drift check: any project 5+ days without a session? Surface top silence.
11. If standup day (Mon-Fri, check `get_events`): draft standup, send to user's DM (U09KQAFK740) immediately.
12. If meeting in 60 min: read `meeting-prep.md` for that meeting.

## Output Format

Always end with ONE concrete recommendation, never a question.

```
{Time of day}. Here's your day:
→ DONE TODAY: [what today's sessions show was already completed]
→ URGENT: [most overdue/blocked item — specific action]
→ Calendar: [next meeting, free blocks]
→ Slack: [unanswered thread or "clear"]
→ DevRev: [N created, N updated, N completed, N hygiene flags]
→ [Drift flag if any silences]
→ [Leave risk if ≤ 14 days]

→ Start with: [the ONE thing to do next — concrete, not "what do you want to work on?"]
```
