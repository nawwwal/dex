#!/usr/bin/env bash
# dev-link.sh — Symlink the plugin cache to the dex source repo for live editing.
# Usage: ./scripts/dev-link.sh
# Effect: Claude loads dex from ~/dex/ directly. Edits are instant.

set -euo pipefail

DEX_SOURCE="$(cd "$(dirname "$0")/.." && pwd)"
INSTALLED_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"

if [ ! -f "$INSTALLED_PLUGINS" ]; then
  echo "Error: $INSTALLED_PLUGINS not found. Install dex first: /plugin install dex@nawwwal-dex"
  exit 1
fi

# Find the install path for dex from installed_plugins.json
INSTALL_PATH=$(python3 -c "
import json, sys
with open('$INSTALLED_PLUGINS') as f:
    data = json.load(f)
plugins = data.get('plugins', {})
# plugins is a dict: 'dex@nawwwal-dex' -> [{ scope, installPath, ... }]
for key, entries in plugins.items() if isinstance(plugins, dict) else []:
    if 'dex' in key and 'nawwwal' in key:
        for entry in (entries if isinstance(entries, list) else [entries]):
            path = entry.get('installPath', '')
            if path:
                print(path)
                sys.exit(0)
print('')
" 2>/dev/null)

# Fallback: find the cache dir by glob
if [ -z "$INSTALL_PATH" ]; then
  INSTALL_PATH=$(find "$HOME/.claude/plugins/cache/nawwwal-dex/dex" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | head -1)
fi

if [ -z "$INSTALL_PATH" ]; then
  echo "Error: Could not find dex install path. Is dex installed?"
  echo "Run: /plugin install dex@nawwwal-dex"
  exit 1
fi

# Verify path is under the expected cache location
case "$INSTALL_PATH" in
  */.claude/plugins/cache/nawwwal-dex/dex/*)
    ;;
  *)
    echo "Error: Install path '$INSTALL_PATH' is not under expected cache location."
    exit 1
    ;;
esac

# Check if already a symlink pointing to the right place
if [ -L "$INSTALL_PATH" ]; then
  TARGET=$(readlink "$INSTALL_PATH")
  if [ "$TARGET" = "$DEX_SOURCE" ]; then
    echo "Already linked: $INSTALL_PATH -> $DEX_SOURCE"
    exit 0
  fi
fi

# Remove the cache dir and create symlink
rm -rf "$INSTALL_PATH"
ln -s "$DEX_SOURCE" "$INSTALL_PATH"

# Verify
if [ -L "$INSTALL_PATH" ] && [ -f "$INSTALL_PATH/.claude-plugin/plugin.json" ]; then
  echo "Linked: $INSTALL_PATH -> $DEX_SOURCE"
  echo "Claude now loads dex from your source repo. Edits are instant."
else
  echo "Error: Symlink created but plugin.json not found. Check your dex repo."
  exit 1
fi
