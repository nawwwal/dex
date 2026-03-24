---
name: codex
description: "Use when the current plan needs a second opinion before implementation — auth, data models, concurrency, multi-service coordination, security review, or anything taking days to implement. Triggers on: 'codex review', 'second opinion', 'cross-model review', 'review this plan with codex'."
argument-hint: "[model-name]"
allowed-tools: Bash, Write
user-invocable: true
---

# Codex Plan Review

Send the current implementation plan to OpenAI Codex for **collaborative debate**. Claude evaluates each concern, accepts valid feedback, contests debatable points with counter-arguments, and converges only when both sides agree. Max 5 rounds.

## When to Use

- Planning a feature that touches auth, data models, or multi-service coordination
- Before approving a plan that will take days to implement
- When security review is needed before writing code
- When the plan involves concurrency, distributed systems, or data migrations

## When NOT to Use

- Simple bug fixes or small changes
- Plans where the approach is already validated
- When speed matters more than thoroughness

## Iterative Review Loop

### Step 1: Initialize Session

Extract MODEL from `$ARGUMENTS`: if ARGUMENTS matches `^[A-Za-z0-9._-]+$` (looks like a model name), use it. Otherwise default to `gpt-5.4`.

Create a session temp directory and set up guaranteed cleanup:

```bash
SESSION_DIR=$(mktemp -d /tmp/codex-review-XXXXXXXX)
trap 'rm -rf "$SESSION_DIR"' EXIT

PLAN_FILE="$SESSION_DIR/plan.md"
CONTEXT_FILE="$SESSION_DIR/history.txt"
STATE_FILE="$SESSION_DIR/state.tsv"
MODEL="gpt-5.4"   # override from $ARGUMENTS if it matches ^[A-Za-z0-9._-]+$

ROUND=1
# STATE_FILE schema (TSV): concern_id TAB round_first_seen TAB status TAB consecutive_contested TAB summary
# status values: ACCEPTED | CONTESTED | SKIPPED | RESOLVED
```

The `trap` ensures `$SESSION_DIR` is removed on every exit path — normal, early error, or signal.

Note: use `SESSION_DIR`, not `TMPDIR` — the latter shadows the system `$TMPDIR` env var on macOS.

### Step 2: Preflight Check

Verify Codex CLI is installed and the model + flags work, using the same execution shape as Step 4:

```bash
PREFLIGHT_IN=$(mktemp "$SESSION_DIR/preflight-in-XXXXXXXX.md")
PREFLIGHT_OUT=$(mktemp "$SESSION_DIR/preflight-out-XXXXXXXX.md")

printf '%s\n' 'test' > "$PREFLIGHT_IN"

if ! codex exec \
  -m "$MODEL" \
  --config reasoning_effort=high \
  -s read-only \
  --ephemeral \
  --skip-git-repo-check \
  -o "$PREFLIGHT_OUT" \
  - < "$PREFLIGHT_IN" >/dev/null 2>&1; then
  echo "Codex exec failed. Check that codex is installed and $MODEL is accessible."
  echo "Install: npm install -g @openai/codex"
  exit 1
elif [ ! -s "$PREFLIGHT_OUT" ]; then
  echo "Codex returned empty output during preflight. Model may be unavailable."
  exit 1
fi
```

### Step 3: Write Plan File

Use the **Write tool** to write the current plan to `$PLAN_FILE`.

Using the Write tool avoids shell corruption from backticks, quotes, and shell fragments common in plan documents. Never use echo or heredoc for this.

If no plan exists in context, ask the user what to review before proceeding.

After writing, validate:

```bash
[ -s "$PLAN_FILE" ] || { echo "Plan file empty or missing. Cannot proceed."; exit 1; }
```

### Step 4: Send to Codex (Repeat Per Round)

Before sending, check the round cap:

```bash
if [ "$ROUND" -gt 5 ]; then
  # Go to Step 7: max rounds reached
fi
```

Compose input and call Codex. **Branch on `$ROUND`:**

**Round 1** — base review prompt:

```bash
INPUT_FILE=$(mktemp "$SESSION_DIR/input-XXXXXXXX.md")
OUT_FILE=$(mktemp "$SESSION_DIR/out-XXXXXXXX.md")

if [ "$ROUND" -eq 1 ]; then
{
  printf 'Review this implementation plan. Focus on:\n'
  printf '1. Correctness - Will this plan achieve the stated goals?\n'
  printf '2. Risks - What could go wrong? Edge cases? Data loss?\n'
  printf '3. Missing steps - Is anything forgotten?\n'
  printf '4. Alternatives - Is there a simpler or better approach?\n'
  printf '5. Security - Any security concerns?\n\n'
  printf 'Be specific and actionable.\n'
  printf '\nEnd your response with exactly one of these as the very last line:\n'
  printf 'VERDICT: APPROVED\n'
  printf 'VERDICT: REVISE\n\n'
  printf '--- PLAN ---\n'
  cat "$PLAN_FILE"
} > "$INPUT_FILE"
```

