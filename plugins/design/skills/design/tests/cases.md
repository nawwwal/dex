# Skill Tests: design

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "before I start on the InfoArea component, what do we know about it?" → Runs ui/before.md, searches decisions + sessions
2. "review the agent marketplace home tab design" → Runs ui/review.md → ui/a11y.md chain
3. "check a11y on this component" → Runs ui/a11y.md standalone, produces WCAG checklist
4. "make this Figma design interactive" → Runs ui/prototype.md, fetches Figma via figma:implement-design
5. "write a case study for SG PayNow" → Runs ui/before.md → ui/case.md chain
6. "make it feel better" → Runs ui/enhance.md (Polish sub-mode)
7. "harden this component" → Runs ui/harden.md (edge cases, overflow, i18n)
8. "fix the typography" → Runs ui/typeset.md
9. "clarify the error messages" → Runs ui/clarify.md
10. "add animation to this modal" → Runs motion/ sub-files

## True Negatives (should NOT trigger)
1. "design a database schema" → Technical design, not product design
2. "redesign this function" → Code refactor, not design
3. "what's good design?" → Conceptual question, not a process trigger
4. "polish this PRD" → Written artifact, routes to elements-of-style skill

## Edge Cases
1. "full design review for X" → Chains all 4: ui/before → ui/review → ui/a11y → ui/case
2. "review" on a code file → Should invoke design-reviewer agent, not ui/review.md
3. "a11y check" when no URL or file provided → Should ask "what would you like me to check?"
4. "feels off" → Routes to ui/enhance.md (Polish), NOT ui/review.md
5. Figma URL with no verb → Ask: "Implement as code, or review the design?"

## Quality Bar
- A "good" /design before: finds 3+ prior decisions, shows rejected alternatives, flags open questions
- A "poor" /design before: generic advice without checking vault data
