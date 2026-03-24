#!/usr/bin/env bash
# Enrich short messages to prevent context-free one-liners
INPUT=$(cat)
MSG_LEN=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('prompt','')))" 2>/dev/null || echo "100")
MSG=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt',''))" 2>/dev/null || echo "")
WORD_COUNT=$(printf '%s' "$MSG" | awk '{print NF}')

# Skip unless the prompt is extremely short and ambiguous.
if [[ "$MSG" == /* ]] || [[ -z "$MSG" ]] || [[ "$MSG_LEN" -ge 10 ]] || [[ "$WORD_COUNT" -gt 2 ]] || [[ "$MSG" =~ [[:punct:]] ]]; then
  exit 0
fi

echo '{"additionalContext": "Short prompt may be ambiguous. Clarify whether the user wants to continue the previous task or start something new."}'
