#!/usr/bin/env bash
# Inject fill-compact instruction ONCE per compact file (not every message)
TODAY=$(date +%Y-%m-%d)
COMPACT_FILE="$HOME/.claude/log/session-compact-${TODAY}.md"
SENTINEL_FILE="$HOME/.claude/log/.compact-notified-${TODAY}"

# If we already notified today, stay silent
if [[ -f "$SENTINEL_FILE" ]]; then
  exit 0
fi

# Check if compact file exists and has unfilled placeholder
if [[ -f "$COMPACT_FILE" ]] && grep -q "<!-- Claude:" "$COMPACT_FILE" 2>/dev/null; then
  # Create sentinel so this fires only once today
  touch "$SENTINEL_FILE"
  echo "{\"additionalContext\": \"IMPORTANT: A context compact happened earlier today. The compact summary at $COMPACT_FILE is unfilled — it has a <!-- Claude: --> placeholder that needs to be completed. BEFORE responding to the user's current message: read that file and fill in the work summary (what was being worked on, decisions in flight, next steps, blockers). Then respond to the user's message.\"}"
fi
