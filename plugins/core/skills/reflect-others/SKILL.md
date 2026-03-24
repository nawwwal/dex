---
name: reflect-others
description: "Use when pasting content where someone else describes or reacts to the user's work — Slack threads, feedback forms, peer reviews, manager comments, 1:1 notes."
allowed-tools: Read, Write, Bash
---

# /reflect-others

You extract observable third-person signals about the user from pasted content and append them to `~/.claude/memory/nawal-through-others.md`.

## Step 0: Check Queue for Staged Candidates

Before expecting pasted content, check `~/.claude/learnings-queue.json` for pending `reflect-others` entries:

```bash
python3 -c "
import json
try:
    q = json.load(open('$HOME/.claude/learnings-queue.json'))
    pending = [x for x in q if x.get('type')=='reflect-others' and x.get('status')=='pending']
    print(len(pending))
except: print(0)
"
```

If pending entries exist: show a summary ("N staged candidate(s) from recent sessions, detected via signal scoring. Review them now?"). If user says yes, proceed to Step 2 using the staged signals as the source. After writing to nawal-through-others.md, mark those entries `status: done` in the queue.

If no staged entries: proceed normally (expect pasted content).

## Step 1: Detect — Is This Third-Person Content?

Score the pasted content for third-person signals:

| Signal | Score |
|--------|-------|
| Second-person reaction ("you did", "your approach", "I noticed you") | +3 |
| Direct reference ("the user", "Adi", "the user", "the designer") | +3 |
| Feedback form patterns ("strengths:", "areas to develop:", "one thing I'd flag") | +2 |
| Evaluative language ("great ownership", "could improve", "well-crafted", "strong work") | +1 |

**Score >= 3: Extract. Score < 3: Reply "This doesn't look like third-person feedback — nothing to extract."**

Do not extract:
- Forwarded external content about unrelated topics
- Slack threads where the user is the sole author
- Technical discussions with no personal observation about the user

## Step 2: Extract

For each distinct observation in the pasted content:
1. **Source type**: Slack DM / Slack thread / feedback form / 1:1 notes / peer review / manager comment
2. **Quote**: exact or close paraphrase (preserve the other person's voice)
3. **Signal**: one sentence on what this reveals that first-person self-documentation would miss

Multiple observations from one paste = multiple entries.

## Step 3: Append to nawal-through-others.md

Read `~/.claude/memory/nawal-through-others.md` first, then append to the `## Observations` section:

```markdown
### YYYY-MM-DD — [Source type]
**Source:** [Who / context — anonymize role, not name, if sensitive]
**Quote:** "[exact or close paraphrase]"
**Signal:** [what this reveals]
```

Append ONLY to the Observations section. Do not modify the Patterns section.

## Step 4: Confirm

Say: "Logged N observation(s) to nawal-through-others.md."

List each observation as a one-line summary: `• [Source] — [first 8 words of quote]`

## Notes

- Do NOT load nawal-model.md during this skill — model updates happen separately via the existing silent update behavior
- Do NOT fabricate implications — only quote what was actually said/written
- Classify "strength" only if the tone is clearly positive, not neutral
- If in doubt about anonymization, use the role ("my manager", "the FE lead") not the name
