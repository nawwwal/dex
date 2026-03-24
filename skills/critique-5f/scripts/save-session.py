#!/usr/bin/env python3
"""
5F Review Session Saver — Stop Hook
Runs when Claude Code session ends. Finds all /tmp/5f-review-session-*.json
temp files written during the session and persists them to the project-local
.claude/5f-reviews/feedback/review-sessions.jsonl file.

Data lives in {cwd}/.claude/5f-reviews/ — project-local, not inside the skill.
"""

import json
import os
import datetime
import sys
import glob
import uuid

# Project-local data dir (where the user ran Claude Code from)
DATA_DIR = os.path.join(os.getcwd(), '.claude', '5f-reviews', 'feedback')
os.makedirs(DATA_DIR, exist_ok=True)
JSONL = os.path.join(DATA_DIR, 'review-sessions.jsonl')

# Find all session temp files (handles multiple reviews per session)
tmp_files = glob.glob('/tmp/5f-review-session-*.json')
if not tmp_files:
    sys.exit(0)  # No review ran this session

saved = 0
for tmp in tmp_files:
    try:
        with open(tmp) as f:
            data = json.load(f)
        data['review_id'] = str(uuid.uuid4())
        data['saved_at'] = datetime.datetime.now().isoformat()
        with open(JSONL, 'a') as out:
            out.write(json.dumps(data) + '\n')
        os.remove(tmp)
        saved += 1
    except Exception as e:
        print(f"Warning: failed to save {tmp}: {e}", file=sys.stderr)

if saved > 0:
    print(f"✓ {saved} review session(s) saved to {JSONL}")
