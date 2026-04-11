# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`dex` is a Claude/Codex plugin published as `nawwwal/dex` on the plugin marketplace. It ships three installable plugins — `core`, `design`, `tools` — each containing skills, agents, and templates that extend the assistants with persistent memory, onboarding, and design intelligence.

## Development

**No build step.** Everything is shell scripts and Markdown. Edit files in `plugins/` and start a new Claude session (or run `/reload-plugins`) to pick up changes.

**Prerequisites** (required by setup and local scripts): `python3`, `jq`, `node`

## Releasing

```text
/dex release core
/dex release design minor
/dex release tools major
```

The release skill bumps the selected plugin version across the plugin's Claude and Codex manifests plus the Claude marketplace metadata, then commits, tags, and pushes. Must be on `main` with a clean worktree.

## Plugin architecture

```
plugins/
├── core/                    # Memory scaffolding, core skills, templates
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/              # SKILL.md files (one dir per skill)
│   ├── agents/              # Agent .md files
│   └── templates/           # CLAUDE.md template + memory scaffolds
├── design/                  # Design critique, UI review, motion, shader
│   ├── skills/
│   └── agents/
└── tools/                   # Research, dev tools, creative tools
    └── skills/
```

Each plugin ships separate Claude and Codex manifests. The root `.claude-plugin/marketplace.json` mirrors published Claude plugin versions, and `.agents/plugins/marketplace.json` exposes the same plugin folders as a repo-local Codex marketplace.

## Adding a skill

1. Create `plugins/{plugin}/skills/{skill-name}/SKILL.md`
2. Add frontmatter: `name:` and `description:` (description is what users see in skill listings)
3. Start a new session or run `/reload-plugins` — no other registration needed

Skills support sub-files (e.g. `references/`, `templates/`) that the SKILL.md can reference as `${CLAUDE_PLUGIN_ROOT}/skills/{name}/references/...`.

## Adding an agent

Create `plugins/{plugin}/agents/{agent-name}.md` with frontmatter following the standard agent schema. No registration needed — agents are available by filename.

## Memory system (user-side, not in this repo)

The vault lives at `~/.claude/` and is scaffolded by `/dex setup`. Template files for memory scaffolds are in `plugins/core/templates/memory-scaffolds/`.
