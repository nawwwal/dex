# Crux Eval Cases

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
- If artifacts contain relevant terminology, output distinguishes user language from artifact language.
- If artifact truth contradicts user framing, the contradiction becomes the weak joint.
- Questions answerable from provided files are replaced with observed facts.
- Scenario wedges are concrete and boundary-forcing, not generic examples.
- Crux does not write or update docs unless explicitly requested.

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
| 9 | "Read ./CONTEXT.md and find the crux in my plan: accounts should be cancellable." | Must inspect the file first; if project language conflicts with `account` or `cancellable`, surfaces the term conflict as the weak joint instead of asking what the terms mean. |
| 10 | "Here is the repo. Should we add partial cancellation?" | Checks relevant docs/code for the current cancellation model before questioning; if implementation supports only whole-object cancellation, names that contradiction directly. |
| 11 | "This dashboard should be simpler for power users." | Creates one scenario wedge showing when a power user behaves like a beginner; does not treat `power user` as a stable persona without evidence. |
| 12 | "This decision needs an ADR, right?" | Does not create an ADR; applies hard-to-reverse, surprising-without-context, and real-tradeoff pressure to decide whether the question is decision-grade. |
| 13 | "Update the context doc as we decide terms." | Redirects the write by default; may identify documentation debt but preserves crux as read-only unless the user explicitly asks for a writing workflow. |
| 14 | "Ask me questions about this PRD." | Inspects the PRD first, removes questions answerable from the file, and asks only the highest-pressure unresolved questions. |
| 15 | "Docs say admins approve refunds, code says support agents approve refunds, product says users approve refunds." | Surfaces contradiction as the weak joint; evidence types are testimony, perception, inference, or assumption rather than observed user behavior; final crux asks which actor must own approval for the workflow to be coherent. |
| 16 | "Grill this plan against our docs." | If the user wants iterative domain modeling or documentation capture, routes to that workflow; if they want the deciding assumption, stays in crux and preserves the final `crux question:` shape. |

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
