# Skill Tests: log

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "done" → Runs task.md, writes YYYY-MM-DD-{project}-session.md, runs /simplify first
2. "wrapping up this task" → Same as above
3. "eod" (Tuesday) → Runs day.md, writes YYYY-MM-DD-eod.md, runs qmd update
4. "eod" (Friday) → Chains task → day → week → signals /think emerge
5. "morning" → Runs morning.md, writes YYYY-MM-DD-dashboard.html
6. "plan my week" → Runs plan.md, generates Mon-Fri day-by-day plan

## True Negatives (should NOT trigger)
1. "what's the status of the task?" → Not a lifecycle trigger (should not invoke /log)
2. "done button" → In-conversation code reference (context should clarify)
3. "/polish before commiting" → Invokes /polish (now a spec/prose quality skill), not /log

## Edge Cases
1. "done, eod, and plan my week" → Should chain all three in order
2. "done" on a Friday → Should check if it's Friday and extend to week.md
3. "morning" while already in a project dir → Still runs morning.md but skips ~/ context

## Quality Bar
- A "good" /log done: writes a dated session file, runs /simplify, marks TASKS.md items complete
- A "poor" /log done: just summarizes without writing a file, doesn't run /simplify
