# Vault Graph Health

Diagnose the vault topology using Obsidian CLI (with grep fallback).

## Step 1: Try Obsidian CLI
```bash
# Try obsidian-cli first (requires Obsidian to be open)
if command -v ob &>/dev/null || command -v obsidian &>/dev/null; then
  OB_CMD=$(command -v ob || command -v obsidian)
  echo "=== ORPHANS (no incoming links) ===" && $OB_CMD orphans 2>/dev/null
  echo "=== DEADENDS (no outgoing links) ===" && $OB_CMD deadends 2>/dev/null
  echo "=== UNRESOLVED [[links]] ===" && $OB_CMD unresolved 2>/dev/null
  echo "=== TAG COUNTS ===" && $OB_CMD tags counts sort=count 2>/dev/null
else
  echo "obsidian-cli not found, using grep fallback"
  exit 1
fi
```

## Step 2: Grep Fallback (if Obsidian not running)
```bash
VAULT="$HOME/.claude"
echo "=== Notes with no outgoing wikilinks (deadends) ==="
find "$VAULT/sessions" "$VAULT/memory" "$VAULT/work" -name "*.md" 2>/dev/null | \
  xargs grep -L "\[\[" 2>/dev/null | head -20

echo "=== TIL notes with no links (orphans) ==="
find "$VAULT/til" "$VAULT/learn" -name "*.md" 2>/dev/null | \
  xargs grep -L "\[\[" 2>/dev/null

echo "=== Wikilink density ==="
TOTAL_LINKS=$(grep -r "\[\[" "$VAULT" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
TOTAL_NOTES=$(find "$VAULT" -name "*.md" 2>/dev/null | grep -v ".obsidian\|plugins\|cache" | wc -l | tr -d ' ')
echo "$TOTAL_LINKS links across $TOTAL_NOTES notes = $(echo "scale=1; $TOTAL_LINKS / $TOTAL_NOTES" | bc) per note"
```

## Step 3: Report
Summarize findings:
- Orphan count by folder
- Deadend count (no outgoing links)
- Wikilink density (target: >= 3.0)
- Any unresolved [[wikilinks]] to non-existent notes
- Top 5 most-linked notes (hubs)
- Stale skills (not mentioned in sessions in last 30 days)

## Step 4: Recommendations
For each orphan: suggest 1 likely parent note to link from.
For TIL orphans: suggest linking to source session + patterns.md.
