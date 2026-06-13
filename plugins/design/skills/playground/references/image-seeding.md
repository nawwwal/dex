# Image Seeding

Use `tools:media-tools` when a bitmap seed, texture, scene, mockup, specimen, or visual reference would materially improve the artifact. Media generation is a source of visual constraints or assets, not a replacement for interaction design.

## Inspiration Seed

Use this when the artifact needs a stronger visual grammar but should remain semantic HTML/SVG/canvas.

1. Generate one bitmap first.
2. Extract composition, depth, texture, lighting, rhythm, density, material, spatial metaphor, and color logic.
3. Rebuild the useful grammar in HTML, CSS, SVG, or canvas.
4. Keep essential text, controls, state, and export behavior outside the bitmap.

## Asset Seed

Use this when the image itself is a useful object in the artifact.

- Use the generated image directly as a scene, texture, background specimen, product mockup, diagram anchor, or visual reference.
- If the asset belongs to a project artifact, store it in the workspace instead of leaving it only in generated image scratch space.
- Include `alt`, `role`, `prompt_or_source`, and provenance notes in artifact metadata.

## Do Not

- Use generated images as wallpaper.
- Hide essential information, labels, controls, or data inside a bitmap.
- Generate multiple visual directions through media-tools; use `design:diverge` for options.
- Let media-tools decide information architecture, affordances, control layout, text legibility, or interaction state.
- Leave project-used assets only in `$CODEX_HOME/generated_images`.
