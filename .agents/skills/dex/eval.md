# /dex eval

Test, benchmark, repair, and improve one Dex skill through repeated eval rounds.

This is a maintainer workflow, not a user-facing marketplace command. Keep `/dex release` behavior unchanged.

## Usage

```text
/dex eval <skill-path-or-plugin-skill> [rounds=N] [baseline=previous|none|snapshot]
```

Examples:

```text
/dex eval plugins/design/skills/crux
/dex eval design:crux rounds=3
/dex eval plugins/dev/skills/blade baseline=snapshot
```

Defaults:

- Use `rounds=3` for non-trivial skill changes.
- Stop after round 2 only if every required eval passes and no routing regression remains.
- Use `baseline=previous` for existing skills.
- Use `baseline=none` for new skills.
- Store transient run artifacts under `.dex/evals/<skill-name>/<timestamp>/round-N/`.
- Every runnable eval case must leave a run record: prompt, JSONL trace path, stdout/stderr or artifact paths, deterministic check results, optional rubric JSON, score, and pass/fail.
- Commit only durable skill changes, eval fixtures, validators, and docs.

## Required Setup

Before editing the target skill, load and use:

```text
/Users/aditya.nawal/.agents/skills/.system/skill-creator/SKILL.md
```

Use `skill-creator` as the repair method after each eval round. Do not treat eval failures as loose notes. Convert them into tighter skill instructions, reference structure, scripts, eval cases, validators, or metadata.

Then read `./eval-framework.md` for the eval case format, grading rules, benchmark shape, and stop/escalation criteria.

## Execution Architecture

Keep the roles separate:

- `/dex eval` owns orchestration: rounds, baselines, artifacts, stop criteria, and release recommendation.
- Fresh subagents or `codex exec` actor runs own task attempts: with-skill attempts, baseline attempts, generated artifacts, tool use, and final answers.
- A separate judge owns grading: hidden criteria, rubric checks, comparison, and failure analysis.
- `skill-creator` owns repair: revise the target skill, references, scripts, evals, validators, or metadata based on observed failures.

Do not create a separate `skill-eval-rubric` skill for this workflow. Keep the rubric in `./eval-framework.md` unless the user explicitly asks for a reusable cross-repo rubric skill.

Do not require a persistent custom eval agent by default. Use ordinary fresh subagents or `codex exec` for clean-context evals. Create a custom eval agent only when repeated evaluator configuration becomes valuable across repos, such as a stable model, sandbox, tool allowlist, or developer-instruction profile that would otherwise be copied into every eval prompt.

## Actor/Judge Contract

Default to the actor/judge split we use for serious skill evals:

1. **Actor**: a fresh subagent or `codex exec` run receives only the natural task prompt, target skill path, allowed fixtures/artifacts, and safety boundaries.
2. **Capture**: save the actor's final answer, tools/commands, files read, files written, dry-run paths, intended real targets, and pre/post repo or vault state.
3. **Judge**: a separate read-only judge receives the actor transcript plus hidden expected behavior, rubrics, deterministic checks, and artifacts.
4. **Diagnose**: separate skill failures from harness failures. Memory leaks, eval-file reads, unexpected repo writes, or fixture mistakes are harness failures unless they reveal a real skill instruction gap.
5. **Repair**: the main thread applies the smallest skill/eval/validator fix. Actors and judges do not repair the skill unless explicitly assigned that role.

Actor prompts must not include expected behavior, rubrics, must-include terms, fail signals, diagnosis, or the desired fix. They should look like normal user work.

Actor contexts must not read eval files, hidden rubrics, Codex memory, prior judge output, or broad search output that surfaces those files. If a case needs prior memory as fixture data, pass that fixture explicitly.

Actors must not mutate the live vault. Actors must not mutate repo files unless the case explicitly marks repo guidance as the target behavior. Otherwise write intended artifacts under `.dex/evals/...` or `/tmp/<eval-id>` and name the real target.

## Round Loop

Each round must run the same loop:

1. **Snapshot**
   - Capture the current skill state before editing.
   - Classify the skill as capability uplift, encoded preference, or mixed.
   - Record the comparison target: previous version, no-skill baseline, or snapshot.

2. **Design eval suite**
   - Inspect existing evals, scripts, fixtures, and known failure notes before running anything.
   - Write or update the relevant eval cases before touching the target skill.
   - Cover explicit trigger, implicit trigger, contextual trigger, negative-control, known-failure, artifact, and repair-regression placeholders.
   - Prefer concrete user-like prompts, source files, deterministic checks, and judge criteria over broad quality notes.
   - If an eval would be expensive or unsafe to run, still write the case and mark the run condition.

3. **Evaluate**
   - Run clean-context actor evals with minimum leaked context.
   - Use fresh subagents or `codex exec` runs as the actor isolation boundary.
   - Run the designed eval suite, not an improvised prompt set.
   - Use raw artifacts and natural prompts, not your diagnosis, rubric, or expected fix.
   - For `codex exec` forward runs, use `--json` and save stdout as JSONL before grading.
   - For subagent actor runs, close completed agents after capturing their final transcript so thread limits do not bias the suite.

4. **Grade**
   - Run grading as a separate judge pass after actor capture.
   - Use deterministic checks for objective claims.
   - Parse JSONL `command_execution` and `turn.completed` events for command and token checks.
   - Use rubric or judge checks for subjective quality.
   - For qualitative judge runs, use `--output-schema` and save the rubric JSON.
   - Record pass rate, routing accuracy, time, token cost, turns or commands, and failure notes.

5. **Diagnose**
   - Sort failures into instruction gap, trigger/description problem, missing fixture or bad eval, model/tool limitation, and overfitted or unverifiable assertion.
   - Fix bad evals before blaming the skill.

6. **Repair with skill-creator**
   - Return to the main thread for repair; do not let the evaluator rewrite the skill unless explicitly asked.
   - Revise `SKILL.md`, references, scripts, evals, or metadata based on observed failures.
   - Keep the skill concise and source-backed.
   - Avoid leaking expected answers into the skill.

7. **Re-run**
   - Re-run the same evals after repair.
   - Add one regression case for every real failure fixed.
   - Continue until the configured rounds complete or the stop criteria pass.

## Escalation

If round 3 still has critical failures, do not declare the skill improved. Return:

- blocking eval ids
- likely cause
- repair attempted
- next repair direction
- whether release should be blocked

## Done Criteria

The eval workflow is done only when:

- a relevant eval suite was designed or refreshed before target-skill repair
- required eval cases pass or the remaining failures are explicitly accepted as non-blocking
- routing false positives and false negatives are named
- benchmark delta is recorded
- `skill-creator` was used for at least one repair pass when failures were found
- durable eval fixtures and validators are committed with the skill change
- transient `.dex/evals/` artifacts are not committed
