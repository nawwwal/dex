#!/bin/bash
# SessionStart hook: restore only the highest-signal session context.
# Keep startup context lean: summarize files and counts, never dump whole files.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
SOURCE=$(echo "$INPUT" | jq -r '.source // "startup"')

MEMORY_DIR="$HOME/.claude/memory"
CLAUDE_DIR="$HOME/.claude"
SESSIONS_DIR="$CLAUDE_DIR/sessions"
REGISTRY="$CLAUDE_DIR/config/project-registry.json"
TASKS_FILE="$HOME/.claude/TASKS.md"
LEARNINGS_QUEUE="$HOME/.claude/learnings-queue.json"

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

print_recent_titles() {
  local file="$1"
  local limit="$2"
  local prefix="$3"
  if [ -f "$file" ]; then
    grep '^### ' "$file" 2>/dev/null | tail -"$limit" | sed "s/^### /$prefix/"
  fi
}

PROJECT_NAME=""
PROJECT_SLACK=""
PROJECT_DEVREV=""
PROJECT_INFO=$(resolve_project "$CWD")
if [ $? -eq 0 ]; then
  PROJECT_NAME=$(echo "$PROJECT_INFO" | sed -n '1p')
  PROJECT_SLACK=$(echo "$PROJECT_INFO" | sed -n '2p')
  PROJECT_DEVREV=$(echo "$PROJECT_INFO" | sed -n '3p')
fi

if [ "$SOURCE" = "clear" ]; then
  TASK_COUNT=0
  if [ -f "$TASKS_FILE" ]; then
    TASK_COUNT=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
  fi
  echo "Session cleared. Active tasks: $TASK_COUNT"
  exit 0
fi

DATE_TODAY=$(date '+%Y-%m-%d')
ENCODED_PATH=$(echo "$CWD" | sed 's|/|-|g')
PROJECT_MEMORY="$HOME/.claude/projects/$ENCODED_PATH/CLAUDE.md"
PROJECT_CONTEXT_FILE=""
PROJECT_KEY=$(echo "$CWD" | tr '/[:space:]' '--' | tr -cd '[:alnum:]._-' | sed 's/--*/-/g; s/^-//; s/-$//' | cut -c1-120)
[ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"
COMPACT_FILE="$SESSIONS_DIR/session-compact-${PROJECT_KEY}.md"

if [ -f "$PROJECT_MEMORY" ]; then
  PROJECT_CONTEXT_FILE="$PROJECT_MEMORY"
elif [ -f "$CWD/CLAUDE.md" ]; then
  PROJECT_CONTEXT_FILE="$CWD/CLAUDE.md"
fi

case "$SOURCE" in
  compact) CONTEXT_LABEL="=== COMPACT ===" ;;
  resume)  CONTEXT_LABEL="=== RESUMED SESSION CONTEXT ===" ;;
  *)       CONTEXT_LABEL="=== SESSION CONTEXT ===" ;;
esac

if [ "$SOURCE" = "compact" ]; then
  echo "$CONTEXT_LABEL"
  echo "Repo: $(basename "$CWD")"
  [ -n "$PROJECT_NAME" ] && echo "Project: $PROJECT_NAME"

  if [ -f "$COMPACT_FILE" ]; then
    if grep -q "<!-- Claude:" "$COMPACT_FILE" 2>/dev/null; then
      echo "Snapshot: pending"
    else
      echo "Snapshot: ready"
    fi
  fi

  if [ -n "$PROJECT_CONTEXT_FILE" ]; then
    if [ "$PROJECT_CONTEXT_FILE" = "$CWD/CLAUDE.md" ]; then
      echo "Context: CLAUDE.md"
    else
      echo "Context: project memory"
    fi
  fi

  if [ -f "$TASKS_FILE" ]; then
    TOTAL_OPEN=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
    if [ "${TOTAL_OPEN:-0}" -gt 0 ] 2>/dev/null; then
      echo "Tasks: $TOTAL_OPEN open"
    fi
  fi

  if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
    BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
    DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h' 2>/dev/null)
    GIT_LINE="Git: $BRANCH, $DIRTY dirty"
    [ -n "$LAST_COMMIT" ] && GIT_LINE="$GIT_LINE, $LAST_COMMIT"
    echo "$GIT_LINE"
  fi

  exit 0
