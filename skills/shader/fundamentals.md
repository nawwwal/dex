# GLSL Fundamentals

## Coordinate Systems
- `gl_FragCoord` — pixel coordinates (bottom-left origin)
- `uv = gl_FragCoord.xy / iResolution.xy` — normalized 0-1
- Centered UV: `uv = (gl_FragCoord.xy - 0.5 * iResolution.xy) / iResolution.y`

## Built-in Uniforms (Shadertoy)
```glsl
uniform vec3 iResolution;   // viewport resolution (pixels)
uniform float iTime;        // shader playback time (seconds)
uniform vec4 iMouse;        // mouse pixel coords: xy=current, zw=click
uniform sampler2D iChannel0; // texture channel
```

## Data Types
```glsl
float f = 1.0;     // ALWAYS use decimal point for floats
vec2 uv;           // 2D vector: uv.x, uv.y (or uv.r, uv.g)
vec3 col;          // 3D: col.rgb, col.xyz
vec4 fragColor;    // 4D: fragColor.rgba
mat2, mat3, mat4;  // matrices
```

## Fragment Shader Structure
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec3 col = vec3(uv, 0.5 + 0.5 * sin(iTime));
    fragColor = vec4(col, 1.0);
}
```

## Key Built-in Functions
```glsl
mix(a, b, t)        // linear interpolation
smoothstep(a, b, x) // smooth 0-1 interpolation
clamp(x, 0.0, 1.0)  // clamp to range
length(v)           // vector length
normalize(v)        // unit vector
dot(a, b)           // dot product
fract(x)            // fractional part (repeat 0-1)
mod(x, y)           // modulo
abs(x), sin(x), cos(x), pow(x, y)
```

## WebGL Context
```javascript
const gl = canvas.getContext('webgl2');
// Uniforms set via: gl.uniform1f(loc, value)
// Textures bound via: gl.bindTexture(gl.TEXTURE_2D, tex)
```