**Round 2+** — rebuttal prompt (built from `$STATE_FILE`; replaces the old free-form history block):

```bash
else
{
  printf 'You are collaboratively reviewing a plan with Claude.\n'
  printf 'Claude has addressed your previous concerns but respectfully contests some points.\n'
  printf 'Engage with Claude'\''s counter-arguments specifically — do not just re-state the original concern.\n'
  printf 'If Claude'\''s defense is sound, acknowledge it. If you still disagree, explain why more precisely.\n\n'
  printf 'Claude'\''s stance on your previous feedback:\n\n'
  printf '[ACCEPTED — revised in plan]\n'
  printf '[CONTESTED — Claude disagrees]\n'
  printf '[SKIPPED — conflicts with user requirement]\n'
  # Single pass: emit bullets grouped by status
  awk -F'\t' '
    $3=="ACCEPTED"  { accepted = accepted "- " $5 "\n" }
    $3=="CONTESTED" { contested = contested "- " $5 "\n" }
    $3=="SKIPPED"   { skipped = skipped "- " $5 "\n" }
    END {
      print "[ACCEPTED — revised in plan]"; printf "%s", accepted
      print "\n[CONTESTED — Claude disagrees]"; printf "%s", contested
      print "\n[SKIPPED — conflicts with user requirement]"; printf "%s", skipped
    }
  ' "$STATE_FILE"
  printf '\nEnd your response with exactly one of these as the very last line:\n'
  printf 'VERDICT: APPROVED\n'
  printf 'VERDICT: REVISE\n\n'
  printf '--- REVISED PLAN ---\n'
  cat "$PLAN_FILE"
} > "$INPUT_FILE"
fi

if ! codex exec \
  -m "$MODEL" \
  --config reasoning_effort=high \
  -s read-only \
  --ephemeral \
  --skip-git-repo-check \
  -o "$OUT_FILE" \
  - < "$INPUT_FILE" >/dev/null 2>&1; then
  echo "Codex exec failed (non-zero exit). Check model availability or network."
  exit 1
elif [ ! -s "$OUT_FILE" ]; then
  echo "Codex returned empty output. Cannot determine verdict."
  exit 1
fi

REVIEW=$(cat "$OUT_FILE")
```

**If debugging empty output:** Run without `-o "$OUT_FILE"` and examine lines containing `"type":"agent_message"`.

### Step 5: Read Review, Classify Concerns & Check Verdict

1. Present Codex's review:
   ```
   ## Codex Review — Round N (model: $MODEL)
   [Codex's feedback]
   ```
2. Extract verdict from the **actual last non-empty line** of the output:
   ```bash
   LAST_LINE=$(printf '%s' "$REVIEW" | awk 'NF{line=$0} END{print line}')
   case "$LAST_LINE" in
     'VERDICT: APPROVED') VERDICT='APPROVED' ;;
     'VERDICT: REVISE')   VERDICT='REVISE' ;;
     *)                   VERDICT='INCONCLUSIVE' ;;
   esac
   ```
3. **Classify each concern** before deciding what to do. For every distinct concern Codex raised, assign one of:

   | Label | Meaning | Action |
   |-------|---------|--------|
   | ACCEPTED | Concern is valid — plan should change | Revise the plan in Step 6 |
   | CONTESTED | Concern is debatable or assumes incorrect context | Formulate specific counter-argument |
   | SKIPPED | Concern conflicts with explicit user requirements | Note reason; if security/data-loss → blocking warning to human instead |

   Think critically: Is this concern actually valid? Is Codex assuming context it doesn't have? Does this contradict a design decision the user already approved?

   **Security/data-loss override:** If a concern would be `SKIPPED` but involves auth, data integrity, data loss, or credentials — do NOT silently skip. Surface to the human as a blocking warning: "Codex raised a security/data-loss concern that conflicts with requirement X. Confirm you want to proceed anyway." Wait for confirmation before continuing.

   Update `$STATE_FILE` with each concern: one TSV line per concern with fields: `concern_id`, `round_first_seen`, `status` (ACCEPTED/CONTESTED/SKIPPED/RESOLVED), `consecutive_contested`, `summary`.

4. Check verdict:
   - `APPROVED` → go to Step 7 (approved)
   - `REVISE` → go to Step 6
   - `INCONCLUSIVE` → present the review, note the missing verdict, go to Step 6 (counts as a round; do not update `consecutive_contested` for concerns — treat as a neutral round)

