# dex

Dex is a small agent toolkit for the work that keeps repeating: setting up an agent environment, teaching unfamiliar concepts before execution, finding the crux of a product problem, checking design quality, shipping Blade-heavy dashboard work, reviewing plans with another model, and turning media or memory into something usable.

It is not a giant prompt pack. The point is to keep the sharp workflows close, named plainly, and split by ownership so an agent can load the right behavior without dragging half the repo into context.

## The Shape

Dex ships four marketplace plugins.

| Plugin | Owns | Does not own |
|---|---|---|
| `core` | Agent setup, teaching unfamiliar concepts, council-style investigation, communication, reflection, DevRev, session wrap-up, Portent/Tolaria knowledge records | Design implementation, browser tooling, media utilities |
| `design` | Product thinking, content design, divergence, presentation narrative, interactive playground artifacts | Blade, shaders, sound, generic code hardening, private review frameworks |
| `dev` | Design engineering: Blade, dashboard implementation, hardening, shaders, sound | Product strategy, presentation coaching, third-party browser tools |
| `tools` | Utility tools: Codex review, image generation, media optimization, mymind | Core setup, design critique, implementation doctrine |

This split is the product. When a workflow starts to sprawl, move it to the plugin that owns the actual behavior instead of making a router that knows too much.

## Install

Add the marketplace once:

```text
/plugin marketplace add nawwwal/dex
```

Install only what you need:

```text
/plugin install core@nawwwal-dex
/plugin install design@nawwwal-dex
/plugin install dev@nawwwal-dex
/plugin install tools@nawwwal-dex
```

Current released versions:

<!-- dex-current-versions:start -->
| Plugin | Version |
|---|---:|
| `core` | `1.1.2` |
| `design` | `1.2.1` |
| `dev` | `1.0.4` |
| `tools` | `1.0.2` |
<!-- dex-current-versions:end -->

Then bootstrap the shared agent home:

```text
/dex setup
```

`/dex setup` creates and verifies the current `~/.agents/` structure, then wires Claude/Codex compatibility links. It does not read Slack, DevRev, Drive, Figma, or any external service. Setup should make the machine usable, not pretend to know the person.

Required local binaries:

```text
python3
jq
node
```

Optional integrations depend on the skill you use: Figma MCP for Figma work, DevRev MCP for DevRev workflows, Slack MCP for message workflows, Tolaria MCP for Portent knowledge-base work, `mymind` for mymind search, and `agent-browser` for skills that explicitly call it as an external browser tool. Dex does not package `agent-browser`.

## What Each Plugin Gives You

### Core

`core` is the control plane. It should stay boring in the best way: setup, teaching, routing to durable records, and workflows that help agents reason across context and close sessions cleanly.

| Skill | Use it for |
|---|---|
| `dex` | Fresh setup, doctor checks, `.agents` bootstrap, Claude/Codex compatibility links, project design-context capture |
| `teach` | Explaining unfamiliar code, architecture, concepts, alternatives, tradeoffs, and clever functions before execution; recording learned concepts in `~/.agents/memory/teach/` with a hook-refreshed SQLite search index |
| `council` | Parallel research, code audits, expert lenses, blind-spot passes, architecture investigations |
| `communicate` | Drafting or sending Slack messages in the user's voice |
| `reflect` | Portent/Tolaria reflection: emerging patterns, leverage points, and drift across active knowledge objects |
| `devrev` | Sprint routines, grooming, enrichment, DevRev issue/enhancement work |
| `wrap` | End-of-session recap, meaningful micro-commits, verification summary, and Portent handoff |
| `portent` | Tolaria knowledge-base capture, session logs, project context, current todos, briefings, organization, search, and archive using the Portent object model |

`teach` ships a Codex Stop hook for refreshing its SQLite concept index. Codex plugin hooks run only when `[features].plugin_hooks = true` is enabled and the hook is trusted through the normal `/hooks` review flow; without that, the Markdown notes remain canonical and the index can be rebuilt manually.

`council` lives here because it is a thinking primitive, not a misc tool.

### Design

`design` is for deciding what something should be and how to explain it. It should not own implementation-specific systems.

| Skill | Use it for |
|---|---|
| `content-design` | Product copy, UX writing, voice systems, in-product marketing, Razorpay-style marketing copy, errors, empty states, onboarding, accessibility labels, localization checks, and copy audits |
| `crux` | Compressing vague claims, PRDs, opinions, or product problems down to the load-bearing issue |
| `diverge` | Brainstorms, alternatives, product directions, interaction concepts, different approaches |
| `present` | Design review narrative, stakeholder framing, rehearsal, explaining tradeoffs to a room |
| `playground` | Interactive, visually distinctive playgrounds for exploring topics, systems, code, data, design, copy, motion, reviews, and handoffs. |

Design has no catch-all router now. If the user wants Blade, go to `dev`. If the user wants browser automation, use the relevant external browser tool. If the user wants critique from a private review framework, keep that framework as a local skill outside Dex.

### Dev

`dev` is where design becomes code and production behavior.

| Skill | Use it for |
|---|---|
| `blade` | Razorpay Blade adherence, Blade MCP workflow, known pattern recreation, component ownership, interaction quality, motion primitives, Blade-only constraints, Blade score, design-system drift |
| `dashboard-design` | Razorpay dashboard feature workflows: create, build, share, PR, ship |
| `harden` | A11y, density, hierarchy, typography, state coverage, production UI checks |
| `shader` | GLSL, Shadertoy, SDFs, procedural visuals, fragment shader effects |
| `create-sound` | Sound definitions, audio feedback, reverse-engineering samples, rendering previews |

