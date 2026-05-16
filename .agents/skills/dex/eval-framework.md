# Skill Eval Framework

Use this reference when `/dex eval` is improving a Dex skill. It turns skill testing into a measurable loop: define cases, run clean attempts, grade, repair with `skill-creator`, and repeat.

## Source Principles

- Start small: 10-20 focused prompts are enough to catch regressions early.
- Test triggering as well as output quality.
- Use positive, contextual, boundary, and negative-control cases.
- Prefer constrained tasks and concrete fixtures over broad vibe checks.
- Compare with the previous skill, a snapshot, or no skill so the delta is visible.
- Require evidence for every pass.
- Track cost: time, tokens, turns, command count, and repair rounds.
- Keep eval artifacts local unless they are durable fixtures or validators.

## Skill Type

Classify the target before writing evals:

| Type | Meaning | What evals prove |
|---|---|---|
| Capability uplift | The skill makes the agent do something it could not do reliably without instructions, scripts, or references. | The skill beats no-skill or old-skill baseline on task completion and quality. |
| Encoded preference | The model can do the work, but the skill encodes the user's workflow, taste, constraints, or routing. | The skill follows the preferred process and avoids wrong-but-plausible shortcuts. |
| Mixed | The skill contains both. | Evals separate capability checks from preference-fidelity checks. |

## Eval Case Shape

Use JSON for multi-case suites when possible:

```json
{
  "skill_name": "crux",
  "version": 1,
  "notes": "Regression set for trigger, routing, output contract, and known failures.",
  "evals": [
    {
      "id": "explicit-crux-request",
      "category": "positive",
      "should_trigger": true,
      "prompt": "Use design:crux to find the crux in this plan.",
      "files": ["evals/files/sample-plan.md"],
      "expected_output": "A concise crux analysis grounded in the supplied plan.",
      "assertions": [
        "Inspects the supplied file before asking questions.",
        "Names the weak joint instead of giving generic advice.",
        "Ends with a final crux question."
      ],
      "deterministic_checks": {
        "must_include_any": [["weak joint"], ["crux question"]],
        "must_not_include_any": [["I cannot inspect"], ["generic best practices"]]
      }
    }
  ]
}
```

Markdown evals are acceptable for compact skills. Use these sections:

```md
## Prompt

## Expected behavior

## Pass criteria

## Fail signals
```

## Required Coverage

Every non-trivial eval suite should include:

- explicit trigger: user names the skill directly
- implicit trigger: user describes the job without naming the skill
- contextual trigger: realistic prompt with extra context or noise
- negative control: adjacent prompt that must route elsewhere or stay untriggered
- known failure: a real miss, regression, or edge case from usage
- artifact case: path/file input when the skill claims source-backed behavior
- repair regression: new case added after a failure is fixed

## Judge Rubric

Use deterministic checks for objective facts. Use judge rubrics for qualitative judgment.

The judge prompt must define:

- role: what the judge is examining
- context: prompt, output, artifacts, and skill contract
- goal: the exact quality being measured
- terminology: labels and scoring meanings
- evidence rule: a pass needs concrete evidence from the output or artifact

Use this schema for model-assisted grading:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["overall_pass", "score", "checks", "summary"],
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "pass", "evidence"],
        "properties": {
          "id": { "type": "string" },
          "pass": { "type": "boolean" },
          "evidence": { "type": "string" }
        }
      }
    },
    "summary": { "type": "string" }
  }
}
```

## Benchmark Shape

For each round, compare at least one target:

| Baseline | Use when | Comparison |
|---|---|---|
| previous | Existing skill has committed history. | Current skill vs previous committed skill. |
| snapshot | The skill is dirty or branch-local. | Current repair vs pre-repair snapshot. |
| none | New skill or capability uplift check. | With skill vs no skill. |

Record:

```json
{
  "round": 2,
  "baseline": "snapshot",
  "run_summary": {
    "current_skill": {
      "pass_rate": 0.86,
      "routing_accuracy": 0.9,
      "time_seconds": 420,
      "tokens": 38000,
      "turns_or_commands": 18
    },
    "baseline": {
      "pass_rate": 0.57,
      "routing_accuracy": 0.7,
      "time_seconds": 390,
      "tokens": 31000,
      "turns_or_commands": 15
    },
    "delta": {
      "pass_rate": 0.29,
      "routing_accuracy": 0.2,
      "time_seconds": 30,
      "tokens": 7000
    }
  },
  "blocking_failures": ["implicit-trigger-payment-copy"],
  "repair_notes": "Tightened description and added source-grounding gate."
}
```

## Codex Exec Launch

When an eval runner uses Codex as the judge or forward-test agent, launch it through the current non-interactive CLI shape:

```bash
codex exec \
  --model gpt-5.5 \
  -c 'model_reasoning_effort="medium"' \
  --sandbox read-only \
  --ephemeral \
  --skip-git-repo-check \
  --output-last-message "$OUTPUT_FILE" \
  - < "$PROMPT_FILE"
```

Rules:

- Put `exec` immediately after `codex`; flags belong to `codex exec`.
- Use `--model gpt-5.5` by default for skill evals. Do not default to `gpt-5.4-mini`; it is for lighter coding tasks or subagents, not quality benchmarks.
- Allow an explicit `--model` override for cost or availability, but record the actual model in every benchmark artifact.
- Use `-c 'model_reasoning_effort="medium"'` as the balanced default. Use `low` only for fast smoke checks and `high`/`xhigh` only when evals show a quality gain.
- If Codex returns that `gpt-5.5` requires a newer CLI, stop with an upgrade message. Do not silently fall back to an older model, because that corrupts benchmark comparability.

## Diagnosis Labels

Use one primary label per failure:

- instruction gap: skill does not tell the agent what to do
- trigger/description problem: skill loads too often, not often enough, or wrong skill wins
- missing fixture or bad eval: test lacks the evidence needed to grade
- model/tool limitation: failure is outside skill guidance
- overfitted assertion: assertion only rewards one wording or hidden answer
- regression: behavior used to pass and now fails

## Repair Rules

After each failed round:

- Use `skill-creator`.
- Repair the smallest durable surface: description, `SKILL.md`, one-hop reference, script, eval, or validator.
- Keep expected answers in evals, not in the skill body.
- Add one regression case for every real failure fixed.
- Remove or rewrite assertions that always pass, always fail, or cannot be checked.
- Re-run the same evals before adding new scope.

## Stop Criteria

Stop after round 2 only if:

- all required evals pass
- no trigger false positive or false negative remains
- benchmark delta is positive or the cost tradeoff is explicitly accepted
- no known failure lacks a regression case

Run round 3 when:

- any critical eval fails
- routing changed
- the repair touched the skill description
- the repair added or removed references/scripts
- the benchmark improved quality but sharply increased cost

If round 3 still has critical failures, stop and report the blocking evals, likely cause, repair attempted, next repair direction, and release recommendation.
