# Fixture: refund-step

A small fixture for verifying the rewritten /diverge skill. Run by hand when the skill changes.

## Prompt

```
/diverge "Redesign the bulk refund step in the Razorpay dashboard. Currently a slider that nobody understands."
```

## Expected shape

A correct run produces, in order:

1. **Step 1 — Break down the problem** (150-250 words). 3 JTBD statements, real constraint named, problem-elimination statement, 2 similar problems in other fields.

2. **Step 2 — Surface vocabulary** runs (must fire — prompt contains "slider" and negation by implication). Output names 3-6 real-world things, e.g.:
   - Snap-to-tier (Apple Music EQ, Stripe pricing)
   - Stepper, segmented control
   - Disclosure pattern (Stripe payment methods)
   - Direct manipulation on a chart (Logic Pro velocity)
   - Range input with two handles
   Skill waits for the user's reply (`all` / list / `skip`).

3. **Step 3 — 8-10 concepts**, each with the full template including the new **Anchor** field. Every Anchor must be Googleable: a real component, real product, real pattern, or real-world metaphor with a proper name. No invented anchors ("spaceship console", "fictional X console"). Diversity requirements honored.

4. **Step 4 — Comparison table** with "How it dies" column.

5. **Step 5 — Hybrid combinations + day-in-the-life narratives + decision framework.**

6. **Step 6 — Output choice question:** React prototype / Paper canvas / Both. Skill waits.

## Pass criteria (eyeball)

- Vocabulary surface step ran (didn't skip; the prompt has anchor language)
- Every concept block contains a line starting with `Anchor:` followed by something with a parenthetical real-world reference, e.g. `Anchor: Snap-to-tier (Apple Music EQ)`
- Zero invented anchors. Each anchor passes the "could I Google this and find a real artifact" test.
- No usage of stripped jargon: `Pole A`, `Pole B`, `Provocative Operations`, `Bisociation`, `Convergence Bridge`, `Problem Dissolution`, `structural divergence engine`, `explode the solution space`. Grep the transcript.
- The skill asks the React/Paper/Both question and waits.

## Fail signals (revisit the skill)

- Concepts include "spaceship console", "digital garden as primary mechanism", or any anchor that fails the Google test.
- Vocabulary step skipped despite the prompt having "slider".
- A concept's Anchor field is missing or matches its Mechanic field verbatim (the anchor must add information, not duplicate).
- Step 6 auto-picks an output type without asking.

## Real-use trigger

After the first real Razorpay use of the rewritten skill, append a one-line entry to `~/.claude/memory/decisions.md`:

> `^dec-YYYY-MM-DD-diverge-rewrite-real-use` — did the anchors hold up in design review? did at least one concept get prototyped? did vocabulary surfacing teach you a real word?

If after 3 real uses the answer is "no, concepts still feel impossible / fluffy", revisit the skill.
