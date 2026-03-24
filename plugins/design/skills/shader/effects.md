# Visual Shader Effects

## Glow / Bloom
```glsl
float glow = exp(-dist * 8.0);  // exponential falloff
col += glowColor * glow * intensity;
```

## Chromatic Aberration
```glsl
float aberration = 0.003;
float r = texture(iChannel0, uv + vec2(aberration, 0.0)).r;
float g = texture(iChannel0, uv).g;
float b = texture(iChannel0, uv - vec2(aberration, 0.0)).b;
col = vec3(r, g, b);
```

## Film Grain
```glsl
float grain(vec2 uv, float time) {
  return fract(sin(dot(uv * time, vec2(12.9898, 78.233))) * 43758.5453);
}
col += (grain(uv, iTime) - 0.5) * 0.05; // subtle noise
```

## Vignette
```glsl
vec2 center = uv - 0.5;
float vignette = 1.0 - dot(center, center) * 2.0;
col *= clamp(vignette, 0.0, 1.0);
```

## Glitch
```glsl
float glitch = step(0.98, sin(iTime * 50.0 + uv.y * 10.0));
uv.x += glitch * 0.02;
```

## IQ Cosine Palette (Inigo Quilez)
```glsl
vec3 iqPalette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
  return a + b * cos(6.28318 * (c * t + d));
}
// Colorful: iqPalette(t, vec3(0.5), vec3(0.5), vec3(1.0), vec3(0.0, 0.33, 0.67))
// Blue/teal: iqPalette(t, vec3(0.5, 0.5, 0.5), vec3(0.5, 0.5, 0.5), vec3(1.0), vec3(0.0, 0.1, 0.2))
```
