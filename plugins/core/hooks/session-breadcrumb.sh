#!/bin/bash
# Stop hook: Save a lightweight breadcrumb of what was being worked on.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')

REGISTRY="$HOME/.claude/config/project-registry.json"

# --- resolve_project: look up CWD against project-registry.json ---
resolve_project() {
  local cwd="$1"
  if [ ! -f "$REGISTRY" ]; then
    return 1
  fi
  python3 -c "
import json, sys
cwd = sys.argv[1]
with open(sys.argv[2]) as f:
    registry = json.load(f)
for proj in registry['projects']:
    for alias in proj['aliases']:
        if alias in cwd:
            print(proj['name'])
            sys.exit(0)
sys.exit(1)
" "$cwd" "$REGISTRY" 2>/dev/null
}

# Only proceed if CWD matches a registered project
PROJECT_NAME=$(resolve_project "$CWD")
if [ $? -ne 0 ]; then
  exit 0
fi

ENCODED_PATH=$(echo "$CWD" | sed 's|/|-|g')
PROJECT_MEMORY="$HOME/.claude/projects/$ENCODED_PATH/CLAUDE.md"

if [ -f "$PROJECT_MEMORY" ]; then
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
  BREADCRUMB=""
  if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
    BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
    LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h %s' 2>/dev/null)
    DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | head -5)
    BREADCRUMB="- Branch: $BRANCH\n- Last commit: $LAST_COMMIT"
    if [ -n "$DIRTY" ]; then
      BREADCRUMB="$BREADCRUMB\n- Uncommitted changes present"
    fi
  fi

  if grep -q "<!-- Auto-updated" "$PROJECT_MEMORY"; then
    sed -i '' "s|<!-- Auto-updated.*-->|Last session: $TIMESTAMP\n$BREADCRUMB\n<!-- Auto-updated by session-breadcrumb hook -->|" "$PROJECT_MEMORY"
  fi
fi

exit 0
