# YouTube Research - Quick Start Guide

## 30-Second Overview

**What:** Automated research that analyzes 50+ YouTube videos + 20+ articles → generates comprehensive markdown summary

**How:** Ask Claude Code: "Research [your topic]"

**Time:** 10-30 minutes

**Output:** `$HOME/.claude/work/deep-research/{topic}/summary-{date}.md`

---

## First-Time Setup (5 minutes)

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/deep-research
./setup.sh
```

**What it does:**
- ✓ Installs Python packages
- ✓ Installs yt-dlp (YouTube extractor)
- ✓ Installs Playwright (browser automation)
- ✓ Sets up NotebookLM authentication
- ✓ Creates Vault directory

**You'll need:**
- Python 3.8+
- Node.js or Deno (for yt-dlp)
- Google account (for NotebookLM)

---

## Basic Usage

### Option 1: Via Claude Code (Recommended)

Just ask:
```
Research API design best practices
Deep dive into prompt engineering
Learn about distributed systems
```

Claude automatically:
1. Searches YouTube for videos
2. Extracts all transcripts
3. Finds web articles
4. Creates NotebookLM notebook
5. Uploads sources
6. Runs analysis
7. Generates summary

### Option 2: Manual Execution

```bash
# 1. Search YouTube
python3 scripts/search_youtube.py \
  "your topic" \
  "$HOME/.claude/work/deep-research/test/youtube.json" \
  --max-results 50

# 2. Get web URLs (use Claude's WebSearch or manual list)
cat > $HOME/.claude/work/deep-research/test/urls.json << 'EOF'
{
  "query": "your topic",
  "urls": ["https://...", "https://..."]
}
EOF

# 3. Extract web content
python3 scripts/search_web.py \
  "$HOME/.claude/work/deep-research/test/urls.json" \
  "$HOME/.claude/work/deep-research/test/web.json"

# 4. Run NotebookLM research
python3 scripts/notebooklm_research.py \
  "your topic" \
  "$HOME/.claude/work/deep-research/test/youtube.json" \
  "$HOME/.claude/work/deep-research/test/web.json" \
  "references/deep-research-prompt.md" \
  "$HOME/.claude/work/deep-research/test/summary-2026-03-10.md"
```

---

## Example Output

**Input:** "Research API design best practices"

**Process:**
1. YouTube: 43 videos, 2.5 hours of content
2. Web: 18 articles, 45,000 words
3. NotebookLM: Analyzes 61 sources
4. Summary: 3,500 words, 10 sections

**Output file:** `$HOME/.claude/work/deep-research/api-design-best-practices/summary-2026-03-10.md`

**Sections:**
1. Key Themes & Core Concepts
2. Best Practices & Methodologies
3. Common Mistakes & Pitfalls
4. Expert Insights & Notable Quotes
5. Practical Applications & Use Cases
6. Emerging Trends & Future Directions
7. Technical Details & Specifications
8. Points of Disagreement
9. Knowledge Gaps & Open Questions
10. Learning Progression

---

## Configuration

Edit `.env` to customize:

```bash
# Fast mode (less comprehensive)
YOUTUBE_MAX_RESULTS=20
WEB_MAX_RESULTS=10
NOTEBOOKLM_TIMEOUT=900

# Balanced (recommended)
YOUTUBE_MAX_RESULTS=50
WEB_MAX_RESULTS=20
NOTEBOOKLM_TIMEOUT=1800

# Deep mode (very comprehensive)
YOUTUBE_MAX_RESULTS=100
WEB_MAX_RESULTS=30
NOTEBOOKLM_TIMEOUT=3600
```

---

## Common Issues

### "yt-dlp: command not found"
```bash
pip3 install -U yt-dlp
```

### "ERROR: js-interpreter not found"
```bash
brew install node
```

### "NotebookLM authentication failed"
```bash
notebooklm login
```

### "No videos with transcripts"
- Normal - some videos lack captions
- Try different search terms
- Script automatically skips them

### Module import errors
```bash
pip3 install -r scripts/requirements.txt
```

---

## Tips for Better Results

**✓ Good topics:**
- "REST API design patterns for microservices"
- "Product management frameworks for B2B"
- "React Server Components best practices 2024"

**✗ Avoid:**
- Too broad: "programming"
- Too niche: obscure technical terms
- Single word: "APIs"

**Best practices:**
- Be specific about technology/domain
- Include year for current trends
- Combine multiple aspects
- Use terms that would appear in video titles

---

## Verification

Check installation:
```bash
./verify.sh
```

Should see:
```
✓ Python 3: 3.x.x
✓ yt-dlp: 2026.xx.xx
✓ Node.js: v20.x.x
✓ All Python packages installed
✓ NotebookLM CLI installed
✓ Utils module working
✓ YouTube search working
✓ Vault directory exists
```

---

## File Locations

```
$HOME/.claude/work/deep-research/
└── {topic-slug}/
    ├── summary-2026-03-10.md    ← Main output
    └── temp/
        ├── youtube_sources.json  ← Video data
        └── web_sources.json      ← Article data
```

---

## Next Steps After Setup

1. Run verification: `./verify.sh`
2. Try a test research: Ask Claude "Research python tutorials"
3. Check output: `$HOME/.claude/work/deep-research/python-tutorials/summary-{date}.md`
4. Explore NotebookLM notebook for deeper analysis
5. Customize `.env` if needed

---

## Support

**Common questions:**
- How long does it take? 10-30 minutes typical
- Can I stop and resume? No, must complete in one session
- How much does it cost? Free (uses unofficial NotebookLM API)
- How many sources? 50+ videos, 20+ articles (configurable)

**For issues:**
1. Check `./verify.sh` output
2. Review error messages
3. See README.md troubleshooting section
4. Check logs in terminal output

---

## What Gets Created

**Per research session:**
- 1 NotebookLM notebook (online, accessible via URL)
- 1 markdown summary (local, in $HOME/.claude/work/deep-research/)
- 2 temp JSON files (can be deleted after)

**Storage:**
- Summaries: ~10-50 KB each
- Temp files: ~500 KB - 5 MB each
- NotebookLM: Stored in your Google account

---

## Workflow Diagram

```
User Request
    ↓
1. Generate slug & create directories
    ↓
2. PARALLEL:
   ├─→ Search YouTube (yt-dlp)
   │   └─→ Extract transcripts
   └─→ Search Web (WebSearch MCP)
       └─→ Extract article content
    ↓
3. Create NotebookLM notebook
    ↓
4. Upload sources (videos + articles)
    ↓
5. Trigger deep research analysis
    ↓
6. Generate markdown summary
    ↓
7. Report completion
    ↓
Output: $HOME/.claude/work/deep-research/{slug}/summary-{date}.md
```
