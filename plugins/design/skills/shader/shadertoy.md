# Shadertoy Conventions + RzpGlass/JARVIS Patterns

## Shadertoy Entry Point
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Your code here
    fragColor = vec4(col, 1.0);
}
```

## Standard UV Setup
```glsl
vec2 uv = fragCoord / iResolution.xy;       // 0-1 range
vec2 suv = (fragCoord * 2.0 - iResolution.xy) / iResolution.y; // -1 to 1, centered
```

## RzpGlass Fluted Glass Pattern (Razorpay Razorsense)
```glsl
// The exact technique from the RzpGlass component
// Creates vertical ridges (fluted glass displacement)
uniform float uCollapseProgress; // 0 = open/active, 1 = collapsed

vec2 flutedDisplace(vec2 uv, float progress) {
  float ridgeFreq = 8.0;
  float ridgeAmp = 0.008 * (1.0 - progress);
  float stripe = sin(uv.x * ridgeFreq * 3.14159 * 2.0);
  return uv + vec2(0.0, stripe * ridgeAmp);
}
```

## JARVIS Holographic Effect (project-specific)
```glsl
// Dual-Gaussian orb gradient
vec3 orbGradient(vec2 uv, vec3 color1, vec3 color2) {
  float d = length(uv);
  float orb1 = exp(-d * 3.0);
  float orb2 = exp(-d * 8.0);
  return mix(color1, color2, 1.0 - orb1) * orb2;
}

// IQ cosine palette colorama (seeded by agent name)
vec3 agentPalette(float seed) {
  return iqPalette(seed, vec3(0.5), vec3(0.5), vec3(1.0), vec3(seed, seed*0.33, seed*0.67));
}
```

## WebGL Setup (for non-Shadertoy use)
```javascript
// Minimal WebGL2 shader setup
const vs = `#version 300 es\nin vec2 a;void main(){gl_Position=vec4(a,0,1);}`;
const fs = `#version 300 es\nprecision highp float;out vec4 c;\n${fragmentShaderCode}`;
// ... compile, link, render quad
```

## Performance Notes
- Avoid `texture2D` in tight loops (cache lookups)
- `smoothstep` is cheaper than `pow` for anti-aliasing
- Use `fract` for tiling patterns
- Avoid dynamic branching in fragment shaders
- Test on mobile: mobile GPUs are 10x weaker than desktop
