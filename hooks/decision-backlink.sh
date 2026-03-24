#!/usr/bin/env bash
# When decisions.md is written (or via --full-scan), add backlinks to work/*/index.md
# Idempotent: safe to run multiple times. Never double-writes the same dec-slug.

DECISIONS_FILE="$HOME/.claude/memory/decisions.md"
WORK_DIR="$HOME/.claude/work"

# -------------------------------------------------------------------
# Core logic: scan ALL decisions, add any missing backlinks
# -------------------------------------------------------------------
run_backlink_scan() {
  if [[ ! -f "$DECISIONS_FILE" ]]; then
    return 0
  fi

  python3 - "$DECISIONS_FILE" "$WORK_DIR" << 'PYEOF'
import sys, re, os

decisions_file = sys.argv[1]
work_dir = os.path.realpath(sys.argv[2])

content = open(decisions_file).read()

# Match ### header lines that contain a ^dec- anchor on the same line
block_pattern = re.compile(
    r'^### \d{4}-\d{2}-\d{2}:.*?(\^dec-[a-z0-9-]+)',
    re.MULTILINE
)
# Match [[work/<project>/index|...]] wikilinks
project_pattern = re.compile(
    r'\[\[work/([^/]+)/index\|[^\]]*\]\]'
)

pairs = []
for m in block_pattern.finditer(content):
    slug = m.group(1)
    # Search within the next 400 chars for the Project: line
    window = content[m.start():m.start() + 400]
    pm = project_pattern.search(window)
    if pm:
        pairs.append((slug, pm.group(1)))

for slug, project in pairs:
    index_path = os.path.join(work_dir, project, 'index.md')

    # Security guard: must stay within work_dir
    if not os.path.realpath(index_path).startswith(work_dir + os.sep):
        continue

    if not os.path.isfile(index_path):
        continue

    content_idx = open(index_path).read()

    # Already backlinked — skip
    if slug in content_idx:
        continue

    # Add <!-- Decisions --> marker if missing
    if '<!-- Decisions -->' not in content_idx:
        with open(index_path, 'a') as f:
            f.write('\n<!-- Decisions -->\n')
        content_idx += '\n<!-- Decisions -->\n'

    # Insert backlink immediately after the marker
    backlink = f'- [[memory/decisions#{slug}|{slug}]]'
    updated = content_idx.replace(
        '<!-- Decisions -->',
        f'<!-- Decisions -->\n{backlink}',
        1
    )
    with open(index_path, 'w') as f:
        f.write(updated)
PYEOF
}

# -------------------------------------------------------------------
# CLI mode: --full-scan bypasses hook stdin (for backfill and testing)
# -------------------------------------------------------------------
if [[ "$1" == "--full-scan" ]]; then
  run_backlink_scan
  exit 0
fi

# -------------------------------------------------------------------
# Hook mode: only run when decisions.md was written
# -------------------------------------------------------------------
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except:
    print('')
" 2>/dev/null || echo "")

if ! echo "$FILE_PATH" | grep -q 'decisions.md'; then
  exit 0
fi

run_backlink_scan
exit 0
