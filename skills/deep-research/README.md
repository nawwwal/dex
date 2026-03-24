# 🔬 Deep Research Skill for Claude Code

**Automated research that analyzes 50+ YouTube videos and 20+ web articles to generate comprehensive markdown summaries**

## Why This Exists

### The Problem
- Claude Code's built-in search is great for code, but lacks depth for learning new domains
- Most technical tutorials and insights are on YouTube, but hard to search and synthesize
- NotebookLM is powerful but requires manual source uploading
- Getting depth on a topic manually takes hours of watching videos and reading articles

### The Solution
This skill automates the entire research workflow:
1. **Searches YouTube** for 50+ relevant videos and extracts transcripts
2. **Searches the web** for 20+ authoritative articles
3. **Creates NotebookLM notebook** and uploads all sources automatically
4. **Generates comprehensive summary** (10 sections, 3,500+ words)
5. **Saves to Obsidian-compatible markdown** for your knowledge base

**Result:** 10-30 minutes to get expert-level understanding of any topic

---

## What You Get

### Input
```
"Research API design best practices"
```

### Output
```
📄 Summary (3,500 words):
  ├─ Key Themes & Core Concepts
  ├─ Best Practices & Methodologies
  ├─ Common Mistakes & Pitfalls
  ├─ Expert Insights & Notable Quotes
  ├─ Practical Applications & Use Cases
  ├─ Emerging Trends & Future Directions
  ├─ Technical Details & Specifications
  ├─ Points of Disagreement
  ├─ Knowledge Gaps & Open Questions
  └─ Learning Progression

🔗 NotebookLM Notebook (61 sources):
  ├─ 43 YouTube videos with transcripts
  └─ 18 authoritative articles

💾 Obsidian-Ready:
  ├─ Markdown formatted
  ├─ Internal links
  └─ Citations & references
```

---

## Real-World Example

**Topic:** "Fintech fraud defense beyond MFA"

**Sources Analyzed:**
- 18 YouTube videos (fraud detection ML, AI security, cybersecurity)
- 64 articles (Visa, Mastercard, FIDO Alliance, IBM, McKinsey, Federal Reserve)

**Output:**
- 35,000-word executive summary
- Emerging fraud patterns (deepfakes, synthetic IDs, account takeover)
- Defense strategies (passkeys, behavioral biometrics, AI detection)
- Industry case studies (JPMorgan 40% fraud reduction)
- Implementation roadmap

**Time:** 25 minutes automated vs. 10+ hours manual

---

## One-Click Installation

### Prerequisites
- macOS or Linux
- Python 3.8+
- Google account (for NotebookLM)

### Install

```bash
# Clone or download this skill
cd /path/to/youtube-research

# Run installer
chmod +x install.sh
./install.sh
```

**What it installs:**
- ✓ Python packages (yt-dlp, notebooklm-py, beautifulsoup4, etc.)
- ✓ Node.js/Deno (if not already installed, prompts for manual install)
- ✓ Playwright browser automation
- ✓ NotebookLM authentication (opens browser for Google login)
- ✓ Vault directory for research outputs

**Installation time:** 5-10 minutes

---

## Usage

### Option 1: Via Claude Code (Recommended)

Just ask:
```
Research API design best practices
Deep dive into prompt engineering
Learn about distributed systems architecture
```

Claude automatically runs the entire workflow and saves the summary.

### Option 2: Manual Execution

```bash
# 1. Set your topic
TOPIC="your research topic"

# 2. Run the workflow
python3 scripts/search_youtube.py "$TOPIC" output/youtube.json --max-results 50
# (Use Claude's WebSearch to get URLs, save to urls.json)
python3 scripts/search_web.py output/urls.json output/web.json
python3 scripts/notebooklm_research.py "$TOPIC" \
  output/youtube.json \
  output/web.json \
  references/deep-research-prompt.md \
  output/summary.md
```

---

## Configuration

Edit `.env` to customize:

