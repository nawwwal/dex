#!/usr/bin/env bash
# Enrich bare continuation messages to force explicit intent declaration
INPUT=$(cat)
MSG=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt','').strip().lower())" 2>/dev/null || echo "")

# Match bare continuation words (with optional punctuation)
if echo "$MSG" | grep -qxE '(continue|yes|proceed|done|next|go|okay|ok|sure|yep|yup)[.!?]?'; then
  echo '{"additionalContext": "User approved continuation without specifying direction. Before executing: declare your top 2 planned actions and ask if the user wants to skip or reprioritize anything. Wait for confirmation before proceeding."}'
fi
