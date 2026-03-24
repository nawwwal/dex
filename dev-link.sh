#!/usr/bin/env bash
# dev-link.sh — Symlink all 3 plugin caches to the dex source repo for live editing.
# Run from anywhere inside the dex repo.
#
# Usage: ./dev-link.sh
# Effect: Claude loads core/design/tools from your source repo directly. Edits are instant.

set -euo pipefail

DEX_ROOT="$(cd "$(dirname "$0")" && pwd)"
CACHE_BASE="$HOME/.claude/plugins/cache/nawwwal-dex"
INSTALLED_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"

for plugin in core design tools; do
  PLUGIN_SOURCE="$DEX_ROOT/plugins/$plugin"

  if [ ! -d "$PLUGIN_SOURCE" ]; then
    echo "ERROR: Plugin dir not found: $PLUGIN_SOURCE"
    exit 1
  fi

  # Get version from plugin.json
  VERSION=$(python3 -c "import json; print(json.load(open('$PLUGIN_SOURCE/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "1.0.1")
  CACHE_PATH="$CACHE_BASE/$plugin/$VERSION"

  # Check if already linked correctly
  if [ -L "$CACHE_PATH" ] && [ "$(readlink "$CACHE_PATH")" = "$PLUGIN_SOURCE" ]; then
    echo "Already linked: $plugin/$VERSION → plugins/$plugin"
    continue
  fi

  # Create parent dir, remove old entry, symlink
  mkdir -p "$CACHE_BASE/$plugin"
  rm -rf "$CACHE_PATH"
  ln -s "$PLUGIN_SOURCE" "$CACHE_PATH"
  echo "Linked: cache/$plugin/$VERSION → plugins/$plugin"
done

echo ""
echo "All 3 plugins linked. Edits in ~/projects/dex/plugins/ are live."
echo "Run /reload-plugins to pick up changes in an active session."
