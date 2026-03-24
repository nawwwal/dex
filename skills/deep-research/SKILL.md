---
name: deep-research
description: "Use when researching a topic in depth — learning a new technical domain, competitive analysis, market research, or preparing strategy documents. Runs a yt-dlp + NotebookLM pipeline across 50+ YouTube videos and 20+ web articles."
---

# Deep Research Skill

## Overview

Automates research by searching YouTube (50+ videos) + web (20+ articles), uploading all sources to NotebookLM, then generating a 10-section markdown summary via the NotebookLM MCP.

**Time:** 10-30 minutes | **Output:** `~/.claude/work/deep-research/{topic-slug}/summary-{date}.md`

```
SKILL_DIR=${CLAUDE_PLUGIN_ROOT}/skills/deep-research
VAULT_DIR=$HOME/.claude/work/deep-research
PYTHON=$SKILL_DIR/.venv/bin/python3
```

## How It Works

### Step 1: Initialize

Set up variables and check for existing research:

```bash
SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/deep-research"
VAULT_DIR="$HOME/.claude/work/deep-research"
TOPIC="{user's topic}"
SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//;s/-$//')
TOPIC_DIR="$VAULT_DIR/$SLUG"

[ -d "$TOPIC_DIR" ] && echo "Existing research — will update" || echo "New topic"
[ -f "$TOPIC_DIR/notebook_id.txt" ] && echo "Notebook: https://notebooklm.google.com/notebook/$(cat $TOPIC_DIR/notebook_id.txt)"
mkdir -p "$TOPIC_DIR/temp"
```

### Step 2: Search YouTube

```bash
$SKILL_DIR/.venv/bin/python3 $SKILL_DIR/scripts/search_youtube.py \
  "$TOPIC" "$TOPIC_DIR/temp/youtube_sources.json" \
  --max-results 50 --min-duration 120
```

Videos without transcripts → URLs collected and uploaded directly to NotebookLM.

If < 10 videos found, continue but warn. Node.js error? `brew install node`.

### Step 3: Search Web

Use WebSearch MCP to collect 20-30 article URLs, then extract content:

```bash
cat > "$TOPIC_DIR/temp/web_urls.json" << EOF
{ "query": "$TOPIC", "urls": ["https://...", "https://..."] }
EOF

$SKILL_DIR/.venv/bin/python3 $SKILL_DIR/scripts/search_web.py \
  "$TOPIC_DIR/temp/web_urls.json" "$TOPIC_DIR/temp/web_sources.json" \
  --min-words 300
```

Skip articles that fail (paywall, 404). Continue with successful extractions.

### Step 4: Upload Sources + Generate Summary

**Hybrid approach** — Python handles notebook creation + source upload (needs one-time auth); NotebookLM MCP handles summarization (already authenticated in Claude Code).

**4a — Upload sources:**

```bash
# Use run_with_ssl.py wrapper (required for Zscaler corporate proxy)
$SKILL_DIR/.venv/bin/python3 $SKILL_DIR/scripts/run_with_ssl.py \
  $SKILL_DIR/scripts/notebooklm_research.py \
  "$TOPIC" \
  "$TOPIC_DIR/temp/youtube_sources.json" \
  "$TOPIC_DIR/temp/web_sources.json" \
  "$SKILL_DIR/references/deep-research-prompt.md" \
  "$TOPIC_DIR/summary-$(date +%Y-%m-%d).md" \
  --timeout 1800
```

This creates (or reuses) a notebook, uploads all sources, saves the notebook ID to `notebook_id.txt`, and may generate a summary. If auth fails: `$SKILL_DIR/.venv/bin/notebooklm login`.

**4b — Generate summary via MCP** (skip if 4a already wrote a summary):

Read `$SKILL_DIR/references/deep-research-prompt.md`, then call the `mcp__notebooklm__ask_question` tool with:
- `notebook_url`: `https://notebooklm.google.com/notebook/{id from notebook_id.txt}`
- `question`: contents of `deep-research-prompt.md`

Save the response to `$TOPIC_DIR/summary-$(date +%Y-%m-%d).md`.

### Step 5: Report

```
Research complete: {topic}
Sources: {N} YouTube videos + {M} web articles
Summary: ~/.claude/work/deep-research/{slug}/summary-{date}.md
NotebookLM: https://notebooklm.google.com/notebook/{id}
```

## Output Structure

```
~/.claude/work/deep-research/{topic-slug}/
  summary-2026-03-20.md   # 10-section summary
  notebook_id.txt         # reused on future runs
  temp/
    youtube_sources.json
    web_sources.json
```

**10 sections:** Key Themes, Best Practices, Common Mistakes, Expert Insights, Practical Applications, Emerging Trends, Technical Details, Disagreements, Knowledge Gaps, Learning Progression.

## Configuration

Edit `$SKILL_DIR/.env`:
- `YOUTUBE_MAX_RESULTS=50` (use 20 for faster, 100 for deeper)
- `WEB_MAX_RESULTS=20`
- `NOTEBOOKLM_TIMEOUT=1800` (use 3600 for large source sets)
- `MIN_VIDEO_DURATION=120`
- `MIN_ARTICLE_WORDS=300`

## Troubleshooting

**"yt-dlp not found"** — use full path: `${CLAUDE_PLUGIN_ROOT}/skills/deep-research/.venv/bin/yt-dlp`

**"js-interpreter not found"** — `brew install node`

**"NotebookLM auth failed"** — re-auth using agent-browser:
```bash
agent-browser --headed open https://notebooklm.google.com
# Sign in to Google in the browser window, wait for NotebookLM homepage
agent-browser state save ~/.notebooklm/storage_state.json
agent-browser close
```

**NotebookLM MCP auth** — use existing Chrome CDP connection:
```bash
# Find Chrome's active CDP port
cat ~/Library/Application\ Support/Google/Chrome/DevToolsActivePort
# Output: <port>\n<ws-path>
agent-browser connect "ws://localhost:<port><ws-path>"
agent-browser open "https://notebooklm.google.com/notebook/<id>"
```

**Zscaler SSL error with httpx** — always use `run_with_ssl.py` wrapper (already in skill). The wrapper patches `httpx.VERIFY_X509_STRICT` using `~/zscaler-combined-ca.pem`.

**"Module not found"**:
```bash
${CLAUDE_PLUGIN_ROOT}/skills/deep-research/.venv/bin/pip install -r \
  ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/scripts/requirements.txt
```

## Verification

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/deep-research
$S/.venv/bin/yt-dlp --version
$S/.venv/bin/python3 -c "import notebooklm, bs4, readability, html2text; print('OK')"
node --version || deno --version
```
