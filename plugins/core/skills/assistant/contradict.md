# Find Incompatible Beliefs

Searches the vault for decisions or patterns that contradict each other.

## Step 1: Load All Solid Beliefs
Read memory/decisions.md and memory/patterns.md. Extract entries marked `[solid]`.

## Step 2: Search for Contradictions
For each [solid] belief:
1. Search sessions for evidence of the opposite behavior
2. Search decisions.md for a later decision that reverses it
3. Search patterns.md for a pattern that conflicts

```bash
# Example: if we decided "Blade only" but then built custom components
grep -i "custom component\|ad-hoc\|workaround" ~/.claude/log/*.md 2>/dev/null | head -10
grep -i "blade" ~/.claude/memory/decisions.md 2>/dev/null | head -10
```

## Step 3: Fabrication Check
For each potential contradiction found: search the vault for "this contradiction is acknowledged" or similar.
If already noted — skip it.

## Step 4: Report
For each real contradiction:
```
**Contradiction found:**
- Belief A: [what you decided/believe] [from: source]
- Evidence against: [what actually happened] [from: session/date]
- Reconcile or update: [suggested resolution]
```

## Step 5: Update Confidence Markers
If a `[solid]` belief was contradicted → suggest changing to `[questioning]`.
If a `[hypothesis]` was confirmed → suggest changing to `[solid]` or `[evolving]`.
