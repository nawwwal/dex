# Playground Modes

Playground has two execution modes. Pick one before building.

## Build Mode (default)

Use when the user wants one artifact, a polished deliverable, or a single interaction model executed well.

- Produce one self-contained artifact.
- Choose one interaction model, state why, and execute it fully.
- Use the matching `assets/templates/` scaffold as the starting structure.
- Include live preview, reset, and export/paste-back when the model requires it.
- Run `scripts/validate_playground_html.py` on the finished HTML before returning.
- Do not produce 2–3 sketch variants unless the user explicitly asked for options or exploration.

## Sketch Mode

Use when the user asks for options, variants, a few approaches, exploration, or sketch mode by name.

- Produce 2–3 fast variants, not 5–7 full diverge directions.
- Keep variants tied to the same source fixture and shared source assumptions.
- Name the interaction model for each variant and what differs.
- Include compare, pick-one, or build-next export so the user can choose a direction.
- Prefer lighter polish than build mode; prove the interaction idea, not production craft.
- Do not run `design:diverge` layer diagnosis, product model, or handoff blueprint unless the user explicitly asks for diverge.

## When To Hand Off To Diverge

Route to `design:diverge` instead of sketch mode when the user wants:

- many directions (5+ concepts or layered frameworks)
- product-model or handoff-blueprint depth
- divergence before any artifact exists

Sketch mode is fast iteration inside playground. Diverge is strategic option generation.

## Mode Selection Signals

| User signal | Mode |
|-------------|------|
| build, polished, one artifact, implement this | build |
| default when mode is unspecified | build |
| sketch, explore, options, variants, a few approaches, compare before I pick | sketch |
| show me directions, brainstorm product concepts, diverge | `design:diverge` (not sketch) |
