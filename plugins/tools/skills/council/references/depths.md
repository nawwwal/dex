# Depth and Fan-Out

Choose the smallest useful council. Wider fan-out is not better unless the perspectives are genuinely distinct.

## Permanent coverage rules

Every council must cover these lenses across the spawned agents and parent synthesis:

1. `Core mapper`
2. `Dependency / blast radius`
3. `Devil's advocate`
4. `Blind-spot`
5. `Actionability`

Hard requirements:

- The `devil's advocate` lens is mandatory in every depth tier.
- The `blind-spot` lens must be distinct from `devil's advocate`.
- Each spawned agent must have a clearly different perspective.
- Every prompt must include a short `Do not duplicate` section.

## Depth presets

### Quick

Spawn `4` agents. Use when the topic is narrow or the user wants speed.

Required agents:

1. `Core mapper`
2. `Dependency / blast radius`
3. `Devil's advocate`
4. `Blind-spot`

Parent synthesis responsibilities:

- add the `actionability` lens inline
- state what is still uncertain due to the smaller council

### Standard

Spawn `6` agents. Use for most investigations.

Required agents:

1. `Core mapper`
2. `Dependency / blast radius`
3. `Devil's advocate`
4. `Blind-spot`
5. `Actionability`
6. one mode-specific lens with the highest expected signal

Optional 7th agent:

- a second mode-specific lens when the topic crosses boundaries or has meaningful ambiguity

### Deep

Spawn `8-10` agents. Use for broad audits and architecture-scale investigations.

Required agents:

1. `Core mapper`
2. `Dependency / blast radius`
3. `Devil's advocate`
4. `Blind-spot`
5. `Actionability`
6-10. mode-specific lenses chosen for the topic

Prefer breadth with discipline. Do not pad the council with low-signal variants of the same question.

## Shared agent return contract

Tell every agent to return:

- `Findings:` concrete bullets only
- `Evidence:` file paths, artifacts, or source anchors
- `Confidence:` `high`, `medium`, or `low`
- `Open questions:` unresolved unknowns
- `Next move:` one recommended follow-up

## Shared prompt skeleton

Use this shape for each agent:

```text
You are the [LENS NAME] lens for a council investigation on: [TOPIC]

Working context:
- mode: [MODE]
- depth: [DEPTH]
- goal: [GOAL]
- scope note: [SCOPE]

Your job:
[FOCUS ON]

Do not duplicate:
[WHAT OTHER LENSES OWN]

Return:
- Findings
- Evidence
- Confidence
- Open questions
- Next move

Do not describe your plan. Do the investigation.
```

## Failure handling

- If one agent fails, continue and mark the missing coverage.
- If two agents fail, continue only if the permanent coverage still includes `core`, `dependency`, `devil's advocate`, and `blind-spot`.
- If evidence stays thin, label conclusions as tentative instead of pretending certainty.
