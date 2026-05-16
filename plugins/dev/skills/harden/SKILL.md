---
name: harden
description: "Use when checking product interfaces for accessibility, semantic frontend structure, density, hierarchy, typography, production hardening, state coverage, copy clarity, CSS maintainability, native browser behavior, dependency weight, design-system normalization, frontend production risk, or anti-patterns."
---

# Harden

Check interface quality. Default to read-only critique unless the user explicitly asks for implementation.

Use this skill for:
- UI quality checks and critique
- Accessibility and WCAG checks
- Semantic HTML, native control behavior, and frontend substrate quality
- Density, spacing, hierarchy, and typography
- Production hardening: overflow, loading, empty, error, disabled, and permission states
- Anti-pattern detection
- CSS maintainability, cascade cost, and design-system normalization at the generic interface level
- Dependency restraint, asset cost, and readable JavaScript checks
- UX copy clarity

Do not use this skill for:
- Blade scoring or Blade-specific migration work. Route to `blade`.
- Blade-project interaction feel, motion, transitions, component normalization, or design-system replacement. Route to `blade` first so MCP owns the API and Blade-native motion.
- Dialkit, interaction primitives, or interface craft work. Route to `interface-craft`.
- Agentation toolbar, annotations, pending feedback, or self-driving critique. Route to `agentation`.
- Browser automation, screenshots, clicking, or authenticated page capture. Route to `agent-browser`.
- Shader, GLSL, Shadertoy, SDF, or procedural visual work. Route to `design:shader`.
- Motion-system design or animation implementation unless the review target is a static UI issue.
- Sound, audio feedback, or earcons. Route to `create-sound` or the available sound skill.

## Operating Mode

Start with the user's artifact: screenshot, file path, diff, URL, Figma frame, or product description.

If the target is a URL and the check needs live inspection, do not run `curl`, open browsers, or diagnose reachability inside `harden`. Stop and say: `Route to agent-browser for live capture. harden needs captured evidence before page-specific findings.` Inspect only after the captured output exists.

If the project uses Razorpay Blade and the request is about Blade adherence, scoring, component replacement, product-surface ownership, motion, hover/focus/tap, transition polish, or known Blade pattern recreation, do not score it from memory. Stop and route to `blade`; include the literal skill name `blade` in the response.

## Core Mechanics

Inspect the frontend substrate before visual polish. Review in this order:

1. Semantics: native elements, button/link intent, labels, forms, headings, and browser defaults carry the right meaning.
2. Layout flow: Flexbox/Grid, document flow, responsive constraints, and text behavior solve layout without brittle absolute positioning.
3. Cascade cost: selectors, specificity, overrides, globals, one-off values, and `!important` stay easy to delete or replace.
4. Interaction state: keyboard, focus, loading, disabled, empty, error, partial-data, permission, and long-content states are explicit.
5. Runtime cost: imports, assets, render-blocking CSS/JS, DOM reflow risk, and dependency weight do not slow the first useful screen. When code imports a third-party helper for simple behavior, include an import/dependency finding that names the import and the local/platform alternative.
6. Visual polish: hierarchy, density, typography, color, copy, and rhythm improve the already-correct structure. For vague style words like `premium`, use `Term -> meaning -> execution -> avoid`, then lead with responsive, cascade, or structural issues before color, texture, or decorative finish.

## Reference Map

Load only the reference needed for the request:

- Overall UI quality: `references/review.md`
- Accessibility: `references/a11y.md`
- Anti-patterns: `references/anti-patterns.md`
- Frontend substrate, CSS flow, cascade, JS restraint, and asset cost: `references/frontend-foundations.md`
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
