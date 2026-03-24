# Hooks and Subagents in Skills

Reference for safe, production-ready patterns. Read [SKILL.md](SKILL.md) for the overview.

## Hooks in Skill Frontmatter

### Stop Hook — Completeness Guard

The most valuable hook pattern: keep Claude working until all checklist items are done.

```yaml
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Check if all tasks from the active skill checklist are marked complete. If any remain, respond with {\"ok\": false, \"reason\": \"<what specifically remains>\"}. If all done, respond {\"ok\": true}."
```

**REQUIRED: Infinite loop guard for command-type Stop hooks.**
If you use a `command` hook (not `prompt`), you MUST check `stop_hook_active` or you will create an infinite loop:

```bash
#!/bin/bash
INPUT=$(cat)
# Exit immediately if Claude is already in a stop-hook loop
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi
# ... rest of your check logic
```

Prompt-type and agent-type hooks handle this automatically — the infinite loop guard is only required for `command`-type Stop hooks.

### PostToolUse — Auto-format After File Edits

```yaml
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          # Hook input arrives via stdin as JSON — read it first, then extract the file path
          command: "INPUT=$(cat); FILE=$(echo \"$INPUT\" | jq -r '.tool_input.file_path // empty'); [ -n \"$FILE\" ] && npx prettier --write \"$FILE\" 2>/dev/null || true"
```

**Safety notes:**
- Hook input arrives via **stdin** (not an env var). Always `INPUT=$(cat)` first, then parse with `jq`
- Always quote `$FILE` when passing to commands — paths can contain spaces and special chars
- Use `|| true` so a formatter failure doesn't block the tool result
- This re-triggers when the formatted file is written — confirm your formatter is idempotent
- Matcher `Edit|Write` is the documented syntax from the Claude Code hooks guide

### PostToolUse — Agent-based Verification

Use an `agent` hook when you need to inspect actual codebase state, not just reason from input data:

```yaml
hooks:
  Stop:
    - hooks:
        - type: agent
          prompt: "Run the test suite and verify all tests pass. Return {\"ok\": true} if passing, {\"ok\": false, \"reason\": \"<failing tests>\"} if not."
          timeout: 120
```

Agent hooks get up to 50 tool-use turns. Default timeout is 60 seconds — **always set an explicit `timeout` for agent Stop hooks** since 60s is too short for most test suites. Override with `timeout` (in seconds).

### PreToolUse — Block Dangerous Commands

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/scripts/validate-command.sh"
```

```bash
#!/bin/bash
# validate-command.sh — blocks destructive commands in this skill's domain
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$COMMAND" ] && exit 0

if echo "$COMMAND" | grep -iE '\b(rm -rf|DROP TABLE|DELETE FROM)\b' > /dev/null; then
  echo "Blocked: destructive command not allowed in this skill context" >&2
  exit 2
fi
exit 0
```

**Exit codes:** 0 = allow, 2 = block (stderr becomes Claude's feedback), any other non-zero = logged but not blocked.

---

## Subagent Frontmatter — Annotated Example

This goes in `.claude/agents/your-agent.md`, not in SKILL.md frontmatter.

**Note:** Plugin subagents do NOT support `hooks`, `mcpServers`, or `permissionMode` in frontmatter — remove those fields when packaging as a plugin.

```markdown
---
name: api-developer
description: Implement API endpoints following team conventions. Use proactively when adding new API routes.
tools: Read, Edit, Write, Bash
# Preload skill content at startup — subagents do NOT inherit parent conversation skills
skills:
  - api-conventions
  - error-handling-patterns
# Persist learnings across sessions — 'project' scope recommended (in VCS, shareable)
memory: project
# Run in an isolated git worktree — auto-cleaned if no changes are made
isolation: worktree
# Cap turns to prevent runaway agents
maxTurns: 30
# Hooks scoped only to this subagent's lifecycle (not supported in plugin subagents)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          # Path is relative to CWD when the agent runs — use an absolute path for reliability
          command: "$CLAUDE_PROJECT_DIR/scripts/validate-api-command.sh"
---

You are an API developer following the team's conventions loaded in your skills context...
```

**Field source:** All fields above are from the official Claude Code sub-agents documentation at https://code.claude.com/docs/en/sub-agents.

### Memory scope comparison

| Scope | Location | Use when |
|---|---|---|
| `user` | `~/.claude/memory/` | Cross-project learnings (shared with main memory) |
| `project` | `.claude/memory/<name>/` | Project-specific, in VCS (recommended default) |
| `local` | `.claude/memory-local/<name>/` | Project-specific, gitignored |

When `memory` is set, first 200 lines of `MEMORY.md` are injected into the subagent's system prompt at startup.
