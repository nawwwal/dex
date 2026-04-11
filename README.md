# dex

A vault system for Claude Code. Gives Claude persistent memory, design intelligence, quality agents, and smart onboarding. Built for the design team at Razorpay.

## Install

```
/plugin marketplace add nawwwal/dex
/plugin install core@nawwwal-dex       # everyone — setup, memory, workflow
/plugin install design@nawwwal-dex     # designers — critique, dashboard, UI review
/plugin install tools@nawwwal-dex      # optional — research, dev, creative tools
/dex setup
```

Add the marketplace once, then install the plugins you need. `/dex setup` reads your Slack and DevRev (with your permission) to generate a personalized `CLAUDE.md` and scaffold your memory structure.

For local Codex development in this repo, use the repo marketplace at `.agents/plugins/marketplace.json` and restart Codex after changing plugin files.

## Prerequisites

- **Compass plugin** (includes Blade MCP) — required
- **Figma MCP** — optional, enables design skills
- **python3**, **jq**, **node** — required by setup and local scripts

## What you get

### Skills

| Category | Skills |
|---|---|
| **Design** | `dashboard-design`, `critique-5f`, `design` |
| **Thinking** | `council`, `codex`, `deep-research` |
| **Development** | `tdd`, `react-doctor`, `agent-browser`, `agent-development` |
| **Workflow** | `assistant`, `ops`, `today`, `switch-project` |
| **Writing** | `writing-skills`, `beautiful-mermaid`, `generate-image` |
| **Meta** | `dex`, `self-review-gather`, `reflect-others` |

### Agents

Specialized subagents Claude spawns automatically: code reviewer, design reviewer, blade implementer, standup writer, sprint planner, animation expert, Next.js expert, GLSL reviewer, and more.

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

Dex does not require `~/.agents/skills` or `~/.agents/agents` to mirror `~/.claude/`.
Leave `~/.agents/` available for tools that manage their own installs there.

## For developers

If you're developing dex (editing skills, agents, templates):

**Working directory:** Always `~/dex/`.

**After editing:** Start a new Claude session or run `/reload-plugins`. Changes are live.

## Releasing

Release maintenance is project-local, not part of the shipped plugin.

- The installed plugin keeps only the user-facing `dex setup` workflow.
- Repo-maintainer workflows like release operations live only in `.claude/skills/dex/` and `.agents/skills/dex/`.
- This keeps the shipped plugin focused on usable end-user skills while leaving project maintenance local to this repository.

When you're ready to push updates to teammates:

```
/dex release tools            # patch bump tools
/dex release tools minor      # minor bump tools
/dex release tools major      # major bump tools
```

The project-level release skill bumps the selected plugin version, updates marketplace metadata, commits, tags, pushes, and creates a GitHub Release with changelog notes. Teammates update with:

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
