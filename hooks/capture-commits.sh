#!/usr/bin/env bash
# Capture git commits to a daily log and per-project work log
INPUT=$(cat)

COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Only process git commit commands
if ! echo "$COMMAND" | grep -q 'git commit'; then
  exit 0
fi

TODAY=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
SESSIONS_DIR="$HOME/.claude/log"

# Extract commit info
HASH=$(git log --format='%h' -1 2>/dev/null || echo "unknown")
MSG=$(git log --format='%s' -1 2>/dev/null || echo "unknown")
PROJECT=$(git branch --show-current 2>/dev/null | sed 's|the user/||' | sed 's|/|-|g' | cut -c1-30)
if [[ -z "$PROJECT" ]]; then
  PROJECT=$(basename "$PWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-30)
fi

# Append to daily commits log
COMMITS_LOG="$SESSIONS_DIR/${TODAY}-${PROJECT}-commits.md"
echo "[$TIME] $PROJECT | $HASH | $MSG" >> "$COMMITS_LOG"

# Append to per-project work log
WORK_LOG_DIR="$HOME/.claude/work/$PROJECT"
if [[ -d "$WORK_LOG_DIR" ]]; then
  echo "- ${TODAY} ${HASH}: ${MSG}" >> "$WORK_LOG_DIR/work-log.md"
fi

exit 0
