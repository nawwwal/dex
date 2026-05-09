# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this repo is

`dex` is a Claude/Codex plugin published as `nawwwal/dex` on the plugin marketplace. It ships four installable plugins: `core`, `design`, `dev`, and `tools`. These contain skills and templates for agent environment setup, memory-aware workflows, design intelligence, development workflows, and creative tooling.

## Development

**No build step.** Everything is shell scripts and Markdown. Edit files in `plugins/` and start a new Codex session (or run `/reload-plugins`) to pick up changes.

**Prerequisites** (required by setup and local scripts): `python3`, `jq`, `node`

## Releasing

```text
/dex release core
/dex release design minor
/dex release dev minor
/dex release tools major
```

The release skill bumps the selected plugin version across the plugin's Claude and Codex manifests plus the Claude marketplace metadata, then commits, tags, and pushes. Must be on `main` with a clean worktree.

## Plugin architecture

```
plugins/
├── core/                    # Agent setup, core skills, templates
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/              # SKILL.md files (one dir per skill)
│   └── templates/           # Minimal AGENTS.md + memory README templates
├── design/                  # Crux, divergence, 5F review, presentation, visual handoffs
│   └── skills/
├── dev/                     # Blade, dashboard implementation, UI hardening, shaders, sound
│   └── skills/
└── tools/                   # Codex review, image/media tools, mymind
    └── skills/
```

Each plugin ships separate Claude and Codex manifests. The root `.claude-plugin/marketplace.json` mirrors published Claude plugin versions, and `.agents/plugins/marketplace.json` exposes the same plugin folders as a repo-local Codex marketplace.

## Adding a skill

1. Create `plugins/{plugin}/skills/{skill-name}/SKILL.md`
2. Add frontmatter: `name:` and `description:` (description is what users see in skill listings)
3. Start a new session or run `/reload-plugins` — no other registration needed

Skills support sub-files (e.g. `references/`, `templates/`) that the SKILL.md can reference as `${CLAUDE_PLUGIN_ROOT}/skills/{name}/references/...`.

## Memory system (user-side, not in this repo)

User-side agent configuration lives under `~/.agents/`. `/dex setup` creates the minimal current folder structure and Claude/Codex compatibility links. Templates live in `plugins/core/templates/`.
