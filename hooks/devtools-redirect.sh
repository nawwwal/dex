#!/usr/bin/env bash
# Gently remind Claude to prefer defuddle/WebFetch over Chrome DevTools for reading URLs
# Uses systemMessage (warning only) — does NOT block legitimate DevTools usage
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
ACTION=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); t=d.get('tool_input',{}); print(t.get('action',t.get('command','')))" 2>/dev/null || echo "")
URL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('url',''))" 2>/dev/null || echo "")

# Only fire on chrome devtools navigation to URLs (not screenshots, fills, or JS eval)
if echo "$TOOL_NAME" | grep -qi "chrome\|devtools\|browser"; then
  if [[ -n "$URL" ]] && echo "$ACTION" | grep -qi "navigate\|open\|goto"; then
    echo '{"systemMessage": "Reminder: For reading web pages/docs, prefer obsidian:defuddle (best for articles), WebFetch (for raw content), or WebSearch. Chrome DevTools is for screenshots, form fills, JS execution, and authenticated sessions only."}'
  fi
fi
