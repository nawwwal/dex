# PMB Memory Skill Migration

Goal: replace Dex's retired memory workflow with a fresh PMB-native `memory` skill, remove duplicate hook behavior, and connect Codex/Claude Code to the shared PMB workspace.

## Status

- [x] Added a validation script for the new runtime skill.
- [x] Verified the validator failed before the skill existed.
- [x] Added the PMB-only `memory` skill.
- [x] Verified the validator passes.
- [x] Removed the duplicate Dex hook layer.
- [x] Removed retired memory and session-close skill directories.
- [x] Updated Core plugin manifests and marketplace metadata.
- [x] Updated README, DevRev, Why, Reflect, and setup guidance to use PMB.
- [x] Connected Codex and Claude Code to PMB workspace `oddly-specific`.
- [x] Imported source notes into PMB and rebuilt the graph.
- [x] Ran final skill, audit, scan, and JSON validation.

## Verification

- `python3 plugins/core/skills/memory/scripts/validate_memory_skill.py`
- `python3 plugins/core/skills/devrev/scripts/audit.py sync_contract_check plugins/core/skills/devrev`
- `python3 plugins/core/skills/why/scripts/validate_why_evals.py`
- `python3 -m json.tool plugins/core/.codex-plugin/plugin.json`
- `python3 -m json.tool plugins/core/.claude-plugin/plugin.json`
- `python3 -m json.tool .claude-plugin/marketplace.json`
- `rg -n -i "portent|tolaria|qmd" plugins/core .claude-plugin/marketplace.json README.md`
- `rg -n "\bwrap\b|wrap-up|session wrap" README.md plugins/core/.codex-plugin/plugin.json plugins/core/.claude-plugin/plugin.json .claude-plugin/marketplace.json plugins/core/skills`

## PMB Notes

- Workspace: `oddly-specific`
- Import result: 2398 source items imported.
- Graph result: 8102 entities and 214022 edges after rebuild.
- Doctor result: 13 ok, 0 warn, 0 fail.
- Audit caveat: PMB reported 75 conflicts to review after import.
