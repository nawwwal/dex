# Skill Tests: ops

## Category: Encoded Preference

## True Positives (should trigger + produce good output)
1. "write a PRD for a payment retry flow" → Runs prd.md, asks 3-5 clarifying questions, produces structured PRD
2. "analyze this PRD as a designer" → Runs lens.md, extracts personas + 8-12 design questions
3. "why did we design the InfoArea as we did?" → Runs rationale.md, checks decisions.md
4. "create a handoff spec for the agent marketplace home tab" → Runs spec.md, maps Blade components
5. "make a diagram of our API architecture" → Runs visual.md, produces self-contained HTML
6. "full design package for the US research feature" → Chains prd → lens → rationale → spec

## True Negatives (should NOT trigger)
1. "what's the PRD say about X?" → Reading/searching, not creating a PRD
2. "spec your answer" → Clarification request, not handoff spec
3. "visualize your reasoning" → Meta instruction, not /ops visual

## Edge Cases
1. Table with 4 columns and 5 rows mentioned → Should proactively offer visual.md
2. "analyze this Google Doc [URL]" → Should read the document if available, otherwise ask for pasted/exported content
3. "slides for tomorrow's meeting" → Ambiguous; clarify whether new slides or convert PPT

## Quality Bar
- A "good" /ops prd: asks clarifying questions, writes all 8 sections, includes success metrics
- A "poor" /ops prd: writes a template without asking questions, uses vague requirements
