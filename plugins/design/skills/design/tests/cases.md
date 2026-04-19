# Skill Tests: design

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "review the agent marketplace home tab design" → Runs ui/review.md → ui/a11y.md chain
2. "check a11y on this component" → Runs ui/a11y.md standalone, produces WCAG checklist
3. "make this Figma design interactive" → Runs ui/prototype.md, fetches Figma via figma:implement-design
4. "make it feel better" → Runs ui/enhance.md (Polish sub-mode)
5. "harden this component" → Runs ui/harden.md (edge cases, overflow, i18n)
6. "fix the typography" → Runs ui/typeset.md
7. "clarify the error messages" → Runs ui/clarify.md
8. "add animation to this modal" → Runs motion/ sub-files
9. "distill this component" → Runs ui/distill.md

## True Negatives (should NOT trigger)
1. "design a database schema" → Technical design, not product design
2. "redesign this function" → Code refactor, not design
3. "what's good design?" → Conceptual question, not a process trigger
4. "polish this PRD" → Written artifact, routes to elements-of-style skill
5. "setup design" → Routes to /dex setup design, not /design

## Edge Cases
1. "full design review for X" → Chains: ui/review → ui/a11y
2. "review" on a code file → Should invoke design-reviewer agent, not ui/review.md
3. "a11y check" when no URL or file provided → Should ask "what would you like me to check?"
4. "feels off" → Routes to ui/enhance.md (Polish), NOT ui/review.md
5. Figma URL with no verb → Ask: "Implement as code, or review the design?"

## Quality Bar
- A "good" /design review: captures screenshot, invokes design-reviewer agent, chains to a11y, produces scored report
- A "poor" /design review: skips agent invocation, generic advice without checking code
