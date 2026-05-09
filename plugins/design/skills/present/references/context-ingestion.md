# Context Ingestion

Use this when the user provides docs, Slack threads, meeting notes, PRDs, research notes, Figma comments, or pasted fragments.

## Extraction Pass

Return a compact map before asking questions:

- decision needed
- audience
- problem candidate
- evidence
- constraints
- current solution
- explored alternatives
- open questions
- risks or resistance
- useful exact language
- missing information

Do not preserve chronology unless chronology explains the decision.

## Slack Context

Slack threads often mix decision, emotion, status, and side concerns. Separate them:

- request: what someone is asking for
- concern: what risk or objection they are naming
- preference: what they personally like or dislike
- evidence: what concrete fact they cite
- decision: what needs to be resolved
- politics: who seems aligned, blocked, or anxious

Never refer to Slack users or channels by ID in the final wording.

## Doc Context

Docs often contain too much setup. Extract:

- the problem sentence
- the proof points worth showing
- assumptions
- constraints
- the proposed direction
- known non-goals
- unresolved decisions

Then ask what kind of room this narrative is for.

## Figma Or Design Artifact Context

If the user describes screens or flows, map the design to:

- entry point
- user's job
- major decision moments
- feedback or system response
- failure states
- completion state
- where the design proves the problem is solved

If interaction matters, recommend showing a prototype or walkthrough before static frames.

## Synthesis Format

Use this compact format:

Known:
- ...

Weak joint:
- ...

Questions:
1. ...
2. ...
3. ...

Next move:
- ...

Keep the weak joint precise. Examples:

- "The problem is currently a solution preference."
- "The audience is undefined, so the feedback ask cannot be sharp."
- "The open questions are too broad to protect the review."
- "The proof is in the doc, but not in the meeting sequence."
