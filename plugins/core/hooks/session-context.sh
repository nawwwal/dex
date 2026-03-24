#!/bin/bash
# SessionStart hook: Lean context injection — target 25-40 lines output.
# Claude already loads CLAUDE.md files and project lessons automatically.
# This hook provides only signal-dense data not available elsewhere.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"')

MEMORY_DIR="$HOME/.claude/memory"
CLAUDE_DIR="$HOME/.claude"
TASKS_FILE="$HOME/.claude/TASKS.md"
LEARNINGS_QUEUE="$HOME/.claude/learnings-queue.json"
REGISTRY="$CLAUDE_DIR/config/project-registry.json"

# --- resolve_project ---
resolve_project() {
  local cwd="$1"
  [ ! -f "$REGISTRY" ] && return 1
  python3 -c "
import json, sys
cwd = sys.argv[1]
with open(sys.argv[2]) as f:
    registry = json.load(f)
for proj in registry['projects']:
    for alias in proj['aliases']:
        if alias in cwd:
            print(proj['name'])
            print(proj.get('slack', ''))
            print(proj.get('devrev', ''))
            sys.exit(0)
sys.exit(1)
" "$cwd" "$REGISTRY" 2>/dev/null
}

PROJECT_NAME=""
PROJECT_DEVREV=""
PROJECT_INFO=$(resolve_project "$CWD")
if [ $? -eq 0 ]; then
  PROJECT_NAME=$(echo "$PROJECT_INFO" | sed -n '1p')
  PROJECT_DEVREV=$(echo "$PROJECT_INFO" | sed -n '3p')
fi

DATE_TODAY=$(date '+%Y-%m-%d')

# --- /clear: minimal output ---
if [ "$SOURCE" = "clear" ]; then
  TASK_COUNT=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
  echo "Session cleared. Active tasks: $TASK_COUNT"
  [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ] && echo "Pending learnings — run /reflect"
  exit 0
fi

# --- Header (3-4 lines) ---
case "$SOURCE" in
  compact) LABEL="=== POST-COMPACT CONTEXT ===" ;;
  resume)  LABEL="=== RESUMED SESSION ===" ;;
  *)       LABEL="=== SESSION CONTEXT ===" ;;
esac
echo "$LABEL"
echo "CWD: $CWD | Date: $DATE_TODAY"
[ -n "$PROJECT_NAME" ] && echo "Project: $PROJECT_NAME${PROJECT_DEVREV:+ | DevRev: $PROJECT_DEVREV}"
echo ""

