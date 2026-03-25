#!/bin/bash
# vault-health.sh — SessionStart hook (runs before session-context.sh)
# Writes memory/health.md with staleness checks, content audits, and self-tests.
# Auto-fixes: chmod +x on non-executable hooks, qmd refresh if stale.
# Optimized: batches all python3 work into 2 calls. Target: <2.5s

CLAUDE_DIR="$HOME/.claude"
MEMORY_DIR="$CLAUDE_DIR/memory"
LEARN_DIR="$CLAUDE_DIR/learn"
CAREER_DIR="$CLAUDE_DIR/career"
LOG_DIR="$CLAUDE_DIR/log"
HEALTH_FILE="$MEMORY_DIR/health.md"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%d %H:%M')
CURRENT_MONTH=$(date '+%Y-%m')

# ============================================================
# PYTHON3 BATCH: File stats, plan detection, QMD age, prev failures
# Single python3 call replaces ~12 individual subprocess calls
# Write python to temp file first (avoids heredoc-in-subshell issues on bash 3.2)
# ============================================================

PYFILE=$(mktemp /tmp/vault-health-XXXXXX.py)
cat > "$PYFILE" << 'PYEOF'
import os, re, glob, time, json
from datetime import date, datetime

home = os.path.expanduser('~')
memory_dir = os.path.join(home, '.claude', 'memory')
career_dir = os.path.join(home, '.claude', 'career')
learn_dir  = os.path.join(home, '.claude', 'learn')
today = date.today()
current_month = today.strftime('%Y-%m')

output = {}

# --- File staleness ---
thresholds = {
    'goals.md': 7,
    'decisions.md': 14,
    'projects.md': 14,
    'people.md': 30,
    'nawal-through-others.md': 30,
    'meetings.md': 14,
    'razorpay-context.md': 14,
    'reminders.md': 14,
    'terms.md': 14,
    'voice.md': 14,
    'devrev.md': 30,
    'slack-channels.md': 14,
}
memory_action_map = {
    'meetings.md': ('/productivity:update', 'confirm-required'),
    'projects.md': ('/productivity:update', 'confirm-required'),
    'people.md': ('/productivity:update', 'confirm-required'),
    'decisions.md': ('/decisions:archive', 'confirm-required'),
    'nawal-model.md': ('/assistant emerge', 'safe-auto'),
    'goals.md': ('/assistant week', 'confirm-required'),
    'voice.md': ('manual update', 'confirm-required'),
    'terms.md': ('update from session context', 'safe-auto'),
    'razorpay-context.md': ('update from Slack/calendar context', 'safe-auto'),
    'reminders.md': ('review and clear expired items', 'safe-auto'),
    'devrev.md': ('refresh via Compass DevRev MCP tools', 'safe-auto'),
    'slack-channels.md': ('refresh via Compass Slack MCP (slack_get_channels)', 'safe-auto'),
}
staleness_rows = []
staleness_warnings = 0
for fname, threshold in thresholds.items():
    action, safety = memory_action_map.get(fname, ('\u2014', '\u2014'))
    fpath = os.path.join(memory_dir, fname)
    if not os.path.exists(fpath):
        staleness_rows.append(f'| {fname} | missing | MISSING | {action} | {safety} |')
        staleness_warnings += 1
    else:
        mtime = os.path.getmtime(fpath)
        mod = datetime.fromtimestamp(mtime)
        days = (today - mod.date()).days
        mod_str = mod.strftime('%Y-%m-%d')
        if days >= threshold:
            staleness_rows.append(f'| {fname} | {mod_str} | STALE ({days}d, warn after {threshold}d) | {action} | {safety} |')
            staleness_warnings += 1
        else:
            staleness_rows.append(f'| {fname} | {mod_str} | OK ({days}d) | {action} | {safety} |')
output['staleness_rows'] = staleness_rows
output['staleness_warnings'] = staleness_warnings

