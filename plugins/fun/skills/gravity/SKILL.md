---
name: gravity
description: "Use when the user wants to apply a transform to its own output over and over — rewrite a rewrite, summarize a summary, translate back and forth, restyle repeatedly — to see what the text collapses toward (its semantic fixed point / attractor). Triggers on 'what does this keep turning into', 'run this rewrite again and again', 'simplify until it stops changing', 'what's my default voice / what do I sound like'. On the user's own writing the attractor is their unconscious default voice. A frame-break skill: estrange the familiar by over-applying the ordinary."
argument-hint: "[text or @file] [transform, e.g. 'make it warmer' | 'summarize' | 'translate EN<->FR']"
allowed-tools: Read, Write
---

# Gravity

This skill makes the model refuse its default — produce one clean answer and stop. Instead it applies a transform to its own output, over and over, until the text stops moving, and reports the **attractor**: the place the language falls toward when you stop steering.

A single rewrite hides this. The fiftieth rewrite of the rewrite exposes it. On the user's own prose, the attractor is the voice they reach for when they aren't thinking — their unconscious default. On a summary, it's the irreducible core (or the hallucinated one). On a translation round-trip, it's the drift the language can't hold.

This is the iteration harness. The contract lives in `${CLAUDE_PLUGIN_ROOT}/skills/gravity/references/iteration-harness.md` — read it before running.

## Inputs

- **Text** — pasted, or `@file` (Read it).
- **Transform** — the function applied each step. If the user gives one, use it verbatim. If not, default to **"rewrite this faithfully in your own words"** (the purest attractor-finder) and say so.

The transform must be a closed loop: its output must be valid input to itself. Reject transforms that change type each step (e.g. "answer this question" → the output is an answer, not a re-answerable thing). If the transform isn't closed, name why and propose the nearest closed one.

## Run

1. Read the harness reference. Set `N` (default 25; cap 50; the user may request fewer).
2. Apply the transform to the input → step 1 output. Apply it to step 1 output → step 2. Continue.
3. **Capture every step's full text.** Do not paraphrase the trajectory — the words are the data.
4. After each step, measure movement against the previous step (see harness: token overlap / length delta / "has the meaning stopped changing"). Stop early when movement falls below the convergence threshold for 3 consecutive steps, or at `N`.
5. Detect the outcome class: **fixed point** (text stabilizes), **limit cycle** (oscillates between 2–3 states — report the cycle), or **collapse** (decays to a degenerate stub or a generic platitude — this is itself the finding).

## Report

- The **attractor**: the final stable text (or the cycle, or the collapse end-state), quoted in full.
- The **trajectory**: show steps 1, 2, a middle step, and the last two — enough to see the fall, not all 25. For long runs, write the full trajectory to a file with Write and link it.
- The **read**: name what the attractor reveals. For the user's own writing: "left alone, your language defaults to X." For a summary: "the irreducible claim is X" or "it converged on a platitude — the original had less substance than it looked." For translation: name what drifted and what survived.
- One line of **velocity**: did it converge fast (rigid text, strong attractor) or slow (genuinely varied source)?

## Rules

- Never present only the final state. The fall is the point; show the slope.
- Do not secretly steer toward a "nicer" attractor. Apply the transform honestly even when it collapses to mush — collapse is a true result about the text.
- If the user supplies their own writing and asks "what's my voice," do not flatter. Report the default voice as observed, including its tics and crutches.
- Keep `N` bounded — this is N model passes; respect cost. Default 25, never exceed 50 without explicit ask.
- If the transform isn't a closed loop, fix it or refuse it; don't silently mutate it mid-run.
- The trajectory text is canonical. If you summarize it for the chat, keep the full version in a file.

## Pairs with

Run gravity on the user's own writing to surface their default voice, then hand that attractor to `clone` to build a sharper self-model (and onward to `cartography` to see how that voice behaves in a relationship).
