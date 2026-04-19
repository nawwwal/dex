---
name: design
description: "Design review, a11y, UI implementation, motion, shader, interface polish, archaeology, prototypes, case studies."
argument-hint: "[review | a11y | implement | enhance | harden | typeset | clarify | normalize | motion | shader | archaeology | prototype | case | context | distill]"
allowed-tools: Read, Write, Bash, Grep, Glob, Skill, Agent, Edit
---

# /design — Design Intelligence Router

Classify intent from the action verb, then load the matching sub-file. First match wins.

## Precedence Rules

- Accessibility floors always come from `ui/a11y.md`. Hit areas, focus treatment, and WCAG compliance win over visual polish.
- Animation timing, easing, and performance come from `motion/principles.md`, `motion/components.md`, and `motion/performance.md`.
- Typography rendering details such as `text-wrap`, font smoothing, and `tabular-nums` come from `ui/typeset.md`.
- Micro-polish details such as concentric radii, optical alignment, image outlines, and shadows-over-borders come from `ui/enhance.md`.
- Requests to "polish" UI, "make it feel better", or fix something that "feels off" are visual work. Do not route them to the written-artifacts-only polish branch.

## Dispatch Logic

### ANALYZE routes

**Design Review + Accessibility**
Triggers: "review", "critique", "design feedback", "annotate", "check the design"
Chain: `$CLAUDE_SKILL_DIR/ui/review.md` → `$CLAUDE_SKILL_DIR/ui/a11y.md` [auto-chains]

**Accessibility Only**
Triggers: "a11y", "accessibility", "WCAG", "blade score", "keyboard nav", "screen reader"
Chain: `$CLAUDE_SKILL_DIR/ui/a11y.md`

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
Triggers: "enhance", "improve", "level up", "make it feel better", "feel better", "visual polish", "UI polish", "hover state", "micro-interaction", "press feedback", "optical alignment", "border radius", "image outline", "box shadow", "feels off"
Chain: `$CLAUDE_SKILL_DIR/ui/enhance.md`

**Typeset**
Triggers: "typeset", "typography", "type scale", "font", "font smoothing", "tabular numbers", "tabular-nums", "text-wrap", "text balance", "text pretty"
Chain: `$CLAUDE_SKILL_DIR/ui/typeset.md`

**Clarify**
Triggers: "clarify", "UX copy", "error message", "microcopy", "label text"
Chain: `$CLAUDE_SKILL_DIR/ui/clarify.md`

**Normalize / Arrange**
Triggers: "normalize", "arrange", "clean up layout"
Chain: `$CLAUDE_SKILL_DIR/ui/normalize.md` → `$CLAUDE_SKILL_DIR/ui/arrange.md`

**Polish (written artifacts ONLY)**
Triggers: "polish", "tighten", "refine" — ONLY for specs, plans, PRDs, emails, Slack drafts.
Chain: `elements-of-style` skill (via Skill tool)
**Contract:** Visual polish → use "enhance" or "review" instead. Polish = written artifacts only.

### CONTEXT routes

**Archaeology**
Triggers: "before I start on X", "what do we know about X", "prior decisions"
Chain: `$CLAUDE_SKILL_DIR/ui/before.md`

**Case Study**
Triggers: "case study", "portfolio piece", "promotion narrative"
Chain: `$CLAUDE_SKILL_DIR/ui/before.md` → `$CLAUDE_SKILL_DIR/ui/case.md`

**Prototype**
Triggers: "prototype", "make interactive", "build playground"
Chain: `$CLAUDE_SKILL_DIR/ui/prototype.md`

**Design Context**
Triggers: "design context", "setup design", "DESIGN.md"
Chain: `$CLAUDE_SKILL_DIR/ui/context.md`

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
Chain: `$CLAUDE_SKILL_DIR/ui/before.md` → `$CLAUDE_SKILL_DIR/ui/review.md` → `$CLAUDE_SKILL_DIR/ui/a11y.md` → `$CLAUDE_SKILL_DIR/ui/case.md`
