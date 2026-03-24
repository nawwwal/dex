#!/bin/bash
# track-skill-usage.sh — PostToolUse hook for the Skill tool
# Records skill invocations to memory/skill-usage.json
# Clears pending-updates.json entries when file was actually modified

MEMORY_DIR="$HOME/.claude/memory"
TODAY=$(date '+%Y-%m-%d')
LOCK_DIR="/tmp/skill-usage.lock"

# Acquire lock (macOS-portable: no flock)
mkdir "$LOCK_DIR" 2>/dev/null || exit 0
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

# Single python3 call: extract skill, normalize, update usage.json, prune pending-updates
python3 - "$MEMORY_DIR" "$TODAY" <<'PYEOF'
import json, os, sys
from datetime import datetime

memory_dir = sys.argv[1]
today = sys.argv[2]
skill_usage_path = os.path.join(memory_dir, 'skill-usage.json')
pending_path = os.path.join(memory_dir, 'pending-updates.json')
last_weekly_file = os.path.join(memory_dir, 'last-weekly-update.txt')

# Read stdin payload
try:
    raw = sys.stdin.read()
    d = json.loads(raw)
    skill_invoked = d.get('tool_input', {}).get('skill', '')
except Exception:
    sys.exit(0)

if not skill_invoked:
    sys.exit(0)

# Normalize to top-level name (think:emerge -> think, log:week -> log)
skill_top = skill_invoked.split(':')[0]

# Update skill-usage.json
try:
    usage = {}
    if os.path.exists(skill_usage_path):
        with open(skill_usage_path) as f:
            usage = json.load(f)
    usage[skill_top] = today
    tmp = skill_usage_path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(usage, f, indent=2)
    os.rename(tmp, skill_usage_path)
except Exception:
    pass

# Clear matching pending-updates.json entry if target file was actually modified
if not os.path.exists(pending_path):
    sys.exit(0)

try:
    with open(pending_path) as f:
        entries = json.load(f)
    if not isinstance(entries, list):
        sys.exit(0)

    remaining = []
    for entry in entries:
        if entry.get('variant', '') != skill_invoked:
            remaining.append(entry)
            continue
        # Exact variant match — verify target file was modified after queuing
        target = os.path.expanduser(entry.get('target_file', ''))
        queued_at_str = entry.get('queued_at', '')
        if not target or not queued_at_str or not os.path.exists(target):
            remaining.append(entry)
            continue
        try:
            queued_ts = datetime.fromisoformat(queued_at_str).timestamp()
        except Exception:
            remaining.append(entry)
            continue
        if os.path.getmtime(target) > queued_ts:
            pass  # File updated — drop from queue
        else:
            remaining.append(entry)

    if not remaining:
        os.remove(pending_path)
        with open(last_weekly_file, 'w') as f:
            f.write(today + '\n')
    elif len(remaining) != len(entries):
        tmp = pending_path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(remaining, f, indent=2)
        os.rename(tmp, pending_path)
except Exception:
    pass
PYEOF

exit 0
