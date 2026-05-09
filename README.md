# dex

Dex is a small agent toolkit for the work that keeps repeating: setting up an agent environment, finding the crux of a product problem, checking design quality, shipping Blade-heavy dashboard work, reviewing plans with another model, and turning media or memory into something usable.

It is not a giant prompt pack. The point is to keep the sharp workflows close, named plainly, and split by ownership so an agent can load the right behavior without dragging half the repo into context.

## The Shape

Dex ships four marketplace plugins.

| Plugin | Owns | Does not own |
|---|---|---|
| `core` | Agent setup, council-style investigation, communication, reflection, DevRev, session logs | Design implementation, browser tooling, media utilities |
| `design` | Product thinking, divergence, presentation narrative, 5F design review, visual handoffs | Blade, shaders, sound, generic code hardening |
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

Optional integrations depend on the skill you use: Figma MCP for Figma work, DevRev MCP for DevRev workflows, Slack MCP for message workflows, `mymind` for mymind search, and `agent-browser` for skills that explicitly call it as an external browser tool. Dex does not package `agent-browser`.

## What Each Plugin Gives You

### Core

`core` is the control plane. It should stay boring in the best way: setup, routing to durable records, and workflows that help agents reason across context.

| Skill | Use it for |
|---|---|
| `dex` | Fresh setup, doctor checks, `.agents` bootstrap, Claude/Codex compatibility links, project design-context capture |
| `council` | Parallel research, code audits, expert lenses, blind-spot passes, architecture investigations |
| `communicate` | Drafting or sending Slack messages in the user's voice |
| `reflect` | Surfacing patterns from sessions, finding leverage, noticing drift |
| `devrev` | Sprint routines, grooming, enrichment, DevRev issue/enhancement work |
| `log` | Task-scoped session journals after real work is done |

`council` lives here because it is a thinking primitive, not a misc tool.

### Design

`design` is for deciding what something should be and how to explain it. It should not own implementation-specific systems.

| Skill | Use it for |
|---|---|
| `crux` | Compressing vague claims, PRDs, opinions, or product problems down to the load-bearing issue |
| `diverge` | Brainstorms, alternatives, product directions, interaction concepts, different approaches |
| `present` | Design review narrative, stakeholder framing, rehearsal, explaining tradeoffs to a room |
| `reviewing-designs-5f` | Razorpay UX research team's 5F review framework for B2B SaaS design critique |
| `visual` | Diagrams, system flows, dense explanations, visual handoffs, component/state/screen breakdowns |

Design has no catch-all router now. If the user wants Blade, go to `dev`. If the user wants browser automation, use the relevant external browser tool. If the user wants generic critique, pick the concrete review skill instead of launching a manifesto.

### Dev

`dev` is where design becomes code and production behavior.

| Skill | Use it for |
|---|---|
| `blade` | Razorpay Blade adherence, Blade score, component selection, design-system drift |
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

The root marketplace files expose those plugins:

```text
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
```

For local Codex development, the repo marketplace lives at:

```text
.agents/plugins/marketplace.json
```

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

Release maintenance is project-local. The shipped `core` plugin owns user-facing `/dex setup`; repo-maintainer release logic lives in:

```text
.agents/skills/dex/
.claude/skills/dex/
```

Examples:

```text
/dex release dev
/dex release design minor
/dex release tools minor
```

The release skill:

1. Checks that the repo is on `main` and clean.
2. Bumps the selected plugin's Claude and Codex manifests.
3. Updates the Claude marketplace metadata.
4. Validates the Codex marketplace shape.
5. Commits, tags, pushes, and creates a GitHub Release.

Version policy:

| Bump | Use it when |
|---|---|
| `patch` | Bug fix, wording change, metadata-only update, or behavior-preserving edit |
| `minor` | New skill, moved skill with a replacement path, renamed skill with an obvious successor, noticeable behavior change |
| `major` | Rare. Existing installs cannot keep working without manual migration |
| `initial` | First release of a newly added plugin |

Major is not a cleanup prize. If there is no explicit migration step for users, use `minor`.

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
