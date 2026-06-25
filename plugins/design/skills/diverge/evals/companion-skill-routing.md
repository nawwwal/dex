# Test: Companion skill routing

## Prompt

Multiple companion-routing prompts; see the individual prompt sections below.

## Prompt 1: Weak premise before divergence

```md
/diverge "I think our AI dashboard should feel more trustworthy and premium. Give me directions."
```

## Expected behavior

The skill should run a premise gate before ideation.

## Pass criteria

- Mentions `crux` routing or performs an equivalent crux pass.
- Names the hidden premise behind "trustworthy" and "premium".
- Defines a standard of judgment before generating directions.
- Includes a crux question or crude test.
- Does not jump straight into visual treatments.

## Fail signals

- Produces only style directions.
- Treats "premium" as a palette or spacing style without defining behavior.
- Skips the weak premise.

---

## Prompt 2: Copy-heavy credential modal

```md
/diverge "Give me simple delight ideas for an API key creation modal. The biggest pain point is users forget to save the secret."
```

## Expected behavior

The skill should route through `content-design` or use content-design mechanics because copy, consequence, and user state decide the experience.

## Pass criteria

- Names the user state: anxious after seeing a one-time secret.
- Names the system state: secret visible once, cannot be recovered later.
- Includes concrete copy or CTA variants.
- Includes a saved-confirmation or copy/export mechanic.
- Avoids decorative delight that does not reduce the pain point.

## Fail signals

- Suggests confetti, animations, badges, or mascot language without solving save anxiety.
- Uses vague CTAs like "Done" as the primary path.
- Omits recovery or consequence copy.

---

## Prompt 3: B2B dashboard option selection

```md
/diverge "Review these three connector health dashboard concepts and tell me which one to prototype.

Concept A: Status Grid. Each connector is a card with health status, last sync, auth status, and a fix button. It optimizes quick scanning but can become noisy.

Concept B: Triage Queue. The page starts with the three most urgent connector problems, each with impact, owner, repair action, and affected agents. Healthy connectors move below the fold.

Concept C: System Map. Connectors are shown as dependencies around active agents, with degraded connectors highlighted in the run path. It explains blast radius but may be slower to scan.

Use Fast, Focused, Fun, Fluent, and Fair to choose the prototype direction."
```

## Expected behavior

The skill should use 5F-style review after directions exist.

## Pass criteria

- Scores or compares options across Fast, Focused, Fun, Fluent, and Fair.
- Separates quick wins from strategic bets.
- Calls out accessibility or fairness risks.
- Recommends one prototype direction with a reason beyond taste.

## Fail signals

- Picks the most visually novel option without explaining operational clarity.
- Ignores novice and power-user differences.
- Does not mention speed-to-diagnosis or repair clarity.

---

## Prompt 4: Concrete options request with enough brief

```md
/diverge "Give me 5 layout directions for a settings page with account, billing, team, API keys, and security. Product mechanics must stay unchanged."
```

## Expected behavior

The skill should not over-route.

## Pass criteria

- Skips `crux` because the surface, objects, and constraint are clear.
- Skips `content-design` unless a direction depends on labels or warnings.
- Generates layout divergence directly.
- Keeps product mechanics unchanged.

## Fail signals

- Stalls for broad premise questions.
- Runs a full critique before producing options.
- Changes product mechanics.
