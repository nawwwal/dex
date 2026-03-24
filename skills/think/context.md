# Deep Vault Context Loading

Multi-hop vault traversal. Like internetVin's /context — reads the vault graph to build a full picture.

## Step 1: Read Core Files
1. Read ~/.claude/index.md (vault home)
2. Read ~/.claude/memory/goals.md (current priorities)
3. Read ~/.claude/career/case.md first 50 lines (promotion status)

## Step 2: Multi-Hop Graph Traversal
```bash
# Use obsidian-cli if available for proper backlink traversal
if command -v ob &>/dev/null; then
  ob read file="index" 2>/dev/null
  ob backlinks file="goals" 2>/dev/null | head -10
else
  # Grep-based: find all files linked FROM index.md
  grep -o '\[\[[^]]*\]\]' ~/.claude/index.md 2>/dev/null | sed 's/\[\[//g' | sed 's/\]\]//g'
fi
```
Follow the links — read each linked file, then follow their links up to 2 hops deep.

## Step 3: Recent Activity
```bash
# Last 5 session journals
ls -t ~/.claude/log/*.md 2>/dev/null | grep -v "compact\|commits\|changes\|dashboard" | head -5 | xargs tail -20
```

## Step 4: Run Vault Health
Run the graph.md diagnostics:
- Orphan count
- Unresolved links
- Tag frequency

## Step 5: Synthesize
Output:
- Current priorities (ranked)
- Active projects and their status
- Open questions (unresolved decisions)
- Recent belief shifts (compare decisions this week vs last month)
- Vault health summary

End with: "Context loaded. What would you like to work on?"
