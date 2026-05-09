---
name: harden
description: "Use when checking product interfaces for accessibility, density, hierarchy, typography, production hardening, state coverage, copy clarity, design-system normalization, or anti-patterns."
---

# Harden

Check interface quality. Default to read-only critique unless the user explicitly asks for implementation.

Use this skill for:
- UI quality checks and critique
- Accessibility and WCAG checks
- Density, spacing, hierarchy, and typography
- Production hardening: overflow, loading, empty, error, disabled, and permission states
- Anti-pattern detection
- Design-system normalization at the generic interface level
- UX copy clarity

Do not use this skill for:
- Blade scoring or Blade-specific migration work. Route to `design:blade`.
- Dialkit, interaction primitives, or interface craft work. Route to `interface-craft`.
- Agentation toolbar, annotations, pending feedback, or self-driving critique. Route to `agentation`.
- Browser automation, screenshots, clicking, or authenticated page capture. Route to `agent-browser`.
- Shader, GLSL, Shadertoy, SDF, or procedural visual work. Route to `design:shader`.
- Motion-system design or animation implementation unless the review target is a static UI issue.
- Sound, audio feedback, or earcons. Route to `create-sound` or the available sound skill.

## Operating Mode

Start with the user's artifact: screenshot, file path, diff, URL, Figma frame, or product description.

If the target is a URL and the check needs live inspection, stop and route capture to `agent-browser`; then inspect the captured output.

If the project uses Razorpay Blade and the request is about Blade adherence, scoring, or component replacement, stop and route to `design:blade`.

## Reference Map

Load only the reference needed for the request:

- Overall UI quality: `references/review.md`
- Accessibility: `references/a11y.md`
- Anti-patterns: `references/anti-patterns.md`
- Layout and spacing: `references/arrange.md`
- Copy clarity: `references/clarify.md`
- Simplification: `references/distill.md`
- Production readiness and edge states: `references/harden.md`
- Design-system alignment: `references/normalize.md`
- Typography: `references/typeset.md`

## Output Shape

Lead with the biggest flaw and name the weak joint.

For critique, use severity-ranked findings with concrete evidence:

```text
Critical
- [area/file] Problem: what breaks. Mechanic: why it breaks. Fix: specific change.

High
- ...
```

For recommendations, state the assumption and tradeoff. Keep style terms executable: connect each term to layout, type, color, composition, state, copy, hierarchy, interaction, or behavior.
