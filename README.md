# dex

An agent environment toolkit for Claude Code and Codex. It ships setup checks, memory-aware workflows, design thinking, development workflows, and creative tooling.

## Install

```
/plugin marketplace add nawwwal/dex
/plugin install core@nawwwal-dex       # setup, memory-aware workflow
/plugin install design@nawwwal-dex     # crux, divergence, 5F review, presentation, visuals
/plugin install dev@nawwwal-dex        # Blade, dashboard implementation, hardening, shaders, sound
/plugin install tools@nawwwal-dex      # research, Codex review, media, mymind
/dex setup
```

Add the marketplace once, then install the plugins you need. `/dex setup` bootstraps and verifies the current `~/.agents/` structure plus Claude/Codex compatibility links. It does not read external services or personalize memory.

For local Codex development in this repo, use the repo marketplace at `.agents/plugins/marketplace.json` and restart Codex after changing plugin files.

## Prerequisites

- **python3**, **jq**, **node** - required by setup and local scripts
- **Figma MCP** - optional, enables Figma-backed design workflows

## What you get

### Skills

| Category | Skills |
|---|---|
| **Design** | `crux`, `diverge`, `present`, `reviewing-designs-5f`, `visual` |
| **Dev** | `blade`, `dashboard-design`, `harden`, `shader`, `create-sound` |
| **Thinking** | `council`, `codex`, `reflect` |
| **Development** | `media-optimizer` |
| **Workflow** | `communicate` |
| **Writing / Media** | `generate-image`, `mymind` |
| **Meta** | `dex` |

## Memory system

`/dex setup` creates the minimal current structure outside the plugin:

```
~/.agents/
├── AGENTS.md
├── instructions/
├── references/
├── memory/
│   ├── preferences/
│   ├── reference/
│   └── records/
├── skills/
├── plugins/
└── state.json
```

`~/.claude/CLAUDE.md`, `~/.claude/memory`, and `~/.claude/skills` are compatibility links back to `~/.agents/`.

## Customizing

Plugin files are managed by the plugin system. To customize a skill:

1. Copy it to `~/.agents/skills/`
2. Edit the local copy
3. The local copy takes precedence over the plugin version

Your customizations are never overwritten by plugin updates.

Dex does not create `~/.agents/agents`. The old plugin-agent surface has been removed.

## For developers

If you're developing dex (editing skills or templates):

**Working directory:** Always `~/dex/`.

**After editing:** Start a new Claude session or run `/reload-plugins`. Changes are live.

## Releasing

Release maintenance is project-local, not part of the shipped plugin.

- The installed plugin owns the user-facing `/dex setup` environment workflow.
- Repo-maintainer workflows like release operations live only in `.claude/skills/dex/` and `.agents/skills/dex/`.
- This keeps the shipped plugin focused on usable end-user skills while leaving project maintenance local to this repository.

When you're ready to push updates to teammates:

```
/dex release dev              # patch bump dev
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
/plugin update dev@nawwwal-dex
/plugin update tools@nawwwal-dex
```

Or reload plugins in an active session:

```
/reload-plugins
```
