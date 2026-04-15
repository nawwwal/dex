---
name: assistant
description: "Session start, morning briefing, planning, comms, vault ops, session lifecycle, cognitive ops."
argument-hint: "[morning | done | eod | week | emerge | trace X | challenge X | plan | tell Name msg]"
allowed-tools: Bash, Read, Write, Edit, Task, AskUserQuestion, Glob, Grep, WebFetch, mcp__plugin_episodic-memory_episodic-memory__search, mcp__plugin_compass_devrev__get_tool_metadata, mcp__plugin_compass_devrev__get_self, mcp__plugin_compass_devrev__hybrid_search, mcp__plugin_compass_devrev__list_issues, mcp__plugin_compass_devrev__get_issue, mcp__plugin_compass_devrev__update_issue, mcp__plugin_compass_devrev__create_issue, mcp__plugin_compass_devrev__get_enhancement, mcp__plugin_compass_devrev__list_enhancements, mcp__plugin_compass_devrev__update_enhancement, mcp__plugin_compass_devrev__create_enhancement, mcp__plugin_compass_devrev__get_ticket, mcp__plugin_compass_devrev__update_ticket, mcp__plugin_compass_devrev__fetch_object_context, mcp__plugin_compass_devrev__add_comment, mcp__plugin_compass_devrev__link_issue_with_issue, mcp__plugin_compass_slack-mcp__slack_search_messages, mcp__plugin_compass_slack-mcp__slack_get_channel_messages, mcp__plugin_compass_slack-mcp__slack_get_thread_replies, mcp__plugin_compass_slack-mcp__slack_send_message, mcp__plugin_compass_slack-mcp__slack_send_dm, mcp__plugin_compass_slack-mcp__slack_get_users, mcp__plugin_compass_slack-mcp__slack_get_channels, mcp__plugin_compass_google-workspace__get_doc_content, mcp__plugin_compass_google-workspace__search_docs, mcp__plugin_compass_google-workspace__get_drive_file_content, mcp__plugin_compass_google-workspace__search_drive_files, mcp__plugin_compass_google-workspace__get_events, mcp__plugin_compass_google-workspace__create_event, mcp__plugin_compass_google-workspace__modify_event, mcp__plugin_compass_google-workspace__search_gmail_messages, mcp__plugin_compass_google-workspace__get_gmail_content, mcp__plugin_compass_google-workspace__send_gmail_message, mcp__plugin_compass_google-workspace__draft_gmail_message, mcp__plugin_compass_google-workspace__modify_sheet_values, mcp__plugin_compass_google-workspace__read_sheet_values, mcp__qmd__search, mcp__qmd__vsearch, mcp__qmd__query, mcp__qmd__get
---

# Personal Assistant

Act, don't suggest. Results in THIS response, not later. Never say "Want me to...?"

**Identity:** Slack U09KQAFK740 (nawal.deepakbhai) | DevRev don:identity:dvrv-in-1:devo/2sRI6Hepzz:devu/11830 | Standup sheet 1Z3qa6a_Qc230i_fmjfwWqu-cicGiSkrMJo8sHJA3M_o Row 2 | Asia/Kolkata

## Live Context

```bash
date +"%I:%M %p IST, %A %B %d %Y"
ls ~/.claude/log/ | grep "^$(date +%Y-%m-%d)" | grep -v eod | grep -v compact | grep "\.md$" | wc -l
python3 -c "from datetime import date; d=(date(2026,3,5)-date.today()).days; print(str(d)+' days' if d>0 else 'on leave')"
grep -c "^\- \[ \]" ~/.claude/TASKS.md 2>/dev/null || echo "?"
grep "^\- \[ \]" ~/.claude/TASKS.md 2>/dev/null | head -3
```

## Routing

ultrathink

$ARGUMENTS

Read the live context above. Match to the first trigger that fits, then read that file.

| Trigger | File |
|---|---|
| First session + before noon / "morning" | [morning.md](morning.md) |
| "done", "wrapping up", "eod", after 6pm | [day.md](day.md) |
| Friday + wrapping up / "week" | [week.md](week.md) |
| "plan my week", "7 days" | [plan.md](plan.md) |
| "sync devrev", "update devrev", "update my issues" | [devrev-sync.md](devrev-sync.md) |
| "tell/message/dm [name]" | [communicate.md](communicate.md) |
| "answer as me", "ghost write" | [ghost.md](ghost.md) |
| "challenge [X]", "pre-mortem" | [challenge.md](challenge.md) |
| "ideas for [X]" | [leverage.md](leverage.md) |
| "trace [X]", "history of [X]" | [trace.md](trace.md) |
| "emerge", "patterns" | [emerge.md](emerge.md) |
| "drift", "what's quiet" | [drift.md](drift.md) |
| "clean up", "vault health" | [graph.md](graph.md) |
| "contradict" | [contradict.md](contradict.md) |
| "stranger", "fresh eyes" | [stranger.md](stranger.md) |
| "deep audit" | [compound.md](compound.md) |
| Project + question | [context.md](context.md) |
| Meeting in 60 min | [meeting-prep.md](meeting-prep.md) |

**Always-on flags:** If any project 7+ days silent, run [drift.md](drift.md) too. If leave ≤ 14 days, append risk warning.

**Priority when multiple match (max 3):** Communication first, drift flag second, temporal mode third.

## Rules

- Slack to others: show draft, send on "go"/"yep"
- Slack to self (U09KQAFK740): send directly
- Local lookup order: TASKS.md -> `work/{slug}/index.md` -> Slack
- #product-design-bulletin: business context, Figma link, PRD link, Blade Score (dashboard/onboarding only), tags `// @Pingal @Varghese @[PM] @[EM]`, screenshots. Send to own DM immediately.
