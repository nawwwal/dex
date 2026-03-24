#!/bin/bash
# SubagentStart hook: keep subagent context tiny and index-like.

MEMORY_DIR="$HOME/.claude/memory"
PATTERNS_FILE="$MEMORY_DIR/patterns.md"

echo "--- SUBAGENT CONTEXT ---"

if [ -f "$PATTERNS_FILE" ]; then
  PATTERN_TITLES=$(grep '^### ' "$PATTERNS_FILE" 2>/dev/null | tail -5 | sed 's/^### /- /')
  if [ -n "$PATTERN_TITLES" ]; then
    echo "Recent patterns:"
    echo "$PATTERN_TITLES"
  fi
fi

echo "Load ~/.claude/memory/voice.md before drafting communication."
echo "Pull broader project context on demand instead of assuming from hook state."
