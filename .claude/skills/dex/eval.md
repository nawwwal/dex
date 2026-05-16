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
- Fresh subagents or `codex exec` runs own evaluation: with-skill attempts, baseline attempts, judge checks, comparison, and failure analysis.
- `skill-creator` owns repair: revise the target skill, references, scripts, evals, validators, or metadata based on observed failures.

Do not create a separate `skill-eval-rubric` skill for this workflow. Keep the rubric in `./eval-framework.md` unless the user explicitly asks for a reusable cross-repo rubric skill.

Do not require a persistent custom eval agent by default. Use ordinary fresh subagents or `codex exec` for clean-context evals. Create a custom eval agent only when repeated evaluator configuration becomes valuable across repos, such as a stable model, sandbox, tool allowlist, or developer-instruction profile that would otherwise be copied into every eval prompt.

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
   - Run clean-context evals with minimum leaked context.
   - Use fresh subagents or `codex exec` runs as the isolation boundary.
   - Run the designed eval suite, not an improvised prompt set.
   - Use raw artifacts and prompts, not your diagnosis or expected fix.

4. **Grade**
   - Use deterministic checks for objective claims.
   - Use rubric or judge checks for subjective quality.
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
