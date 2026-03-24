# Skill Tests: design

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "before I start on the InfoArea component, what do we know about it?" → Runs before.md, searches decisions + sessions
2. "review the agent marketplace home tab design" → Runs review.md → a11y.md chain
3. "check a11y on this component" → Runs a11y.md standalone, produces WCAG checklist
4. "make this Figma design interactive" → Runs prototype.md, fetches Figma via figma:implement-design
5. "write a case study for SG PayNow" → Runs before.md → case.md chain

## True Negatives (should NOT trigger)
1. "design a database schema" → Technical design, not product design (/ops or general)
2. "redesign this function" → Code refactor, not design
3. "what's good design?" → Conceptual question, not a process trigger

## Edge Cases
1. "full design review for X" → Chains all 4: before → review → a11y → case
2. "review" on a code file → Should invoke design-reviewer agent, not review.md
3. "a11y check" when no URL or file provided → Should ask "what would you like me to check?"

6. "my button hit target is too small" → pseudo-elements.md, negative inset for hit target expansion
7. "how do I apply Fitts's Law to my navigation?" → laws.md, Fitts's Law section (44px, pseudo-element expansion)
8. "should I add a sound when a payment is confirmed?" → audio-feedback.md, behavioral guidelines
9. "how do I prefetch the next page before users hover?" → harden.md, predictive prefetching section (useForesight)
10. "show me how to set up Agentation with Claude Code" → agentation.md, MCP setup + watch mode

## Quality Bar
- A "good" /design before: finds 3+ prior decisions, shows rejected alternatives, flags open questions
- A "poor" /design before: generic advice without checking vault data