```bash
# Number of YouTube videos to search
YOUTUBE_MAX_RESULTS=50  # Default: 50, Range: 10-100

# Number of web articles to find
WEB_MAX_RESULTS=20      # Default: 20, Range: 5-30

# NotebookLM analysis timeout
NOTEBOOKLM_TIMEOUT=1800 # Default: 30 min, Range: 15-60 min

# Minimum video duration (seconds)
MIN_VIDEO_DURATION=120  # Default: 2 min

# Minimum article word count
MIN_ARTICLE_WORDS=300   # Default: 300 words
```

**Presets:**
- **Fast:** 20 videos, 10 articles, 15 min timeout → 10-15 min
- **Balanced:** 50 videos, 20 articles, 30 min timeout → 20-30 min (default)
- **Deep:** 100 videos, 30 articles, 60 min timeout → 45-60 min

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│ 1. User Request: "Research [topic]"                    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 2. Claude Code creates directory & slug                 │
│    /Vault/{topic-slug}/                                 │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────┐    ┌─────────▼────────┐
│ 3a. YouTube  │    │ 3b. Web Search   │
│  search_     │    │  (WebSearch MCP) │
│  youtube.py  │    │                  │
│              │    │  search_web.py   │
│ yt-dlp       │    │  beautifulsoup4  │
│ extracts     │    │  readability     │
│ transcripts  │    │  html2text       │
└───────┬──────┘    └─────────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 4. notebooklm_research.py                               │
│                                                          │
│  ┌─────────────────────────────────────────┐            │
│  │ Create NotebookLM notebook              │            │
│  └───────────────┬─────────────────────────┘            │
│                  │                                       │
│  ┌───────────────▼─────────────────────────┐            │
│  │ Upload YouTube transcripts (text)       │            │
│  │ Upload YouTube URLs (no transcript)     │            │
│  │ Upload web articles (text)              │            │
│  └───────────────┬─────────────────────────┘            │
│                  │                                       │
│  ┌───────────────▼─────────────────────────┐            │
│  │ Trigger deep research analysis          │            │
│  │ (NotebookLM AI processes all sources)   │            │
│  └───────────────┬─────────────────────────┘            │
│                  │                                       │
│  ┌───────────────▼─────────────────────────┐            │
│  │ Generate 10-section markdown summary    │            │
│  └───────────────┬─────────────────────────┘            │
└──────────────────┼──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 5. Output:                                              │
│  ✓ /Vault/{topic}/summary-{date}.md                     │
│  ✓ /Vault/{topic}/notebook_id.txt                       │
│  ✓ NotebookLM URL for interactive research              │
└─────────────────────────────────────────────────────────┘
```

### Key Technologies

- **yt-dlp:** YouTube video metadata and transcript extraction
- **notebooklm-py:** Unofficial NotebookLM API client (browser automation)
- **BeautifulSoup4 + readability:** Web content extraction
- **Playwright:** Browser automation for NotebookLM authentication
- **Claude Code WebSearch MCP:** Finding relevant web articles

---

## Output Structure

### File Organization
```
~/Documents/Work related/Claude code/Vault/
└── {topic-slug}/
    ├── summary-2026-03-18.md     ← Main output (Obsidian-ready)
    ├── notebook_id.txt            ← NotebookLM notebook ID
    └── temp/
        ├── youtube_sources.json   ← Video metadata + transcripts
        └── web_sources.json       ← Article content
