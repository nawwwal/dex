#!/usr/bin/env bash
# Keep /resume context lean: point Claude to the right sources instead of inlining them.
INPUT=$(cat)
MSG=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt',''))" 2>/dev/null || echo "")

if echo "$MSG" | grep -q '/resume'; then
  CONTEXT="Resume requested. Ask what changed since the last session before taking action. If more context is needed, read the latest compact summary or project breadcrumb directly instead of relying on injected summaries."
  python3 -c "import json, sys; print(json.dumps({'additionalContext': sys.argv[1]}))" "$CONTEXT"
fi
