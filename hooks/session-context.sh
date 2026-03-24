#!/bin/bash
# SessionStart hook: Restore context from all relevant places.
# Reads Obsidian session logs, memory files, TASKS.md, and project CLAUDE.md
# so that sessions starting after a compaction have full context.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"')

MEMORY_DIR="$HOME/.claude/memory"
CLAUDE_DIR="$HOME/.claude"
SESSIONS_DIR="$CLAUDE_DIR/sessions"
REGISTRY="$CLAUDE_DIR/config/project-registry.json"
TASKS_FILE="$HOME/.claude/TASKS.md"
LEARNINGS_QUEUE="$HOME/.claude/learnings-queue.json"

# --- resolve_project: look up CWD against project-registry.json ---
resolve_project() {
  local cwd="$1"
  if [ ! -f "$REGISTRY" ]; then
    return 1
  fi
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

# Resolve project from CWD
PROJECT_NAME=""
PROJECT_SLACK=""
PROJECT_DEVREV=""
PROJECT_INFO=$(resolve_project "$CWD")
if [ $? -eq 0 ]; then
  PROJECT_NAME=$(echo "$PROJECT_INFO" | sed -n '1p')
  PROJECT_SLACK=$(echo "$PROJECT_INFO" | sed -n '2p')
  PROJECT_DEVREV=$(echo "$PROJECT_INFO" | sed -n '3p')
fi

# --- /clear: minimal output ---
if [ "$SOURCE" = "clear" ]; then
  TASK_COUNT=0
  if [ -f "$TASKS_FILE" ]; then
    TASK_COUNT=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
  fi
  echo "Session cleared. Active tasks: $TASK_COUNT"
  # Pending learnings alert
  if [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ]; then
    QUEUE_DATA_C=$(python3 -c "
import json
try:
    with open('$LEARNINGS_QUEUE') as f:
        d = json.load(f)
    if not isinstance(d, list): d = []
    total = len(d)
    ro = sum(1 for x in d if x.get('type') == 'reflect-others' and x.get('status') == 'pending')
    print(f'{total} {ro}')
except:
    print('0 0')
" 2>/dev/null || echo "0 0")
    read -r QUEUE_ITEMS_C REFLECT_OTHERS_C <<< "$QUEUE_DATA_C"
    if [ "${QUEUE_ITEMS_C:-0}" != "0" ]; then
      echo "Pending learnings — run /reflect to process"
    fi
    if [ "${REFLECT_OTHERS_C:-0}" != "0" ]; then
      echo "${REFLECT_OTHERS_C} reflect-others candidate(s) pending — run /reflect-others to review and confirm."
    fi
  fi
  exit 0
fi

DATE_TODAY=$(date '+%Y-%m-%d')
DATE_YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d yesterday '+%Y-%m-%d' 2>/dev/null)

ENCODED_PATH=$(echo "$CWD" | sed 's|/|-|g')
PROJECT_MEMORY="$HOME/.claude/projects/$ENCODED_PATH/CLAUDE.md"

# --- Output header ---
case "$SOURCE" in
  compact) CONTEXT_LABEL="=== POST-COMPACT CONTEXT RESTORED ===" ;;
  resume)  CONTEXT_LABEL="=== RESUMED SESSION CONTEXT ===" ;;
  *)       CONTEXT_LABEL="=== SESSION CONTEXT ===" ;;
esac

echo "$CONTEXT_LABEL"
echo "CWD: $CWD"
echo "Date: $DATE_TODAY"
echo "Session source: $SOURCE"
if [ -n "$PROJECT_NAME" ]; then
  echo "Project: $PROJECT_NAME"
  [ -n "$PROJECT_DEVREV" ] && echo "DevRev: $PROJECT_DEVREV"
  [ -n "$PROJECT_SLACK" ] && echo "Slack: $PROJECT_SLACK"
fi
echo ""

