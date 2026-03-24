#!/usr/bin/env bash
# Enforce structured response on frustration signals
INPUT=$(cat)
MSG=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt','').lower())" 2>/dev/null || echo "")

FRUSTRATION_PATTERN='bullshit|what the|this is wrong|still wrong|revert|start over|terrible|not working again|same issue|keeps breaking|why is this|wtf|what happened|broke again'

if echo "$MSG" | grep -qE "$FRUSTRATION_PATTERN"; then
  echo '{"additionalContext": "User is frustrated. MANDATORY response structure before anything else: (1) What failed: [specific mechanism that broke] (2) Why it failed: [root cause, not symptom] (3) One targeted fix: [single precise change]. Do NOT suggest a complete restart unless you can explain specifically why the current approach cannot work. No apologies, no long preambles — go straight to the structured analysis."}'
fi
