# Example Routing

Use these only when the request is still hard to classify.

## Example 1

Prompt: `Audit the council skill and tell me what it's missing.`

- mode: `code`
- depth: `quick`
- goal: `findings`
- ask questions: `no`

## Example 2

Prompt: `Map the blast radius of changing the core hook lifecycle.`

- mode: `system`
- depth: `deep`
- goal: `risks`
- ask questions: `no`

## Example 3

Prompt: `How do other design systems handle dark mode token architecture?`

- mode: `research`
- depth: `standard`
- goal: `findings`
- ask questions: `no`

## Example 4

Prompt: `Review this workflow and surface hidden bottlenecks.`

- mode: `workflow`
- depth: `standard`
- goal: `findings`
- ask questions: `only if the workflow is not named`

## Example 5

Prompt: `Should we use Zustand or Jotai for this state management?`

- mode: `opinion`
- depth: `standard`
- goal: `decision`
- ask questions: `no`

## Example 6

Prompt: `Give me a fast contrarian review of this system design.`

- mode: `system`
- depth: `quick`
- goal: `risks`
- ask questions: `no`

## Example 7

Prompt: `Take a look at this and tell me what you think.`

- mode: `unknown`
- depth: `standard`
- goal: `findings`
- ask questions: `yes, ask up to 3 routing questions`

## Example 8

Prompt: `What are the best practices for designing webhook retry systems?`

- mode: `research`
- depth: `standard`
- goal: `findings`
- ask questions: `no`

## Example 9

Prompt: `I'm thinking of splitting this monolith. Get me different expert perspectives.`

- mode: `opinion`
- depth: `deep`
- goal: `decision`
- ask questions: `maybe 1 to clarify which monolith`

## Example 10

Prompt: `Compare how Stripe, Razorpay, and Adyen handle payment retries.`

- mode: `research`
- depth: `deep`
- goal: `findings`
- ask questions: `no`