# --- Vault health (0-2 lines, only if issues) ---
HEALTH_FILE="$MEMORY_DIR/health.md"
if [ -f "$HEALTH_FILE" ]; then
  WARNINGS=$(python3 -c "
import re, sys
try:
    c = open(sys.argv[1]).read()
    m = re.search(r'warnings: (\d+)', c[:500])
    print(int(m.group(1)) if m else 0)
except: print(0)
" "$HEALTH_FILE" 2>/dev/null || echo 0)
  if [ "${WARNINGS:-0}" -gt 0 ] 2>/dev/null; then
    echo "⚠ Vault: ${WARNINGS} issues — see memory/health.md"
    echo ""
  fi
fi

# --- Active tasks (top 5, with count) ---
if [ -f "$TASKS_FILE" ]; then
  OPEN_TASKS=$(grep '^\- \[ \]' "$TASKS_FILE" 2>/dev/null | head -5)
  if [ -n "$OPEN_TASKS" ]; then
    TOTAL_OPEN=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
    echo "--- TASKS ($TOTAL_OPEN open) ---"
    echo "$OPEN_TASKS" | cut -c1-120
    [ "$TOTAL_OPEN" -gt 5 ] 2>/dev/null && echo "  ... $((TOTAL_OPEN - 5)) more — ~/.claude/TASKS.md"
    echo ""
  fi
fi

# --- Last session breadcrumb (2-3 lines max) ---
JOURNAL_DIR="$CLAUDE_DIR/log"
JOURNAL_PROJECT=$(git -C "$CWD" branch --show-current 2>/dev/null | sed 's|the user/||;s|/|-|g' | cut -c1-30)
if [[ -z "$JOURNAL_PROJECT" ]] || [[ "$JOURNAL_PROJECT" == "main" ]] || [[ "$JOURNAL_PROJECT" == "master" ]]; then
  JOURNAL_PROJECT=$(basename "$CWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-30)
fi
SESSION_FILE=$(find "$JOURNAL_DIR" -maxdepth 1 \( -name "*-${JOURNAL_PROJECT}-*-session.md" -o -name "*-${JOURNAL_PROJECT}-session.md" \) 2>/dev/null | sort -r | head -1)
if [ -n "$SESSION_FILE" ] && [ -f "$SESSION_FILE" ]; then
  BREADCRUMB=$(grep -v '^$\|^#\|^---' "$SESSION_FILE" | tail -3 | head -2)
  if [ -n "$BREADCRUMB" ]; then
    echo "--- LAST SESSION ---"
    echo "$BREADCRUMB"
    echo ""
  fi
fi

# --- Memory index (3 lines — pointer only) ---
DEC_COUNT=$(grep -c '^### ' "$MEMORY_DIR/decisions.md" 2>/dev/null || echo 0)
PAT_COUNT=$(grep -c '^### ' "$MEMORY_DIR/patterns.md" 2>/dev/null || echo 0)
LAST_DEC=$(grep '^### ' "$MEMORY_DIR/decisions.md" 2>/dev/null | tail -1 | sed 's/^### //')
echo "--- MEMORY ($DEC_COUNT decisions · $PAT_COUNT patterns) ---"
[ -n "$LAST_DEC" ] && echo "  Last: $LAST_DEC"
echo "  Search: qmd vsearch '<topic>' --collection memory"
echo ""

# --- Git state (2-3 lines) ---
if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
  DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h %s' 2>/dev/null)
  echo "--- GIT --- $BRANCH | uncommitted: $DIRTY"
  echo "  $LAST_COMMIT"
  echo ""
fi

# --- Time-sensitive alerts (deferred tasks + overdue reminders) ---
ALERTS=""

# Deferred tasks now due
if [ -f "$TASKS_FILE" ]; then
  IN_DEFERRED=false
  while IFS= read -r line; do
    [[ "$line" == "## Deferred (date-gated)"* ]] && IN_DEFERRED=true
    [[ "$IN_DEFERRED" == true ]] && [[ "$line" =~ ^"## " ]] && [[ "$line" != "## Deferred"* ]] && IN_DEFERRED=false
    if [[ "$IN_DEFERRED" == true ]] && [[ "$line" =~ "- [ ]" ]]; then
      ITEM_DATE=$(echo "$line" | grep -oE "\*\*[0-9]{4}-[0-9]{2}-[0-9]{2}\*\*" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      SNOOZE=$(echo "$line" | grep -oE "\(snooze: [0-9]{4}-[0-9]{2}-[0-9]{2}\)" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      if [[ -n "$ITEM_DATE" ]] && [[ ! "$ITEM_DATE" > "$DATE_TODAY" ]]; then
        if [[ -z "$SNOOZE" ]] || [[ ! "$SNOOZE" > "$DATE_TODAY" ]]; then
          TITLE=$(echo "$line" | sed 's/^- \[ \] \*\*[0-9-]*\*\* — //' | sed 's/ (snooze:.*//' | cut -c1-70)
          ALERTS="${ALERTS}⏰ Deferred ($ITEM_DATE): $TITLE\n"
        fi
      fi
    fi
  done < "$TASKS_FILE"
fi

# TCD warnings (≤3 days)
WARN_DATE=$(python3 -c "from datetime import date, timedelta; print((date.today()+timedelta(days=3)).strftime('%Y-%m-%d'))" 2>/dev/null)
if [ -f "$TASKS_FILE" ] && [ -n "$WARN_DATE" ]; then
  while IFS= read -r line; do
    if [[ "$line" =~ "TCD " ]] && [[ "$line" =~ "- [ ]" ]]; then
      PARSED=$(python3 -c "
from datetime import datetime
import re, sys
m = re.search(r'TCD ([A-Za-z]+ [0-9]+)', sys.argv[1])
if m:
  try: print(datetime.strptime('2026 ' + m.group(1), '%Y %b %d').strftime('%Y-%m-%d'))
  except: pass
" "$line" 2>/dev/null)
      if [[ -n "$PARSED" ]] && [[ ! "$PARSED" > "$WARN_DATE" ]] && [[ ! "$PARSED" < "$DATE_TODAY" ]]; then
        TITLE=$(echo "$line" | sed 's/^- \[ \] \*\*//' | sed 's/\*\*//' | sed 's/ — TCD.*//' | sed 's/ | \[.*//' | cut -c1-70)
        ALERTS="${ALERTS}⚠ TCD $PARSED: $TITLE\n"
      fi
    fi
  done < "$TASKS_FILE"
fi

# Overdue reminders
REMINDERS_FILE="$MEMORY_DIR/reminders.md"
if [ -f "$REMINDERS_FILE" ]; then
  CUR_DATE=""; CUR_TITLE=""
  while IFS= read -r line; do
    if [[ "$line" =~ ^"### "[0-9]{4}-[0-9]{2}-[0-9]{2}: ]]; then
      CUR_DATE=$(echo "$line" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      CUR_TITLE=$(echo "$line" | sed "s/### [0-9-]*: //")
    fi
    [[ "$line" == "Status: pending" ]] && [[ -n "$CUR_DATE" ]] && [[ ! "$CUR_DATE" > "$DATE_TODAY" ]] && ALERTS="${ALERTS}⏰ Reminder ($CUR_DATE): $CUR_TITLE\n"
  done < "$REMINDERS_FILE"
fi

if [ -n "$ALERTS" ]; then
  echo "--- ALERTS ---"
  printf "%b" "$ALERTS"
  echo ""
fi

# --- Pending learnings (0-1 line) ---
if [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ]; then
  Q=$(python3 -c "import json; d=json.load(open('$LEARNINGS_QUEUE')); print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo 0)
  if [ "${Q:-0}" != "0" ]; then
    echo "📚 $Q pending learnings — /reflect"
    echo ""
  fi
fi

# --- Morning mode (first session from home dir) ---
if [ "$CWD" = "$HOME" ] || [ "$CWD" = "$HOME/" ]; then
  echo "First session from ~/ — /assistant for morning briefing."
  echo ""
fi

echo "=== END | /assistant · /switch-project ==="
exit 0