```

### Summary Format

Each summary includes:

1. **Metadata**
   - Research date
   - Source count (videos + articles)
   - NotebookLM link

2. **10 Comprehensive Sections**
   - Key Themes & Core Concepts
   - Best Practices & Methodologies
   - Common Mistakes & Pitfalls
   - Expert Insights & Notable Quotes
   - Practical Applications & Use Cases
   - Emerging Trends & Future Directions
   - Technical Details & Specifications
   - Points of Disagreement
   - Knowledge Gaps & Open Questions
   - Learning Progression

3. **Citations**
   - All sources linked
   - YouTube video URLs
   - Article URLs
   - Timestamp references

---

## Use Cases

### Product Management
- Competitive research (analyze competitor demos, customer reviews)
- Market trends (fintech innovations, regulatory changes)
- Best practices (product frameworks, strategy templates)

### Engineering
- Learning new technologies (React Server Components, Rust async)
- Architecture patterns (microservices, event-driven systems)
- Tool evaluations (CI/CD platforms, observability tools)

### Design
- Design systems (component libraries, accessibility patterns)
- User research (UX case studies, usability principles)
- Tools & techniques (Figma plugins, prototyping methods)

### Leadership
- Industry trends (AI impact on SaaS, remote work evolution)
- Management frameworks (OKRs, team topologies)
- Strategic planning (GTM strategies, pricing models)

---

## Obsidian Integration

### Setup

1. **Add Vault to Obsidian:**
   - Open Obsidian
   - "Open folder as vault"
   - Select: `~/Documents/Work related/Claude code/Vault/`

2. **Recommended Plugins:**
   - Dataview (query research by topic/date)
   - Graph view (visualize knowledge connections)
   - Tag wrangler (organize by research areas)

3. **Folder Structure:**
```
Vault/
├── api-design-best-practices/
│   └── summary-2026-03-10.md
├── fraud-detection-ai/
│   └── summary-2026-03-16.md
└── product-management-frameworks/
    └── summary-2026-03-12.md
```

### Workflow

1. Research with Claude Code: `Research [topic]`
2. Summary appears in Obsidian automatically
3. Create notes linking to research
4. Build knowledge graph over time

---

## Verification

Check installation:
```bash
./verify.sh
```

Expected output:
```
✓ Python 3: 3.x.x
✓ pip3: xx.x.x
✓ yt-dlp: 2026.xx.xx
✓ Node.js: v20.x.x (or Deno)
✓ notebooklm-py: installed
✓ beautifulsoup4: installed
✓ playwright: installed
✓ All dependencies OK
✓ Vault directory exists
✓ Test YouTube search: SUCCESS
```

---

## Troubleshooting

### Common Issues

#### 1. "yt-dlp: command not found"
```bash
pip3 install -U yt-dlp
```

#### 2. "ERROR: js-interpreter not found"
yt-dlp needs Node.js or Deno for YouTube:
```bash
# macOS
brew install node

