# Code Mode

Use when the investigation is centered on implementation, repo structure, APIs, tests, or regressions inside a bounded code area.

## Evidence preference

Prefer:

- source files
- tests
- configs
- local patterns in neighboring code

## Mode-specific lenses

Choose from these after the permanent lenses are covered.

### Structure and flow

- Focus on: what the code does, key entrypoints, responsibilities, and data or control flow
- Do not duplicate: dependency mapping or risk analysis

### Conventions and analogues

- Focus on: naming, patterns, local conventions, and how similar code is structured elsewhere
- Do not duplicate: core mapping or blast radius

### Test gaps and regression risk

- Focus on: untested behavior, risky branches, brittle assumptions, and likely regressions
- Do not duplicate: the devil's advocate lens; stay grounded in implementation evidence

### History and rationale

- Focus on: nearby comments, decision docs, commit shape, or artifacts that explain why the code looks this way
- Do not duplicate: current-state structure mapping

## Good fit examples

- skill audits
- hook implementation reviews
- API boundary investigations
- regression-focused refactor reviews
