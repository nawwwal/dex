# Devil's Advocate

Builds the strongest counterargument against a position using vault evidence.

## Step 1: Understand the Claim
What is the position being challenged? Extract the core claim.

## Step 2: Search Vault for Evidence Against
```bash
# Search for contradicting evidence
grep -r "mistake\|wrong\|failed\|didn't work\|reverted\|reconsidering" ~/.claude/memory/decisions.md ~/.claude/memory/patterns.md 2>/dev/null | grep -i "$CLAIM_KEYWORDS" | head -10
```

## Step 3: Build the Strongest Case Against
Use the actual vault data. Don't invent arguments — use what actually happened:
- Decisions that went against this principle
- Patterns that contradicted this approach
- Sessions where this failed

## Step 4: Fabrication Check
Every counter-argument must cite actual vault evidence. No invented examples.

## Step 5: Output
```
## Challenge: {CLAIM}

### The strongest case against this:
[3-5 arguments, each with vault evidence]

### What you'd be betting on if you're right:
[what must be true for the original position to hold]

### What would change your mind:
[specific evidence that would refute the challenge]
```
