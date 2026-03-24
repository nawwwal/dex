#!/usr/bin/env bash
# Vault health diagnostics — used by graph.md
# Falls back to grep if obsidian-cli is unavailable

VAULT="${HOME}/.claude"

echo "=== VAULT HEALTH REPORT ==="
echo "Date: $(date)"
echo ""

# Wikilink density
TOTAL_LINKS=$(grep -r "\[\[" "$VAULT" --include="*.md" 2>/dev/null | grep -v ".obsidian\|plugins\|cache" | wc -l | tr -d ' ')
TOTAL_NOTES=$(find "$VAULT" -name "*.md" 2>/dev/null | grep -v ".obsidian\|plugins\|cache" | wc -l | tr -d ' ')
echo "Wikilink density: $TOTAL_LINKS links / $TOTAL_NOTES notes = $(echo "scale=1; $TOTAL_LINKS / $TOTAL_NOTES" | bc 2>/dev/null || echo "N/A") per note"
echo ""

# TIL / learn notes without links
TIL_DIR=""
[[ -d "$VAULT/learn" ]] && TIL_DIR="$VAULT/learn"
[[ -d "$VAULT/til" ]] && TIL_DIR="$VAULT/til"
if [[ -n "$TIL_DIR" ]]; then
  ORPHAN_TIL=$(find "$TIL_DIR" -name "*.md" 2>/dev/null | xargs grep -L "\[\[" 2>/dev/null | wc -l | tr -d ' ')
  echo "TIL orphans (no wikilinks): $ORPHAN_TIL"
fi

# Empty compact files
EMPTY_COMPACTS=$(grep -l "<!-- Claude:" "$VAULT/sessions/session-compact-"*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Unfilled compact files: $EMPTY_COMPACTS"

# Recent sessions count
TODAY=$(date +%Y-%m-%d)
TODAY_SESSIONS=$(ls "$VAULT/sessions/${TODAY}-"*.md 2>/dev/null | grep -v "compact\|commits\|changes\|dashboard" | wc -l | tr -d ' ')
echo "Sessions today: $TODAY_SESSIONS"

echo ""
echo "=== DONE ==="
