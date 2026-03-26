#!/bin/bash
# PreCompact hook: Save working state before context compaction.
# Aligned with /briefing skill — persists to Obsidian sessions, memory files, and project CLAUDE.md.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
ENCODED_PATH=$(echo "$CWD" | sed 's|/|-|g')
PROJECT_MEMORY="$HOME/.claude/projects/$ENCODED_PATH/CLAUDE.md"

CLAUDE_DIR="$HOME/.claude"
SESSIONS_DIR="$CLAUDE_DIR/sessions"
REGISTRY="$CLAUDE_DIR/config/project-registry.json"
PROJECT_KEY=$(echo "$CWD" | tr '/[:space:]' '--' | tr -cd '[:alnum:]._-' | sed 's/--*/-/g; s/^-//; s/-$//' | cut -c1-120)
[ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"
COMPACT_FILE="$SESSIONS_DIR/session-compact-${PROJECT_KEY}.md"

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

# Gather git state
GIT_CONTEXT=""
if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  GIT_BRANCH=$(git -C "$CWD" branch --show-current 2>/dev/null)
  GIT_DIRTY=$(git -C "$CWD" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  GIT_STAGED=$(git -C "$CWD" diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
  GIT_LAST_COMMIT=$(git -C "$CWD" log -1 --format='%h %s' 2>/dev/null)
  GIT_CONTEXT="branch=$GIT_BRANCH | uncommitted=$GIT_DIRTY | staged=$GIT_STAGED | last-commit: $GIT_LAST_COMMIT"
fi

# Write shell-level breadcrumb to Obsidian sessions directory
if [ -d "$CLAUDE_DIR" ]; then
  mkdir -p "$SESSIONS_DIR"
  cat > "$COMPACT_FILE" <<BLOCK
# Session Compact Snapshot

Overwritten on each compact for this project. Keep only current context.

## Snapshot at $TIMESTAMP
- **CWD:** \`$CWD\`
${PROJECT_NAME:+- **Project:** $PROJECT_NAME}
${GIT_CONTEXT:+- **Git:** $GIT_CONTEXT}

<!-- Claude: replace with <=8 bullets: active work, live decisions, next steps, blockers. Skip stale/completed items. -->

BLOCK
fi

# NOTE: PreCompact stdout is shown in verbose mode (Ctrl+O) to the user only.
# Claude does NOT see this output — per the official docs, only SessionStart
# and UserPromptSubmit stdout is added to Claude's context.
# Context recovery happens via the SessionStart hook reading the Obsidian file
# written above, when the next session (or post-compact session) starts.

# Verbose-mode status for the human user
echo "PreCompact: saved compact snapshot to $COMPACT_FILE"
echo "  Project: ${PROJECT_NAME:-unknown} | Git: ${GIT_CONTEXT:-not a git repo}"
echo "  SessionStart hook will restore this context on next session."

exit 0
