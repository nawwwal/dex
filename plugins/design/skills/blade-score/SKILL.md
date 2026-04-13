---
name: blade-score
description: "Use when measuring Blade design system adoption on a live page URL. Triggers on: blade score, blade coverage, design system percentage, % blade components, coverage check."
argument-hint: "<url> [--threshold 95] [--no-navbars] [--headed] [--json] [--storage-state path]"
user-invocable: true
allowed-tools: Bash
---

# blade-score

Measures Blade design system coverage on a running page. Runs the canonical `calculateBladeCoverage` algorithm (vendored from the Blade Chrome extension) via headless Playwright.

## Quick usage

```bash
node ${CLAUDE_SKILL_DIR}/scripts/blade-score.js https://x.razorpay.com/app/dashboard

# Blade Coverage: 78.43%
# Blade Nodes:    266 / 341
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--threshold <n>` | none | Exit 1 if coverage < n% |
| `--no-navbars` | off | Exclude sidenav and top-nav from the count |
| `--headed` | off | Show browser window (useful for debugging auth) |
| `--json` | off | Output `{ url, bladeCoverage, totalNodes, bladeNodes, threshold, pass }` |
| `--storage-state <path>` | none | Playwright storage state file for authenticated pages |
| `--settle-ms <n>` | 1000 | Wait n ms after `domcontentloaded` before measuring |
| `--timeout-ms <n>` | 30000 | Navigation timeout in ms |

## Auth

For pages that require login, pass a Playwright storage state file:

```bash
# Save auth state once (with agent-browser or Playwright codegen)
agent-browser --headed open https://x.razorpay.com && agent-browser state save /tmp/rzp.json

# Then pass it to blade-score
node ${CLAUDE_SKILL_DIR}/scripts/blade-score.js https://x.razorpay.com/app/home \
  --storage-state /tmp/rzp.json
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success (or no threshold set) |
| 1 | Coverage below `--threshold` |
| 2 | Setup or dependency error |
| 3 | Navigation or auth timeout |

## Script mode (for other skills)

```bash
result=$(node ${CLAUDE_SKILL_DIR}/scripts/blade-score.js "$URL" --json)
coverage=$(echo "$result" | jq '.bladeCoverage')
```

## How it works

Counts all visible, non-empty, non-media DOM elements under `body *`. An element is a **Blade node** if it has `data-blade-component`. Excluded from the count:
- Hidden elements (recursive ancestor check, `element.hidden`, `display:none`, etc.)
- Empty nodes (no childNodes)
- Media elements (`img`, `video`, `audio`, `source`, `picture`)
- SVG internals (children of `data-blade-component="icon"`)
- Blade `box` wrappers (transparent container, not a semantic component)
- Table-cell inner divs (Blade table library internals)
- When `--no-navbars`: elements inside `data-blade-component="sidenav"` or `"top-nav"`

Coverage = `bladeNodes / totalNodes × 100`, two decimal places.

## Prerequisites

Playwright must be available in the project or globally:

```bash
npm install playwright && npx playwright install chromium
```

The script resolves `playwright` from `process.cwd()/node_modules` first, so a project that already has Playwright installed works without any extra setup.
