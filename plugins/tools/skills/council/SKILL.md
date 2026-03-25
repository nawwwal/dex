---
name: council
description: "Multi-agent deep investigation across codebase or vault."
disable-model-invocation: true
argument-hint: "[topic or area of interest]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, mcp__qmd__query, mcp__qmd__vsearch, mcp__qmd__search
---

# Council — Multi-Agent Research

Topic: **$ARGUMENTS**

Follow the full protocol in `$CLAUDE_SKILL_DIR/instructions.md`.
Output format is defined in `$CLAUDE_SKILL_DIR/output-template.md`.
