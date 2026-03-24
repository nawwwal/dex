#!/usr/bin/env bash
# Block git commit if: no verification signal OR no recent /simplify run
INPUT=$(cat)

COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Only run on git commit commands
if ! echo "$COMMAND" | grep -q 'git commit'; then
  exit 0
fi

# Skip check for merge commits — no new code to verify
if [[ -f "$(git rev-parse --git-dir 2>/dev/null)/MERGE_HEAD" ]]; then
  exit 0
fi

TRANSCRIPT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('transcript_path',''))" 2>/dev/null || echo "")

VERIFIED=0
SIMPLIFIED=0

if [[ -f "$TRANSCRIPT" ]]; then
  # Only match deliberate verification signals — specific phrases, not the word "verified" alone
  if grep -qi \
    "verification complete\|tests passed\|test pass\|npm test.*pass\|✓ all\|all tests pass\|agent_browser\|screenshot.*taken\|dogfood.*pass\|visual.*confirm\|checked.*browser\|looks good.*browser" \
    "$TRANSCRIPT" 2>/dev/null; then
    VERIFIED=1
  fi
  # /simplify must have been explicitly invoked
  if grep -qi \
    "Running /simplify\|/simplify.*complete\|simplify.*done\|code-simplifier\|simplify.*finished" \
    "$TRANSCRIPT" 2>/dev/null; then
    SIMPLIFIED=1
  fi
fi

# If transcript path was empty/missing, allow commit but warn
if [[ -z "$TRANSCRIPT" ]] || [[ ! -f "$TRANSCRIPT" ]]; then
  echo '{"systemMessage": "No transcript available to verify. Ensure you have verified changes visually and run /simplify."}'
  exit 0
fi

if [[ "$VERIFIED" -eq 0 ]]; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Verify changes with agent browser first. Take a screenshot or run tests, then commit."}}'
  exit 2
fi

if [[ "$SIMPLIFIED" -eq 0 ]]; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Run /simplify on changed files before committing to remove AI slop."}}'
  exit 2
fi

exit 0
