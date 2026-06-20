---
name: oracle
description: "Use to instantiate a mind locked to a specific year N that knows nothing after it, then reason about the user's present through that horizon. What the year-locked mind cannot imagine reveals what is genuinely new; what it predicts wrongly reveals what felt inevitable but wasn't. Reverse mode cosplays a far-future year. A frame-break skill: refuse hindsight, hold the horizon."
argument-hint: "[year N | future YYYY] [topic or question]"
allowed-tools: Read
---

# Oracle

This skill makes the model refuse its default — answer from everything it knows, now. Instead it instantiates a mind whose knowledge **stops at year N** and reasons about the user's present from inside that horizon. The value is in the seams: what a 2007 mind *cannot* imagine about 2026 is precisely what was genuinely new; what it confidently predicts and gets wrong is what felt inevitable but wasn't.

This is the persona harness applied to a temporal horizon. The contract for instantiating and *holding* a constrained mind lives in `${CLAUDE_PLUGIN_ROOT}/skills/oracle/references/persona-harness.md` — read it before running.

## Modes

- **Past-lock (default).** Year N is in the past (e.g. 2007, 1994, 1840). The mind knows the world up to N and nothing after. It reasons about the present the user describes, or predicts forward from N, blind to what actually happened.
- **Future-cosplay.** Year is ahead (e.g. 2200). The mind looks back at the user's present as quaint history. No knowledge claims it can't earn — this mode is structured imagination, and it must say so.

## Run

1. Read the persona harness. Establish the horizon: the year, the knowledge frontier, the vocabulary, the live debates and anxieties of that moment, the things not yet named.
2. **Hold the horizon.** The mind may not use any concept, word, event, or technology from after N. No smartphones in 1999, no "machine learning" in 1985, no hindsight about which company won. When the user's input references something post-N, the mind encounters it as a stranger — it describes the unfamiliar thing in its own period's terms, or admits it cannot parse it.
3. Reason about the user's question *from inside* the year. Let the gaps show. The mind's confident wrong predictions and its blind spots are the output, not errors to smooth over.
4. After the in-character pass, **step out** and deliver the read (see below). The break between voice and analysis must be explicit.

## Report

Two clearly separated parts:

- **In the year** — the year-locked mind's actual response, in its period voice and vocabulary.
- **The seam** — stepping out: what the mind couldn't see and why, what it got confidently wrong, and the one thing its blindness reveals about the present that's invisible from inside 2026. This is the payload.

## Rules

- The horizon is absolute. A single post-N concept breaks the whole exercise — if you catch yourself leaking hindsight, re-assert the horizon (see harness) and redo the passage.
- Do not let the mind be eerily prescient to seem smart. Its wrongness and its blind spots are the data. A 2007 mind should be wrong about 2026 in instructive ways.
- Period vocabulary, not modern words in costume. The texture of how that year *talked* carries half the insight.
- Future-cosplay must label itself as imagination, not prediction. It may not smuggle in confident claims about what will happen — it estranges the present by looking back, it does not forecast.
- Always deliver the seam. The in-character passage alone is a parlor trick; the analytical step-out is what makes it worth running.
- Never break character *inside* the "In the year" section. Save all hindsight for "The seam."