# --- 0. Vault health warnings + memory hygiene reminders ---
# Single health.md read covers both sections
HEALTH_FILE="$MEMORY_DIR/health.md"
if [ -f "$HEALTH_FILE" ]; then
  HEALTH_OUTPUT=$(python3 - <<'PYEOF'
import re, sys
try:
    content = open(sys.argv[1]).read()
    # Warning count
    m = re.search(r'warnings: (\d+)', content[:500])
    warnings = int(m.group(1)) if m else 0
    # Confirm-required stale rows
    rows = re.findall(r'\| (\S+\.md) \| [0-9-]+ \| STALE[^|]* \| ([^|]+) \| confirm-required \|', content)
    sys.stdout.write(f'WARNINGS={warnings}\n')
    for fname, action in rows:
        sys.stdout.write(f'HYGIENE:{fname} -> {action.strip()}\n')
except Exception:
    sys.stdout.write('WARNINGS=0\n')
PYEOF
  "$HEALTH_FILE" 2>/dev/null)

  HEALTH_WARNINGS=$(echo "$HEALTH_OUTPUT" | grep '^WARNINGS=' | cut -d= -f2)
  HYGIENE_REMINDERS=$(echo "$HEALTH_OUTPUT" | grep '^HYGIENE:' | sed 's/^HYGIENE:/  /')

  if [ "${HEALTH_WARNINGS:-0}" -gt 0 ] 2>/dev/null; then
    echo "--- VAULT HEALTH (${HEALTH_WARNINGS} issues) ---"
    grep -E "STALE|MISSING|NEEDED|NOT RUN|\[FAIL\]|\[PERSISTENT\]" "$HEALTH_FILE" | head -12
    echo "(Full report: memory/health.md)"
    echo ""
  fi
  if [ -n "$HYGIENE_REMINDERS" ]; then
    echo "--- MEMORY HYGIENE (when you have time) ---"
    echo "$HYGIENE_REMINDERS"
    echo ""
  fi
fi

