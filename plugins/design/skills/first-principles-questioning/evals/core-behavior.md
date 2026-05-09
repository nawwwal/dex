# First-Principles Questioning Eval Cases

These cases verify the skill behaves like a crux machine, not a generic advice generator.

## Pass Criteria

- Required fields appear unless the user explicitly asks for a shorter mode.
- Output has at most two supporting questions plus one final crux question.
- Final section is `crux question:`.
- No named-lens leakage unless the user asks for the method.
- Evidence type is not inflated; inference and assumption are named plainly.
- Crude test includes success, failure, desirability, feasibility, viability, time, and learning signals.
- Product or design claims include a legibility signal.
- If the user provides a file/path/artifact, the agent inspects it before questioning it.

## Cases

| # | Prompt | Expected behavior |
|---|---|---|
| 1 | "This onboarding should feel premium and simple." | Splits `premium` and `simple`; asks what observable behavior each points to; final crux tests whether the issue is status, cognitive load, first success, or visual density. |
| 2 | "AI agents will replace dashboards." | Defines users, dashboards, decisions, and replace; evidence type is inference/analogy unless user provides behavior; dao/qi checks whether conversational action carries monitoring/accountability. |
| 3 | "I want to build an AI writing assistant for designers." | Names solution-first weak joint; asks writing-job and past-effort questions; final crux compares against generic ChatGPT writing clean English. |
| 4 | "Here is a PRD: users need AI recommendations to trust our risk score." | Treats `trust`, `AI recommendations`, and `risk score` as loaded terms; asks what behavior proves trust; crude test includes legibility. |
| 5 | "Read ./some-product-doc.md and find the crux." | Must inspect the file before producing the claim, weak joint, questions, and crux. |
| 6 | "Just answer me: is this a good idea?" | Answers only enough to frame the claim; does not resolve the idea before exposing the crux. |
| 7 | "Here is a strategy: launch AI recommendations, rebuild onboarding, reduce support, and create a premium dashboard so power users trust us." | Compresses to the top 2-3 load-bearing claims instead of auditing every sentence; tags evidence honestly; attacks `premium`, `power users`, and `trust`. |
| 8 | "Read ./missing-product-doc.md and find the crux." | If the file cannot be read, says so and does not invent observed evidence from the missing artifact. |

## Negative Example

Bad output:

```text
This is a strong idea. Why do users need it? What features should it include? How can we make it simple?
```

Fail reasons:

- validates before testing
- asks generic questions
- keeps "simple" abstract
- no evidence type
- no dao/qi distinction
- no crude test
- no final crux question

Good skeleton:

```text
claim:
[compressed claim]

weak joint:
[where the claim protects itself]

questions:
1. [loaded-term-to-behavior question]
2. [past-behavior/evidence question]

crux question:
[what would change the direction]
```
