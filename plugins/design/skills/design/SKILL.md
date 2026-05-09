---
name: design
description: "Use when routing design, UI review, design-system, interaction, motion, audio, shader, browser-inspection, visual handoff, first-principles, or divergence requests to the correct focused design skill."
argument-hint: "[review | blade | craft | agentation | browser | crux | diverge | polish | sound | shader | visual]"
allowed-tools: Read, Bash, Grep, Glob, Skill
---

# /design - Thin Design Router

Route the request to the first matching focused skill. Do not reproduce embedded fallback instructions from this file. If the routed skill is unavailable, state exactly which skill is missing and stop.

## Routing Rules

| User intent or trigger language | Route |
|---|---|
| Blade, Blade score, Blade coverage, Razorpay design-system adherence, Blade components | `design:blade` |
| Dialkit, interface craft, interaction primitives, craft components | `interface-craft` |
| Agentation, annotations, pending feedback, critique toolbar, self-driving critique | `agentation` |
| Browser automation, localhost inspection, screenshots, snapshots, page interaction | `agent-browser` |
| First-principles questioning, claims, opinions, PRDs, strategy, problem statements, premises, crux, Gretchenfrage, dao/qi, question generation | `design:first-principles-questioning` |
| Divergence, diverge, brainstorm, alternatives, alternate concepts, concepts, different directions, different approaches | `design:diverge` |
| Polish, make it feel better, animation polish, transitions, motion, interaction feel | `web-animation-design` and/or `make-interfaces-feel-better` |
| Sound, audio feedback, earcons | `create-sound` or the available sound skill |
| Shader, GLSL, Shadertoy, SDF, procedural graphics | `design:shader` |
| Visual handoff, engineer handoff, implementation spec, component inventory, screen inventory, state inventory, component breakdown, motion handoff | `visual` |
| Generic UI review, a11y, hardening, density, hierarchy, typography, anti-patterns, state checks | `design:interface-review` |

## Precedence

1. Use `design:blade` whenever the request is about Razorpay Blade, Blade Score, coverage, or design-system adherence, even if it also says review, polish, or a11y.
2. Use `agent-browser` when the user asks to inspect a running page, capture screenshots, interact with localhost, or verify page state.
3. Use `design:first-principles-questioning` when the request is about interrogating a claim, PRD, strategy, premise, problem statement, dao/qi fit, crux, or question set before solution work.
4. Use `agentation` for annotation toolbar workflows and self-driving critique loops.
5. Use `design:diverge` for concept generation or alternate directions before critique or polish.
6. Use motion/polish routes only after ruling out Blade, browser inspection, first-principles questioning, Agentation, and divergence.
7. Use `visual` for handoff and artifact-generation requests before using read-only interface review.
8. Use `design:interface-review` for broad UI critique when no more specific route applies.

## Multi-Route Handling

- If one request clearly needs multiple skills, name the sequence before loading them.
- Prefer the narrowest route that can complete the job.
- For "make it feel better" on a running page, use `agent-browser` first for inspection, then `make-interfaces-feel-better` or `web-animation-design`.
- For Blade UI polish, use `design:blade` first; add motion or interface-feel skills only for non-Blade interaction details.

## Retired Routes

Do not route to retired critique-specific skills. Use `design:interface-review` for design critique unless a more specific route applies.
