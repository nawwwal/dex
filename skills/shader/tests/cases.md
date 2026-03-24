# Skill Tests: shader

## Category: Capability Uplift (monitor for model obsolescence)

## True Positives
1. "how does GLSL work?" → Runs fundamentals.md, explains uniforms/coordinates/built-ins
2. "build a circle SDF" → Runs sdf.md, provides sdCircle + rendering code
3. "add glow effect to this shader" → Runs effects.md, provides glow pattern
4. "shadertoy shader for RzpGlass" → Runs shadertoy.md, provides Razorpay-specific patterns
5. "build a full fragment shader for a glass card" → Chains fundamentals → sdf → effects

## True Negatives
1. "how does the shadow DOM work?" → Web API, not GLSL
2. "shade this region in the chart" → Data visualization coloring, not shader programming
3. "what shader should I use for this Figma layer?" → Figma effect, not GLSL

## Edge Cases
1. "RzpGlass shader" → shadertoy.md (Razorpay-specific)
2. "JARVIS holographic effect" → shadertoy.md (maps to old glsl stub pattern)
3. "glsl on mobile" → fundamentals.md with mobile performance note

## Retirement Monitoring
This is a capability uplift skill. If `claude-4-opus` or later can answer all true positives correctly without the skill loaded, consider retiring.
Run baseline test monthly: invoke without skill, check quality of GLSL answer.
