#!/usr/bin/env bash
#
# Stop hook: keep the agent working until the plan and user requests are 100% done.
#
# Uses a session-scoped counter to prevent infinite loops.
# Set TASKMASTER_MAX to change the max continuation count (default: 10, 0 = infinite).
#
set -euo pipefail

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path')
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# --- loop guard ---
COUNTER_DIR="${TMPDIR:-/tmp}/taskmaster"
mkdir -p "$COUNTER_DIR"
COUNTER_FILE="${COUNTER_DIR}/${SESSION_ID}"
MAX=${TASKMASTER_MAX:-10}

COUNT=0
if [ -f "$COUNTER_FILE" ]; then
  COUNT=$(cat "$COUNTER_FILE")
fi

# If another stop hook has already blocked this stop, do not stack more blockers.
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  rm -f "$COUNTER_FILE"
  exit 0
fi

# After max continuations, allow stop and clean up (0 = infinite, never cap)
if [ "$MAX" -gt 0 ] && [ "$COUNT" -ge "$MAX" ]; then
  rm -f "$COUNTER_FILE"
  exit 0
fi

# --- transcript analysis ---
HAS_INCOMPLETE_SIGNALS=false

if [ -f "$TRANSCRIPT" ]; then
  TAIL=$(tail -50 "$TRANSCRIPT" 2>/dev/null || true)

  # Check for task-list items still pending/in-progress
  if echo "$TAIL" | grep -qi '"status":\s*"in_progress"\|"status":\s*"pending"' 2>/dev/null; then
    HAS_INCOMPLETE_SIGNALS=true
  fi

  # Check for recent errors in tool results
  if echo "$TAIL" | grep -qi '"is_error":\s*true' 2>/dev/null; then
    HAS_INCOMPLETE_SIGNALS=true
  fi

fi

# Ordinary complete sessions should stop cleanly.
if [ "$HAS_INCOMPLETE_SIGNALS" = false ]; then
  rm -f "$COUNTER_FILE"
  exit 0
fi

# --- decide ---
NEXT=$((COUNT + 1))
echo "$NEXT" > "$COUNTER_FILE"

# Build the continuation reason with context
PREAMBLE="Incomplete tasks or recent errors were detected in the session."

if [ "$MAX" -gt 0 ]; then
  LABEL="TASKMASTER (${NEXT}/${MAX})"
else
  LABEL="TASKMASTER (${NEXT})"
fi

REASON="${LABEL}: ${PREAMBLE}

Review the latest transcript tail for the pending task or error signal, then either:
- finish the incomplete work, or
- fix the recent error before stopping.

Only continue if there is still real unfinished work. Do not loop just to re-verify a clean session."

jq -n --arg reason "$REASON" '{ decision: "block", reason: $reason }'
