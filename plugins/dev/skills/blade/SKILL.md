---
name: blade
description: "Use for Razorpay Blade UI work: MCP-backed component/pattern truth, exact pattern recreation, Blade-only motion, coverage, drift audit, and browser validation."
allowed-tools: Read, Grep, Glob, Bash
---

# blade

Blade operating workflow for Razorpay UI work. This skill is a guidance layer over Blade MCP. MCP is the API source of truth; this skill decides what to ask MCP and how to implement product-quality UI with Blade primitives, patterns, tokens, and motion instead of custom CSS or undocumented motion wrappers.

Browser work in this skill uses `agent-browser`, not Playwright. For the detailed browser workflow, read `references/agent-browser.md`.

## Core workflow

1. Identify the real consumer app root. Use the app being edited, not the Dex plugin repo. Confirm `package.json` contains `@razorpay/blade` when possible.
2. Classify product intent before coding: known pattern recreation, page pattern, semantic component owner, token/util need, motion, or runtime verification. If the user names or implies a known Blade pattern, read `references/pattern-recreation.md` before component selection.
3. Query Blade MCP for the exact contract. MCP proves props, slots, triggers, providers, icons, tokens, examples, and constraints. Storybook/index and local source can help with vocabulary; they do not prove Blade API.
4. Declare ownership. Blade owns product meaning, interaction, feedback, surfaces, typography, and motion. `Box` and local layout wrappers may arrange Blade components, provide stable dimensions, or create a DOM/ref boundary; they must not replace Blade behavior.
5. Prove runtime behavior when visual state, motion, focus, overlay, navigation, disclosure, or hover changed. `blade gate` checks compliance/drift only; it is necessary, not sufficient.

Before non-trivial Blade edits, keep this working note in your context:

```text
Intent: <pattern/component/token/motion/runtime>
Blade candidate: <candidate names; not contract>
MCP proof: <patterns/components/topics checked; constraints extracted>
Owner: <semantic owner>; layout code owns only <arrange/layer/stable dimensions/ref boundary>
Verification: <browser proof | auth-blocked fallback | static-only reason>
```

## Intent classifier

| User intent | First reference | MCP packet | Proof required |
| --- | --- | --- | --- |
| Recreate a known Blade pattern or a prompt that implies one | `references/pattern-recreation.md` | Pattern docs first, then listed component docs and general docs | Pattern parity checklist plus browser proof or explicit auth blocker |
| Choose components for a product surface | `references/component-selection.md` then `references/mcp-workflow.md` | Candidate components with `currentProjectRootDirectory` | Source/type proof; browser proof if visual or interactive |
| Decide whether Blade owns a surface, token, wrapper, or fallback | `references/surface-taxonomy.md` | Component, token, or general docs that match the owner | Limitation log when Blade cannot express it |
| Improve feel, density, focus, hover, surface polish, or transition mapping | `references/interaction-quality.md` | MCP docs for the owning component and any motion primitive | Browser interaction proof |
| Implement animation, route motion, hover/focus/tap, or branded loading/success | `references/motion.md` | Motion primitive or pattern docs | Browser diff/screenshot plus reduced-motion/focus sanity |
| Validate a live route, auth flow, overlay, or responsive behavior | `references/agent-browser.md` | N/A unless Blade APIs changed | Runtime proof packet |

## Triggered references

- Exact known pattern recreation: `references/pattern-recreation.md`.
- Product-surface ownership, source-truth order, or fallback decisions: `references/surface-taxonomy.md`.
- Component choice after pattern routing is ruled out: `references/component-selection.md`.
- MCP lookup, name failures, or version/source truth: `references/mcp-workflow.md`.
- Interaction polish, transition mapping, typography, density, hit areas, surface feel: `references/interaction-quality.md`.
- Motion primitive API, animation triggers, hover/focus/tap implementation, route motion, branded success/loading: `references/motion.md`.
- Browser/runtime proof, auth, screenshots, or interaction diff: `references/agent-browser.md`.
- Razorpay Dashboard-specific traps: `references/dashboard-gotchas.md`.

`interaction-quality.md` decides whether an interaction belongs in the product context. `motion.md` decides which Blade motion primitive and trigger contract can implement it. Use both for motion-sensitive UI.

## Hard gates

Every rule should force one of three outcomes: use a Blade primitive, query MCP for exact API, or document a Blade limitation and choose the closest Blade-native behavior.

| Question | What to decide | Failure signal |
| --- | --- | --- |
| Product meaning | Which Blade primitive or pattern owns it? | A layout wrapper, CSS class, local component, or motion wrapper owns meaning Blade covers. |
| API truth | What did MCP confirm? | A prop, child slot, trigger, provider, token, or icon was assumed from memory. |
| Product fit | Does the available API fit this context? | Available API is treated as permission even when it causes poor interaction, layout, or focus behavior. |
| Blade-only constraint | What does Blade not expose, and which Blade-native fallback did you choose? | Custom CSS, undocumented Framer wrappers, timers, or local wrappers recreate behavior Blade should own. |
| Runtime proof | What did the browser prove? | `blade gate` is used as final proof for visual or interactive work. |

MCP hard stop: if Blade MCP is unavailable, unauthorized, or cannot read the consumer app root after one correction, do not claim a Blade prop, slot, trigger, provider, icon, or pattern API. You may inspect local source for installed-version evidence, but label the result as `MCP unavailable; API unverified`.

## CLI

Resolve the Blade skill directory first. In the Dex repo, run commands from the repo root as `node plugins/dev/skills/blade/scripts/blade.js ...`. In an installed Claude skill, `${CLAUDE_SKILL_DIR}` points at this directory. In any other runtime, use the directory containing this `SKILL.md`.

```bash
# Runtime coverage, same canonical Blade extension algorithm
node plugins/dev/skills/blade/scripts/blade.js score http://localhost:3000 --json --threshold 95

# Static advisory scan of source files
node plugins/dev/skills/blade/scripts/blade.js audit /path/to/app

# Final gate: score threshold + high-risk static drift
node plugins/dev/skills/blade/scripts/blade.js gate http://localhost:3000 /path/to/app --threshold 95
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
| `--headed` | off | Pass headed mode to `agent-browser` for auth/debugging. |
| `--json` | off | Emit machine-readable output. |
| `--state <path>` | none | Pass an Agent Browser state file for authenticated pages. |
| `--profile <name-or-path>` | none | Reuse a Chrome profile snapshot or persistent profile path. |
| `--session <name>` | generated | Reuse a named Agent Browser session. Generated sessions close automatically. |
| `--keep-open` | off | Keep a generated session open for inspection after scoring. |
| `--settle-ms <n>` | `1000` | Run `agent-browser wait <n>` after navigation before measuring. |
| `--timeout-ms <n>` | `30000` | Sets `AGENT_BROWSER_DEFAULT_TIMEOUT` for score/gate commands. |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success, or advisory audit completed. |
| 1 | Runtime Blade coverage below threshold. |
| 2 | Usage, setup, or dependency error. |
| 3 | Navigation or auth timeout. |
| 4 | Gate failed because high-risk static drift was found. |

## Prerequisites

Agent Browser must be available for `score`, `gate`, and browser validation:

```bash
npm install -g agent-browser
agent-browser install
agent-browser doctor --offline --quick
```

Use `--state`, `--profile`, or `--session` for authenticated dashboards. Do not add Playwright dependencies for this skill.