# --- Stale daily plan detection ---
goals_path = os.path.join(memory_dir, 'goals.md')
plan_status = 'OK'
plan_warning = 0
if os.path.exists(goals_path):
    try:
        content = open(goals_path).read(4096)  # only read first 4KB
        m = re.search(r"Today's Plan \xe2\x80\x94 ([A-Za-z]+ [0-9]+)", content)
        if not m:
            m = re.search(r"Today's Plan -- ([A-Za-z]+ [0-9]+)", content)
        if not m:
            m = re.search(r"Today's Plan - ([A-Za-z]+ [0-9]+)", content)
        if not m:
            m = re.search(r"Today.s Plan .{1,5} ([A-Za-z]+ [0-9]+)", content)
        if m:
            plan_str = m.group(1)
            try:
                plan_date = datetime.strptime(f'{today.year} {plan_str}', '%Y %b %d').date()
                # Cross-year fix: if parsed date is in the future, it's from last year (e.g. Dec plan in Jan)
                if plan_date > today:
                    plan_date = datetime.strptime(f'{today.year - 1} {plan_str}', '%Y %b %d').date()
                if plan_date < today:
                    plan_status = f'STALE - daily plan from "{plan_str}" still in goals.md (today: {today})'
                    plan_warning = 1
                else:
                    plan_status = f'OK - plan dated {plan_str}'
            except:
                plan_status = 'OK - could not parse plan date'
        else:
            plan_status = 'OK - no Today\'s Plan section found'
    except:
        plan_status = 'OK - could not read goals.md'
output['plan_status'] = plan_status
output['plan_warning'] = plan_warning

# --- decisions.md line count ---
decisions_path = os.path.join(memory_dir, 'decisions.md')
dec_warning = 0
if not os.path.exists(decisions_path):
    dec_status = 'MISSING'
    dec_warning = 1
    dec_count = 0
else:
    with open(decisions_path) as f:
        dec_lines = 0
        dec_count = 0
        for line in f:
            dec_lines += 1
            if line.startswith('### 20'):
                dec_count += 1
    if dec_lines > 300:
        dec_status = f'{dec_lines} lines - ARCHIVE NEEDED (threshold: 300). Run /decisions:archive.'
        dec_warning = 1
    else:
        dec_status = f'{dec_lines} lines - OK'
output['dec_status'] = dec_status
output['dec_warning'] = dec_warning
output['dec_count'] = dec_count

# --- learn/ category coverage ---
design_count = len(glob.glob(os.path.join(learn_dir, f'design-{current_month}-*.md')))
people_count = len(glob.glob(os.path.join(learn_dir, f'people-{current_month}-*.md')))
eng_files = glob.glob(os.path.join(learn_dir, f'{current_month}-*.md'))
eng_count = len(eng_files)
learn_rows = []
learn_warnings = 0
if design_count == 0:
    learn_rows.append(f'Design TILs: 0 this month - MISSING')
    learn_warnings += 1
else:
    learn_rows.append(f'Design TILs: {design_count} this month')
if people_count == 0:
    learn_rows.append(f'Interpersonal TILs: 0 this month - MISSING')
    learn_warnings += 1
else:
    learn_rows.append(f'Interpersonal TILs: {people_count} this month')
learn_rows.append(f'Engineering TILs: {eng_count} this month')
output['learn_rows'] = learn_rows
output['learn_warnings'] = learn_warnings

# --- career/gaps.md recency ---
gaps_path = os.path.join(career_dir, 'gaps.md')
case_warning = 0
if not os.path.exists(gaps_path):
    case_status = 'NOT RUN - career/gaps.md missing. Run /assistant week on next Friday.'
    case_warning = 1
else:
    mtime = os.path.getmtime(gaps_path)
    mod = datetime.fromtimestamp(mtime)
    days = (today - mod.date()).days
    mod_str = mod.strftime('%Y-%m-%d')
    if days > 7:
        case_status = f'STALE - last ran {mod_str} ({days}d ago). Run /assistant week.'
        case_warning = 1
    else:
        case_status = f'OK - last ran {mod_str} ({days}d ago)'
output['case_status'] = case_status
output['case_warning'] = case_warning

