---
name: dex
description: "Use when configuring or checking a Dex agent environment, especially fresh installs, .agents bootstrap, Claude/Codex compatibility links, plugin wiring, or project design context capture."
disable-model-invocation: true
argument-hint: "[setup | doctor | setup design]"
---

# /dex - Dex Environment

## Dispatch

**setup** or **doctor** -> Read `$CLAUDE_SKILL_DIR/setup.md`

**setup design** -> Read `$CLAUDE_SKILL_DIR/design-context.md`
Generates `.agents/DESIGN.md` with project design system context.

If no argument: ask whether to run environment setup/doctor or design context capture.
