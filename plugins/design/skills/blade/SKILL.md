---
name: blade
description: "Use for Razorpay Blade design-system work: semantic component selection, Blade MCP lookup, Blade coverage scoring, drift audits, and PR gates. Triggers on blade, Blade MCP, Blade score, Blade coverage, using only Blade, design system adherence, custom CSS drift, dashboard nav, profile menu, test mode banner, setup steps, cards, tables, charts, menus, modals, drawers, tooltips, and alerts."
allowed-tools: Read, Grep, Glob, Bash
---

# blade

Blade operating workflow for Razorpay UI work. Use it before implementation to choose the right Blade primitive, during implementation to keep MCP docs in the loop, and after implementation to measure coverage and detect drift.

## Core workflow

1. Detect the real consumer project root. Use the app being edited, not the Dex plugin repo. Confirm `package.json` contains `@razorpay/blade` when possible.
2. Read `references/component-selection.md` before choosing components from product language.
3. Query Blade MCP before custom UI:
   - Pattern-level surfaces: call `get_blade_pattern_docs` first.
   - Component-level surfaces: call `get_blade_component_docs` for the candidates.
   - Setup/tokens/icons: call `get_blade_general_docs`.
4. Use Blade semantic components first. `Box` is layout glue, not a substitute for `Card`, `Alert`, `SideNav`, `Table`, `StepGroup`, `Menu`, charts, forms, or feedback components.
5. If custom UI remains, record why Blade could not cover it and keep custom CSS local, minimal, and token-based.
6. After implementation, run `blade gate` for final checks or `blade audit` for advisory diagnosis.

For exact MCP sequencing and failure recovery, read `references/mcp-workflow.md`.

## CLI

```bash
# Runtime coverage, same canonical Blade extension algorithm
node ${CLAUDE_SKILL_DIR}/scripts/blade.js score http://localhost:3000 --json --threshold 95

# Static advisory scan of source files
node ${CLAUDE_SKILL_DIR}/scripts/blade.js audit /path/to/app

# Final gate: score threshold + high-risk static drift
node ${CLAUDE_SKILL_DIR}/scripts/blade.js gate http://localhost:3000 /path/to/app --threshold 95
```

### Commands

| Command | Purpose | Default failure behavior |
| --- | --- | --- |
| `score <url>` | Measures live DOM Blade coverage. | Fails only when `--threshold` is provided and unmet. |
| `audit [path]` | Reports custom CSS and missed-Blade drift with file/line evidence. | Advisory; exits 0 unless setup fails. |
| `gate <url> [path]` | Runs `score` plus `audit`. | Defaults to `--threshold 95`; fails on low score or high-risk drift. |

### Shared flags

| Flag | Default | Description |
| --- | --- | --- |
| `--threshold <n>` | `95` in `gate`, none in `score` | Minimum coverage percentage. |
| `--no-navbars` | off | Exclude Blade `sidenav` and `top-nav` nodes from runtime coverage. |
| `--headed` | off | Show browser window for auth/debugging. |
| `--json` | off | Emit machine-readable output. |
| `--storage-state <path>` | none | Playwright auth state file. |
| `--settle-ms <n>` | `1000` | Wait after `domcontentloaded` before measuring. |
| `--timeout-ms <n>` | `30000` | Navigation timeout. |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success, or advisory audit completed. |
| 1 | Runtime Blade coverage below threshold. |
| 2 | Usage, setup, or dependency error. |
| 3 | Navigation or auth timeout. |
| 4 | Gate failed because high-risk static drift was found. |

## Prerequisites

Playwright must be available in the consumer project or globally for `score` and `gate`:

```bash
npm install playwright && npx playwright install chromium
```

The script resolves `playwright` from `process.cwd()/node_modules` first, so projects with Playwright already installed work without a Dex-local dependency.
