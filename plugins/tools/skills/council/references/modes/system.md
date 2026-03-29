# System Mode

Use when the investigation spans multiple repo areas or asks about architecture, hooks, lifecycle, ownership, integrations, or blast radius.

## Evidence preference

Prefer:

- architectural seams
- cross-plugin references
- hook wiring
- lifecycle entrypoints
- integration boundaries

## Mode-specific lenses

Choose from these after the permanent lenses are covered.

### Ownership and boundaries

- Focus on: which component or subsystem owns which responsibility, and where boundaries are muddy
- Do not duplicate: core mapping

### Failure modes

- Focus on: integration breakpoints, race conditions, lifecycle mismatches, and operational fragility
- Do not duplicate: dependency mapping or generic adversarial critique

### Observability and diagnosability

- Focus on: what would be hard to see, trace, or debug if this failed
- Do not duplicate: action planning

### Comparison and analogue

- Focus on: how similar systems in the repo solve comparable problems, and what can be learned from them
- Do not duplicate: conventions inside a single code area

## Good fit examples

- hook lifecycle investigations
- cross-plugin dependency mapping
- architecture blind-spot reviews
- blast-radius analysis before major changes
