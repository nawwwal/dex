---
name: ui-design
description: Use when reviewing, implementing, polishing, hardening, or auditing UI — components, pages, or designs. Also for typography/spacing fixes, UX copy, edge case hardening, anti-pattern detection, accessibility, Figma implementation, design context capture, laws of UX, CSS pseudo-elements, shadow systems, prefetching, or audio feedback. Chains sub-skills automatically based on intent.
allowed-tools: Read, Write, Bash, Grep, Glob, Skill, Agent
---

# /ui-design — UI Design Intelligence Router

## Intent Classification (strict order — first match wins)

**Step 1: Classify primary intent from the action verb, not the URL.**

```
ANALYZE:    Action verb is "review", "critique", "feedback", "audit", "look at",
            "check", "what's wrong", "a11y", "5F", "score", "evaluate"
            → ALWAYS ANALYZE, even if a Figma URL is also present
            → "review this Figma" = ANALYZE, NOT implement

IMPLEMENT:  Action verb is "implement", "build", "generate code", "code this",
            "build from", "make this component", "convert to code"
            AND a Figma URL is present
            → Bare Figma URL with no action verb → ask user

EDIT:       Action verb is "fix", "clean", "typeset", "arrange", "normalize",
            "harden", "clarify", "distill", "polish", "enhance", "improve"
```

**Rule:** If both a Figma URL and a review verb are present → ANALYZE always wins.
**Rule:** Bare Figma URL with no verb → ask: "Should I implement this as code, or review the design?"

---

## Dispatch Logic

### ANALYZE routes

**Design Review + Accessibility**
Triggers: "review", "critique", "design feedback", "annotate", "check the design"
Chain: `$CLAUDE_SKILL_DIR/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` → `$CLAUDE_SKILL_DIR/anti-patterns.md` [auto-chains]

**Accessibility Only**
Triggers: "a11y", "accessibility", "WCAG", "blade score", "keyboard nav", "screen reader"
Chain: `$CLAUDE_SKILL_DIR/a11y.md` [standalone]

**Anti-pattern Detection / Audit**
Triggers: "anti-patterns", "audit", "slop check", "what's wrong visually", "design debt"
Note: "design audit" or "full audit" → use Full Comprehensive Review instead (includes review + a11y + anti-patterns)
Chain: `$CLAUDE_SKILL_DIR/anti-patterns.md`

**Visual Design / Figma Review**
Triggers: Figma URL present AND review/critique/5F/feedback verb
Chain: `critique-5f` skill

**Before Starting (Archaeology)**
Triggers: "before I start on X", "what do we know about X", "prior decisions on X"
Chain: `$CLAUDE_SKILL_DIR/before.md`

**Case Study**
Triggers: "case study", "portfolio piece", "narrative for X", "promotion narrative"
Chain: `$CLAUDE_SKILL_DIR/before.md` → `$CLAUDE_SKILL_DIR/case.md`

**Full Comprehensive Review**
Triggers: "full design review", "comprehensive audit", "everything"
Chain: `$CLAUDE_SKILL_DIR/before.md` → `$CLAUDE_SKILL_DIR/review.md` → `$CLAUDE_SKILL_DIR/a11y.md` → `$CLAUDE_SKILL_DIR/anti-patterns.md`

---

### IMPLEMENT routes

**Figma Implementation (Blade or Generic)**
Triggers: "implement", "build from figma", "generate code", "code this", "convert to code" + Figma URL
Chain: `$CLAUDE_SKILL_DIR/implement.md`
Note: implement.md auto-detects Blade mode (package.json check) and routes to blade-implementer agent or inline generic workflow

**Interactive Prototype**
Triggers: "prototype", "make interactive", "build playground", "dialkit", "interactive demo"
Chain: `$CLAUDE_SKILL_DIR/prototype.md`

---

### EDIT routes

**Typography / Font / Type Scale**
Triggers: "typeset", "fix typography", "font", "type scale", "vertical rhythm", "font hierarchy"
Chain: `$CLAUDE_SKILL_DIR/typeset.md`

**Layout / Spacing / Whitespace**
Triggers: "arrange", "fix spacing", "layout", "whitespace", "visual rhythm", "grid"
Chain: `$CLAUDE_SKILL_DIR/arrange.md`

**Design System Normalization**
Triggers: "normalize", "design system", "blade tokens", "replace hardcoded", "clean up tokens"
Chain: `$CLAUDE_SKILL_DIR/normalize.md`

**Edge Cases / Hardening**
Triggers: "harden", "edge cases", "i18n", "text overflow", "empty states", "error handling"
Chain: `$CLAUDE_SKILL_DIR/harden.md`

**UX Copy / Microcopy**
Triggers: "clarify", "ux copy", "button labels", "error messages", "microcopy", "empty state copy"
Chain: `$CLAUDE_SKILL_DIR/clarify.md`

**Simplification**
Triggers: "distill", "simplify", "strip to essence", "reduce complexity", "too noisy", "too busy"
Chain: `$CLAUDE_SKILL_DIR/distill.md`

**Visual Enhancement**
Triggers: "enhance", "polish", "bolder", "quieter", "colorize", "delight", "more personality", "tighten"
Chain: `$CLAUDE_SKILL_DIR/enhance.md`

**CSS Pseudo-elements**
Triggers: "pseudo-element", "::before", "::after", "::backdrop", "::placeholder",
          "view transition", "view-transition-name", "::selection", "hit target expansion",
          "negative inset", "pseudo before after"
Chain: `$CLAUDE_SKILL_DIR/pseudo-elements.md`

**Laws of UX**
Triggers: "fitts", "hick", "miller", "doherty", "postel", "jakob", "ux law",
          "laws of ux", "cognitive load", "progressive disclosure", "zeigarnik",
          "von restorff", "serial position", "peak end", "tesler", "goal gradient",
          "law of proximity", "miller's law", "aesthetic usability"
Chain: `$CLAUDE_SKILL_DIR/laws.md`

**Audio Feedback (when and whether to use sound)**
Triggers: "sound feedback", "audio feedback", "when to use sound", "payment sound",
          "confirmation sound", "notification behavior", "mute button", "audio ux",
          "sound for payments", "should I add sound"
Chain: `$CLAUDE_SKILL_DIR/audio-feedback.md`
Note: For Web Audio API technical implementation → load /motion skill ("AudioContext", "oscillator")

**Predictive Prefetching**
Triggers: "prefetch", "foresight", "trajectory prediction", "next.js prefetch",
          "hover prefetch", "intent-based prefetch", "useForesight"
Chain: `$CLAUDE_SKILL_DIR/harden.md` (prefetching section)

**Agentation (Visual Annotation)**
Triggers: "agentation", "annotation toolbar", "watch annotations", "visual feedback loop",
          "annotate my UI", "agentation_watch", "agentation setup"
Chain: `$CLAUDE_SKILL_DIR/agentation.md`

---

### CONTEXT route

**Design Context Capture**
Triggers: "design context", "DESIGN.md", "capture design rules", "teach design", "design onboarding"
Chain: `$CLAUDE_SKILL_DIR/context.md`