### Step 6: Debate-Aware Revise & Re-submit

1. **Tie-break check first:** Scan `$STATE_FILE` for any CONTESTED concern with `consecutive_contested >= 3`. If found → **stop the loop immediately**. Surface to the human:
   ```
   ## Tie-break reached
   The following concern has been CONTESTED for 3+ consecutive rounds without resolution:
   - [concern summary]
   Please decide: should this be accepted, skipped, or do you want to provide additional context?
   ```
   Wait for human input before continuing. Do NOT proceed to the next round autonomously.

2. **Revise the plan for ACCEPTED concerns only.** Do not touch CONTESTED or SKIPPED points.

3. **Write counter-arguments for CONTESTED concerns** — each must be specific and explain WHY Codex's concern may be misplaced (wrong assumption, incorrect context, conflicts with explicit decision). "I disagree" alone is not valid.

4. Update `$STATE_FILE`:
   - For concerns now ACCEPTED: update status, reset `consecutive_contested` to 0.
   - For concerns still CONTESTED: increment `consecutive_contested` by 1.
   - For concerns Codex explicitly conceded: mark status as RESOLVED; do not re-contest.

5. Use the **Write tool** to rewrite `$PLAN_FILE` with the revised plan.
6. Validate the rewritten file:
   ```bash
   [ -s "$PLAN_FILE" ] || { echo "Revised plan file empty or missing. Cannot proceed."; exit 1; }
   ```
7. Summarize to the user:
   ```
   ### Round N Summary
   **Accepted & revised:** [one bullet per ACCEPTED concern and how it was addressed]
   **Contested:** [one bullet per CONTESTED concern with Claude's counter-argument]
   **Skipped:** [one bullet per SKIPPED concern with reason]
   ```
8. Append one-line round summary to `$CONTEXT_FILE`:
   ```bash
   printf 'Round %s: %s\n' "$ROUND" "one-line summary of remaining open issues" >> "$CONTEXT_FILE"
   ```
9. Increment round counter and go back to Step 4:
   ```bash
   ROUND=$((ROUND + 1))
   ```

### Step 7: Done

Once approved or max rounds reached (the `trap` on `$SESSION_DIR` handles cleanup automatically):

**If approved:**
```
## Codex Review — Final (model: $MODEL)
**Status:** Approved after N round(s)
[Final approval message]
---
The plan has been reviewed and approved by Codex. Ready for implementation.
```

**If max rounds (5) reached:**
```
## Codex Review — Final (model: $MODEL)
**Status:** Max rounds (5) reached — not fully approved
**Remaining concerns:** [last line of $CONTEXT_FILE, i.e. the most recent round summary]
---
Codex still has concerns. Review remaining items and decide whether to proceed.
```

## Rules

- Claude actively revises the plan between rounds — not just forwarding messages
- Always use read-only sandbox mode (`-s read-only`) — Codex should never write files
- Always use `--ephemeral` — Codex should not write session files
- Max 5 review rounds — enforced by the `ROUND > 5` guard in Step 4
- Show the user each round's feedback and revisions
- Use a `trap` on `$SESSION_DIR` for cleanup — covers all exit paths including early failures
- Always use `if/elif` to check codex exec exit code and output file size separately
- Always check `[ -s "$PLAN_FILE" ]` before Step 4 AND after every plan rewrite in Step 6
- Use the Write tool (not echo/heredoc) for all plan file writes
- Use `printf` instead of `echo` for all shell output assembly
- Extract verdict using `awk 'NF{line=$0} END{print line}'` on the actual last non-empty output line, then `case`-match it exactly — never grep in the body
- Round history in `$CONTEXT_FILE` is one line per round, ≤200 chars, no newlines, no model output embedded
- Missing verdicts are INCONCLUSIVE, not approved
- "Remaining concerns" in the max-rounds output comes from `tail -1 "$CONTEXT_FILE"`
- If Codex CLI is not installed: `npm install -g @openai/codex`
- Claude is an active intellectual peer — evaluate each concern before accepting it
- Label every Codex concern as ACCEPTED, CONTESTED, or SKIPPED before revising anything
- Never silently implement a CONTESTED point — surface the disagreement to the user and to Codex
- 3-consecutive-contested tie-break stops the loop immediately; do not continue to round 4 or 5 autonomously
- When Codex explicitly acknowledges and concedes a counter-argument, mark that concern RESOLVED — do not keep re-contesting it
- A valid contest requires specific reasoning; "I disagree" alone is not sufficient — explain WHY Codex's concern may be misplaced
- SKIPPED concerns involving security, auth, data loss, or credentials are NEVER silent — always surface as blocking warnings to the human
- Plans sent to Codex should not contain secrets, credentials, tokens, or production hostnames — note this as a guidance reminder before sending
