#!/bin/bash
# Stop hook: Remind Claude to make meaningful commits before finishing.
# Does NOT ask for a commit after every tiny change — only fires once
# when Claude is about to stop and there are uncommitted changes.

INPUT=$(cat)

# Prevent infinite loops: if we already reminded once, let Claude stop.
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

# Only relevant inside a git repo
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
if ! git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  exit 0
fi

# Check for any staged or unstaged changes (tracked files + untracked)
CHANGES=$(git -C "$CWD" status --porcelain 2>/dev/null)
if [ -z "$CHANGES" ]; then
  exit 0  # Working tree clean, nothing to remind about
fi

REASON="Uncommitted changes remain. Review and commit if ready."

jq -n --arg reason "$REASON" '{ decision: "block", reason: $reason }'
