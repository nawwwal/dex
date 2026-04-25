# Fixture: refund-step

A small fixture for verifying the rewritten /diverge skill. Run by hand when the skill changes.

## Prompt

```
/diverge "Redesign the bulk refund step in the Razorpay dashboard. Currently a slider that nobody understands."
```

## Expected shape

A correct run produces, in order:

1. **Step 1a — Brief interview.** Skill posts ONE message with the 3 required questions (Main thing, References, Constraints + anti-patterns) and waits. After the user replies, the skill emits a Brief block with rave-tweet, altitude, audience (inferred), consistency contract (inferred) drafted, and waits for `go` or corrections.

2. **Step 1b — Break down the problem** (150-250 words). 3 JTBD statements (one obvious, one emotional/social, one surprising), real constraint named with primary + secondary, problem-elimination statement, 2 similar problems in other fields. Each item cross-references the Brief's main thing.

3. **Step 2 — Surface vocabulary** runs (must fire — prompt contains "slider" and negation by implication). Output names 3-6 real-world things, e.g.:
   - Snap-to-tier (Apple Music EQ, Stripe pricing)
   - Stepper, segmented control
   - Disclosure pattern (Stripe payment methods)
   - Direct manipulation on a chart (Logic Pro velocity)
   - Range input with two handles
   Skill waits for the user's reply (`all` / list / `skip`).

4. **Step 3 — 8-10 concepts**, each with the full template including **Modality** (input → output → feedback loop), **Structural thesis** (one rigorous sentence referencing the Brief's main thing), **Anchor**, and **Delight moment** fields. Every Anchor and Delight reference must be Googleable. Diversity requirements honored.

5. **Step 4 — Kill ledger.** Skill runs every concept through Keep / Rewrite / Kill with one-line fatal flaw + required revision. Killed list shown as one-line summary. User sees only Keep + Rewritten concepts in Step 5.

6. **Step 5 — Comparison table** with "How it dies" column. Hybrid combinations proposed if interesting.

7. **Step 6 — Deepen the picks.** Day-in-the-life narratives + simplicity pass (before/after one-liner) + real-world states (substantively different from happy path) + decision framework.

8. **Step 7 — Output choice question:** React prototype / Paper canvas / Both. Skill waits.

## Pass criteria (eyeball)

- **Brief extraction.** Step 1a fires, posts the 3 questions in ONE message, waits, then emits Brief block. If user typed `skip brief`, output marked DEGRADED at top.
- **Structural thesis present and unique.** Every concept has a Structural thesis line. No two theses are interchangeable when read in sequence.
- **Modality present.** Every concept has a single-line Modality field. Concepts that share all three modality components (input + output + feedback loop) flagged as layout variations in the kill ledger.
- **Kill ledger reasoning.** Step 4 emits Keep / Rewrite / Kill labels for all 10 concepts with explicit fatal flaw lines. Zero Kill/Rewrite requires explicit justification per concept.
- **Vocabulary step ran** (didn't skip; the prompt has anchor language).
- Every concept block contains BOTH an `Anchor:` line and a `Delight moment:` line, each with a real-world reference cited in the parenthetical.
- Zero invented anchors or delights. Each passes the "could I Google this and find a real artifact" test.
- **Cross-bucket quota satisfied across the 10 concepts:**
  - Anchors: ≥2 from video games, ≥2 from arts/cinema/music/literature/mythology, ≥2 from history/ritual/sport/craft/architecture, ≥1 from domestic/social/fashion, ≤3 from software.
  - Delights: ≥1 video game, ≥2 arts cluster, ≥1 history/sport/craft cluster, ≥1 domestic/social, ≤3 software.
- **Taste-targeted anchors.** When the Brief names 3-5 references, within-bucket anchor selection reflects the Brief's *qualities* (deadpan, ambient, ritual-temporal, etc.), not just adjacent works in one bucket.
- **Simplicity pass shown.** Step 6 produces a before/after one-liner per shortlisted concept. If identical, gate failed.
- **Real-world states substantively different.** No "loading shows a spinner". Empty / error / first-time / long-content states each describe a concrete different shape.
- Delight moments name a sensory instant (sees / hears / feels), not a generic pattern label.
- No usage of stripped jargon: `Pole A`, `Pole B`, `Provocative Operations`, `Bisociation`, `Convergence Bridge`, `Problem Dissolution`, `structural divergence engine`, `explode the solution space`, `Studio Weird`, `Fever Dream`, `Ship Weird`. Grep the transcript.
- The skill asks the React/Paper/Both question and waits.

## Fail signals (revisit the skill)

- Step 1a Brief interview skipped — skill jumped straight to decomposition without the 3 questions.
- Concepts include "spaceship console", "digital garden as primary mechanism", or any anchor that fails the Google test.
- Vocabulary step skipped despite the prompt having "slider".
- A concept's Anchor or Delight field is missing, or matches its Mechanic field verbatim (the references must add information, not duplicate).
- Two concepts' Structural thesis sentences are interchangeable — kill gate failed.
- Kill ledger absent or rubber-stamps all 10 concepts as Keep without reasoning.
- More than 3 of 10 anchors come from software / SaaS / consumer apps. The library is the bottleneck — push the model into games / arts / history.
- Delight moments read as decorative ("confetti on submit", "celebration animation"). The load-bearing test fails: removing the delight leaves the concept unchanged.
- Simplicity pass output identical to original (gate not run honestly).
- Real-world states copy-paste the happy-path description.
- Step 7 auto-picks an output type without asking.

## Real-use trigger

After the first real Razorpay use of the rewritten skill, append a one-line entry to `~/.claude/memory/decisions.md`:

> `^dec-YYYY-MM-DD-diverge-rewrite-real-use` — did the anchors hold up in design review? did at least one concept get prototyped? did vocabulary surfacing teach you a real word? did the Brief extraction add signal or feel like friction?

If after 3 real uses the answer is "no, concepts still feel impossible / fluffy", revisit the skill.
