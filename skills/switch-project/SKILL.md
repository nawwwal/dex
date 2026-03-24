---
name: switch-project
description: "Use when switching context to a different project — 'switch to [project]', 'work on [project]', or 'context switch'."
argument-hint: "[project-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__qmd__search, mcp__qmd__vsearch
---

# Project Context Switch

Cleanly transition between projects by loading target context.

## Steps

### 1. Identify Target Project

Parse the argument to identify which project. Match against known projects:
- `nexus` / `agent-marketplace` → `~/projects/nexus-agent-marketplace/`
- `dashboard` → `~/projects/dashboard/`
- `i18n` / `checkout` → `~/projects/i18n-checkout/`
- `co-branding` / `configurator` → `~/projects/Co-branding UI Configurator/`
- `logovault` → `~/projects/logovault/`
- `moto` / `sg` → `~/projects/moto-singapore/`
- `ralph` → `~/projects/ralph-main/`
- `dialkit` → `~/projects/dialkit/`

### 2. Load Project Context

1. Read the project's `CLAUDE.md` if it exists
2. Read `~/.claude/memory/projects.md` for project status
3. Search QMD for recent project docs: `qmd_search` with project name
4. Check git status in the project directory
5. Show the last 5 commits if it's a git repo

### 3. Present Context Summary

```
## Switching to: [Project Name]

### Project Info
[from CLAUDE.md or projects.md]

### Current State
- Branch: [current branch]
- Last commit: [date] — [message]
- Uncommitted changes: [yes/no]

### Recent Activity
[last 5 commits]

### Related Docs
[QMD search results]
```

### 4. Suggest Next Steps

Based on project state, suggest what to work on next.
