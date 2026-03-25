# Design Decision Archaeology

Before starting any significant design work, surface what the vault knows about this component/pattern.

## Step 1: Extract the Component/Pattern
What is being designed? Extract key terms: component name, pattern name, page/screen name.

## Step 2: Search Vault
```bash
COMPONENT="$1"  # extracted from user message

echo "=== Decisions about this component ==="
grep -r "$COMPONENT" ~/.claude/memory/decisions.md 2>/dev/null | head -10

echo "=== Sessions mentioning this ==="
grep -r "$COMPONENT" ~/.claude/log/*.md 2>/dev/null -l | head -5

echo "=== TIL / Learn notes ==="
grep -r "$COMPONENT" ~/.claude/learn/ ~/.claude/til/ 2>/dev/null 2>/dev/null | head -5

echo "=== Project work notes ==="
find ~/.claude/work -name "*.md" | xargs grep -l "$COMPONENT" 2>/dev/null | head -5
```

## Step 3: Synthesize
Output:
```
## Vault Knowledge: {COMPONENT}

### Prior Decisions
- [list of relevant decisions with dates and links]

### What Was Tried Before
- [approaches that were attempted, with outcomes]

### Rejected Approaches
- [what was explicitly decided against and why]

### Relevant Patterns
- [patterns from memory/patterns.md that apply]

### Open Questions
- [unresolved [[wikilinks]] or open questions mentioning this component]
```

## Step 4: Blade MCP Check
"Also run the Blade MCP to verify if a Blade component already handles this use case before designing from scratch."
