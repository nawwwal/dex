# dex

Vault system for the R1 Design team — session lifecycle, design intelligence, quality agents, smart onboarding.

## Install

```
/plugin marketplace add nawwwal/dex
/plugin install dex@nawwwal-dex
/dex:setup
```

That's it. Three commands.

## Prerequisites

- **Compass plugin** (includes Blade MCP) — required
- **Figma MCP** — optional, needed for design skills
- **python3**, **jq**, **node** — required for hooks

## What you get

- **37 skills**: design critique, dashboard patterns, council, TDD, agent-browser, deep-research, and more
- **16 agents**: code reviewer, design reviewer, sprint planner, standup writer, and more
- **22 hooks**: session lifecycle, frustration detection, commit capture, skill tracking
- **Smart onboarding**: `/dex:setup` reads your Slack/DevRev (with consent) and generates a personalized CLAUDE.md + memory structure

## Customizing

Plugin files are read-only. To customize a skill or agent:
1. Copy it to your `~/.claude/skills/` or `~/.claude/agents/`
2. Edit the local copy
3. The local copy takes precedence over the plugin version

## Updating

Plugin updates are pulled automatically when the marketplace refreshes. Your local customizations (in `~/.claude/`) are never overwritten.

## Memory structure

`/dex:setup` scaffolds these directories (one-time, not part of plugin):

```
~/.claude/
├── CLAUDE.md          (personalized identity + rules)
├── TASKS.md           (task tracking)
├── memory/            (20 files: goals, patterns, decisions, voice, etc.)
├── career/            (promotion case, evidence)
├── log/               (session journals)
├── sessions/          (session state)
├── config/            (project registry)
├── work/              (project workspaces)
├── archive/           (archived decisions, patterns)
├── agent-memory/      (agent state)
├── people/            (people profiles)
└── projects/          (project context)
```
