#!/usr/bin/env bash
# Write a minimal session note at session end if none exists for today
TODAY=$(date +%Y-%m-%d)
SESSIONS_DIR="$HOME/.claude/log"

# Get project from git branch or CWD (same derivation as session-context.sh reader)
PROJECT=$(git branch --show-current 2>/dev/null | sed 's|the user/||' | sed 's|/|-|g' | cut -c1-30)
if [[ -z "$PROJECT" ]] || [[ "$PROJECT" == "main" ]] || [[ "$PROJECT" == "master" ]]; then
  PROJECT=$(basename "$PWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-30)
fi

# Skip if running in a subagent context (no CLAUDE_SESSION_ID = subagent Stop, not main session)
# Subagent invocations were producing one stub file per subagent, overwhelming log/ with noise
if [[ -z "${CLAUDE_SESSION_ID}" ]]; then
  exit 0
fi

# Per-session deduplication: use CLAUDE_SESSION_ID
SESSION_KEY="${CLAUDE_SESSION_ID}"
# Truncate session key to 16 chars to keep filenames reasonable
SESSION_KEY="${SESSION_KEY:0:16}"

# Skip if this session already wrote a journal (any file matching this session key)
EXISTING=$(ls "$SESSIONS_DIR/"*"-${SESSION_KEY}-session.md" 2>/dev/null | head -1)

if [[ -z "$EXISTING" ]]; then
  OUTFILE="$SESSIONS_DIR/${TODAY}T$(date +%H%M)-${PROJECT}-${SESSION_KEY}-session.md"
  {
    echo "---"
    echo "date: ${TODAY}"
    echo "project: ${PROJECT}"
    echo "type: session"
    echo "---"
    echo ""
    echo "# Session: ${PROJECT} — ${TODAY}"
    echo ""
    echo "## Git log (last 10)"
    git log --oneline -10 2>/dev/null || echo "(no git)"
    echo ""
    echo "## Changed files"
    git status --short 2>/dev/null || echo "(no git)"
    echo ""
    echo "## Notes"
    echo "<!-- Fill in: what was accomplished, decisions made, next steps -->"
  } > "$OUTFILE"
fi

# --- Design + Interpersonal TIL prompt ---
# Soft reminder if no non-engineering TIL was captured this month
MONTH=$(date +%Y-%m)
LEARN_DIR="$HOME/.claude/learn"
DESIGN_COUNT=$(find "${LEARN_DIR}" -maxdepth 1 -name "design-${MONTH}-*.md" 2>/dev/null | wc -l | tr -d ' ')
PEOPLE_COUNT=$(find "${LEARN_DIR}" -maxdepth 1 -name "people-${MONTH}-*.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "${DESIGN_COUNT:-0}" = "0" ] || [ "${PEOPLE_COUNT:-0}" = "0" ]; then
  MISSING=""
  [ "${DESIGN_COUNT:-0}" = "0" ] && MISSING="design thinking"
  [ "${PEOPLE_COUNT:-0}" = "0" ] && MISSING="${MISSING:+${MISSING} + }interpersonal"
  echo "TIL: No ${MISSING} TIL this month. Anything from today worth capturing? (learn/design-YYYY-MM-DD-slug.md or learn/people-YYYY-MM-DD-slug.md)"
fi

exit 0
