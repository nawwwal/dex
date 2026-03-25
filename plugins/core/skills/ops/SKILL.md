---
name: ops
description: "Design documents, PRDs, design rationale, handoff specs, presentations."
argument-hint: "[prd | lens | rationale | slides | visual | spec]"
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /ops — Document Generation Router

## Dispatch Logic

### PRD Generation
Triggers: "prd", "requirements", "spec out", "product requirements", "write a PRD for"
→ Read `$CLAUDE_SKILL_DIR/prd.md`

### PRD Analysis (Designer's POV)
Triggers: "analyze this PRD", "review this PRD", "designer's POV", "what questions should I ask", "extract personas", "user stories from PRD"
→ Read `$CLAUDE_SKILL_DIR/lens.md`
Note: For deep analysis of a Google Doc URL → invoke prd-analyzer agent instead

### Design Rationale
Triggers: "rationale", "why did we design it this way", "document the decision", "explain this design choice"
→ Read `$CLAUDE_SKILL_DIR/rationale.md`

### Handoff Spec
Triggers: "handoff", "spec", "states", "edge cases", "engineer handoff", "Blade mapping", "component inventory"
→ Read `$CLAUDE_SKILL_DIR/spec.md`
Then: Auto-runs /design review a11y as final check

### Visual Explanation
Triggers: "diagram", "architecture diagram", "visual explanation", "make this visual", "explain this system", "diff review", OR any table with >3 columns and >4 rows
→ Read `$CLAUDE_SKILL_DIR/visual.md`

### Presentation / Slides
Triggers: "presentation", "slides", "create a deck", "convert PPT", "PPTX to web", "talk slides"
→ Read `$CLAUDE_SKILL_DIR/slides.md`

### Full Design Package
Triggers: "full design package for X", "complete design doc", "everything for X"
Chain: `$CLAUDE_SKILL_DIR/prd.md` → `$CLAUDE_SKILL_DIR/lens.md` → `$CLAUDE_SKILL_DIR/rationale.md` → `$CLAUDE_SKILL_DIR/spec.md`
Uses elements-of-style:writing-clearly-and-concisely on all written outputs.

## Writing Quality
For all documents: apply Strunk & White principles (from elements-of-style skill):
- Omit needless words
- Use active voice
- Be specific and concrete
- Prefer the short word over the long
