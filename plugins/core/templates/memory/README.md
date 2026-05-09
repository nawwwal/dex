# Memory

Memory is trigger-loaded context. It is not the place for global workflow rules.

Use these folders:

| Folder | Purpose | Examples |
|---|---|---|
| `preferences/` | User behavior, voice, learned patterns, and modeling context | `voice.md`, `nawal-model.md`, `patterns.md` |
| `reference/` | Lookup facts and directories | `people.md`, `terms.md`, `projects.md`, `slack-channels.md` |
| `records/` | Append-only logs, health reports, messages, and decisions | `decisions.md`, `messages.md`, `health.md` |

Rule:

- If the file tells an agent how to operate globally, put it in `~/.agents/instructions/`.
- If the file helps an agent adapt to the user or recall context only when triggered, keep it in `memory/`.
- If the file is a tool or domain manual, put it in `~/.agents/references/`.