This plugin exists because coding agents need different instructions than design agents. A design critique can be exploratory. A code change needs evidence, file refs, constraints, and verification.

### Tools

`tools` is for utilities that help other work happen.

| Skill | Use it for |
|---|---|
| `codex` | Cross-model plan review through the Codex CLI |
| `generate-image` | Image generation and editing through local scripts |
| `media-optimizer` | Compressing, converting, resizing images and video |
| `mymind` | Searching, saving, organizing, and inspecting mymind |

Tools should stay tools. If a tool grows taste, policy, or product judgment, it probably belongs somewhere else.

## The Agent Home

Dex uses `~/.agents` as the shared source of truth.

```text
~/.agents/
├── AGENTS.md
├── instructions/
├── references/
├── memory/
│   ├── preferences/
│   ├── reference/
│   └── records/
├── skills/
├── plugins/
└── state.json
```

Claude compatibility links point back into that tree:

```text
~/.claude/CLAUDE.md -> ~/.agents/AGENTS.md
~/.claude/memory    -> ~/.agents/memory
~/.claude/skills    -> ~/.agents/skills
```

The rule is simple: one control plane, compatibility links where needed. Do not create parallel homes and then ask agents to guess which one matters.

## Custom Skills

Plugin files are managed by the plugin system. Personal overrides belong in `~/.agents/skills`.

```text
~/.agents/skills/my-skill/SKILL.md
```

Local skills take precedence over plugin skills. That is where experiments, personal workflows, and private edits should live. The plugin should carry reusable behavior, not every local preference.

## Repo Development

There is no build step. This repo is Markdown, JSON, shell, and small scripts.

Edit under:

```text
plugins/
```

Each plugin has both runtime manifests:

```text
plugins/<plugin>/.claude-plugin/plugin.json
plugins/<plugin>/.codex-plugin/plugin.json
```

Codex UI metadata, including plugin logos and composer icons, lives in each plugin's `.codex-plugin/plugin.json` and points at files under `plugins/<plugin>/assets/`.

The root marketplace files expose those plugins:

```text
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
```

For local Codex development, the repo marketplace lives at:

```text
.agents/plugins/marketplace.json
```

Codex marketplace entries use `local` sources, with paths relative to the marketplace checkout. The marketplace itself is Git-tracked; individual plugin entries should not use Git source fields.

After editing plugin files, start a new session or run:

```text
/reload-plugins
```

## Adding a Skill

Create:

```text
plugins/<plugin>/skills/<one-word-name>/SKILL.md
```

Use frontmatter:

```md
---
name: one-word-name
description: "Use when..."
---
```

Skill names should be short routing tokens, not sentence fragments or fake departments. The description is routing surface, not marketing copy. It should say when the skill should load and what it owns.

Before adding a skill, ask:

- Is this a reusable behavior or just a note?
- Which plugin owns the outcome?
- What evidence should an agent inspect?
- What tools should it call or avoid?
- What should it return?
- How does the agent know it is done?

If those answers are vague, the skill is not ready.

## Release Workflow

Release and skill-eval maintenance are project-local. The shipped `core` plugin owns user-facing `/dex setup`; repo-maintainer release and eval logic lives in:

```text
.agents/skills/dex/
.claude/skills/dex/
```

Examples:

```text
/dex release dev
/dex release design
/dex release tools minor
/dex eval plugins/design/skills/crux
```

The release skill:

1. Checks that the repo is on `main` and clean.
2. Requires README and release-doc review when plugin topology, skill inventory, marketplace metadata, or user-facing behavior changed.
3. Bumps the selected plugin's Claude and Codex manifests.
4. Updates the Claude marketplace metadata.
5. Validates the Codex marketplace shape.
6. Commits, tags, pushes, and creates a GitHub Release.

Version policy:

| Bump | Use it when |
|---|---|
| `patch` | Default: skill edits/removals, prompt rewrites, metadata fixes, docs updates, stale/private content removal |
| `minor` | Meaningful new public capability: new plugin, new skill family, new setup command, new integration path |
| `major` | Rare: plugin/marketplace/install contract changed |
| `initial` | First release of a newly added plugin |

Skills are package contents, not library APIs. Skill edits and removals are patch releases. Major is only for marketplace/install-contract changes.

The eval skill is for testing and improving Dex skills before release. It uses `skill-creator` and runs repeated eval-and-repair rounds: snapshot the current skill, design or refresh the relevant eval suite before touching the target skill, run clean-context trigger and quality evals, grade deterministic and rubric checks, diagnose failures, repair the skill or evals, then re-run. Local run artifacts belong under `.dex/evals/`; commit only durable skill changes, eval fixtures, validators, and docs.

## Update

Update installed plugins:

```text
/plugin update core@nawwwal-dex
/plugin update design@nawwwal-dex
/plugin update dev@nawwwal-dex
/plugin update tools@nawwwal-dex
```

Or reload active sessions:

```text
/reload-plugins
```

For Codex tracked marketplace installs, committed and pushed changes are what matter. Local uncommitted source edits do not magically appear in the tracked install.

## Maintenance Rules

- Keep plugin boundaries sharper than the prose. If a skill owns Blade, it belongs in `dev`, not `design`.
- Do not recreate third-party tools as Dex skills. Route to them or document the dependency.
- Do not add broad routers unless routing is the product. Prefer a skill that owns one outcome.
- Do not hide implementation detail in beautiful language. A skill should change agent behavior predictably.
- Keep examples current or delete them. Stale examples are worse than no examples.
- Update README, manifests, marketplace metadata, and release docs in the same pass when topology changes.

Dex should feel like a set of well-labeled cupboards on a messy workbench: open the right one, do the work, close it, move on.
