#!/bin/bash
# SessionStart hook: emit a tiny session index, not a full briefing.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"')

CLAUDE_DIR="$HOME/.claude"
MEMORY_DIR="$CLAUDE_DIR/memory"
SESSIONS_DIR="$CLAUDE_DIR/sessions"
TASKS_FILE="$HOME/.claude/TASKS.md"
LEARNINGS_QUEUE="$HOME/.claude/learnings-queue.json"
HEALTH_FILE="$MEMORY_DIR/health.md"

if [ "$SOURCE" = "clear" ]; then
  exit 0
fi

PROJECT_KEY=$(echo "$CWD" | tr '/[:space:]' '--' | tr -cd '[:alnum:]._-' | sed 's/--*/-/g; s/^-//; s/-$//' | cut -c1-120)
[ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"
COMPACT_FILE="$SESSIONS_DIR/session-compact-${PROJECT_KEY}.md"

CONTEXT_FILE=""
PROJECT_MEMORY="$HOME/.claude/projects/$(echo "$CWD" | sed 's|/|-|g')/CLAUDE.md"
if [ -f "$PROJECT_MEMORY" ]; then
  CONTEXT_FILE="project memory"
elif [ -f "$CWD/CLAUDE.md" ]; then
  CONTEXT_FILE="CLAUDE.md"
fi

TASKS_OPEN=0
if [ -f "$TASKS_FILE" ]; then
  TASKS_OPEN=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
fi

QUEUE_PENDING=0
if [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ]; then
  QUEUE_PENDING=$(python3 -c "
import json
try:
    with open('$LEARNINGS_QUEUE') as f:
        data = json.load(f)
    print(len(data) if isinstance(data, list) else 0)
except Exception:
    print(0)
" 2>/dev/null || echo 0)
fi

HEALTH_WARNINGS=0
if [ -f "$HEALTH_FILE" ]; then
  HEALTH_WARNINGS=$(grep -m1 -oE 'warnings: [0-9]+' "$HEALTH_FILE" | awk '{print $2}')
fi

echo "=== SESSION ==="
echo "Repo: $(basename "$CWD") | Source: $SOURCE"

if git -C "$CWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
  DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h' 2>/dev/null)
  echo "Git: ${BRANCH:-detached} | Dirty: ${DIRTY:-0}${LAST_COMMIT:+ | Last: $LAST_COMMIT}"
fi

[ "${TASKS_OPEN:-0}" -gt 0 ] 2>/dev/null && echo "Tasks: $TASKS_OPEN open"
[ "${QUEUE_PENDING:-0}" -gt 0 ] 2>/dev/null && echo "Queue: $QUEUE_PENDING pending"
[ "${HEALTH_WARNINGS:-0}" -gt 0 ] 2>/dev/null && echo "Health: $HEALTH_WARNINGS warnings"
[ -n "$CONTEXT_FILE" ] && echo "Context: $CONTEXT_FILE"

if [ "$SOURCE" = "compact" ] && [ -f "$COMPACT_FILE" ]; then
  if grep -q "<!-- Claude:" "$COMPACT_FILE" 2>/dev/null; then
    echo "Compact: pending"
  else
    echo "Compact: ready"
  fi
fi

exit 0
