---
name: council
description: >
  Use when multi-agent deep investigation is needed across a codebase, vault, or problem space.
  Triggers on: "council", "/council [topic]", "deep research on", "thoroughly investigate",
  "full audit of", "multi-agent analysis of", "audit the vault", "find inconsistencies",
  "what's wrong with", "investigate this".
argument-hint: "[topic or area of interest]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, mcp__qmd__query, mcp__qmd__vsearch, mcp__qmd__search
---

# Council — Multi-Agent Research

Topic: **$ARGUMENTS**

Follow the full protocol in `$CLAUDE_SKILL_DIR/instructions.md`.
Output format is defined in `$CLAUDE_SKILL_DIR/output-template.md`.
