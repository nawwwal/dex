# Synthesis Contract

The parent agent owns synthesis. Do not just concatenate subagent outputs.

## Core principle

Synthesize the tension between lenses, not just the inventory of observations.

## Required report structure

```markdown
# Council Report: [TOPIC]
*[depth] council · [date]*

## Top 3 Takeaways
- ...
- ...
- ...

## What We Know vs. What We Infer
- Known: ...
- Inferred: ...

## Perspective Findings
### Core mapper
...
### Dependency / blast radius
...
### Devil's advocate
...
### Blind-spot
...
### [other lenses]
...

## Where Agents Agree
- ...

## Where Agents Disagree
- ...

## What the Devil's Advocate Changed
- ...

## What the Blind-Spot Lens Surfaced
- ...

## Prioritized Next Actions
1. ...
2. ...
3. ...

## Open Questions
- ...

## Assumptions
- ...
```

## Synthesis rules

- Lead with the highest-signal conclusions, not with process.
- Distinguish observed facts from inference.
- Name disagreements explicitly.
- Call out when the devil's advocate invalidated a comfortable assumption.
- Call out when the blind-spot lens surfaced a new frame, not just a new detail.
- End with prioritized actions specific enough to execute.

## Small-council rules

When running `quick` depth:

- say that the review was intentionally narrow
- note which deeper lenses were not covered
- keep actions tight and reversible

## Partial-failure rules

If one or more agents fail:

- state which lens was missing
- reduce confidence where that missing lens matters
- do not imply comprehensive coverage

## Goal-specific emphasis

Adjust the report emphasis by `goal`:

- `findings`: emphasize current-state understanding and gaps
- `risks`: emphasize failure modes, fragility, and blast radius
- `decision`: emphasize tradeoffs, disagreements, and recommendation logic
- `actions`: emphasize sequence, priorities, and low-regret moves
