# dex

A vault system for Claude Code. Gives Claude persistent memory, session lifecycle management, design intelligence, quality agents, and smart onboarding. Built for the design team at Razorpay.

## Install

```
/plugin marketplace add nawwwal/dex
/plugin install core@nawwwal-dex       # everyone — hooks, setup, workflow
/plugin install design@nawwwal-dex     # designers — critique, dashboard, UI review
/plugin install tools@nawwwal-dex      # optional — research, dev, creative tools
/dex setup
```

Add the marketplace once, then install the plugins you need. `/dex setup` reads your Slack and DevRev (with your permission) to generate a personalized `CLAUDE.md` and scaffold your memory structure.

## Prerequisites

- **Compass plugin** (includes Blade MCP) — required
- **Figma MCP** — optional, enables design skills
- **python3**, **jq**, **node** — required by hooks

## What you get

### Skills

| Category | Skills |
|---|---|
| **Design** | `dashboard-design`, `critique-5f`, `design` |
| **Thinking** | `council`, `codex`, `deep-research` |
| **Development** | `tdd`, `react-doctor`, `agent-browser`, `agent-development` |
| **Workflow** | `assistant`, `ops`, `today`, `switch-project`, `taskmaster` |
| **Writing** | `writing-skills`, `beautiful-mermaid`, `generate-image` |
| **Meta** | `dex`, `self-review-gather`, `reflect-others` |

### Agents

Specialized subagents Claude spawns automatically: code reviewer, design reviewer, blade implementer, standup writer, sprint planner, animation expert, Next.js expert, GLSL reviewer, and more.

### Hooks

Session lifecycle hooks that fire automatically: vault health checks, session context loading, frustration detection, commit capture, skill usage tracking, session breadcrumbs.

## Memory system

`/dex setup` creates this structure (one-time, outside the plugin):

```
~/.claude/
├── CLAUDE.md           ← personalized identity + behavioral rules
├── TASKS.md            ← task tracking
├── memory/             ← 20 files: goals, patterns, decisions, voice, projects, etc.
├── career/             ← promotion case, evidence
├── log/                ← session journals
├── sessions/           ← session state persistence
├── config/             ← project registry
├── work/               ← project workspaces
├── archive/            ← archived decisions, patterns
└── people/             ← people profiles
```

`memory/projects.md` is a lightweight index that points into `work/` for project context.

## Customizing

Plugin files are managed by the plugin system. To customize a skill or agent:

1. Copy it to `~/.claude/skills/` or `~/.claude/agents/`
2. Edit the local copy
3. The local copy takes precedence over the plugin version

Your customizations are never overwritten by plugin updates.

## For developers

If you're developing dex (editing skills, agents, hooks):

**Working directory:** Always `~/dex/`.

**After editing:** Start a new Claude session or run `/reload-plugins`. Changes are live.

## Releasing

When you're ready to push updates to teammates:

```
/dex release          # patch bump (1.0.0 → 1.0.1)
/dex release minor    # minor bump (1.0.1 → 1.1.0)
/dex release major    # major bump (1.1.0 → 2.0.0)
```

This bumps version, commits, tags, and pushes. Teammates update with:

```
/plugin update dex@nawwwal-dex
```

## Updating

```
/plugin update core@nawwwal-dex
/plugin update design@nawwwal-dex
/plugin update tools@nawwwal-dex
```

Or reload plugins in an active session:

```
/reload-plugins
```
