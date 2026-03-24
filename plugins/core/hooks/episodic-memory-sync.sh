#!/bin/bash
# Stop hook: Sync episodic memory at session end.
# Uses --background so it doesn't block session close.

SYNC_CLI="$HOME/.claude/plugins/cache/superpowers-marketplace/episodic-memory/1.0.15/dist/sync-cli.js"

if [ -f "$SYNC_CLI" ]; then
  node "$SYNC_CLI" --background 2>/dev/null &
fi

exit 0
