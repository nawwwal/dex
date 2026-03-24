# PRD Generator

Generates a structured Product Requirements Document.

## Step 1: Ask 3-5 Clarifying Questions
Before writing, ask:
1. What problem is this solving for which user?
2. What's the success metric — how will we know it worked?
3. Are there existing solutions or constraints to consider?
4. What's out of scope?
5. Who are the key stakeholders?

Wait for answers before writing.

## Step 2: Structure

Write to `~/.claude/work/{project}/prd-{feature}.md` or show inline:

```markdown
---
date: YYYY-MM-DD
project: {project}
type: prd
status: draft
---

# PRD: {Feature Name}

## Problem
[1-2 sentences: what problem, for who, how bad is it?]

## Users
[Primary user and their job-to-be-done]

## Success Criteria
- Metric 1: [specific, measurable]
- Metric 2: [specific, measurable]

## Solution
[What we're building at a high level]

## User Stories
- As a [user], I want [action] so that [outcome]
- ...

## Requirements
### Must Have
- [ ] ...

### Should Have
- [ ] ...

### Won't Have (out of scope)
- ...

## Design Considerations
[Key design decisions and constraints]

## Open Questions
- [ ] ...

## References
- [[work/{project}/index]]
```

## Step 3: Offer Follow-ups
- "Want me to run /ops lens to analyze this from a designer's POV?"
- "Should I create a /design spec from this?"
