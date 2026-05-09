# Signed Distance Functions (SDF)

## Primitive SDFs
```glsl
// Circle
float sdCircle(vec2 p, float r) { return length(p) - r; }

// Box
float sdBox(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// Rounded box
float sdRoundedBox(vec2 p, vec2 b, float r) {
  vec2 d = abs(p) - b + r;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0) - r;
}
```

## Boolean Operations
```glsl
float opUnion(float d1, float d2) { return min(d1, d2); }
float opSubtraction(float d1, float d2) { return max(-d1, d2); }
float opIntersection(float d1, float d2) { return max(d1, d2); }

// Smooth union (blending)
float opSmoothUnion(float d1, float d2, float k) {
  float h = max(k - abs(d1 - d2), 0.0) / k;
  return min(d1, d2) - h * h * k * 0.25;
}
```

## Rendering SDFs
```glsl
// Render a shape from SDF
vec3 renderSDF(float d, vec3 shapeColor, vec3 bgColor) {
  float alpha = smoothstep(0.01, -0.01, d); // anti-aliased edge
  return mix(bgColor, shapeColor, alpha);
}

// Glow from SDF
float glow = 1.0 / (1.0 + d * d * 20.0);
col += glowColor * glow;
```

## RzpGlass Fluted Displacement (from Razorpay codebase)
```glsl
// Creates vertical ridge displacement (fluted glass effect)
vec2 createStripedDisplacement(vec2 uv, float frequency, float amplitude) {
  float stripe = sin(uv.x * frequency * 3.14159 * 2.0);
  return vec2(0.0, stripe * amplitude);
}
```
