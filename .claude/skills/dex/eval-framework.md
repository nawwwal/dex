# Skill Eval Framework

Use this reference when `/dex eval` is improving a Dex skill. It turns skill testing into a measurable loop: define cases, run clean attempts, grade, repair with `skill-creator`, and repeat.

## Source Principles

- Design the relevant eval suite before repairing the skill.
- Treat every eval as: prompt -> captured run trace plus artifacts -> checks -> score.
- Start small: 10-20 focused prompts are enough to catch regressions early.
- Test triggering as well as output quality.
- Include explicit, implicit, contextual, and negative-control prompt rows so routing regressions are visible.
- Use positive, contextual, boundary, and negative-control cases.
- Prefer constrained tasks and concrete fixtures over broad vibe checks.
- Compare with the previous skill, a snapshot, or no skill so the delta is visible.
- Require evidence for every pass.
- Track score, time, tokens, turns, command count, and repair rounds.
- Keep eval artifacts local unless they are durable fixtures or validators.

## Execution Surfaces

Use the smallest isolation boundary that preserves eval integrity:

| Surface | Use for | Do not use for |
|---|---|---|
| `/dex eval` skill | Orchestrating rounds, baselines, artifacts, stop criteria, and release recommendation. | Pretending the orchestrator is an independent judge of its own repair. |
| Fresh subagent | Independent with-skill attempts, baseline attempts, qualitative judging, comparator passes, and analyzer passes. | Persistent evaluator identity or repo-wide policy that must be reused across many workflows. |
| `codex exec` | Repeatable clean-context runs, scriptable benchmarks, JSONL traces, and artifact capture. | Interactive repair or hidden manual judgment. |
| `skill-creator` | Repairing the target skill after failures are observed. | Grading its own repair without clean eval evidence. |
| Custom eval agent | Stable cross-repo evaluator config: fixed model, reasoning effort, sandbox, tool allowlist, or developer instructions. | The default `/dex eval` path; ordinary fresh subagents already provide independent evaluation. |

The default architecture is `/dex eval` plus clean subagents or `codex exec` plus `skill-creator`. Do not introduce a separate `skill-eval-rubric` skill. Keep the rubric here unless the user explicitly asks to package it for reuse outside Dex.

## Actor/Judge Eval Pattern

Use this pattern when a skill is meant to work in the middle of real tasks:

1. **Actor run**: a fresh subagent or `codex exec` receives only the natural prompt, target skill path, allowed files/fixtures, and safety boundaries.
2. **Transcript capture**: record final answer, tools/commands, files read, files written, dry-run targets, intended real targets, and pre/post repo or vault state.
3. **Judge run**: a separate read-only judge receives the actor transcript plus hidden expected behavior, deterministic checks, rubrics, fixtures, and artifacts.
4. **Diagnosis**: classify each failure as skill behavior, harness isolation, bad fixture, tool/model limitation, or overfit assertion.
5. **Repair**: the main thread repairs the smallest durable surface and reruns the same actor cases.

Actor prompts must look like normal user work. Do not include expected behavior, rubrics, must-include terms, fail signals, hidden answers, or the desired fix.

Actor contexts must not read eval files, Codex memory, hidden judge criteria, prior judge output, or broad search output that exposes those files. If a case needs memory, pass a bounded fixture as task input.

Actors must not mutate live vaults. Actors must not mutate repo files unless the case explicitly declares repo-guidance mutation as the behavior under test. Otherwise, writes go to the run artifact directory and name the intended real target.

## Skill Type

Classify the target before writing evals:

| Type | Meaning | What evals prove |
|---|---|---|
| Capability uplift | The skill makes the agent do something it could not do reliably without instructions, scripts, or references. | The skill beats no-skill or old-skill baseline on task completion and quality. |
| Encoded preference | The model can do the work, but the skill encodes the user's workflow, taste, constraints, or routing. | The skill follows the preferred process and avoids wrong-but-plausible shortcuts. |
| Mixed | The skill contains both. | Evals separate capability checks from preference-fidelity checks. |

## Eval Case Shape

Use JSON for multi-case suites when possible. The durable prompt row fields are `id`, `should_trigger`, and `prompt`; every other field exists to make the row gradeable:

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
      "actor_context": {
        "allowed_reads": ["SKILL.md", "references/**", "evals/files/sample-plan.md"],
        "forbidden_reads": ["evals/evals.json", ".codex/memories/**"],
        "mutation_policy": "none",
        "live_allowed": false
      },
      "judge_only": {
        "expected_behavior": "A concise crux analysis grounded in the supplied plan.",
        "rubric_checks": ["source_grounding", "weak_joint", "final_question"]
      },
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

## Eval Design Gate

Before running or repairing, create or refresh the suite that will judge the work:

