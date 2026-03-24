#!/bin/bash
# Stop hook: Remind Claude to make meaningful commits before finishing.
# Does NOT ask for a commit after every tiny change — only fires once
# when Claude is about to stop and there are uncommitted changes.

INPUT=$(cat)

# Prevent infinite loops: if we already reminded once, let Claude stop.
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

# Only relevant inside a git repo
CWD=$(echo "$INPUT" | jq -r '.cwd // "."')
if ! git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  exit 0
fi

# Check for any staged or unstaged changes (tracked files + untracked)
CHANGES=$(git -C "$CWD" status --porcelain 2>/dev/null)
if [ -z "$CHANGES" ]; then
  exit 0  # Working tree clean, nothing to remind about
fi

# There are uncommitted changes — block and remind
cat <<'EOF'
Before finishing, review your uncommitted changes (git status / git diff).
If there are meaningful, logically-grouped changes, commit them now.

Guidelines:
- Group related changes into one commit (e.g. "Add user auth endpoint with tests").
- Do NOT commit after every single-line tweak — batch related edits together.
- Use clear, descriptive commit messages that explain WHY, not just WHAT.
- Skip committing if the changes are trivial WIP that the user will handle later.

Check git status now and decide whether a commit is appropriate.
EOF

exit 2  # Block stop so Claude acts on the reminder
