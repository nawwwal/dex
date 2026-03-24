#!/bin/bash
# SubagentStart hook: inject lightweight vault context into agent sessions.
# Main sessions get full context via session-context.sh (SessionStart).
# Subagents don't inherit that — this fills the gap with behavioral files.
# Payload budget: ~4KB total. Patterns first (highest signal).

MEMORY_DIR="$HOME/.claude/memory"

# Load 20 most recent patterns (recency bias — newest most relevant)
PATTERNS_FILE="$MEMORY_DIR/patterns.md"
if [ -f "$PATTERNS_FILE" ]; then
  echo "--- KEY PATTERNS (recent 20) ---"
  grep -n '^###' "$PATTERNS_FILE" | tail -20 | while IFS=: read -r linenum _; do
    sed -n "${linenum},$((linenum+6))p" "$PATTERNS_FILE"  # 6: header + Source + Date + description + blank
    echo ""
  done
fi

# Load voice revision checklist only (not full voice.md — just the checklist section)
VOICE_FILE="$MEMORY_DIR/voice.md"
if [ -f "$VOICE_FILE" ]; then
  CHECKLIST=$(grep -A 15 "Revision Checklist" "$VOICE_FILE" 2>/dev/null | head -18)
  if [ -n "$CHECKLIST" ]; then
    echo "--- VOICE REVISION CHECKLIST ---"
    echo "$CHECKLIST"
    echo ""
  fi
fi

# Load active projects — conditional: only if file is 30 lines or fewer
PROJECTS_FILE="$MEMORY_DIR/projects.md"
if [ -f "$PROJECTS_FILE" ]; then
  LINE_COUNT=$(wc -l < "$PROJECTS_FILE")
  if [ "$LINE_COUNT" -le 30 ]; then
    echo "--- ACTIVE PROJECTS ---"
    cat "$PROJECTS_FILE"
  fi
fi
