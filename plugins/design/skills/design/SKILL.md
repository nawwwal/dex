---
name: design
description: "Use for design archaeology ('before I start on X'), design review/annotation, accessibility audits ('a11y', 'WCAG'), Figma prototypes, or case studies. When a Figma URL or design image is present alongside 'critique', prefer critique-5f."
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /design — Design Process Intelligence Router

## Dispatch Logic

### Archaeology (Before Starting)
Triggers: "before I start on X", "what do we know about X", "prior decisions on X", "what have we built like this before"
Chain: `$CLAUDE_SKILL_DIR/before.md`

### Design Review + Accessibility
Triggers: "review", "critique", "design feedback", "annotate", "check the design"
Chain: `$CLAUDE_SKILL_DIR/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` [auto-chains]

### Accessibility Only
Triggers: "a11y", "accessibility", "WCAG", "blade score", "keyboard nav", "screen reader"
Chain: `$CLAUDE_SKILL_DIR/a11y.md` [standalone]

### Prototype
Triggers: "prototype", "make interactive", "build playground", "Figma to code", "interactive demo"
Chain: `$CLAUDE_SKILL_DIR/prototype.md`

### Case Study
Triggers: "case study", "portfolio piece", "narrative for X", "promotion narrative"
Chain: `$CLAUDE_SKILL_DIR/before.md` [gather vault context] → `$CLAUDE_SKILL_DIR/case.md`

### Visual Design / Figma Review
Triggers: Input is a Figma link, uploaded design image, or screenshot AND intent signals critique/review/evaluation (words: "review", "critique", "5F", "design scorecard", "B2B critique", "feedback")
Chain: `critique-5f` skill
**Intent guard:** Do NOT route here for Figma URLs where intent is prototyping, implementation, or code generation — those stay in `/design` or `figma:implement-design`.

### Full Design Review (Comprehensive)
Triggers: "full design review", "comprehensive audit", "everything"
Chain: `$CLAUDE_SKILL_DIR/before.md` → `$CLAUDE_SKILL_DIR/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` → `$CLAUDE_SKILL_DIR/case.md`
