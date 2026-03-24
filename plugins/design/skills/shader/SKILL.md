---
name: shader
description: "Use when writing GLSL shaders — fundamentals, signed distance functions, visual effects ('glow', 'glitch', 'grain'), or Shadertoy/RzpGlass/JARVIS patterns."
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /shader — GLSL Router

## Dispatch Logic

### Fundamentals
Triggers: "fundamentals", "how does GLSL work", "uniforms", "coordinates", "vertex shader", "fragment shader"
-> Read `$CLAUDE_SKILL_DIR/fundamentals.md`

### Signed Distance Functions
Triggers: "SDF", "shape", "signed distance", "raymarching", "sphere SDF", "box SDF"
-> Read `$CLAUDE_SKILL_DIR/sdf.md`

### Visual Effects
Triggers: "effects", "glow", "bloom", "glitch", "grain", "chromatic aberration", "vignette", "scanlines", "dissolve"
-> Read `$CLAUDE_SKILL_DIR/effects.md`

### Shadertoy / Platform Patterns
Triggers: "shadertoy", "fragment shader", "JARVIS", "RzpGlass", "holographic", "fluted glass"
-> Read `$CLAUDE_SKILL_DIR/shadertoy.md`

### Full Shader Implementation
Triggers: "build shader for X", "create a shader", "implement shader"
-> Chain: `$CLAUDE_SKILL_DIR/fundamentals.md` -> [relevant sub-skill] -> `$CLAUDE_SKILL_DIR/effects.md` [if visual polish needed]

### Visual target (optional)
Before writing any GLSL, if the target effect can be described in words, invoke
`/generate-image` to produce a reference render — a concrete aesthetic target to code toward:
> `/generate-image` — prompt: "[effect name]: [visual description], digital art, real-time shader aesthetic" — aspect-ratio: 1:1
