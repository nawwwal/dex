# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`dex` is a Claude Code plugin published as `nawwwal/dex` on the plugin marketplace. It ships three installable plugins — `core`, `design`, `tools` — each containing skills, agents, and hooks that extend Claude Code with persistent memory, session lifecycle management, and design intelligence.

## Development

**No build step.** Everything is shell scripts and Markdown. Edit files in `plugins/` and start a new Claude session (or run `/reload-plugins`) to pick up changes.

**Prerequisites** (required by hooks): `python3`, `jq`, `node`

## Releasing

```
/dex release           # patch bump
/dex release minor
/dex release major
```

The release skill bumps versions across **four files** (`plugins/{core,design,tools}/.claude-plugin/plugin.json` and root `.claude-plugin/marketplace.json`), commits, tags, and pushes. Must be on `main` with a clean worktree.

## Plugin architecture

```
plugins/
├── core/                    # Session lifecycle, hooks, memory, core skills
│   ├── .claude-plugin/plugin.json
│   ├── hooks/               # Shell scripts + hooks.json wiring
│   ├── skills/              # SKILL.md files (one dir per skill)
│   ├── agents/              # Agent .md files
│   └── templates/           # CLAUDE.md template + memory scaffolds
├── design/                  # Design critique, UI review, motion, shader
│   ├── skills/
│   └── agents/
└── tools/                   # Research, dev tools, creative tools
    └── skills/
```

Each plugin's `plugin.json` contains `name` and `version`. The root `.claude-plugin/marketplace.json` mirrors all three versions — always keep them in sync.

## Adding a skill

1. Create `plugins/{plugin}/skills/{skill-name}/SKILL.md`
2. Add frontmatter: `name:` and `description:` (description is what users see in skill listings)
3. Start a new session or run `/reload-plugins` — no other registration needed

Skills support sub-files (e.g. `references/`, `templates/`) that the SKILL.md can reference as `${CLAUDE_PLUGIN_ROOT}/skills/{name}/references/...`.

## Adding a hook

1. Create the shell script in `plugins/core/hooks/`
2. Register it in `plugins/core/hooks/hooks.json` under the appropriate event

Hook events: `SessionStart`, `SubagentStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`. `PreToolUse`/`PostToolUse` support a `matcher` field (tool name prefix). Hooks receive JSON on stdin via `INPUT=$(cat)`. The `$CLAUDE_PLUGIN_ROOT` env var resolves to the installed plugin directory.

## Adding an agent

Create `plugins/{plugin}/agents/{agent-name}.md` with frontmatter following the standard agent schema. No registration needed — agents are available by filename.

## Memory system (user-side, not in this repo)

The vault lives at `~/.claude/` and is scaffolded by `/dex setup`. Template files for memory scaffolds are in `plugins/core/templates/memory-scaffolds/`. The `session-context.sh` hook reads from this vault at session start; `vault-health.sh` writes staleness checks to `memory/health.md`.