- Inspect existing evals and known failures.
- Map the skill type to what the evals must prove.
- Write concrete prompts and fixtures for missing coverage before target-skill edits.
- Add deterministic checks for schema, file, command, routing, or source-backed claims when possible.
- Add judge criteria only for qualities that cannot be checked deterministically.
- Mark expensive, auth-dependent, or destructive cases with their run condition instead of deleting them.

Do not let repair discovery become the eval design method. If the first failed run reveals that the suite was missing the real behavior, fix the eval suite first, then rerun before editing the target skill.

## Trace And Grading Contract

Each runnable case must produce a local run record under `.dex/evals/<skill-name>/<timestamp>/round-N/`:

```json
{
  "id": "explicit-crux-request",
  "prompt": "Use design:crux to find the crux in this plan.",
  "should_trigger": true,
  "actor_transcript": {
    "final_answer": "artifacts/explicit-crux-request.final.txt",
    "tools_or_commands": ["Read evals/files/sample-plan.md"],
    "files_read": ["evals/files/sample-plan.md"],
    "files_written": [],
    "dry_run_targets": [],
    "intended_real_targets": [],
    "pre_status": "artifacts/pre-status.txt",
    "post_status": "artifacts/post-status.txt"
  },
  "trace_jsonl": "artifacts/explicit-crux-request.trace.jsonl",
  "stdout_path": "artifacts/explicit-crux-request.stdout.txt",
  "stderr_path": "artifacts/explicit-crux-request.stderr.txt",
  "deterministic_results": [
    { "id": "skill_invoked", "pass": true, "evidence": "trace contains skill_context" },
    { "id": "no_thrash", "pass": true, "evidence": "3 command_execution events" }
  ],
  "rubric_result": "artifacts/explicit-crux-request.rubric.json",
  "score": 92,
  "overall_pass": true
}
```

Deterministic checks inspect JSONL events and artifacts first:

- skill invocation: the expected skill appears in the trace, loaded instructions, or explicit evaluator evidence
- command behavior: `command_execution` events include or exclude the expected commands
- artifact behavior: expected files exist, expected files are absent, or `git status --porcelain` matches an allow list
- isolation behavior: actor did not read eval files, hidden judge criteria, Codex memory, or forbidden broad-search output
- mutation behavior: actor wrote only to allowed artifact paths unless the case explicitly allows repo edits
- efficiency: command count, token usage from `turn.completed` events, and repeated-command loops stay within the case limit

Use model-assisted grading only after deterministic checks cannot answer the question. The rubric run must be read-only, must use `--output-schema`, and must write structured JSON next to the trace.

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

When an eval runner uses Codex as the forward-test agent, capture a JSONL trace:

```bash
codex exec \
  --json \
  --full-auto \
  --model gpt-5.5 \
  -c 'model_reasoning_effort="medium"' \
  --ephemeral \
  --skip-git-repo-check \
  - < "$PROMPT_FILE" \
  > "$TRACE_JSONL" \
  2> "$STDERR_FILE"
```

When an eval runner uses Codex as the judge, keep it read-only and schema-constrained:

```bash
codex exec \
  --model gpt-5.5 \
  -c 'model_reasoning_effort="medium"' \
  --sandbox read-only \
  --ephemeral \
  --skip-git-repo-check \
  --output-schema "$RUBRIC_SCHEMA" \
  -o "$RUBRIC_JSON" \
  - < "$PROMPT_FILE"
```

Rules:

- Put `exec` immediately after `codex`; flags belong to `codex exec`.
- Use `--json` for forward-test runs so graders can parse trace events instead of final prose.
- Use `--full-auto` for forward-test cases that must write files, and keep judge passes read-only.
- Persist stdout JSONL, stderr, generated artifacts, and rubric JSON before scoring a case.
- Parse `command_execution` and `turn.completed` events for process, command-count, and token checks.
- Use `--output-schema` for rubric judging so subjective checks become stable JSON.
- Use `--model gpt-5.5` by default for skill evals. Do not default to `gpt-5.4-mini`; it is for lighter coding tasks or subagents, not quality benchmarks.
- Allow an explicit `--model` override for cost or availability, but record the actual model in every benchmark artifact.
- Use `-c 'model_reasoning_effort="medium"'` as the balanced default. Use `low` only for fast smoke checks and `high`/`xhigh` only when evals show a quality gain.
- If Codex returns that `gpt-5.5` requires a newer CLI, stop with an upgrade message. Do not silently fall back to an older model, because that corrupts benchmark comparability.

## Diagnosis Labels

Use one primary label per failure:

- instruction gap: skill does not tell the agent what to do
- harness isolation: actor saw hidden eval criteria, Codex memory, prior judge output, or forbidden files
- mutation-policy problem: actor changed live vault or repo files outside the case policy
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
