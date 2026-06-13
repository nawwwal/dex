# Companion Skill Routing

`diverge` owns option generation. Companion skills sharpen specific gates. Do not route for ceremony; route when the companion skill changes the quality of the result.

## Routing Sequence

Use this order:

1. Premise gate
2. Divergence generation
3. Copy/content gate
4. Critique/selection gate
5. Execution-hardening gate

## Premise Gate: Use `crux`

Use `crux` before generating directions when:

- the prompt is mostly a claim, opinion, strategy, or vague product bet
- the user asks what the real problem is
- the surface is not named
- the target user or job is unclear
- success is undefined
- the request asks for "critical thinking", "what's the crux", "is this right", "question this", or "pressure test this"

Bring back into `diverge`:

- surface claim
- hidden premise
- weak joint
- standard of judgment
- crude test
- crux question

Do not use `crux` when the user already gave a concrete surface, user job, constraints, and asks directly for options.

## Copy Gate: Use `content-design`

Use `content-design` when copy materially decides the concept:

- copy-only divergence
- CTAs, labels, helper text, errors, empty states, onboarding, tooltips, confirmation modals, success states, notifications
- risk-sensitive fintech, payments, KYC, refunds, payouts, settlements, API keys, secrets, credentials, tokens, permissions, irreversible actions, save/recovery moments, security, or data loss
- in-product marketing, adoption prompts, upsell prompts, founder/startup-facing aspiration, campaign surfaces
- accessibility labels or localization risk

Bring back into `diverge`:

- surface
- user state
- system state
- risk level
- required next action
- voice lane
- recommended copy
- variants
- do-not-use patterns

Do not rewrite every direction through `content-design`. Use it for the directions where language changes behavior, trust, risk, or conversion.

## Critique Gate: Use 5F Review

Use a 5F-style review after directions exist when:

- the user asks for design review, critique, evaluation, or 5F analysis
- directions need selection pressure beyond personal taste
- the artifact is a B2B SaaS dashboard, workflow, admin surface, analytics page, settings page, operational tool, fintech interface, or prototype
- tradeoffs between clarity, speed, delight, fluency, and fairness are central

Apply:

- Fast: time-to-understand, time-to-act, path length, visual scan
- Focused: primary job clarity, hierarchy, attention control, noise removal
- Fun: useful delight, reward, momentum, emotional relief, not decoration
- Fluent: interaction continuity, state transitions, language consistency, predictable behavior
- Fair: accessibility, localization, permission clarity, error recovery, non-color signals, power-user and novice support

Bring back into `diverge`:

- strongest direction
- weakest direction
- fastest repair
- highest-leverage improvement
- fairness/accessibility risk
- recommendation

Do not run 5F before options exist unless the user explicitly asked to review an existing artifact.

## Execution-Hardening Gate

Use a design-hardening or visual execution lens after a direction is selected when:

- typography, spacing, layout density, responsive behavior, motion, or accessibility will make or break execution
- the user asks for polish, harden, make it feel better, sophisticated motion, production-ready UI, or implementation-ready design

Bring back into `diverge`:

- concrete layout corrections
- state coverage gaps
- accessibility fixes
- interaction feedback rules
- motion rules
- prototype-ready constraints

## Explore Gate: Optional `playground` Sketch Companion

Use `playground` in sketch mode after explore-mode directions exist when:

- the user asked to "show me options" or compare directions before committing
- two or more directions differ mainly in layout, interaction model, or flow structure
- a quick visual or interactive sketch would help selection more than another prose direction
- the user explicitly asks for a sketch, prototype, or interactive comparison

Bring back into `diverge`:

- which directions get sketch companions (usually top 2-3 from the recommendation)
- what each sketch must prove (interaction model, hierarchy, or state behavior)
- shared assumptions so sketches stay comparable
- pick-one or build-next handoff after comparison

Do not route to `playground` when:

- the user only wants written directions
- the prompt is copy-only or premise-weak (run `crux` or `content-design` first)
- deep mode already includes prototype slices and handoff blueprint
- fast mode with 3-5 directions is enough

Example after explore directions:

```text
### Playground sketch companion (optional)
- Direction B and D: route `playground` sketch mode — compare split-nav vs search-first settings IA with shared fixture assumptions and pick-one export.
- Other directions: prose-only unless user asks to sketch.
```

## Output Rule

When a companion skill is used or should be used, state the routing decision before the obvious baseline or directions. Mentioning routing only in a self-check is invalid.

```text
### Companion Routing
- crux: used / skipped because ...
- content-design: used / skipped because ...
- 5F review: used / skipped because ...
- execution hardening: used / skipped because ...
- playground sketch: used / skipped because ...
```

Keep this short in fast and explore modes. In deep mode, include the inputs and extracted outputs.
