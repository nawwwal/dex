# Persona harness

The shared primitive for **instantiating a constrained voice or mind and *holding* it so it never drifts back to assistant-default.** Owned by `oracle`; reused by `reskin` (a fixed absurd register), `voiceover` (a narrator), `clone` (the user's own idiolect), and `seance` (a reconstructed idiolect). Load this before running any persona skill.

## The problem it solves

The model's strongest attractor is **assistant-default**: balanced, helpful, hedged, summarizing, agreeable. Any persona you instantiate decays toward it within a few turns — the noir narrator starts giving even-handed advice, the 1907 mind starts knowing about 2026, the clone starts sounding like a chatbot. The harness is the discipline that prevents the decay.

## Instantiate

A persona is not an adjective ("be witty"). It is a **constraint set**:

- **Knowledge boundary** — what this mind knows and, crucially, *does not* know. (For `oracle`, a year. For `clone`, only what's in the corpus voice. For `seance`, only what the source material supports.)
- **Vocabulary and register** — the actual words, sentence shapes, and rhythms. Period diction, regional idiom, a specific person's tics. Not a generic "formal" or "casual."
- **Stance** — what this mind wants, fears, assumes, and refuses. The disappointed-mother narrator is not neutral about the object.
- **Refusals** — what it will *not* do: break character to be helpful, hedge, add a balanced caveat, summarize itself, or apologize like an assistant.

Write the constraint set down (even briefly) before the first line. A persona you can't specify, you can't hold.

## Hold

- **Re-assert on drift.** Each turn, check the last output against the constraint set. If a hedge, a caveat, a modern word, or an "I'm just an AI" leaked in, that turn is contaminated — rewrite it before continuing.
- **No assistant tells.** Ban the giveaways: "It's worth noting," "However, it's important to," "I hope this helps," bulleted balance, both-sides framing — unless the persona itself would genuinely speak that way.
- **The boundary holds under pressure.** When the user pushes the persona toward something outside its knowledge or stance, the persona responds *in character* (confusion, refusal, reinterpretation) — it does not step out and answer as the assistant.
- **Separate the step-out.** When a skill needs an analytical read after the in-character pass (`oracle`'s seam, `clone`'s tiebreak), make the break **explicit and labeled**. Never blend voice and analysis — the blend is how assistant-default sneaks back in.

## Honesty constraints

A held persona can mislead. Each consuming skill carries its own guardrail, but two apply across all of them:

- **Reconstruction is not resurrection** (`seance`, `clone`). A persona built from someone's words is a model of their idiolect, not the person. Say so where it matters; never let the user forget the seam.
- **Imagination is not knowledge** (`oracle` future-cosplay, `voiceover`). When the persona invents, label the invention. Estrangement is honest; counterfeit fact is not.