# --- Previous failures from health.md frontmatter ---
health_path = os.path.join(memory_dir, 'health.md')
prev_failures = []
if os.path.exists(health_path):
    try:
        content = open(health_path).read(2000)
        m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if m:
            pf = re.search(r'previous_failures:\n((?:  - .+\n?)*)', m.group(1))
            if pf:
                prev_failures = re.findall(r'  - "(.+?)"', pf.group(1))
    except:
        pass
output['prev_failures'] = prev_failures

# --- decision backlink count (individual lines, not files) ---
backlink_count = 0
for search_dir in [os.path.join(home, '.claude', 'work'), os.path.join(home, '.claude', 'projects')]:
    for root, dirs, files in os.walk(search_dir):
        for fname in files:
            if fname.endswith('.md'):
                fpath = os.path.join(root, fname)
                try:
                    for line in open(fpath):
                        if f'dec-{today.year}-' in line:
                            backlink_count += 1
                except:
                    pass
output['backlink_count'] = backlink_count

# --- Journal quality (stubs vs real content) ---
stub_count = 0
journal_count = 0
log_dir_path = os.path.join(home, '.claude', 'log')
if os.path.isdir(log_dir_path):
    for fname in os.listdir(log_dir_path):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(log_dir_path, fname)
        try:
            size = os.path.getsize(fpath)
            if size < 300:
                stub_count += 1
            else:
                journal_count += 1
        except:
            pass
stub_pct = int(100 * stub_count / max(1, stub_count + journal_count))
output['stub_count'] = stub_count
output['stub_pct'] = stub_pct

# --- Skill freshness ---
skill_usage_path = os.path.join(home, '.claude', 'memory', 'skill-usage.json')
skills_dir_path = os.path.join(home, '.claude', 'skills')
skill_rows = []
skill_warnings = 0

skill_names = []
if os.path.isdir(skills_dir_path):
    for d in sorted(os.listdir(skills_dir_path)):
        if d.startswith('.'):
            continue
        sp = os.path.join(skills_dir_path, d)
        if os.path.isdir(sp) and os.path.exists(os.path.join(sp, 'SKILL.md')):
            skill_names.append(d)

skill_usage = {}
if os.path.exists(skill_usage_path):
    try:
        skill_usage = json.load(open(skill_usage_path))
    except:
        pass

for skill in skill_names:
    last_used = skill_usage.get(skill, 'never')
    if last_used == 'never':
        skill_rows.append(f'| {skill} | never | \u2014 | NEVER USED |')
        skill_warnings += 1
    else:
        try:
            lu_date = datetime.strptime(last_used, '%Y-%m-%d').date()
            days = (today - lu_date).days
            if days > 14:
                skill_rows.append(f'| {skill} | {last_used} | {days} | STALE |')
                skill_warnings += 1
            else:
                skill_rows.append(f'| {skill} | {last_used} | {days} | OK |')
        except:
            skill_rows.append(f'| {skill} | {last_used} | ? | UNKNOWN |')

output['skill_rows'] = skill_rows
output['skill_warnings'] = skill_warnings

import json
print(json.dumps(output))
PYEOF

PYTHON_OUTPUT=$(python3 "$PYFILE" 2>/dev/null)
rm -f "$PYFILE"

# --- Parse all fields from python3 output in one subprocess call ---
# Emits shell assignments for scalars; list fields written to tempfiles
PARSE_FILE=$(mktemp /tmp/vault-parse-XXXXXX.py)
cat > "$PARSE_FILE" << 'PARSEEOF'
import json, sys, os, tempfile

d = json.loads(sys.argv[1])
tmpdir = sys.argv[2]

def sq(s):
    return "'" + str(s).replace("'", "'\\''") + "'"

# Scalar ints
for k in ['staleness_warnings','plan_warning','dec_warning','dec_count','case_warning','learn_warnings','backlink_count','skill_warnings','stub_count','stub_pct']:
    print(f"{k.upper()}={int(d.get(k, 0))}")

# Scalar strings
for k in ['plan_status','dec_status','case_status']:
    print(f"{k.upper()}={sq(d.get(k, ''))}")

