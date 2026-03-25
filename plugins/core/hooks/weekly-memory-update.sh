#!/bin/bash
# weekly-memory-update.sh — SessionStart hook
# Phase 1: Prune stale queue entries (every session)
# Phase 2: Weekly gate — add new safe-auto entries if >7 days since last run

MEMORY_DIR="$HOME/.claude/memory"
PENDING_UPDATES_FILE="$MEMORY_DIR/pending-updates.json"
LAST_WEEKLY_FILE="$MEMORY_DIR/last-weekly-update.txt"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%dT%H:%M:%S')
LOCK_DIR="/tmp/weekly-memory-update.lock"

# Acquire lock (macOS-portable)
mkdir "$LOCK_DIR" 2>/dev/null || exit 0
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

# ============================================================
# PHASE 1: Prune stale queue entries (runs every session)
# ============================================================
if [ -f "$PENDING_UPDATES_FILE" ] && [ -s "$PENDING_UPDATES_FILE" ]; then
    python3 - <<PYEOF
import json, os
from datetime import datetime

pending_path = '$PENDING_UPDATES_FILE'

try:
    with open(pending_path) as f:
        entries = json.load(f)
    if not isinstance(entries, list):
        exit(0)

    remaining = []
    for entry in entries:
        target = os.path.expanduser(entry.get('target_file', ''))
        queued_at_str = entry.get('queued_at', '')
        if not target or not queued_at_str or not os.path.exists(target):
            remaining.append(entry)
            continue
        try:
            queued_ts = datetime.fromisoformat(queued_at_str).timestamp()
        except:
            remaining.append(entry)
            continue
        file_mtime = os.path.getmtime(target)
        if file_mtime > queued_ts:
            # File updated out-of-band — remove from queue
            pass
        else:
            remaining.append(entry)

    if not remaining:
        os.remove(pending_path)
    elif len(remaining) != len(entries):
        tmp = pending_path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(remaining, f, indent=2)
        os.rename(tmp, pending_path)
except Exception:
    pass
PYEOF
fi

# ============================================================
# PHASE 2: Weekly gate — add new safe-auto entries
# ============================================================
DAYS_SINCE=999
if [ -f "$LAST_WEEKLY_FILE" ]; then
    LAST_RUN=$(cat "$LAST_WEEKLY_FILE" 2>/dev/null | tr -d '[:space:]')
    if [ -n "$LAST_RUN" ]; then
        DAYS_SINCE=$(python3 -c "
from datetime import date
try:
    last = date.fromisoformat('$LAST_RUN')
    print((date.today() - last).days)
except:
    print(999)
" 2>/dev/null || echo 999)
    fi
fi

if [ "${DAYS_SINCE:-999}" -ge 7 ] 2>/dev/null; then
    python3 - <<PYEOF2
import json, os
from datetime import datetime, date

memory_dir = '$MEMORY_DIR'
pending_path = '$PENDING_UPDATES_FILE'
last_weekly_file = '$LAST_WEEKLY_FILE'
today = date.today()
now_str = '$NOW'

# Safe-auto memory files and their thresholds
# Only nawal-model.md is safe-auto (local writes only)
safe_auto_files = [
    {
        'fname': 'nawal-model.md',
        'auto_after_days': 30,
        'skill': 'assistant',
        'variant': 'assistant emerge',
    },
]

try:
    # Load existing pending entries
    existing = []
    if os.path.exists(pending_path):
        try:
            with open(pending_path) as f:
                existing = json.load(f)
            if not isinstance(existing, list):
                existing = []
        except:
            existing = []

    existing_ids = {e.get('id') for e in existing}
    new_entries = list(existing)  # copy

    for item in safe_auto_files:
        fpath = os.path.join(memory_dir, item['fname'])
        if not os.path.exists(fpath):
            continue
        mtime = os.path.getmtime(fpath)
        mod_date = datetime.fromtimestamp(mtime).date()
        days_stale = (today - mod_date).days
        if days_stale < item['auto_after_days']:
            continue
        # Build entry
        entry_id = f"{item['fname'].replace('.md', '')}-{today.isoformat()}"
        if entry_id in existing_ids:
            continue  # Already queued
        entry = {
            'id': entry_id,
            'skill': item['skill'],
            'variant': item['variant'],
            'target_file': f"~/.claude/memory/{item['fname']}",
            'reason': f"{item['fname']} stale {days_stale}d",
            'queued_at': now_str,
        }
        new_entries.append(entry)

    if new_entries != existing:
        tmp = pending_path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(new_entries, f, indent=2)
        os.rename(tmp, pending_path)

    # Advance the weekly gate
    with open(last_weekly_file, 'w') as f:
        f.write(today.isoformat() + '\n')

except Exception:
    pass
PYEOF2
fi

exit 0
