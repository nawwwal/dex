#!/usr/bin/env bash
# Inject context when resuming sessions
INPUT=$(cat)
MSG=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt',''))" 2>/dev/null || echo "")

if echo "$MSG" | grep -q '/resume'; then
  # Find project breadcrumb from project CLAUDE.md (written by session-breadcrumb.sh)
  BREADCRUMB=""
  CWD_VAL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null || echo "")
  if [[ -n "$CWD_VAL" ]]; then
    ENCODED_PATH=$(echo "$CWD_VAL" | sed 's|/|-|g')
    PROJECT_MEMORY="$HOME/.claude/projects/$ENCODED_PATH/CLAUDE.md"
    if [[ -f "$PROJECT_MEMORY" ]]; then
      BREADCRUMB=$(grep -A5 'Last session:' "$PROJECT_MEMORY" 2>/dev/null | head -6)
    fi
  fi

  # Also check the session-compact files
  COMPACT=$(ls -t "$HOME/.claude/log/session-compact-"*.md 2>/dev/null | head -1)
  COMPACT_CONTENT=""
  if [[ -f "$COMPACT" ]]; then
    COMPACT_CONTENT=$(tail -15 "$COMPACT" 2>/dev/null)
  fi

  CONTEXT="Session resuming."
  if [[ -n "$BREADCRUMB" ]]; then
    CONTEXT="$CONTEXT Last known state: $BREADCRUMB."
  fi
  if [[ -n "$COMPACT_CONTENT" ]]; then
    CONTEXT="$CONTEXT Recent compact: $COMPACT_CONTENT."
  fi
  CONTEXT="$CONTEXT Ask the user: 'What changed since we last worked on this?' before proceeding with any work."

  # Use Python for safe JSON serialization (prevents injection from file content)
  python3 -c "import json, sys; print(json.dumps({'additionalContext': sys.argv[1]}))" "$CONTEXT"
fi
