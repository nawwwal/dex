#!/usr/bin/env bash
# UserPromptSubmit hook: detect third-person observations about the user
# and stage them to learnings-queue.json for review via /reflect-others.
# Stores score + timestamp only — no raw content.

INPUT=$(cat)

# Cheap bash pre-filter: skip python3 entirely for obvious non-matches
# Covers all high-scoring patterns; false positives just fall through to python scoring
if ! echo "$INPUT" | grep -qiE 'the_user|the user|the_user|strengths[[:space:]]*:|areas (to develop|for improvement)|feedback (for|on) the_user|one thing.*flag|the_user.s approach|observed that the_user|great ownership|well.crafted|could improve'; then
  exit 0
fi

# Parse prompt + score in one python3 call (reads stdin, avoids argv length limits)
# Outputs: "<score>" or "0" if no match
SCORE=$(echo "$INPUT" | python3 - << 'PYEOF'
import sys, re, json

try:
    d = json.load(sys.stdin)
    msg = d.get('prompt', '')[:4000].lower()  # truncate to 4000 chars
except Exception:
    print(0)
    sys.exit(0)

score = 0

# +3 patterns: exact name references
if re.search(r'\bthe_user\b', msg): score += 3
if re.search(r'\bthe user\b', msg): score += 3
if re.search(r'\bthe_user the_user\b', msg): score += 3

# +3 patterns: structured feedback terminology
if re.search(r'strengths\s*:', msg): score += 3
if re.search(r'areas (to develop|for improvement)\s*:', msg): score += 3
if re.search(r'feedback (for|on) the_user', msg): score += 3

# +2 patterns: specific third-person phrases
if re.search(r"one thing i'?d flag", msg): score += 2
if re.search(r"the_user'?s approach", msg): score += 2
if re.search(r'observed that the_user', msg): score += 2

# +1 patterns: only count if score already elevated
if score >= 2:
    if re.search(r'great ownership', msg): score += 1
    if re.search(r'well.crafted', msg): score += 1
    if re.search(r'could improve', msg): score += 1

print(score)
PYEOF
)

if [[ "${SCORE:-0}" -lt 3 ]]; then
  exit 0
fi

# Write to queue + emit systemMessage in one python3 call
QUEUE="$HOME/.claude/learnings-queue.json"
python3 - "$QUEUE" "$SCORE" << 'PYEOF'
import fcntl, json, os, time, sys

queue_path = sys.argv[1]
score = int(sys.argv[2])
tmp_path = queue_path + '.tmp'
lock_path = queue_path + '.lock'

with open(lock_path, 'w') as lf:
    fcntl.flock(lf, fcntl.LOCK_EX)
    try:
        try:
            with open(queue_path) as f:
                q = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            q = []
        if not isinstance(q, list):
            q = []
        q.append({
            "type": "reflect-others",
            "ts": int(time.time() * 1000),
            "score": score,
            "status": "pending"
        })
        with open(tmp_path, 'w') as f:
            json.dump(q, f, indent=2)
        os.replace(tmp_path, queue_path)
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)

# Emit systemMessage in the same process
msg = {
    'systemMessage': f'Third-person signal staged (score={score}). Run /reflect-others to review and confirm before saving to memory.'
}
print(json.dumps(msg))
PYEOF

exit 0
