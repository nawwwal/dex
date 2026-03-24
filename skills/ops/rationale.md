# Design Rationale Document

Documents WHY a design decision was made. The artifact between design and handoff.

## When to Use
- After finalizing a significant design decision
- Before handing off to engineering
- When asked "why did we design it this way?"
- For the promotion case (evidence of decision-making quality)

## Step 1: Understand the Decision
What design decision is being documented?
- Component choice
- Interaction pattern
- Visual treatment
- Information architecture choice

## Step 2: Check Memory
```bash
grep -r "$(user's decision keywords)" ~/.claude/memory/decisions.md 2>/dev/null | head -5
```
Reference any related decisions already logged.

## Step 3: Write the Rationale

```markdown
---
date: YYYY-MM-DD
project: {project}
type: design-rationale
component: {component name}
---

# Design Rationale: {Decision Name}

## Decision
[One sentence: what was decided]

## Context
[Why this decision was needed. What problem triggered it.]

## Options Considered

### Option A: {Name} ✅ Chosen
**Pros:**
-
**Cons:**
-

### Option B: {Name}
**Pros:**
-
**Cons:**
-
**Why not:** [specific reason]

## Rationale
[Why Option A was chosen. What evidence or principles informed this.]

## Trade-offs Accepted
[What we gave up by choosing this approach]

## Success Criteria
[How we'll know this decision was right]

## Revisit If
[Under what conditions should this decision be reconsidered]

## References
- [[memory/decisions#{dec-slug}]]
- [[work/{project}/index]]
```

## Step 4: Log to decisions.md
Append a summary to memory/decisions.md following the standard format.