# List fields: write to tempfiles, emit paths
for k in ['staleness_rows','learn_rows','prev_failures','skill_rows']:
    items = d.get(k, [])
    tf = os.path.join(tmpdir, f'vh_{k}')
    open(tf, 'w').write('\n'.join(str(i) for i in items))
    print(f"_VH_{k.upper()}_FILE={sq(tf)}")
PARSEEOF

eval "$(python3 "$PARSE_FILE" "$PYTHON_OUTPUT" "$(dirname "$PARSE_FILE")" 2>/dev/null)"
rm -f "$PARSE_FILE"

# Read list fields from tempfiles
STALENESS_TABLE=$(cat "$_VH_STALENESS_ROWS_FILE" 2>/dev/null); rm -f "$_VH_STALENESS_ROWS_FILE"
LEARN_LINES=$(cat "$_VH_LEARN_ROWS_FILE" 2>/dev/null); rm -f "$_VH_LEARN_ROWS_FILE"
PREV_FAILURES_LIST=$(cat "$_VH_PREV_FAILURES_FILE" 2>/dev/null); rm -f "$_VH_PREV_FAILURES_FILE"
SKILL_TABLE=$(cat "$_VH_SKILL_ROWS_FILE" 2>/dev/null); rm -f "$_VH_SKILL_ROWS_FILE"

TOTAL_WARNINGS=$((STALENESS_WARNINGS + PLAN_WARNING + DEC_WARNING + LEARN_WARNINGS + CASE_WARNING + SKILL_WARNINGS))

# --- QMD freshness: sentinel-based (LaunchAgent touches ~/.claude/.qmd-last-refresh) ---
QMD_SENTINEL="$CLAUDE_DIR/.qmd-last-refresh"
QMD_AGE=999
if [ -f "$QMD_SENTINEL" ]; then
  QMD_AGE=$(python3 -c "import os,time; print(int((time.time()-os.path.getmtime('$QMD_SENTINEL'))/60))" 2>/dev/null || echo 999)
fi

# ============================================================
# MODULE 6: Infrastructure Self-Tests (bash, fast)
# ============================================================

TEST_INFRA=""
TEST_BEHAVIORAL=""
AUTOFIX_LOG=""
CURRENT_FAILURES=""

# settings.json valid JSON (already parsed by python, reuse)
if python3 -c "import json; json.load(open('$HOME/.claude/settings.json'))" 2>/dev/null; then
  TEST_INFRA="${TEST_INFRA}[PASS] settings.json: valid JSON\n"
else
  TEST_INFRA="${TEST_INFRA}[FAIL] settings.json: invalid JSON\n"
  CURRENT_FAILURES="${CURRENT_FAILURES}settings.json invalid JSON\n"
fi

