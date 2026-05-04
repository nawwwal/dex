# PRD Analysis — Designer's POV

Analyzes a PRD or product document to extract design-relevant information.

## Step 1: Get the PRD
- If a URL (Google Doc): read the document if available; otherwise ask for pasted content or exported text.
- If pasted content: analyze directly.
- If file path: read the file.

## Step 2: Extract Design Information

### Personas & Users
Who are we designing for? Extract all user types mentioned.
For each: job-to-be-done, pain point, success criteria.

### User Stories
Extract explicit and implied user stories.
Format: As a [user], I want [action] so that [outcome].

### Competitive References
Any products or interfaces mentioned as references?
What patterns from those should inform design?

### Design Questions to Ask
Generate 8-12 specific design questions the PRD leaves unanswered:
- Edge cases not covered
- Multi-state behaviors not specified
- Error states
- Empty states
- Loading states
- Mobile considerations
- Accessibility requirements not mentioned

### Open Decisions
What design decisions does the PRD explicitly leave to the designer?
What decisions has the PM already made that constrain design?

## Step 3: Output
```markdown
## Design Brief: {Feature Name}

### Who We're Designing For
[Personas with job-to-be-done]

### Core User Journey
[Step-by-step flow from user's POV]

### Design Questions
1. [Specific question with context]
...

### Competitive References
[Any mentioned + 1-2 suggested to look at]

### Constraints
[Technical, business, brand constraints from PRD]

### Red Flags
[Requirements that seem contradictory or problematic]
```
