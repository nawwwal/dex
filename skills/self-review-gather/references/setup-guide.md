# Self-Review Gather — Setup Guide (v2)

This skill uses MCP tools and direct vault file reads. No browser automation required.

---

## Prerequisites

### Required
- **Vault file access**: `~/.claude/career/case.md` must be readable. This is the minimum.

### Optional (enrich results)
- **QMD**: `qmd` CLI indexed and embedded. Adds semantic search across all vault collections (`log`, `memory`, `learn`, `work`, `career`).
- **DevRev MCP**: `mcp__plugin_compass_devrev__hybrid_search` available. Adds evidence from DevRev issues/enhancements.
- **Slack MCP**: `mcp__plugin_compass_slack-mcp__slack_search_messages` available. Adds Slack corroboration (opt-in, recent 6 weeks only).

### Not required
- Chrome browser
- Chrome DevTools MCP
- Google Workspace MCP
- Google Docs access

---

## Capability Detection

Run `self-review-gather setup` to detect capabilities automatically. The skill probes each source and reports which mode will run:

| Mode | Sources | When |
|------|---------|------|
| `full` | Vault + QMD + DevRev + Slack (if opted in) | All MCPs available |
| `no-devrev` | Vault + QMD + Slack (if opted in) | DevRev MCP unavailable |
| `vault-only` | Vault direct reads + QMD | Only vault accessible |
| ABORT | — | `~/.claude/career/case.md` unreadable |

---

## Migration (v1 → v2 config)

If you have an old `self-review-config.json` (schema v1), run the migration sub-command before setup:

```
self-review-gather migrate
```

This command:
1. Backs up your current config to `self-review-config.json.bak`
2. Removes `totalPages` (no longer page-based)
3. Removes `vaultLastScanned` (moved to `runtime.json`)
4. Adds `schemaVersion: 2`
5. Preserves all other fields (`slackDisplayName`, `dateAfter`, `dateBefore`, `currentLevel`, `targetLevel`, `reviewPurpose`, etc.)

Migration is idempotent — safe to run multiple times.

---

## Setup Flow

Run: `self-review-gather setup`

The skill will:

1. **Detect capabilities** (preflight, in memory — no writes yet)
2. **Run engineering language check** on competency docs — hard failure if engineering terms found
3. **Validate config schema** — prompts to run `migrate` if v1 config detected
4. **Bootstrap state dir**: `mkdir -p ~/.claude/state/self-review-gather/ && chmod 0700 ~/.claude/state/self-review-gather/`
5. **Confirm review period** — prompts to verify dates from config; user can override
6. **Privacy consent for Slack** (if Slack MCP available):
   > "Enable Slack search? This will search public AND private channels/DMs for `from:the user` messages within the last 6 weeks of your review period. (yes/no)"
   - Default is NO — vault + DevRev only
   - If YES: scope persisted in `runtime.json` and cannot silently widen on reruns
7. **Vault pre-check**: reads `career/case.md`, `career/gaps.md`, `memory/goals.md`, `memory/nawal-through-others.md`, `memory/decisions.md`
8. **Output**: "Ready to collect. N entries in case.md. Top 3 gaps: [X, Y, Z]."

---

## Collection

Run: `self-review-gather collect`

Reads `runtime.json` for mode and privacy scope. Collection runs in order:

1. **Vault direct reads** (always): session logs in `~/.claude/log/`, `memory/decisions.md` Evidence Log sections, `memory/goals.md` Evidence Log sections
2. **QMD enrichment** (if `hasQmd: true`): 6 competency queries across `log`, `memory`, `learn`, `work`, `career`
3. **DevRev mining** (if `hasDevRev: true`): searches issues/enhancements with DevRev ownership gate
4. **Slack corroboration** (only if `privacyScope: "all"` AND `hasSlack: true`): last 6 weeks of review period only

Output: `~/.claude/state/self-review-gather/case-candidates.md`

---

## Applying Evidence

After reviewing `case-candidates.md`:

1. Open `~/.claude/state/self-review-gather/case-candidates.md`
2. Copy approved entries into the correct workstream section of `~/.claude/career/case.md`
3. Run `self-review-gather apply` — the skill marks processed candidates

The skill does NOT auto-write to `career/case.md`. All merges are manual.

---

## Reset

Run: `self-review-gather reset`

Clears `~/.claude/state/self-review-gather/runtime.json` and `case-candidates.md`. Does NOT touch `career/case.md` or any vault file. Requires confirmation prompt.

---

## Troubleshooting

**"Engineering language detected in competency docs"**
The competency reference files (`references/competencies/parsed/`) contain engineering role content. Run `/writing-skills` and update the files manually, or re-run this implementation. The specific phrases to remove are: "Senior Software Engineer", "Engineering Excellence", "SDE", "system design", "code quality", "codebase".

**"Config schemaVersion < 2"**
Run `self-review-gather migrate` first.

**"career/case.md not readable"**
Check that `~/.claude/career/case.md` exists and is readable. This is the required minimum file.

**"QMD not available"**
QMD is optional. Collection will fall back to direct vault file reads. To enable QMD: run `qmd update && qmd embed` in `~/.claude/`.

**"DevRev MCP not available"**
DevRev is optional. Skip and proceed — vault + Slack (if opted in) will run.

**"No Slack results"**
Slack is disabled by default. Enable by running `self-review-gather setup` and opting in to `privacyScope: "all"` when prompted. Note: Slack `from:` search is only reliable for the last 6 weeks — older content will not appear.