# --- 0c. Safe-auto directive (Section B — only when pending-updates.json is non-empty) ---
PENDING_UPDATES_FILE="$MEMORY_DIR/pending-updates.json"
if [ -f "$PENDING_UPDATES_FILE" ] && [ -s "$PENDING_UPDATES_FILE" ]; then
  SAFE_AUTO_ITEMS=$(python3 -c "
import json
try:
    entries = json.load(open('$PENDING_UPDATES_FILE'))
    if not isinstance(entries, list): entries = []
    for e in entries:
        variant = e.get('variant', '')
        reason = e.get('reason', '')
        if variant and reason:
            print('  /' + variant + '   (' + reason + ')')
except:
    pass
" 2>/dev/null)
  if [ -n "$SAFE_AUTO_ITEMS" ]; then
    echo "--- SESSION HYGIENE: local refresh ready ---"
    echo "$SAFE_AUTO_ITEMS"
    echo ""
  fi
fi

# --- 1. Recent session log (from ~/.claude/log/, project-filtered) ---
# Derive project slug matching write-session-note.sh's PROJECT derivation
JOURNAL_DIR="$CLAUDE_DIR/log"
JOURNAL_PROJECT=$(git -C "$CWD" branch --show-current 2>/dev/null | sed 's|the user/||' | sed 's|/|-|g' | cut -c1-30)
if [[ -z "$JOURNAL_PROJECT" ]] || [[ "$JOURNAL_PROJECT" == "main" ]] || [[ "$JOURNAL_PROJECT" == "master" ]]; then
  JOURNAL_PROJECT=$(basename "$CWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-30)
fi

SESSION_FILE=""
# Find most recent *-session.md matching this project slug (last 7 days)
if [ -n "$JOURNAL_PROJECT" ] && [ -d "$JOURNAL_DIR" ]; then
  SESSION_FILE=$(find "$JOURNAL_DIR" -maxdepth 1 -name "*-${JOURNAL_PROJECT}-*-session.md" -o -name "*-${JOURNAL_PROJECT}-session.md" 2>/dev/null \
    | sort -r | head -1)
fi
# No global fallback — never inject another project's journal

if [ -n "$SESSION_FILE" ] && [ -f "$SESSION_FILE" ]; then
  echo "--- LAST SESSION NOTES ($(basename "$SESSION_FILE")) ---"
  tail -40 "$SESSION_FILE"
  # Stub detection: warn if journal is thin (< 20 lines)
  LINE_COUNT=$(wc -l < "$SESSION_FILE" | tr -d ' ')
  if [ "${LINE_COUNT:-0}" -lt 20 ] 2>/dev/null; then
    echo ""
    echo "Warning: last session journal is a stub. Run /log eod to synthesize before starting new work."
  fi
  echo ""
fi

# --- 2. Project CLAUDE.md ---
if [ -f "$PROJECT_MEMORY" ]; then
  echo "--- PROJECT MEMORY ($PROJECT_MEMORY) ---"
  cat "$PROJECT_MEMORY"
  echo ""
elif [ -f "$CWD/CLAUDE.md" ]; then
  echo "--- PROJECT CLAUDE.md ---"
  cat "$CWD/CLAUDE.md"
  echo ""
fi

# --- 3. TASKS.md highlights (first 10 uncompleted tasks) ---
if [ -f "$TASKS_FILE" ]; then
  OPEN_TASKS=$(grep '^\- \[ \]' "$TASKS_FILE" 2>/dev/null | head -10)
  if [ -n "$OPEN_TASKS" ]; then
    TOTAL_OPEN=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
    echo "--- ACTIVE TASKS ($TOTAL_OPEN open) ---"
    echo "$OPEN_TASKS"
    if [ "$TOTAL_OPEN" -gt 10 ] 2>/dev/null; then
      echo "... and $((TOTAL_OPEN - 10)) more"
    fi
    echo ""
  fi
fi

# --- 4. Project lessons ---
if [ -f "$CWD/.claude/lessons.md" ]; then
  echo "--- PROJECT LESSONS ---"
  cat "$CWD/.claude/lessons.md"
  echo ""
fi

# --- 5. Recent decisions (last 5 entries) ---
DECISIONS_FILE="$MEMORY_DIR/decisions.md"
if [ -f "$DECISIONS_FILE" ]; then
  echo "--- RECENT DECISIONS (last 5) ---"
  START_LINE=$(grep -n '^### ' "$DECISIONS_FILE" 2>/dev/null \
    | tail -5 | head -1 | cut -d: -f1)
  if [ -n "$START_LINE" ]; then
    tail -n +"$START_LINE" "$DECISIONS_FILE" | head -100
  else
    tail -80 "$DECISIONS_FILE"
  fi
  echo ""
fi

# --- 6. Patterns (always load — prevents repeat mistakes) ---
PATTERNS_FILE="$MEMORY_DIR/patterns.md"
if [ -f "$PATTERNS_FILE" ]; then
  echo "--- PATTERNS & CORRECTIONS ---"
  cat "$PATTERNS_FILE"
  echo ""
fi

# --- 6b. QMD Semantic Filtering — inject project-relevant entries ---
QMD_PROJECT_NAME=""
# Try git branch first
if git -C "$CWD" rev-parse --git-dir &>/dev/null 2>&1; then
  QMD_PROJECT_NAME=$(git -C "$CWD" branch --show-current 2>/dev/null | sed 's|the user/||' | sed 's|/| |g' | cut -c1-40)
fi
# Fallback to directory name
if [[ -z "$QMD_PROJECT_NAME" ]]; then
  QMD_PROJECT_NAME=$(basename "$CWD" 2>/dev/null)
fi

if [[ -n "$QMD_PROJECT_NAME" ]] && command -v qmd &>/dev/null; then
  QMD_CONTEXT=$(qmd vsearch --query "$QMD_PROJECT_NAME" --collection memory --limit 5 2>/dev/null | head -40)
  if [[ -n "$QMD_CONTEXT" ]]; then
    echo ""
    echo "--- Relevant Memory (QMD semantic match for: $QMD_PROJECT_NAME) ---"
    echo "$QMD_CONTEXT"
  fi
fi

# --- 7. Active projects summary ---
PROJECTS_FILE="$MEMORY_DIR/projects.md"
if [ -f "$PROJECTS_FILE" ]; then
  echo "--- ACTIVE PROJECTS ---"
  cat "$PROJECTS_FILE"
  echo ""
fi

# --- 8. Git state if in a repo ---
if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
  DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h %s' 2>/dev/null)
  echo "--- GIT STATE ---"
  echo "Branch: $BRANCH | Uncommitted: $DIRTY files"
  echo "Last commit: $LAST_COMMIT"
  echo ""
fi

# --- 9. Pending learnings + reflect-others alert ---
if [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ]; then
  QUEUE_DATA=$(python3 -c "
import json
try:
    with open('$LEARNINGS_QUEUE') as f:
        d = json.load(f)
    if not isinstance(d, list): d = []
    total = len(d)
    reflect_others = sum(1 for x in d if x.get('type') == 'reflect-others' and x.get('status') == 'pending')
    print(f'{total} {reflect_others}')
except:
    print('0 0')
" 2>/dev/null || echo "0 0")
  read -r QUEUE_ITEMS REFLECT_OTHERS_PENDING <<< "$QUEUE_DATA"

  if [ "${QUEUE_ITEMS:-0}" != "0" ]; then
    echo "Pending learnings — run /reflect to process"
    echo ""
  fi
  if [ "${REFLECT_OTHERS_PENDING:-0}" != "0" ]; then
    echo "${REFLECT_OTHERS_PENDING} reflect-others candidate(s) pending — run /reflect-others to review and confirm."
    echo ""
  fi
fi

# --- Morning mode detection ---
if [ "$CWD" = "$HOME" ] || [ "$CWD" = "$HOME/" ]; then
  SESSIONS_TODAY=$(find "$SESSIONS_DIR" -maxdepth 1 -name "${DATE_TODAY}*.md" -not -name "session-compact-*" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$SESSIONS_TODAY" = "0" ]; then
    echo ""
    echo "First session today — run /assistant for your morning briefing."
  else
    echo ""
    echo "Run /assistant for help with priorities, communication, or context."
  fi
fi

# --- TASKS.md Deferred section: surface date-gated items ---
TASKS_FILE="$HOME/.claude/TASKS.md"
if [ -f "$TASKS_FILE" ]; then
  IN_DEFERRED=false
  DEFERRED_DUE=""
  while IFS= read -r line; do
    if [[ "$line" == "## Deferred (date-gated)"* ]]; then
      IN_DEFERRED=true
    elif [[ "$IN_DEFERRED" == true ]] && [[ "$line" =~ ^"## " ]]; then
      IN_DEFERRED=false
    fi
    if [[ "$IN_DEFERRED" == true ]]; then
      ITEM_DATE=$(echo "$line" | grep -oE "\*\*[0-9]{4}-[0-9]{2}-[0-9]{2}\*\*" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      if [[ -n "$ITEM_DATE" ]] && [[ ! "$ITEM_DATE" > "$DATE_TODAY" ]]; then
        ITEM_TITLE=$(echo "$line" | sed 's/^- \[ \] \*\*[0-9-]*\*\* — //' | sed 's/ (snooze:.*)//')
        SNOOZE_DATE=$(echo "$line" | grep -oE "\(snooze: [0-9]{4}-[0-9]{2}-[0-9]{2}\)" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
        if [[ -z "$SNOOZE_DATE" ]]; then
          DEFERRED_DUE="${DEFERRED_DUE}⏰ (${ITEM_DATE}): ${ITEM_TITLE}\n"
        elif [[ ! "$SNOOZE_DATE" > "$DATE_TODAY" ]]; then
          DEFERRED_DUE="${DEFERRED_DUE}⏰ (${ITEM_DATE}) [snoozed, now due]: ${ITEM_TITLE}\n"
        fi
      fi
    fi
  done < "$TASKS_FILE"

  if [ -n "$DEFERRED_DUE" ]; then
    echo ""
    echo "--- DEFERRED TASKS DUE ---"
    printf "%b" "$DEFERRED_DUE"
    echo ""
    echo "Move to ## Todo or ## In Progress. Snooze: add '(snooze: YYYY-MM-DD)' to the line."
  fi

  # --- TCD early warning: tasks due in ≤ 3 days ---
  WARN_DATE=$(python3 -c "from datetime import date, timedelta; print((date.today()+timedelta(days=3)).strftime('%Y-%m-%d'))" 2>/dev/null)
  if [[ -n "$WARN_DATE" ]]; then
    TCD_WARNINGS=""
    while IFS= read -r line; do
      if [[ "$line" =~ "TCD " ]] && [[ "$line" =~ "- [ ]" ]]; then
        PARSED=$(python3 -c "
from datetime import datetime
import re, sys
m = re.search(r'TCD ([A-Za-z]+ [0-9]+)', sys.argv[1])
if m:
  try:
    d = datetime.strptime('2026 ' + m.group(1), '%Y %b %d')
    print(d.strftime('%Y-%m-%d'))
  except: pass
" "$line" 2>/dev/null)
        if [[ -n "$PARSED" ]] && [[ ! "$PARSED" > "$WARN_DATE" ]] && [[ ! "$PARSED" < "$DATE_TODAY" ]]; then
          TITLE=$(echo "$line" | sed 's/^- \[ \] \*\*//' | sed 's/\*\*//' | sed 's/ — TCD.*//' | sed 's/ | \[.*//')
          TCD_WARNINGS="${TCD_WARNINGS}⚠️  TCD ${PARSED}: ${TITLE}\n"
        fi
      fi
    done < "$TASKS_FILE"
    if [ -n "$TCD_WARNINGS" ]; then
      echo ""
      echo "--- TCD APPROACHING (≤3 days) ---"
      printf "%b" "$TCD_WARNINGS"
    fi
  fi
fi

# --- Reminders.md: surface overdue items (for genuine conditional checks) ---
REMINDERS_FILE="$CLAUDE_DIR/memory/reminders.md"
if [ -f "$REMINDERS_FILE" ]; then
  OVERDUE=""
  CURRENT_DATE=""
  CURRENT_TITLE=""
  while IFS= read -r line; do
    if [[ "$line" =~ ^"### "[0-9]{4}-[0-9]{2}-[0-9]{2}: ]]; then
      CURRENT_DATE=$(echo "$line" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      CURRENT_TITLE=$(echo "$line" | sed "s/### [0-9-]*: //")
    fi
    # Status: pending
    if [[ "$line" == "Status: pending" ]] && [[ -n "$CURRENT_DATE" ]] && [[ ! "$CURRENT_DATE" > "$DATE_TODAY" ]]; then
      OVERDUE="${OVERDUE}⏰ (${CURRENT_DATE}): ${CURRENT_TITLE}\n"
    fi
    # Status: snoozed-to: YYYY-MM-DD (snooze expired)
    SNOOZE_DATE=$(echo "$line" | grep -oE "snoozed-to: [0-9]{4}-[0-9]{2}-[0-9]{2}" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
    if [[ -n "$SNOOZE_DATE" ]] && [[ -n "$CURRENT_DATE" ]] && [[ ! "$SNOOZE_DATE" > "$DATE_TODAY" ]]; then
      OVERDUE="${OVERDUE}⏰ (${CURRENT_DATE}) [snoozed, now due]: ${CURRENT_TITLE}\n"
    fi
  done < "$REMINDERS_FILE"

  if [ -n "$OVERDUE" ]; then
    echo ""
    echo "--- REMINDERS DUE ---"
    printf "%b" "$OVERDUE"
    echo ""
    echo "Mark done: edit ~/.claude/memory/reminders.md → Status: done"
  fi
fi

echo "=== END SESSION CONTEXT ==="
echo "Commands: /assistant (personal assistant), /briefing (workspace), /switch-project (change context)"

exit 0
