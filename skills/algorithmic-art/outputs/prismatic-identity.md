# Prismatic Identity

*An algorithmic art movement in seeded glass refraction*

---

## Philosophy

Each agent identity is a window into the same luminous void. Behind every agent lives an orb of pure light — a radial gradient that breathes like a filament, brilliant white at its core, cooling through amber and indigo into near-black at its boundary. This orb is not a shape. It is a mathematical field: two overlapping Gaussian functions, `0.60·exp(-r²·2.5) + 0.40·exp(-r²·0.85)`, that produce a continuously varying intensity from zero to one. No geometry, no polygons — pure analytic function from radius to luminance. The orb is the soul of every agent, identical in form, waiting to be refracted into something singular.

The fluted displacement is the glass itself. Diagonal ridges — mechanical, precise, architectural — cut across the orb's face at an angle drawn from the agent's name hash. Each ridge is computed in one line: `slantedX = uv.x - uv.y·tan(angle)`. From this single expression emerges an infinite series of parallel channels, each containing its own gradient from displacement peak to trough. The glass bends light: the UV coordinate is shifted before sampling the orb, so each channel shows a slightly displaced cross-section of the luminance field. At the boundary between channels, light collects into crisp bright creases — the unmistakable signature of machined glass. This displacement technique is the same mathematics used in RzpGlass, Razorpay's production glass shader, refined through thousands of hours of visual tuning. Using it here creates visual continuity between agent identicons and the broader product surface.

The colorama transform is where identity crystallises into colour. The displaced luminance — a single floating-point value from zero to one — passes through an IQ cosine palette: `0.5 + spread·cos(6.283185·(t + phase + [hue, hue+0.333, hue+0.667]))`. Three channels oscillate at different phase offsets, producing every hue in a family without repetition. The phase offset (seeded from the agent name) determines which segment of the rainbow dominates: some agents breathe cold blue-violet, others burn in orange-amber, others glow silver-white. The displacement creates local luminance variation; the palette amplifies this variation into chromatic bands. A single uniform — `u_phaseShift` — rotates the entire palette without touching the colour family, enabling infinite tonal variation within a coherent identity.

Every visual phenomenon in this system emerges from fewer than 40 lines of GLSL. The bright seam at each flute boundary, the soft Gaussian specular from the positioned key light, the white bloom at the orb's core, the vignette that draws the eye inward — all are mathematical consequences of the same underlying parameters. No textures, no external assets, no random branching. Pure deterministic function from UV coordinate to RGBA pixel. The same agent name always produces the same orb. This is the meticulously crafted algorithm: not one written once but tuned through iterative refinement, every constant chosen after examining hundreds of renders, the work of a computational aestheticist who treats GLSL as poetry.

The seed system binds each agent to its identity permanently. djb2 hash of the agent name produces a 32-bit integer; mulberry32 PRNG draws 22 values in sequence, each determining a trait: hue family, slit angle, band density, displacement magnitude, palette phase, specular position. These 22 values are the agent's fingerprint — stable across every render, every device, every screen. Two agents with the same hue but different slit angles look like siblings seen from different angles. Two agents with the same angle but different phases look like the same material bathed in different light. The parameter space is a continuous manifold of glass identities, and each agent occupies exactly one point in it — its own, forever.

---

## Implementation

- **Technique:** Procedural dual-Gaussian orb + RzpGlass `createStripedDisplacement` + IQ cosine palette colorama
- **Renderer:** Raw WebGL — two-pass FBO (orb → lens distort → PNG data URL)
- **Seed system:** djb2 hash → mulberry32 PRNG → 22 `GlassOrbTraits` fields
- **Output:** Static PNG, ~144×144px, cached by agent name + size
- **Viewer:** `/tmp/razorsense-orb-identicons.html` — interactive HTML with live sliders, preset agents, mini-grid, download

## Parameters

| Uniform | Trait source | Effect |
|---------|-------------|--------|
| `u_baseHue` | `baseHue / 360` | Which hue family dominates |
| `u_hueSpread` | `0.40 + hueSpread/16·0.25` | Monochrome vs full-spectrum |
| `u_slitAngle` | remapped from `slitAngleDeg` 72–94° → 8–22° | Diagonal tilt of glass flutes |
| `u_numSegments` | `15 + bandCount·5` = 40–50 | Flute density |
| `u_dispX` | `smoothness·0.035` | Horizontal refraction magnitude |
| `u_dispY` | `refraction·0.028` | Vertical refraction magnitude |
| `u_phaseShift` | `(twistDeg-72)/96` | Palette phase rotation |
| `u_highlightAngle` | `highlightAngleDeg·π/180` | Key light clock position |
| `u_highlightStr` | `highlightStrength` | Specular glint intensity |
