# Plugin Architecture Brief — Cross-System Audit

**System:** dex plugin marketplace (`nawwwal/dex`)  
**Scope:** Cross-system behavior across Claude and Codex install surfaces  
**Requested output:** Architecture audit — ownership boundaries, lifecycle gaps, blast radius of manifest changes

## What dex is

dex ships four installable plugins (`core`, `design`, `dev`, `tools`) containing skills, templates, and shell scripts. Each plugin has:

- `plugins/{name}/.claude-plugin/plugin.json`
- `plugins/{name}/.codex-plugin/plugin.json`
- `plugins/{name}/skills/{skill-name}/SKILL.md`

Root marketplaces mirror versions:

- `.claude-plugin/marketplace.json` (Claude)
- `.agents/plugins/marketplace.json` (Codex local marketplace)

Release flow (`/dex release`) bumps versions across all manifests, commits, tags, and pushes.

## Audit motivation

We are adding a fifth plugin (`council` lives in `core` today but may split) and introducing eval fixtures under `plugins/core/skills/council/evals/`. Before expanding:

1. Map how Claude vs Codex resolve `${CLAUDE_PLUGIN_ROOT}` vs `${CLAUDE_SKILL_DIR}` paths
2. Identify duplicated contract surfaces that can drift
3. Understand what breaks when a skill is renamed or moved between plugins
4. Document hook/skill discovery differences between runtimes

## Systems in play

| Surface | Discovery | Config root |
|---------|-----------|-------------|
| Claude Code | `.claude-plugin/` marketplace | User `~/.claude/` + plugin cache |
| Codex | `.codex-plugin/` + `.agents/plugins/` | `~/.agents/` via `/dex setup` |
| Cursor | Plugin cache under `~/.cursor/plugins/cache/` | Separate from Claude/Codex |

Skills reference sub-files via `${CLAUDE_PLUGIN_ROOT}/skills/...`. Setup skill creates `~/.agents/` structure and compatibility symlinks.

## Known pain points

- **Dual manifests:** Version bumps must touch 3+ JSON files per release; missed one causes marketplace mismatch
- **Path variable inconsistency:** Some skills use `CLAUDE_PLUGIN_ROOT`, council uses `CLAUDE_SKILL_DIR` — unclear if Codex resolves both
- **No automated drift check:** `design` skill count in Claude manifest vs actual `skills/` dirs not validated in CI
- **Cache invalidation:** Users report stale skills until `/reload-plugins` or new session; no cachebuster doc for Codex
- **Cross-plugin skill references:** `dev` skills assume `design` skills exist; no declared dependency graph

## Questions for investigation

1. What is the blast radius of renaming `plugins/core/skills/council/`?
2. If marketplace.json version ≠ plugin.json version, which runtime fails and how?
3. Are eval fixtures under a skill directory loaded into agent context unintentionally?
4. Does `/dex setup` idempotently handle plugin add/remove, or leave orphan symlinks?
5. What is the ownership boundary between repo-shipped templates and user-side `~/.agents/memory/`?

## Constraints

- No build step; validation must be shell + jq + node scripts if added
- Release must stay on `main` with clean worktree
- Cannot break existing users on `nawwwal/dex` marketplace mid-quarter
- Skill frontmatter `name` is the public contract; directory name is convention

## Artifacts to inspect

`plugins/core/` manifests and skills, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`

## Desired output

- Dependency / ownership diagram across plugins and user-side config
- Drift risks ranked by severity
- Recommendations: CI checks, manifest consolidation options, path variable standardization
- Explicit list of what **not** to refactor (YAGNI guardrails)
