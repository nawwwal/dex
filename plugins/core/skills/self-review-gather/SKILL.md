---
name: self-review-gather
description: "Gather promotion evidence from vault, DevRev, and Slack."
argument-hint: "[setup | gather | status]"
disable-model-invocation: true
---

# Self-Review Gather (v2)

Evidence gathering for PD1→PD2 promotion self-review. Mines the vault (session logs, decisions, goals), DevRev, and optionally Slack. Outputs `~/.claude/state/self-review-gather/case-candidates.md` — private, user-reviewed, manually merged into `career/case.md`.

**Scope**: Personal skill for the user's PD1→PD2 case. Explicitly scoped to this vault.

**v1 design**: No browser automation. Vault direct reads are the minimum viable path. QMD and DevRev are optional enrichment. Slack is disabled by default — opt-in with full disclosure.

## Sub-commands

| Command | What it does |
|---------|-------------|
| `self-review-gather setup` | Detect capabilities, migrate config, confirm period, set privacy scope |
| `self-review-gather collect` | Mine vault + DevRev + Slack (if opted in), write case-candidates.md |
| `self-review-gather migrate` | Migrate old v1 config to schemaVersion 2 |
| `self-review-gather reset` | Clear runtime state and output (with confirmation prompt) |

---

## Setup

### Preflight (in memory — no writes)

Check each source:

| Source | Probe | Required? |
|--------|-------|-----------|
| File access | `~/.claude/career/case.md` readable | **Required** — ABORT if not |
| QMD | `qmd_search` trivial query | Optional |
| DevRev MCP | `mcp__plugin_compass_devrev__hybrid_search` trivial query | Optional |
| Slack MCP | `mcp__plugin_compass_slack-mcp__slack_search_messages` trivial query | Optional |

**Engineering language hard check**: scan `references/competencies/target-level-summary.md` and `references/competencies/parsed/career-framework.md` for prohibited terms: "Senior Software Engineer", "Engineering Excellence", "SDE", "system design", "code quality", "codebase". If found → **ABORT** with message: "Engineering terms detected in competency docs. Update the parsed competency files before proceeding."

**Config validation**: read `self-review-config.json`, check `schemaVersion`. If `< 2` → ABORT with: "Run `self-review-gather migrate` first."

### State Bootstrap (only after preflight passes)

```bash
mkdir -p ~/.claude/state/self-review-gather/
chmod 0700 ~/.claude/state/self-review-gather/
```

Verify `~/.claude/.gitignore` includes `state/`.

Initialize `runtime.json` (`0600`) — write to temp file first, then rename:
```json
{
  "runtimeSchemaVersion": 1,
  "capabilities": { "hasQmd": false, "hasDevRev": false, "hasSlack": false },
  "privacyScope": "none",
  "reviewPeriod": { "after": null, "before": null },
  "vaultLastScanned": null
}
```

### Review Period Confirmation

Prompt: "Confirm review period — After: [config.dateAfter] / Before: [config.dateBefore]? (press Enter to confirm or type new dates)"

Persist confirmed dates in `runtime.json.reviewPeriod`.

### Privacy Consent (Slack only)

Default: `privacyScope: "none"` — no Slack. If Slack MCP is available:

> "Enable Slack search? This will search public AND private channels/DMs for `from:the user` messages within the last 6 weeks of your review period. Slack `from:` search is unreliable for older messages. (yes/no)"

If yes: persist `privacyScope: "all"` in runtime.json. Scope cannot silently widen on reruns.

### Vault Pre-Check

Direct-read (absolute paths):
- `~/.claude/memory/goals.md` → competency weights + current ratings
- `~/.claude/career/case.md` → build dedup index
- `~/.claude/career/gaps.md` → named gaps (warn if absent, don't fail)
- `~/.claude/memory/nawal-through-others.md` → third-person signals
- `~/.claude/memory/decisions.md` → decision log

Output: "Setup complete. N entries in case.md. Top 3 gaps: [X, Y, Z]. Capabilities: [list]. Run `self-review-gather collect`."

---

## Collect

Reads `runtime.json` for mode and privacy scope. Regenerates `case-candidates.md` from scratch each run (deterministic, no append). Writes atomically: temp file → rename.

**Collection order** (always sequential, later steps optional):

1. **Vault direct reads** (always): session logs in `~/.claude/log/`, `memory/decisions.md` Evidence Log sections, `memory/goals.md` Evidence Log sections
2. **QMD enrichment** (if `hasQmd: true`): 6 competency queries, collections `log`, `memory`, `learn`, `work`, `career`
3. **DevRev mining** (if `hasDevRev: true`): DevRev ownership gate (assignee, authored comment >100 chars, linked artifact, creator)
4. **Slack corroboration** (if `privacyScope: "all"` AND `hasSlack: true`): last 6 weeks of review period only

**After all passes**: cross-source merge (same dedup key → one candidate with multiple sources).

**Output**: `~/.claude/state/self-review-gather/case-candidates.md` (`0600`)

Full collection logic, dedup rules, and output format: see [references/command-template.md](references/command-template.md).

Vault paths, QMD queries, and redaction policy: see [references/vault-integration.md](references/vault-integration.md).

---

## Migrate

Migrates `self-review-config.json` from schema v1 to v2:

1. Backup: `self-review-config.json` → `self-review-config.json.bak`
2. Remove: `totalPages`, `vaultLastScanned`
3. Add: `schemaVersion: 2`
4. Preserve: all other fields
5. Write atomically: temp file → rename over original
6. Idempotent: if already v2, confirm and exit

---

## Reset

Confirms with user: "This will delete `runtime.json` and `case-candidates.md` from `~/.claude/state/self-review-gather/`. Continue? (yes/no)"

Deletes only these known files — never touches `career/case.md` or any vault file.

---

## Applying Candidates

After `collect`, review `~/.claude/state/self-review-gather/case-candidates.md`:

1. Open the file and read candidates by competency area
2. For approved entries: manually copy entry text into the correct workstream section of `~/.claude/career/case.md`
3. The skill does NOT auto-write to `career/case.md`

---

## Competency Reference

Curated PD-specific summaries — no Google Docs access required:

- [Culture competencies](references/competencies/parsed/culture.md)
- [Technical competencies / PD II](references/competencies/parsed/technical.md)
- [Career framework / PD II](references/competencies/parsed/career-framework.md)
- [Target level summary + vocabulary guide](references/competencies/target-level-summary.md)

---

## Troubleshooting

See [references/setup-guide.md](references/setup-guide.md) for:
- Capability detection and mode selection
- Migration instructions
- Common error messages and fixes
