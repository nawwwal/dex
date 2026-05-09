# Examples

Use this only when output calibration is unclear or a bad/good contrast would prevent generic questioning.

## Canonical Example

User: "I want to build an AI writing assistant for designers."

```text
claim:
Designers have a recurring writing problem severe enough to justify a dedicated AI assistant.

hidden premise:
Designers repeatedly face writing moments where quality affects real outcomes and existing generic tools do not solve the risky part.

evidence type:
Assumption until backed by past behavior.

weak joint:
You have named the solution before proving the painful writing moment.

standard of judgment:
Actual user experience: time, reputation, stakeholder friction, or delayed sending. Success means designers already spend effort or ask for help when the stakes are high.

dao:
This may not be about writing. It may be about reducing professional risk: sounding unclear, junior, careless, or misaligned in high-stakes communication.

qi:
A writing assistant is one possible vessel. Other vessels could be critique, rewriting, tone calibration, stakeholder translation, or message rehearsal.

assumption audit:
- must be true: designers repeatedly face writing moments where quality affects outcomes.
- currently assumed: generic AI writing help is not already enough.
- strongest evidence: past behavior showing time, money, reputation, or political cost.
- weakest evidence: designers saying "yes, I would use this."

questions:
1. Does "writing assistant" mean grammar correction, clarity, persuasion, confidence, stakeholder politics, or fear reduction?
2. When did a designer last spend real effort fixing writing before sending it: rewriting, asking a peer, using Grammarly, using ChatGPT, delaying, or avoiding the message?

crude test:
Test method: interview 10 designers about the last high-stakes message they sent. Do not show a product. Collect the original draft, final draft, time spent, emotional stakes, and workaround used.
- success signal: most can name a recent message where writing quality changed the outcome or consumed meaningful effort.
- failure signal: examples are hypothetical, low-stakes, or already solved by ChatGPT/Grammarly.
- desirability signal: designers already spend time, reputation, or social capital to improve these messages.
- feasibility signal: a manual critique/rewrite workflow improves the next message without building software.
- viability signal: the problem appears often enough, or in high-stakes enough moments, to justify a dedicated tool.
- legibility signal: designers can tell whether the assistant is for grammar, persuasion, stakeholder translation, or rehearsal.
- time to test: one day.
- what it teaches: whether the dao is writing support, professional risk reduction, stakeholder translation, or nothing worth building.

crux question:
Would this still matter if ChatGPT already wrote clean English perfectly?
```

## Bad vs Good

Bad:

```text
Great idea. Why do designers need this? What features should it have? How could we make it premium?
```

Failure: generic questions, solution-first framing, vague style language, no evidence type, no weak joint.

Good:

```text
weak joint:
You have named the AI surface before proving the painful writing moment.

questions:
1. Does "writing assistant" mean grammar correction, persuasion, stakeholder translation, confidence, or risk reduction?
2. When did a designer last spend real effort fixing a message before sending it?

crux question:
Would this still matter if generic ChatGPT already wrote clean English perfectly?
```