# Ubuntu
sudo apt install nodejs
```

#### 3. "NotebookLM authentication failed"
Re-authenticate:
```bash
notebooklm login
```

#### 4. "No videos with transcripts found"
- Normal - some videos disable captions
- Videos without transcripts are uploaded as URLs (NotebookLM processes them)
- Try different search terms
- Check `temp/youtube_sources.json` for results

#### 5. "Module not found" errors
Reinstall dependencies:
```bash
pip3 install -r scripts/requirements.txt
playwright install chromium
```

#### 6. "NotebookLM timeout"
- Research still running in background
- Check notebook URL manually
- Increase timeout in `.env`:
  ```bash
  NOTEBOOKLM_TIMEOUT=3600  # 1 hour
  ```

---

## Limitations

### Current Constraints

1. **NotebookLM API**
   - Uses unofficial API (may break with Google updates)
   - Requires browser automation (slower than official API)
   - Rate limits unknown (be conservative)

2. **YouTube**
   - Only videos with available transcripts (auto-captions or manual)
   - Videos without transcripts uploaded as URLs (NotebookLM processes)
   - Regional restrictions may affect availability

3. **Web Content**
   - Paywalled content cannot be extracted
   - Some sites block automated scraping (403 errors)
   - Dynamic content may not be fully captured

4. **Processing Time**
   - NotebookLM analysis takes 10-30 minutes
   - Cannot be paused/resumed
   - Must complete in single session

### Future Enhancements

Potential improvements (not yet implemented):
- ✨ PDF research paper support
- ✨ Google Docs integration
- ✨ Podcast transcript extraction
- ✨ Multi-language support
- ✨ Incremental research (add to existing notebooks)
- ✨ Custom research frameworks
- ✨ Team collaboration (shared notebooks)

---

## Privacy & Security

### Data Flow

1. **YouTube transcripts:** Extracted locally, uploaded to NotebookLM
2. **Web content:** Extracted locally, uploaded to NotebookLM
3. **NotebookLM:** Stored in your Google account (subject to Google's privacy policy)
4. **Local summaries:** Stored only on your machine

### Authentication

- **NotebookLM:** Google OAuth via browser automation (credentials stored locally)
- **No API keys required:** Uses browser session cookies
- **No tracking:** Skill doesn't send data anywhere except NotebookLM

### Recommendations

- ✓ Use a dedicated Google account for NotebookLM
- ✓ Review NotebookLM privacy settings
- ✓ Don't research sensitive/confidential topics
- ✓ Local summaries are yours - back up your Vault

---

## Contributing

This skill was created to solve a specific research workflow problem. If you find it useful and want to enhance it:

### Contribution Ideas
- 🐛 Bug fixes for yt-dlp errors
- 📚 Additional research frameworks (beyond 10-section default)
- 🌐 Better web content extraction
- ⚡ Performance optimizations
- 📖 Documentation improvements

### Sharing

If you modify this skill:
1. Keep the core workflow intact
2. Document new features clearly
3. Share back improvements
4. Credit original source

---

## FAQ

### How much does this cost?
**Free.** Uses unofficial NotebookLM API (Google's free tier). Only costs are your time and electricity.

### How long does it take?
**10-30 minutes** typically. Fast mode: 10-15 min, Deep mode: 45-60 min.

### Can I stop and resume?
**No.** Must complete in one session. NotebookLM doesn't support pausing analysis.

### How many sources can it handle?
**Tested up to 100+** sources. NotebookLM can handle hundreds. Practical limit is time.

### What if I research the same topic twice?
Skill **reuses existing notebook** if found. New sources are added, summary updated.

### Can I use this for work?
**Yes**, but consider:
- Don't research confidential topics (uses Google's NotebookLM)
- Check company policies on AI tool usage
- Summaries are yours to use as needed

### Why not use ChatGPT/Claude directly?
**Depth.** This combines 50+ videos + 20+ articles. LLMs alone can't match the breadth of real sources.

### Can I customize the research framework?
**Yes.** Edit `references/deep-research-prompt.md` to change the 10-section format.

---

## Credits

**Created by:** Renju Balu (PM, Razorpay)

**Built with:**
- yt-dlp (YouTube extraction)
- notebooklm-py (NotebookLM API)
- BeautifulSoup4 (web scraping)
- Playwright (browser automation)
- Claude Code (orchestration)

**Inspiration:**
The need for deeper research than Claude Code search alone provides, especially for learning from YouTube tutorials and synthesizing diverse sources.

---

## License

MIT License - Use freely, modify as needed, share improvements.

---

## Support

### Getting Help

1. **Check verification:** `./verify.sh`
2. **Review error messages:** Most are self-explanatory
3. **Check QUICKSTART.md:** Step-by-step usage guide
4. **See SKILL.md:** Technical implementation details

### Community

Share your research results, improvements, or use cases:
- Internal Slack: `#claude-code-skills`
- GitHub: (if open-sourced)

---

## Quick Reference

### Installation
```bash
chmod +x install.sh && ./install.sh
```

### Usage (Claude Code)
```
Research [your topic]
```

### Manual Execution
```bash
python3 scripts/search_youtube.py "topic" out/yt.json --max-results 50
python3 scripts/search_web.py out/urls.json out/web.json
python3 scripts/notebooklm_research.py "topic" out/yt.json out/web.json references/deep-research-prompt.md out/summary.md
```

### Verification
```bash
./verify.sh
```

### Configuration
```bash
# Edit .env for custom settings
YOUTUBE_MAX_RESULTS=50
WEB_MAX_RESULTS=20
NOTEBOOKLM_TIMEOUT=1800
```

### Output Location
```
~/Documents/Work related/Claude code/Vault/{topic-slug}/summary-{date}.md
```

---

**Ready to start researching? Run `./install.sh` and ask Claude Code: "Research [your topic]"**
