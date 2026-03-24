#!/bin/bash
# PostToolUse hook: capture Figma MCP calls to per-project design action log.
# Fires when any mcp__plugin_figma_figma__* tool is used.
# Logs metadata only — no raw payloads or tokenized URLs.

INPUT=$(cat)
NOW=$(date '+%Y-%m-%d %H:%M')
REGISTRY="$HOME/.claude/config/project-registry.json"

# Parse stdin once: extract tool_name + cwd, then resolve project via registry
read -r TOOL PROJECT <<< "$(echo "$INPUT" | python3 -c "
import json, sys, os
d = json.load(sys.stdin)
tool = d.get('tool_name', '')
cwd = d.get('cwd', '') or os.path.expanduser('~')
reg_path = os.path.expanduser('~/.claude/config/project-registry.json')
project = os.path.basename(cwd)
if os.path.exists(reg_path):
    reg = json.load(open(reg_path))
    for p in reg.get('projects', []):
        if any(a in cwd for a in p.get('aliases', [])):
            project = p['name']
            break
print(tool, project)
" 2>/dev/null)"

WORK_DIR="$HOME/.claude/work"
if [ -d "$WORK_DIR" ] && [ -n "$PROJECT" ] && [ -d "$WORK_DIR/$PROJECT" ]; then
  LOG_FILE="$WORK_DIR/$PROJECT/figma-actions.md"
  if [ ! -f "$LOG_FILE" ]; then
    printf '# Figma Actions — %s\n\n' "$PROJECT" > "$LOG_FILE"
  fi
  printf -- '- [%s] `%s`\n' "$NOW" "$TOOL" >> "$LOG_FILE"
fi
