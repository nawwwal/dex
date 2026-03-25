---
name: design
description: "Design review, a11y, UI implementation, motion, shader, polish, archaeology, prototypes, case studies."
argument-hint: "[review | a11y | implement | motion | shader | polish | archaeology | prototype | case]"
allowed-tools: Read, Write, Bash, Grep, Glob, Skill, Agent, Edit
---

# /design — Design Intelligence Router

Classify intent from the action verb, then load the matching sub-file. First match wins.

## Dispatch Logic

### ANALYZE routes

**Design Review + Accessibility**
Triggers: "review", "critique", "design feedback", "annotate", "check the design"
Chain: `$CLAUDE_SKILL_DIR/ui/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` [auto-chains]

**Accessibility Only**
Triggers: "a11y", "accessibility", "WCAG", "blade score", "keyboard nav", "screen reader"
Chain: `$CLAUDE_SKILL_DIR/a11y.md`

**Visual Design / Figma Review**
Triggers: Figma link + critique/review intent ("review", "critique", "5F", "design scorecard")
Chain: `critique-5f` skill (via Skill tool)
**Guard:** Figma URL + prototyping/implementation intent → IMPLEMENT route, not here.

**Anti-patterns**
Triggers: "anti-pattern", "what's wrong with this pattern"
Chain: `$CLAUDE_SKILL_DIR/ui/anti-patterns.md`

### IMPLEMENT routes

**Figma → Code**
Triggers: "implement", "build", "generate code", "code this", "build from", "convert to code" AND Figma URL
Chain: `$CLAUDE_SKILL_DIR/ui/implement.md`

**Bare Figma URL** (no verb) → ask: "Implement as code, or review the design?"

### EDIT routes

**Harden**
Triggers: "harden", "edge cases", "error states", "loading states"
Chain: `$CLAUDE_SKILL_DIR/ui/harden.md`

**Enhance**
Triggers: "enhance", "improve", "level up"
Chain: `$CLAUDE_SKILL_DIR/ui/enhance.md`

**Typeset**
Triggers: "typeset", "typography", "type scale", "font"
Chain: `$CLAUDE_SKILL_DIR/ui/typeset.md`

**Normalize / Arrange**
Triggers: "normalize", "arrange", "clean up layout"
Chain: `$CLAUDE_SKILL_DIR/ui/normalize.md`

**Polish (written artifacts ONLY)**
Triggers: "polish", "tighten", "refine" — ONLY for specs, plans, PRDs, emails, Slack drafts.
Chain: `$CLAUDE_SKILL_DIR/polish/` content
**Contract:** Visual polish → use "enhance" or "review" instead. Polish = written artifacts only.

### CONTEXT routes

**Archaeology**
Triggers: "before I start on X", "what do we know about X", "prior decisions"
Chain: `$CLAUDE_SKILL_DIR/ui/before.md`

**Case Study**
Triggers: "case study", "portfolio piece", "promotion narrative"
Chain: `$CLAUDE_SKILL_DIR/ui/before.md` → `$CLAUDE_SKILL_DIR/case.md`

**Prototype**
Triggers: "prototype", "make interactive", "build playground"
Chain: `$CLAUDE_SKILL_DIR/prototype.md`

### SPECIALTY routes

**Motion / Animation**
Triggers: "motion", "animation", "framer", "spring", "gesture", "transition", "AnimatePresence"
Chain: `$CLAUDE_SKILL_DIR/motion/` — load the appropriate sub-file based on topic:
- Principles → `motion/principles.md`
- Framer Motion API → `motion/framer.md`
- Components → `motion/components.md`
- Performance → `motion/performance.md`
- Gestures → `motion/gestures.md`
- Audio → `motion/audio.md`
- Review → `motion/review.md`
- Craft → `motion/craft.md`

**Shader / GLSL**
Triggers: "shader", "GLSL", "fragment", "vertex", "SDF", "Shadertoy"
Chain: `$CLAUDE_SKILL_DIR/shader/` — load sub-file by topic:
- Fundamentals → `shader/fundamentals.md`
- SDF → `shader/sdf.md`
- Effects → `shader/effects.md`
- Shadertoy → `shader/shadertoy.md`

**Laws of UX**
Triggers: "laws of UX", "Hick's law", "Fitts", "cognitive load"
Chain: `$CLAUDE_SKILL_DIR/ui/laws.md`

**CSS Pseudo-elements**
Triggers: "pseudo-element", "::before", "::after"
Chain: `$CLAUDE_SKILL_DIR/ui/pseudo-elements.md`

**Audio Feedback**
Triggers: "audio", "sound", "haptic"
Chain: `$CLAUDE_SKILL_DIR/ui/audio-feedback.md`

**Agentation**
Triggers: "agentation", "annotation loop"
Chain: `$CLAUDE_SKILL_DIR/ui/agentation.md`

**Distill**
Triggers: "distill", "simplify component"
Chain: `$CLAUDE_SKILL_DIR/ui/distill.md`

### COMPREHENSIVE
Triggers: "full design review", "comprehensive audit", "everything"
Chain: `$CLAUDE_SKILL_DIR/ui/before.md` → `$CLAUDE_SKILL_DIR/ui/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` → `$CLAUDE_SKILL_DIR/case.md`
