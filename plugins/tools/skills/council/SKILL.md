---
name: council
description: "Multi-angle investigation across code, vault, systems, and workflows. Use when you need an audit, blind-spot review, dependency map, inconsistency hunt, architecture investigation, workflow fragility review, risk review, or a 'what are we missing?' pass."
disable-model-invocation: true
argument-hint: "[topic] [--mode auto|code|vault|system|workflow] [--depth quick|standard|deep] [--goal findings|risks|decision|actions]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, AskUserQuestion, mcp__qmd__query, mcp__qmd__vsearch, mcp__qmd__search
---

# Council — Intent-Aware Multi-Agent Investigation

Topic: **$ARGUMENTS**

Start with `$CLAUDE_SKILL_DIR/references/router.md`.

Follow this order:

1. Infer `mode`, `depth`, and `goal` from the prompt and explicit flags.
2. Ask 0-3 structured questions only if intent is still ambiguous. Use `$CLAUDE_SKILL_DIR/references/questions.md`.
3. Load only the selected mode file from `$CLAUDE_SKILL_DIR/references/modes/`.
4. Load `$CLAUDE_SKILL_DIR/references/depths.md`.
5. Load `$CLAUDE_SKILL_DIR/references/synthesis.md`.
6. Load `$CLAUDE_SKILL_DIR/references/examples.md` only if routing or prompt shaping is still unclear.

Hard rules:

- Keep the initial read surface lean. Do not load every reference file up front.
- Downshift to the smallest useful council for the request.
- Optimize for perspective diversity, not parallel repetition.
- Always include a devil's advocate lens and a blind-spot lens.
- Surface contradictions, confidence, and next actions in the final report.
