#!/usr/bin/env bash
# Inject fill-compact instruction once per compact snapshot.
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
CLAUDE_DIR="$HOME/.claude"
SESSIONS_DIR="$CLAUDE_DIR/sessions"
PROJECT_KEY=$(echo "$CWD" | tr '/[:space:]' '--' | tr -cd '[:alnum:]._-' | sed 's/--*/-/g; s/^-//; s/-$//' | cut -c1-120)
[ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"
COMPACT_FILE="$SESSIONS_DIR/session-compact-${PROJECT_KEY}.md"

# Check if the current project has an unfilled compact snapshot.
if [[ -f "$COMPACT_FILE" ]] && grep -q "<!-- Claude:" "$COMPACT_FILE" 2>/dev/null; then
  SNAPSHOT_ID=$(cksum "$COMPACT_FILE" | awk '{print $1}')
  SENTINEL_FILE="$CLAUDE_DIR/log/.compact-notified-${PROJECT_KEY}-${SNAPSHOT_ID}"
  if [[ -f "$SENTINEL_FILE" ]]; then
    exit 0
  fi
  mkdir -p "$CLAUDE_DIR/log"
  touch "$SENTINEL_FILE"
  echo "{\"additionalContext\": \"Compact snapshot pending: $COMPACT_FILE. Replace the placeholder with <=8 current bullets, then continue.\"}"
fi
