
# /dex setup - Environment Bootstrap

Align a user's local agent environment with the current Dex topology. This is a
fresh-machine bootstrap and doctor, not a personalization or migration wizard.

## Hard Boundaries

- Do not read Slack, DevRev, Gmail, Calendar, or other external services.
- Do not infer identity, role, team, communication style, projects, goals, or tasks.
- Do not create a large personal vault.
- Do not migrate old flat memory files.
- Do not overwrite any existing non-empty user file without explicit confirmation.
- Treat `~/.agents/` as the canonical source of truth. Runtime-specific paths are compatibility aliases.

## Phase 1 - Local Detection

Check what exists:

```
READ ~/.agents/AGENTS.md
READ ~/.agents/memory/README.md
READ ~/.agents/state.json
READ ~/.codex/config.toml       -> if present, inspect Dex plugin enablement
READ ~/.claude/settings.json    -> if present, inspect Claude-side plugin state
CHECK prerequisites:
  - python3: which python3
  - jq: which jq
  - node: which node
CHECK compatibility links:
  - ~/.claude/CLAUDE.md -> ~/.agents/AGENTS.md
  - ~/.claude/memory -> ~/.agents/memory
  - ~/.claude/skills -> ~/.agents/skills
CHECK Dex marketplace/plugin wiring:
  - ~/.agents/plugins/marketplace.json
  - ~/.codex/config.toml entries for nawwwal-dex when using Codex
  - ~/.claude/plugins/marketplaces/nawwwal-dex when using Claude
```

Report before changing anything:

```
Found:
  ~/.agents/AGENTS.md: yes/no
  ~/.agents/memory: yes/no
  compatibility links: ok/drift/missing
  Dex plugin wiring: ok/drift/missing
Missing tools: [...]
Planned changes: [...]
```

If tools are missing, still report the rest of the environment. Do not install system packages.

## Phase 2 - Bootstrap Missing Canonical Files

Create only missing directories:

```bash
mkdir -p ~/.agents/instructions ~/.agents/references
mkdir -p ~/.agents/memory/preferences ~/.agents/memory/reference ~/.agents/memory/records
mkdir -p ~/.agents/skills ~/.agents/plugins
```

Create only missing files:

- `~/.agents/AGENTS.md` from the plugin template `templates/AGENTS.md.template`
- `~/.agents/memory/README.md` from the plugin template `templates/memory/README.md`
- `~/.agents/state.json` with a minimal setup timestamp/status, if absent

If a target file exists, skip it and print `skipped: <path> already exists`.

## Phase 3 - Compatibility Links

Create or fix links only after confirmation when a real file/directory already occupies the path.

```
~/.claude/CLAUDE.md -> ~/.agents/AGENTS.md
~/.claude/memory -> ~/.agents/memory
~/.claude/skills -> ~/.agents/skills
```

Verification commands:

```bash
test -L ~/.claude/CLAUDE.md && readlink ~/.claude/CLAUDE.md
test -L ~/.claude/memory && readlink ~/.claude/memory
test -L ~/.claude/skills && readlink ~/.claude/skills
```

Do not create `~/.agents/agents`. The plugin no longer ships agent folders.

## Phase 4 - Plugin Wiring Check

For Codex, check:

- `~/.agents/plugins/marketplace.json` includes `nawwwal-dex`
- marketplace plugin sources resolve to real `.codex-plugin/plugin.json` files
- `~/.codex/config.toml` enables the desired Dex plugins
- installed cache versions match the expected plugin manifests when available

For Claude, check:

- `~/.claude/plugins/marketplaces/nawwwal-dex` exists when Claude plugin install is expected
- installed plugin manifests parse as JSON

This phase reports drift. It does not run marketplace install/update commands unless the user explicitly asks.

## Phase 5 - Report

```
Dex setup report

Created:
  [paths]

Skipped:
  [existing paths]

Needs attention:
  [missing tools, blocked links, plugin wiring drift]

Verified:
  python3: ok/missing
  jq: ok/missing
  node: ok/missing
  canonical root: ~/.agents
  compatibility links: ok/drift/missing
  Dex plugin wiring: ok/drift/missing
```
