# Iteration harness

The shared primitive for **applying a transform to its own output N times, capturing the trajectory, and surfacing the fixed point.** Owned by `gravity`; reused by `arena`'s generational loop. This file is the contract — load it before running an iterated process.

## The loop

```
state_0 = input
for i in 1..N:
    state_i = transform(state_{i-1})
    record(state_i)
    if converged(last_k states): break
report(trajectory, attractor)
```

`transform` must be **closed**: `transform(x)` is a valid input to `transform`. If type changes each step, the loop isn't iteration, it's a pipeline — refuse or repair it.

## Convergence detection

Movement between consecutive states, measured cheaply and named honestly:

- **Token overlap** — fraction of shared content words with the previous state. Rising overlap → approaching a fixed point.
- **Length delta** — runaway growth or decay toward a stub are both signals (decay often means collapse).
- **Semantic standstill** — the judgment "is this saying anything new versus the last step?" When three consecutive steps add nothing, stop.

Convergence = movement below threshold for **k=3** consecutive steps. Don't declare convergence on a single quiet step; texts plateau and then lurch.

## Outcome classes

- **Fixed point** — `state_i ≈ state_{i-1}`. The attractor is that text.
- **Limit cycle** — the process oscillates between 2–3 recurring states. Report the cycle members; the attractor is the orbit, not a point.
- **Collapse** — decay to a degenerate end-state: an empty stub, or a generic platitude that fits any input. Collapse is a finding, not a failure — it means the transform (or the source) had no stable structure to preserve.
- **Divergence** — no stabilization within N. Report the velocity and the last state; do not fake a fixed point.

## Capture rules

- Record the **full text** of every state, not a paraphrase. The intermediate states are the evidence.
- Index states from 0 (input). When reporting a sampled trajectory, always include `state_1`, one middle state, and the final two.
- For long or multi-state runs, persist the full trajectory to a file; keep only the sampled view inline.

## Reuse note (arena)

In `arena`'s generational loop the "transform" is *one generation of play + strategy evolution* and the "state" is the population's strategies + reputation ledger. Convergence = norms stop shifting (stable cooperation/defection equilibrium, or a stable cycle of regime changes). Same harness: apply, capture, detect the attractor — here the attractor is an **emergent social norm**, not a text.
