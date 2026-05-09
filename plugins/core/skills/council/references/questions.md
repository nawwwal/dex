# Intent Interview

Use this file only when routing is still ambiguous after reading the prompt and doing a lean reconnaissance pass.

## Host Tool Mapping

- **Claude host:** use `AskUserQuestion`
- **Codex host:** use the host's structured ask-question surface when available

Prefer structured multiple-choice questions over open-ended prompts.

## Rules

- Ask the minimum number of questions needed to route correctly.
- Cap the interview at 3 questions.
- Skip the interview entirely when the prompt already implies `mode`, `goal`, and `depth`.
- If the user stays ambiguous after the cap, proceed with the best default and record assumptions.

## Question Bank

### Q1: What are we investigating?

Use when `mode` is unclear.

- `Code area`
- `Research topic (gathering external information)`
- `Expert opinions on a decision`
- `System / architecture / integration`
- `Workflow / process`

### Q2: What do you want most from this?

Use when `goal` is unclear.

- `Findings`
- `Risks`
- `Decision guidance`
- `Prioritized actions`

### Q3: How broad should this be?

Use when `depth` is unclear.

- `Quick pass`
- `Standard investigation`
- `Deep audit`

### Optional Q4: What should the output optimize for?

Use only when the user has a very specific downstream need.

- `Action plan`
- `Risk map`
- `Blind-spot review`
- `Decision memo`
- `Research summary`

## Output Mapping

Map responses into the compact context object:

```json
{
  "investigation_context": {
    "mode": "...",
    "goal": "...",
    "depth": "...",
    "output_shape": "..."
  }
}
```

## Default Fallbacks

If the user declines to answer or stays vague:

- `mode=system` for broad cross-cutting repo questions
- `mode=code` for clearly implementation-local questions
- `mode=research` for questions about external information or best practices
- `mode=opinion` for questions seeking perspectives or recommendations
- `depth=standard`
- `goal=findings`

State the defaults in the final report's assumptions section.