# Hook scripts: executable (auto-fix chmod +x)
HOOK_ALL_OK=1
for hook in "$CLAUDE_DIR/hooks"/*.sh; do
  [ -f "$hook" ] || continue
  if [ ! -x "$hook" ]; then
    if chmod +x "$hook" 2>/dev/null; then
      AUTOFIX_LOG="${AUTOFIX_LOG}[AUTO-FIXED] chmod +x $(basename "$hook")\n"
    else
      TEST_INFRA="${TEST_INFRA}[FAIL] not executable: $(basename "$hook")\n"
      CURRENT_FAILURES="${CURRENT_FAILURES}hook not executable: $(basename "$hook")\n"
      HOOK_ALL_OK=0
    fi
  fi
done
[ "$HOOK_ALL_OK" = "1" ] && TEST_INFRA="${TEST_INFRA}[PASS] hook scripts: all executable\n"

# Hooks in settings.json reference scripts that exist
MISSING_HOOKS=$(python3 -c "
import json, os
try:
    s = json.load(open('$HOME/.claude/settings.json'))
    missing = []
    for event, groups in s.get('hooks', {}).items():
        for group in groups:
            for h in group.get('hooks', []):
                cmd = h.get('command', '')
                for part in cmd.split():
                    if part.endswith('.sh') and part.startswith('/') and not os.path.exists(part):
                        missing.append(part)
    for m in sorted(set(missing)): print(m)
except: pass
" 2>/dev/null)

if [ -n "$MISSING_HOOKS" ]; then
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    TEST_INFRA="${TEST_INFRA}[FAIL] missing hook: $m\n"
    CURRENT_FAILURES="${CURRENT_FAILURES}missing hook: $m\n"
  done <<< "$MISSING_HOOKS"
else
  TEST_INFRA="${TEST_INFRA}[PASS] hook scripts: all registered paths exist\n"
fi

# Episodic memory sync: verify versioned path exists
EPISODIC_SH="$CLAUDE_DIR/hooks/episodic-memory-sync.sh"
if [ -f "$EPISODIC_SH" ]; then
  EPISODIC_PATH=$(grep -o 'plugins/cache[^"]*sync-cli\.js' "$EPISODIC_SH" 2>/dev/null | head -1)
  if [ -n "$EPISODIC_PATH" ]; then
    EPISODIC_FULL="$HOME/$EPISODIC_PATH"
    if [ ! -f "$EPISODIC_FULL" ]; then
      TEST_INFRA="${TEST_INFRA}[FAIL] episodic-memory-sync.sh: sync-cli.js missing at ${EPISODIC_FULL} — re-install episodic-memory plugin\n"
      CURRENT_FAILURES="${CURRENT_FAILURES}episodic-memory-sync: sync-cli.js missing\n"
    else
      TEST_INFRA="${TEST_INFRA}[PASS] episodic-memory-sync.sh: sync-cli.js present\n"
    fi
  fi
fi

# Content-level checks: OoO expiry in slack-channels.md
SLACK_CHANNELS_FILE="$MEMORY_DIR/slack-channels.md"
if [ -f "$SLACK_CHANNELS_FILE" ]; then
  # Check for OoO notes that have passed their expiry date
  OOO_STALE=$(python3 -c "
import re, sys
from datetime import date
today = date.today()
content = open('$SLACK_CHANNELS_FILE').read()
# Look for 'back Mar 18' or 'back Mon' style patterns
matches = re.findall(r'OoO[^|]*back\s+(Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Jan|Feb)\s+(\d+)', content, re.IGNORECASE)
stale = []
for month_str, day_str in matches:
    try:
        d = date(today.year, list(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']).index(month_str.lower())+1, int(day_str))
        if d < today:
            stale.append(f'{month_str} {day_str}')
    except: pass
if stale: print(','.join(stale))
" 2>/dev/null)
  if [ -n "$OOO_STALE" ]; then
    TEST_INFRA="${TEST_INFRA}[FAIL] slack-channels.md: expired OoO note(s) — back date(s) passed: ${OOO_STALE}. Clear them.\n"
    CURRENT_FAILURES="${CURRENT_FAILURES}slack-channels.md: expired OoO note(s)\n"
  else
    TEST_INFRA="${TEST_INFRA}[PASS] slack-channels.md: no expired OoO notes\n"
  fi
fi

# Content-level checks: URGENT flags older than 14 days in projects.md
PROJECTS_FILE="$MEMORY_DIR/projects.md"
if [ -f "$PROJECTS_FILE" ] && grep -q "URGENT" "$PROJECTS_FILE"; then
  # Get file modification time in days
  PROJECTS_AGE=$(python3 -c "import os,time; print(int((time.time()-os.path.getmtime('$PROJECTS_FILE'))/86400))" 2>/dev/null || echo 0)
  if [ "${PROJECTS_AGE:-0}" -gt 14 ] 2>/dev/null; then
    TEST_INFRA="${TEST_INFRA}[FAIL] projects.md: URGENT flag present but file is ${PROJECTS_AGE}d old — review if still urgent.\n"
    CURRENT_FAILURES="${CURRENT_FAILURES}projects.md: stale URGENT flag\n"
  else
    TEST_INFRA="${TEST_INFRA}[PASS] projects.md: URGENT flag present, file fresh (${PROJECTS_AGE}d)\n"
  fi
fi

# Content-level checks: agent definitions that should read voice.md
VOICE_AGENTS=("standup-writer" "ghost")
for agent_name in "${VOICE_AGENTS[@]}"; do
  agent_file="$CLAUDE_DIR/agents/${agent_name}.md"
  if [ -f "$agent_file" ]; then
    if grep -q "voice.md" "$agent_file"; then
      TEST_INFRA="${TEST_INFRA}[PASS] ${agent_name}.md: reads voice.md\n"
    else
      TEST_INFRA="${TEST_INFRA}[FAIL] ${agent_name}.md: does NOT read voice.md — voice drift risk\n"
      CURRENT_FAILURES="${CURRENT_FAILURES}${agent_name}.md: missing voice.md read\n"
    fi
  fi
done

# Agent frontmatter validity
AGENT_VALID=0; AGENT_INVALID=0
for agent in "$CLAUDE_DIR/agents"/*.md; do
  [ -f "$agent" ] || continue
  if head -5 "$agent" | grep -q "^name:"; then
    AGENT_VALID=$((AGENT_VALID + 1))
  else
    AGENT_INVALID=$((AGENT_INVALID + 1))
    CURRENT_FAILURES="${CURRENT_FAILURES}agent bad frontmatter: $(basename "$agent")\n"
  fi
done
if [ "$AGENT_INVALID" -gt 0 ]; then
  TEST_INFRA="${TEST_INFRA}[FAIL] agents: ${AGENT_INVALID} missing name frontmatter\n"
else
  TEST_INFRA="${TEST_INFRA}[PASS] agent definitions: ${AGENT_VALID} valid\n"
fi

# --- Behavioral: write-session-note.sh ---
LOG_RECENT=$(find "$LOG_DIR" -maxdepth 1 -name "*.md" -mtime -7 2>/dev/null \
  | grep -v "compact\|eod\|commits\|changes\|dashboard" | wc -l | tr -d ' ')
if [ "${LOG_RECENT:-0}" -eq 0 ] 2>/dev/null; then
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[FAIL] write-session-note.sh: 0 journals in last 7 days\n"
  CURRENT_FAILURES="${CURRENT_FAILURES}write-session-note.sh: 0 journals\n"
else
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[PASS] write-session-note.sh: ${LOG_RECENT} journals (last 7 days)\n"
fi

# --- Behavioral: journal quality ---
if [ "${STUB_PCT:-0}" -gt 20 ] 2>/dev/null; then
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[WARN] journal quality: ${STUB_COUNT:-0} stubs (${STUB_PCT:-0}% of log/) are under 300 bytes — likely unfilled session notes\n"
  CURRENT_FAILURES="${CURRENT_FAILURES}journal quality: ${STUB_PCT:-0}% stubs\n"
else
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[PASS] journal quality: ${STUB_COUNT:-0} stubs out of $((${STUB_COUNT:-0} + ${STUB_PCT:-0})) checked\n"
fi

# --- Behavioral: decision-backlink.sh ---
if [ "$DEC_COUNT" -gt 5 ] 2>/dev/null && [ "$BACKLINK_COUNT" -eq 0 ] 2>/dev/null; then
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[FAIL] decision-backlink.sh: ${DEC_COUNT} decisions, 0 backlinks\n"
  CURRENT_FAILURES="${CURRENT_FAILURES}decision-backlink.sh: 0 backlinks\n"
else
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[PASS] decision-backlink.sh: ${BACKLINK_COUNT} backlinks for ${DEC_COUNT} decisions\n"
fi

# --- Behavioral: QMD index (auto-fix if stale; sentinel at ~/.claude/.qmd-last-refresh) ---
if [ "${QMD_AGE:-999}" -gt 45 ] 2>/dev/null; then
  if command -v qmd &>/dev/null && qmd update 2>/dev/null && qmd embed 2>/dev/null; then
    touch "$QMD_SENTINEL"
    AUTOFIX_LOG="${AUTOFIX_LOG}[AUTO-FIXED] QMD was ${QMD_AGE}min stale, refreshed\n"
  else
    TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[FAIL] QMD ${QMD_AGE}min stale, auto-refresh failed\n"
    CURRENT_FAILURES="${CURRENT_FAILURES}QMD auto-refresh failed\n"
  fi
else
  TEST_BEHAVIORAL="${TEST_BEHAVIORAL}[PASS] QMD fresh (${QMD_AGE}min ago)\n"
fi

# --- Resolution tracking ---
RESOLVED_SECTION=""
if [ -n "$PREV_FAILURES_LIST" ]; then
  while IFS= read -r prev; do
    [ -z "$prev" ] && continue
    if ! printf "%s" "$CURRENT_FAILURES" | grep -qF "$prev"; then
      RESOLVED_SECTION="${RESOLVED_SECTION}[RESOLVED] ${prev}\n"
    fi
  done <<< "$PREV_FAILURES_LIST"
fi

# --- Build previous_failures YAML for next run ---
PF_YAML=""
if [ -n "$CURRENT_FAILURES" ]; then
  while IFS= read -r fail; do
    [ -z "$fail" ] && continue
    PF_YAML="${PF_YAML}  - \"${fail}\"\n"
  done <<< "$CURRENT_FAILURES"
fi

# Compound effectiveness V1: pattern velocity only
COMPOUND_FILE=$(mktemp /tmp/vault-health-compound-XXXXXX.py)
cat > "$COMPOUND_FILE" << 'PYEOF'
import re, os
from datetime import date, timedelta

patterns_file = os.path.expanduser('~/.claude/memory/patterns.md')
if not os.path.exists(patterns_file):
    print('patterns.md not found')
    exit()

content = open(patterns_file).read()
entries = re.findall(r'^### (.+?) \^pat-', content, re.MULTILINE)
dates = re.findall(r'\*\*Date:\*\* (\d{4}-\d{2}-\d{2})', content)

today = date.today()
recent_30 = sum(1 for d in dates if d >= str(today - timedelta(days=30)))
recent_7 = sum(1 for d in dates if d >= str(today - timedelta(days=7)))

print(f'Total patterns: {len(entries)}')
print(f'Velocity — last 30 days: {recent_30} | last 7 days: {recent_7}')
print('(Recurrence detection requires structured Root Cause field — see V2)')
PYEOF
COMPOUND_STATS=$(python3 "$COMPOUND_FILE")
rm -f "$COMPOUND_FILE"

# ============================================================
# Write health.md atomically
# ============================================================

TMPFILE=$(mktemp /tmp/vault-health-XXXXXX.md)

{
echo "---"
echo "generated: ${NOW}"
echo "warnings: ${TOTAL_WARNINGS}"
echo "previous_failures:"
[ -n "$PF_YAML" ] && printf "%b" "$PF_YAML"
echo "---"
echo ""
echo "# Vault Health — ${NOW}"
echo ""
echo "## File Staleness"
echo "| File | Last Modified | Status | Suggested Action | Safety |"
echo "|------|--------------|--------|-----------------|--------|"
echo "$STALENESS_TABLE"
echo ""
echo "## Today's Plan"
echo "Status: ${PLAN_STATUS}"
echo ""
echo "## decisions.md"
echo "${DEC_STATUS}"
echo ""
echo "## learn/ Coverage (${CURRENT_MONTH})"
echo "$LEARN_LINES"
echo ""
echo "## Promotion Case Synthesis"
echo "${CASE_STATUS}"
echo ""
echo "## Skill Freshness"
echo "| Skill | Last Used | Days | Status |"
echo "|-------|-----------|------|--------|"
echo "$SKILL_TABLE"
echo ""
echo "## System Tests"
echo "Last run: ${NOW}"
echo ""
echo "### Infrastructure"
printf "%b" "$TEST_INFRA"
echo ""
echo "### Behavioral Signals"
printf "%b" "$TEST_BEHAVIORAL"
if [ -n "$AUTOFIX_LOG" ]; then
  echo ""
  echo "### Auto-Fixes Applied"
  printf "%b" "$AUTOFIX_LOG"
fi
if [ -n "$RESOLVED_SECTION" ]; then
  echo ""
  echo "### Resolved Since Last Run"
  printf "%b" "$RESOLVED_SECTION"
fi
echo ""
echo "## Compound Effectiveness (V1)"
printf '%s\n' "$COMPOUND_STATS"
} > "$TMPFILE"

mv "$TMPFILE" "$HEALTH_FILE"
exit 0
