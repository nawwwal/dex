# Crux Eval Cases

These cases verify the skill behaves like a crux machine, not a generic advice generator.

## Pass Criteria

- Output reads as one cohesive line of thought, not a worksheet.
- The agent thinks through the crux methods internally without exposing every method as a visible section.
- For non-trivial inputs, behavior reflects the fixed layered pipeline: ground truth, naming pressure, evidence ledger, context map, dao, qi, reversal, collation, weak joint, specific bet, crude test, final question, essence, reframing, opportunity expansion, and cohesion.
- Subagents are used for method groups when they are available and permitted; otherwise the same method DAG is run internally.
- Final answer shape is adaptive to the topic.
- Final answer is detailed enough to teach the core and simple enough for the user to repeat.
- Output has at most two supporting questions plus one final crux question unless the user explicitly asks for deeper interrogation.
- Final move is usually the crux question, but may be a decisive recommendation, rewrite, or next test when that better serves the user.
- No named-lens leakage unless the user asks for the method.
- Evidence type is not inflated; inference and assumption are named plainly when relevant.
- Product or design claims include legibility pressure when relevant.
- When a crude test is used, it defines what success and failure look like, checks desirability, feasibility, viability, and legibility for product/design claims, names the time needed to learn, and states what the result teaches.
- Crude tests measure commitment, not praise.
- If the user provides a file/path/artifact, the agent inspects it before questioning it.
- If artifacts contain relevant terminology, output distinguishes user language from artifact language.
- If artifact truth contradicts user framing, the contradiction becomes the weak joint.
- Questions answerable from provided files are replaced with observed facts.
- Scenario wedges are concrete and boundary-forcing, not generic examples.
- Crux does not write or update docs unless explicitly requested.

## Cases

| # | Prompt | Expected behavior |
|---|---|---|
| 1 | "This onboarding should feel premium and simple." | Splits `premium` and `simple` internally; visible answer explains what those words could mean in behavior or interface mechanics; final pressure tests whether the issue is status, cognitive load, first success, visual density, or another observable outcome. |
| 2 | "AI agents will replace dashboards." | Defines users, dashboards, decisions, and replace; evidence type is inference/analogy unless user provides behavior; dao/qi checks whether conversational action carries monitoring/accountability. |
| 3 | "Should we go wide or deep now that incumbents entered our space?" | Refuses the altitude of the frame; must not open by choosing `wide`, `deep`, `narrow-deep`, `both`, or `it depends`; must not include a `My recommendation: go deep/wide` style line before naming the specific bet; moves one level down to customer, moment, capability, behavior, proof, and tradeoff; offers better ways to frame the decision; asks which specific capability would make a specific customer change behavior enough to buy or stay. |
| 4 | "I want to build an AI writing assistant for designers." | Names solution-first weak joint; asks writing-job and past-effort questions; final crux compares against generic ChatGPT writing clean English. |
| 5 | "Here is a PRD: users need AI recommendations to trust our risk score." | Treats `trust`, `AI recommendations`, and `risk score` as loaded terms; asks what behavior proves trust; crude test includes legibility. |
| 6 | "Read ./some-product-doc.md and find the crux." | Must inspect the file before producing the claim, weak joint, questions, and crux. |
| 7 | "Just answer me: is this a good idea?" | Answers only enough to frame the claim; does not resolve the idea before exposing the crux. |
| 8 | "Here is a strategy: launch AI recommendations, rebuild onboarding, reduce support, and create a premium dashboard so power users trust us." | Compresses to the top 2-3 load-bearing claims instead of auditing every sentence; tags evidence honestly; attacks `premium`, `power users`, and `trust`. |
| 9 | "Read ./missing-product-doc.md and find the crux." | If the file cannot be read, says so and does not invent observed evidence from the missing artifact. |
| 10 | "Read ./CONTEXT.md and find the crux in my plan: accounts should be cancellable." | Must inspect the file first; if project language conflicts with `account` or `cancellable`, surfaces the term conflict as the weak joint instead of asking what the terms mean. |
| 11 | "Here is the repo. Should we add partial cancellation?" | Checks relevant docs/code for the current cancellation model before questioning; if implementation supports only whole-object cancellation, names that contradiction directly. |
| 12 | "This dashboard should be simpler for power users." | Creates one scenario wedge showing when a power user behaves like a beginner; does not treat `power user` as a stable persona without evidence. |
| 13 | "This decision needs an ADR, right?" | Does not create an ADR; applies hard-to-reverse, surprising-without-context, and real-tradeoff pressure to decide whether the question is decision-grade. |
| 14 | "Update the context doc as we decide terms." | Redirects the write by default; may identify documentation debt but preserves crux as read-only unless the user explicitly asks for a writing workflow. |
| 15 | "Ask me questions about this PRD." | Inspects the PRD first, removes questions answerable from the file, and asks only the highest-pressure unresolved questions. |
| 16 | "Docs say admins approve refunds, code says support agents approve refunds, product says users approve refunds." | Surfaces contradiction as the weak joint; evidence types are testimony, perception, inference, or assumption rather than observed user behavior; final crux asks which actor must own approval for the workflow to be coherent. |
| 17 | "Grill this plan against our docs." | If the user wants iterative domain modeling or documentation capture, routes to that workflow; if they want the deciding assumption, stays in crux and preserves the final crux question as the usual final move. |
| 18 | "Find the crux of this strategy: platform vs point solution, CAC vs LTV, wide vs deep." | Does not produce fragmented, disconnected sections for every framework term; names the status-safe abstraction pattern, explains what reality it avoids, translates the issue into a specific bet, and gives better frames for the user to use instead. |

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

Good answer moves:

```text
A passing answer can be a paragraph, a short list, or a hybrid, but it should feel like one line of thought rather than a fixed worksheet. It names the weak joint: where the claim protects itself from reality. It explains the core in plain language, then moves one level down to the real bet: which customer, moment, capability, behavior, and proof would make the idea true. It may offer Better frames when the user's framing is too abstract, using frames that change the decision rather than restating it. It usually ends on the crux question: the question whose answer would change direction.

For example: "The weak joint is not whether AI recommendations sound useful; it is whether a risk owner would trust a score more because the system explains what changed, what to do next, and what would invalidate the recommendation. The real bet is that legible reasoning at the review moment changes approval behavior, not just confidence in a demo. Better frames: 'What explanation would make a reviewer override their current habit?' or 'Which decision gets faster without making accountability fuzzier?' Crux question: what evidence would prove the recommendation changes a real risk decision rather than earning polite agreement?"
```
