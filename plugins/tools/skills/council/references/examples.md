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

Prompt: `Find inconsistencies in our memory scaffolding.`

- mode: `vault`
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

Prompt: `What are we not thinking about in this plugin architecture?`

- mode: `system`
- depth: `deep`
- goal: `risks`
- ask questions: `maybe 1 question if scope is unclear`

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
