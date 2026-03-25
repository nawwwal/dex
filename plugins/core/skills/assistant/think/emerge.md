# Intelligence Synthesis (Emerge)

Synthesizes patterns, insights, and connections from vault data. Uses the vault-synthesizer agent when available.

## Step 1: Read Recent Sessions
```bash
find ~/.claude/log -name "*.md" -newer ~/.claude/log/$(ls -t ~/.claude/log/*.md | tail -1 | xargs basename) 2>/dev/null | head -20
# Fallback: last 14 days
find ~/.claude/log -name "*.md" -mtime -14 2>/dev/null | grep -v compact | sort -r | head -30
```

## Step 2: Read Knowledge Base
- memory/decisions.md — especially recent entries
- memory/patterns.md — patterns added/applied recently
- memory/goals.md — current goals and evidence gaps

## Step 3: Extract TILs
Look for new insights not yet in til/ or learn/:
- Novel approaches tried
- Bugs fixed with non-obvious root causes
- Tool discoveries
- Process improvements

## Step 4: Map to Competencies
For the promotion case, map discoveries to:
- Design Engineering
- Ownership & Delivery
- UI Design
- Product Thinking
- AI Literacy & Leadership
- Customer Connect
- Mentorship

## Step 5: Synthesis Output
Write to memory/goals.md Evidence Log section:
```markdown
### Week of YYYY-MM-DD Evidence
- [competency]: [evidence entry] — [[session link]]
```

## Step 6: Graduate Ideas
Scan session journals for `#idea` tags or phrases like "I should" or "worth exploring".
Promote 1-3 of these to standalone notes in til/ or learn/.

## Step 7: Fabrication Check
Before reporting any "emergent" pattern: search the vault for it stated plainly.
If it already exists in decisions.md or patterns.md — it's not emergent, skip it.

## Confidence Markers
For each synthesis finding, assign:
- `[solid]` — confirmed across multiple sessions/projects
- `[evolving]` — still developing
- `[hypothesis]` — plausible but unconfirmed