fi

echo "$CONTEXT_LABEL"
echo "CWD: $CWD"
echo "Date: $DATE_TODAY"
echo "Session source: $SOURCE"
if [ -n "$PROJECT_NAME" ]; then
  echo "Project: $PROJECT_NAME"
fi
echo ""

HEALTH_FILE="$MEMORY_DIR/health.md"
if [ -f "$HEALTH_FILE" ]; then
  HEALTH_WARNINGS=$(grep -m1 -oE 'warnings: [0-9]+' "$HEALTH_FILE" | awk '{print $2}')
  if [ "${HEALTH_WARNINGS:-0}" -gt 0 ] 2>/dev/null; then
    echo "--- VAULT HEALTH (${HEALTH_WARNINGS} issues) ---"
    echo "See $HEALTH_FILE"
    echo ""
  fi
fi

PENDING_UPDATES_FILE="$MEMORY_DIR/pending-updates.json"
if [ -f "$PENDING_UPDATES_FILE" ] && [ -s "$PENDING_UPDATES_FILE" ]; then
  SAFE_AUTO_ITEMS=$(python3 -c "
import json
try:
    entries = json.load(open('$PENDING_UPDATES_FILE'))
    if not isinstance(entries, list):
        entries = []
    for e in entries[:2]:
        variant = e.get('variant', '')
        reason = e.get('reason', '')
        if variant and reason:
            print('/' + variant + ' (' + reason + ')')
except:
    pass
" 2>/dev/null)
  if [ -n "$SAFE_AUTO_ITEMS" ]; then
    echo "--- SESSION HYGIENE ---"
    echo "$SAFE_AUTO_ITEMS"
    echo ""
  fi
fi

JOURNAL_DIR="$CLAUDE_DIR/log"
JOURNAL_PROJECT=$(git -C "$CWD" branch --show-current 2>/dev/null | sed 's|the user/||' | sed 's|/|-|g' | cut -c1-30)
if [[ -z "$JOURNAL_PROJECT" ]] || [[ "$JOURNAL_PROJECT" == "main" ]] || [[ "$JOURNAL_PROJECT" == "master" ]]; then
  JOURNAL_PROJECT=$(basename "$CWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-30)
fi

SESSION_FILE=""
if [ -n "$JOURNAL_PROJECT" ] && [ -d "$JOURNAL_DIR" ]; then
  SESSION_FILE=$(find "$JOURNAL_DIR" -maxdepth 1 \( -name "*-${JOURNAL_PROJECT}-*-session.md" -o -name "*-${JOURNAL_PROJECT}-session.md" \) 2>/dev/null | sort -r | head -1)
fi

if [ -n "$SESSION_FILE" ] && [ -f "$SESSION_FILE" ]; then
  SESSION_LINES=$(wc -l < "$SESSION_FILE" | tr -d ' ')
  echo "--- LAST SESSION NOTE ---"
  echo "$(basename "$SESSION_FILE") (${SESSION_LINES} lines)"
  if [ "${SESSION_LINES:-0}" -lt 20 ] 2>/dev/null; then
    echo "Stub note detected - run /assistant eod if you need a proper recap."
  fi
  echo ""
fi

if [ -n "$PROJECT_CONTEXT_FILE" ]; then
  CONTEXT_TITLE=$(grep -m1 '^# ' "$PROJECT_CONTEXT_FILE" 2>/dev/null | sed 's/^# //')
  echo "--- PROJECT CONTEXT ---"
  echo "$PROJECT_CONTEXT_FILE${CONTEXT_TITLE:+ - $CONTEXT_TITLE}"
  echo "Open the file directly or run /briefing if deeper context is needed."
  echo ""
fi

if [ -f "$TASKS_FILE" ]; then
  OPEN_TASKS=$(python3 - "$TASKS_FILE" <<'PYEOF' 2>/dev/null
import re
import sys

items = []
with open(sys.argv[1]) as f:
    for line in f:
        if not line.startswith("- [ ] "):
            continue
        text = line[6:].strip()
        text = text.split(" | ")[0]
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = text.replace(chr(96), "")
        if len(text) > 90:
            text = text[:87].rstrip() + "..."
        items.append(text)
        if len(items) == 2:
            break
print("\n".join(items))
PYEOF
)
  if [ -n "$OPEN_TASKS" ]; then
    TOTAL_OPEN=$(grep -c '^\- \[ \]' "$TASKS_FILE" 2>/dev/null || echo 0)
    echo "--- ACTIVE TASKS ($TOTAL_OPEN open) ---"
    echo "$OPEN_TASKS"
    [ "${TOTAL_OPEN:-0}" -gt 2 ] 2>/dev/null && echo "... and $((TOTAL_OPEN - 2)) more"
    echo ""
  fi
fi

if [ -f "$CWD/.claude/lessons.md" ]; then
  echo "--- PROJECT LESSONS ---"
  LESSON_TITLES=$(print_recent_titles "$CWD/.claude/lessons.md" 3 "- ")
  if [ -n "$LESSON_TITLES" ]; then
    echo "$LESSON_TITLES"
  else
    echo "$CWD/.claude/lessons.md"
  fi
  echo ""
fi

DECISIONS_FILE="$MEMORY_DIR/decisions.md"
if [ -f "$DECISIONS_FILE" ]; then
  DEC_COUNT=$(grep -c '^### ' "$DECISIONS_FILE" 2>/dev/null || echo 0)
  echo "--- RECENT DECISIONS ($DEC_COUNT total) ---"
  print_recent_titles "$DECISIONS_FILE" 2 "- "
  echo "Query details with: qmd vsearch '<topic>' --collection memory"
  echo ""
fi

PATTERNS_FILE="$MEMORY_DIR/patterns.md"
if [ -f "$PATTERNS_FILE" ]; then
  PAT_COUNT=$(grep -c '^### ' "$PATTERNS_FILE" 2>/dev/null || echo 0)
  echo "--- RECENT PATTERNS ($PAT_COUNT total) ---"
  print_recent_titles "$PATTERNS_FILE" 3 "- "
  echo "Query details with: qmd vsearch '<topic>' --collection memory"
  echo ""
fi

if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
  DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h' 2>/dev/null)
  echo "--- GIT STATE ---"
  echo "Branch: $BRANCH | Uncommitted: $DIRTY files"
  [ -n "$LAST_COMMIT" ] && echo "Last commit: $LAST_COMMIT"
  echo ""
fi

if [ -f "$LEARNINGS_QUEUE" ] && [ -s "$LEARNINGS_QUEUE" ]; then
  QUEUE_DATA=$(python3 -c "
import json
try:
    with open('$LEARNINGS_QUEUE') as f:
        d = json.load(f)
    if not isinstance(d, list):
        d = []
    total = len(d)
    reflect_others = sum(1 for x in d if x.get('type') == 'reflect-others' and x.get('status') == 'pending')
    print(f'{total} {reflect_others}')
except:
    print('0 0')
" 2>/dev/null || echo "0 0")
  read -r QUEUE_ITEMS REFLECT_OTHERS_PENDING <<< "$QUEUE_DATA"
  if [ "${QUEUE_ITEMS:-0}" != "0" ]; then
    echo "Pending learnings: ${QUEUE_ITEMS}"
  fi
  if [ "${REFLECT_OTHERS_PENDING:-0}" != "0" ]; then
    echo "Pending reflect-others candidates: ${REFLECT_OTHERS_PENDING}"
  fi
  if [ "${QUEUE_ITEMS:-0}" != "0" ] || [ "${REFLECT_OTHERS_PENDING:-0}" != "0" ]; then
    echo ""
  fi
fi

if [ "$CWD" = "$HOME" ] || [ "$CWD" = "$HOME/" ]; then
  SESSIONS_TODAY=$(find "$SESSIONS_DIR" -maxdepth 1 -name "${DATE_TODAY}*.md" -not -name "session-compact-*" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$SESSIONS_TODAY" = "0" ]; then
    echo "First session today - run /assistant for your morning briefing."
  else
    echo "Run /assistant for help with priorities, communication, or context."
  fi
  echo ""
fi

echo "=== END SESSION CONTEXT ==="
echo "Commands: /assistant, /briefing, /switch-project"

exit 0
