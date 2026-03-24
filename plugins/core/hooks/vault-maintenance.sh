#!/bin/bash
# vault-maintenance.sh — explicit cleanup (run manually, NOT a SessionStart hook)
# Run when: vault disk usage has grown, or as periodic maintenance.

CLAUDE_DIR="$HOME/.claude"
TODAY=$(date '+%Y-%m-%d')

echo "=== Vault Maintenance — $TODAY ==="

# debug/ — delete files older than 7 days
BEFORE=$(ls "$CLAUDE_DIR/debug/" 2>/dev/null | wc -l | tr -d ' ')
find "$CLAUDE_DIR/debug/" -type f -mtime +7 -delete 2>/dev/null
AFTER=$(ls "$CLAUDE_DIR/debug/" 2>/dev/null | wc -l | tr -d ' ')
echo "debug/: $BEFORE → $AFTER files (deleted $((BEFORE - AFTER)))"

# session-env/ — delete empty directories older than 3 days
BEFORE_DIRS=$(find "$CLAUDE_DIR/session-env/" -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
find "$CLAUDE_DIR/session-env/" -mindepth 1 -type d -empty -mtime +3 -delete 2>/dev/null
AFTER_DIRS=$(find "$CLAUDE_DIR/session-env/" -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
echo "session-env/: $BEFORE_DIRS → $AFTER_DIRS dirs (deleted $((BEFORE_DIRS - AFTER_DIRS)))"

# todos/ — exact-match empty JSON array files older than 7 days
BEFORE_TODO=$(ls "$CLAUDE_DIR/todos/" 2>/dev/null | wc -l | tr -d ' ')
find "$CLAUDE_DIR/todos/" -type f -name "*.json" -mtime +7 | while read -r f; do
  content=$(tr -d ' \n\t' < "$f" 2>/dev/null)
  if [ "$content" = "[]" ]; then
    rm "$f"
  fi
done
AFTER_TODO=$(ls "$CLAUDE_DIR/todos/" 2>/dev/null | wc -l | tr -d ' ')
echo "todos/: $BEFORE_TODO → $AFTER_TODO files (deleted $((BEFORE_TODO - AFTER_TODO)))"

echo "=== Maintenance complete ==="
