# dex

Dex is a small agent toolkit for the work that keeps repeating: setting up an agent environment, explaining unfamiliar concepts before execution, finding the crux of a product problem, checking design quality, shipping Blade-heavy dashboard work, reviewing plans with another model, and turning media or memory into something usable.

It is not a giant prompt pack. The point is to keep the sharp workflows close, named plainly, and split by ownership so an agent can load the right behavior without dragging half the repo into context.

## The Shape

Dex ships five marketplace plugins.

| Plugin | Owns | Does not own |
|---|---|---|
| `core` | Agent setup, explaining unfamiliar concepts, council-style investigation, reflection, DevRev, session wrap-up, Portent/Tolaria knowledge records | Design implementation, browser tooling, media utilities |
| `design` | Product thinking, content design, divergence, presentation narrative, interactive playground artifacts | Blade, shaders, sound, generic code hardening, private review frameworks |
| `dev` | Design engineering: Blade, dashboard implementation, hardening, shaders, sound | Product strategy, presentation coaching, third-party browser tools |
| `tools` | Utility tools: Codex review, browser-native HTML visual briefs, unified media generation/optimization, official mymind MCP | Core setup, design critique, implementation doctrine |
| `fun` | Anti-productivity experiments, generative games, voice and taste exercises, strange-but-contained creative prompts | Setup, production work, factual research, workflow automation |

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
/plugin install fun@nawwwal-dex
```

Current released versions:

<!-- dex-current-versions:start -->
| Plugin | Version |
|---|---:|
| `core` | `1.2.9` |
| `design` | `1.2.4` |
| `dev` | `1.0.5` |
| `tools` | `1.3.0` |
| `fun` | `1.0.0` |
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

Optional integrations depend on the skill you use: Figma MCP for Figma work, DevRev MCP for DevRev workflows, Slack MCP for message workflows, qmd for Portent search, Tolaria MCP for Portent vault discovery/opening/writeback, the official mymind MCP for mymind search, and `agent-browser` for skills that explicitly call it as an external browser tool. Dex does not package `agent-browser`.

## What Each Plugin Gives You

### Core

`core` is the control plane. It should stay boring in the best way: setup, explanation before execution, routing to durable records, and workflows that help agents reason across context and close sessions cleanly.

| Skill | Use it for |
|---|---|
| `dex` | Fresh setup, doctor checks, `.agents` bootstrap, Claude/Codex compatibility links, project design-context capture |
| `why` | Explaining unfamiliar code, architecture, concepts, alternatives, tradeoffs, and clever functions before execution; using Tolaria/Portent as the knowledge base for learner profiles and saved concepts |
| `council` | Multi-domain parallel investigation with dynamic lens composition: design critique, product decisions, research, code audits, workflow friction, expert debate |
| `reflect` | Portent/Tolaria reflection: emerging patterns, leverage points, and drift across active knowledge objects |
| `devrev` | Sprint routines, grooming, enrichment, schema-discovered DevRev MCP work, and Portent-backed local DevRev knowledge |
| `wrap` | End-of-session recap, meaningful micro-commits, verification summary, and Portent handoff |
| `portent` | Tolaria knowledge-base capture, qmd-backed search, session logs, project context, source packets, derived assertions, MOCs, current todos, briefings, organization, and archive using the Portent object model |

`why` treats `teach` and `learn` as routing aliases, but the canonical skill and visible token are `why`. It uses Tolaria/Portent for learner profiles and saved concepts instead of a local SQLite memory index. `portent` uses qmd for Portent search and Tolaria for vault discovery, note opening, and writeback. It ships a prompt-time context receipt hook that reminds the agent to use `core:portent` before behavior-changing work when prior context may matter, then write durable session knowledge back before the final response when useful. Codex hooks run when `[features].hooks` is enabled and the hook is trusted through the normal `/hooks` review flow.

`council` lives here because it is a thinking primitive, not a misc tool.

### Design

`design` is for deciding what something should be and how to explain it. It should not own implementation-specific systems.

| Skill | Use it for |
|---|---|
| `content-design` | Product copy, UX writing, voice systems, in-product marketing, Razorpay-style marketing copy, errors, empty states, onboarding, accessibility labels, localization checks, and copy audits |
| `crux` | Compressing vague claims, PRDs, opinions, or product problems down to the load-bearing issue |
| `diverge` | Layered brainstorms, alternatives, product directions, interaction concepts, and different approaches with fast/explore/deep tiers, companion routing, and eval-backed regression coverage |
| `present` | Design review narrative, meeting-flow strategy, stakeholder framing, rehearsal, explaining tradeoffs to a room, and handoff to browser-native deck production |
| `playground` | Interactive playgrounds with build/sketch modes, HTML quality contract, template scaffolds, and eval-backed output validation for topics, systems, design, copy, and handoffs |

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
| `brief` | Browser-native editorial HTML briefs with dynamic sectioning, Blackline-style visuals, inline sources, read-next links, adaptive color themes, and floating section navigation |
| `media-tools` | AI image generation/editing, compression, format conversion, and resizing for images and video |

It also bundles the official mymind MCP server. Use `/mcp` or the Codex MCP server UI to authenticate when the client prompts.

Tools should stay tools. If a tool grows taste, policy, or product judgment, it probably belongs somewhere else.

### Fun

`fun` is the plugin that is not about getting work done. Every other plugin helps you finish a task. `fun` does the opposite. It tells the model to stop acting like a polite, agreeable assistant and instead surprise you: make ordinary things strange, compete, guess, and play. The point is the surprise, not the output. For the full idea behind it, the shared building blocks, and the safety rules, see `plugins/fun/README.md`.

| Skill | Use it for |
|---|---|
| `gravity` | Rewrite a piece of text over and over and watch what it turns into. Run it on your own writing to find the voice you fall back on without thinking. Example: rewrite a paragraph 30 times and see what is left. |
| `oracle` | Talk to a version of the model that only knows the world up to a year you pick. What it cannot imagine shows you what is actually new. Example: ask a 1995 mind to make sense of your phone. |
| `register` | Take everyday information and deliver it in one strong character that never breaks. `--image` narrates a photo (your messy desk as a film noir scene). `--feed` rewrites your daily weather or calendar in a fixed voice every morning. |
| `clone` | Feed it your own writing so it can finish your sentences the way you would. Or split it into two copies of you that argue a decision you are stuck on while you pick the winner. |
| `arena` | Set up a crowd of small characters with different personalities and let them play a game against each other many times. Watch trust, grudges, and cooperation appear on their own. |
| `nemesis` | Tell it a belief you hold. It attacks that belief as hard as it can, then keeps only the points you cannot answer. Can run every week against your strongest opinions. |
| `augury` | Pull a few random things from your own saved notes and find the thread between them. Like tarot, but the cards are your own stuff. It picks at random, you read the meaning. |
| `cartography` | Give it an exported chat history and it maps the shape of the relationship: who texts first, the inside jokes, the warm and cold stretches. It tells you the unflattering parts too. |
| `quest` | Turn your real city into a scavenger hunt. You give it real places, it writes a story and clues that only make sense when you are standing there. Example: a Sunday hunt across your neighborhood. |
| `prospect` | It invents a brand new two-player word game, teaches you the rules, and plays it with you. Most of them are broken, and that is half the fun. |
| `cosmogony` | Give it one silly idea and it builds the whole world that would follow, with a straight face: the rules, the society, the holidays, the wars. Example: what if every houseplant was secretly spying on you. |
| `branch` | Pick a fork in the road, a real decision or a what-if, and it plays out each path in detail, years into the future, side by side. It keeps every version honest, bad parts included. |
| `seance` | Rebuild how someone who is gone used to write, from their old messages, so you can ask the thing you never got to. You open it once and then close it. It is not a chatbot of the dead. |

`fun` is allowed to be strange, but never dishonest. Its safety rules are built into the skills, not optional: keep private things private, never just flatter you, keep the random draw truly random, never invent real places, and treat the seance as a one-time thing you close.

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
/dex release fun initial
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
/plugin update fun@nawwwal-dex
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
