---
name: shader
description: "Focused shader skill for GLSL, Shadertoy, signed distance functions, procedural visuals, and fragment shader effects. Use only for shader work; generic UI review should not load this skill."
---

# Shader

Use this skill only for shader-specific work:
- GLSL fragment shader implementation or debugging
- Shadertoy sketches and ports
- Signed distance functions (SDF)
- Procedural visual systems
- Shader effects such as glow, bloom, chromatic aberration, film grain, glass, distortion, and raymarching

Do not load this skill for generic UI review, web layout critique, Blade adherence, accessibility, or dashboard polish unless the user explicitly asks about shader code or procedural visuals.

## Reference Map

Load only the reference needed for the request:

- GLSL basics, coordinates, uniforms, and common functions: `references/fundamentals.md`
- Visual effects recipes: `references/effects.md`
- Signed distance functions: `references/sdf.md`
- Shadertoy conventions and patterns: `references/shadertoy.md`

## Operating Mode

Identify the target runtime first: Shadertoy, WebGL, Three.js, React Three Fiber, raw canvas, or another host.

When writing shader code:
- Keep coordinate-space setup explicit.
- Use decimal literals for floats.
- Name uniforms and expected ranges.
- Mention any host-side requirements such as textures, resolution, time, mouse input, or precision declarations.

When reviewing shader code, lead with the visible artifact or failure mode, then the likely math/runtime cause, then the smallest correction.
