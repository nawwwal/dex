---
name: decisions
description: "Use when decisions.md needs archiving — health.md shows 'ARCHIVE NEEDED' or decisions.md exceeds 300 lines. Invoke as /decisions:archive."
allowed-tools: Read, Bash
---

# /decisions

## archive

**Trigger:** health.md shows "ARCHIVE NEEDED", or user says "archive decisions" / `/decisions:archive`.

**Action:** Spawn the `decisions-archivist` agent.

Before spawning, confirm with the user:
> "decisions.md is currently N lines. I'll archive entries older than 60 days to archive/decisions-YYYY-MM.md with thematic summaries, and rewrite the live file with those summaries + recent entries. A backup will be created first. Ready?"

If confirmed, spawn the `decisions-archivist` agent and report the result:
> "Archived N entries across M months. decisions.md is now X lines. Archive files: [list]."

**What the agent does:**
1. Backs up decisions.md to decisions.md.bak
2. Classifies entries: ARCHIVE (>60 days) vs KEEP (<=60 days)
3. Writes verbatim ARCHIVE entries to archive/decisions-YYYY-MM.md
4. Verifies archive before touching live file
5. Rewrites decisions.md: header + thematic summaries + KEEP entries
6. All ^dec- block IDs preserved in archive

**Guardrails:**
- Never runs without confirmation
- Never proceeds if archive write failed
- The .bak file persists until user confirms the result looks correct
