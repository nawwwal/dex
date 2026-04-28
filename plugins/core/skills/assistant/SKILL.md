---
name: assistant
description: "Routes to devrev, communicate, reflect, or log skills based on trigger phrase."
argument-hint: "[sync devrev | tell Name msg | emerge | ideas for X | drift | log]"
allowed-tools: Bash, Read
---

# Assistant

**Identity:** Slack U09KQAFK740 (nawal.deepakbhai) | DevRev don:identity:dvrv-in-1:devo/2sRI6Hepzz:devu/11830 | Asia/Kolkata

## Routing

$ARGUMENTS

Match to the first trigger that fits, then invoke that skill.

| Trigger | Skill |
|---|---|
| "sync devrev", "update devrev", "devrev hygiene" | devrev |
| "tell/message/dm [name]" | core:communicate |
| "emerge", "patterns", "ideas for [X]", "drift", "what's quiet" | core:reflect |
| "log task", "session journal" | log |

## Rules

- Slack to others: show draft, send on "go"/"yep"
- Slack to self (U09KQAFK740): send directly
- #product-design-bulletin: business context, Figma link, PRD link, Blade Score (dashboard/onboarding only), tags `// @Pingal @Varghese @[PM] @[EM]`, screenshots. Send to own DM immediately.
