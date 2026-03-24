# How to Share the 5F Design Reviewer Skill

## Overview

The 5F Design Reviewer is a Claude Code skill that can be shared with other teams, designers, and PMs. Choose the method that fits your distribution needs.

---

## Option 1: ZIP Package (Easiest for Internal Teams)

**Best for:** Sharing with Razorpay colleagues via Slack/Drive

### What's Included in the ZIP
- `SKILL.md` - Main orchestrator (626 lines)
- `references/sub-agents/` - 3 specialized agents (5 files)
- `references/` - 5F Framework documentation, examples
- `CHANGELOG.md` - v2.0 redesign details
- `README.md` - Quick start guide
- `INSTALLATION.md` - Setup instructions

### How to Share

**Step 1: Get the ZIP**
```bash
# Already created at:
${CLAUDE_PLUGIN_ROOT}/skills/5F-design-reviewer.zip
```

**Step 2: Upload to Slack/Drive**
- Slack: Post in #pm-tools or #design-team with message:
  ```
  🎨 5F Design Reviewer v2.0 is ready!

  - Sub-agent architecture (3 specialized agents)
  - RICE prioritization framework
  - Evidence-backed recommendations via HeyMarvin
  - 60% faster, scannable output

  Installation: Unzip to your Compass skills folder, run /reload
  See INSTALLATION.md for details
  ```

- Google Drive: Upload to shared folder, add comment with install instructions

**Step 3: Recipients Install**
See `INSTALLATION.md` for detailed steps.

---

## Option 2: GitHub Repository (Best for External/Public Sharing)

**Best for:** Open-source distribution, version control, collaboration

### Setup GitHub Repo

**Step 1: Create Repository**
```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/5F-design-reviewer"

# Initialize git (if not already in a repo)
git init
git add .
git commit -m "Initial commit: 5F Design Reviewer v2.0"

# Create repo on GitHub, then push
git remote add origin https://github.com/YOUR-USERNAME/5F-design-reviewer.git
git branch -M main
git push -u origin main
```

**Step 2: Add GitHub Documentation**
- Create a GitHub README (use existing `README.md`)
- Add topics/tags: `claude-code`, `design-review`, `b2b-saas`, `ux`, `rice-framework`
- Add license file (MIT, Apache 2.0, or proprietary)

**Step 3: Share the Repo**
- Share URL: `https://github.com/YOUR-USERNAME/5F-design-reviewer`
- Recipients clone and install (see `INSTALLATION.md`)

### GitHub Features You Get
- ✅ Version control (track changes, rollbacks)
- ✅ Issues (users can report bugs, request features)
- ✅ Pull requests (community contributions)
- ✅ Releases (versioned distributions)
- ✅ GitHub Actions (automated testing)
- ✅ Documentation site (GitHub Pages)

---

## Option 3: Claude Code Marketplace (Future)

**Status:** Not yet available
**When available:** Skills will be installable via Claude Code UI

Once the marketplace launches, you'll be able to:
1. Submit skill for review
2. Get listed in official marketplace
3. Users install with one click

For now, use Option 1 or 2.

---

## What Recipients Need

### Minimum Requirements
- **Claude Code** installed
- **Compass plugin** configured
- No other dependencies

### Optional (for full features)
- **HeyMarvin MCP** - For evidence-backed user stories
  - Without it: Agent 3 flags research gaps
  - With it: Agent 3 includes real user quotes

### No Installation Needed
- No Python packages
- No npm dependencies
- No API keys (except HeyMarvin MCP if desired)

---

## Support & Maintenance

### If Users Have Issues

**Common issues:**
1. **"Skill not loading"**
   - Check folder location
   - Run `/reload` in Claude Code
   - Verify `SKILL.md` has correct frontmatter

2. **"Sub-agent failed"**
   - Check all 5 files exist in `references/sub-agents/`
   - Check file permissions (should be readable)

3. **"HeyMarvin not working"**
   - This is expected if they don't have HeyMarvin MCP
   - Skill works without it (flags research gaps instead)

### Version Updates

When you improve the skill:
1. Update `CHANGELOG.md` with new version
2. Re-create ZIP package
3. Re-share via same channels
4. Or: Push to GitHub, users pull updates

---

## Recommended Sharing Message

**For Slack/Internal:**
```
🎨 Introducing: 5F Design Reviewer v2.0

A Claude Code skill that reviews B2B SaaS designs using the 5F Framework
(Fast, Focused, Fun, Fluent, Fair) with evidence-backed prioritization.

✨ What's New in v2.0:
- 3 specialized sub-agents (parallel analysis)
- RICE prioritization (UX-centered Impact scoring)
- HeyMarvin integration (evidence-backed user stories)
- Problem-first output (scannable in 60 seconds)
- 75% reduction in context size

📥 Install: [Attach 5F-design-reviewer.zip]
📖 Docs: See INSTALLATION.md inside the ZIP

Try it: "Review this design using 5F Framework"
```

**For GitHub/External:**
```markdown
# 5F Design Reviewer

A Claude Code skill for evidence-based B2B SaaS design critique using the
5F Framework (Fast, Focused, Fun, Fluent, Fair).

## Features
- 🎯 Problem-first output (top 3 issues highlighted)
- 📊 RICE prioritization (user experience-centered)
- 🔍 Evidence-backed recommendations via HeyMarvin
- 🚀 Sub-agent architecture (3 specialized agents)
- 📈 Market-specific insights (Indian B2B SaaS)

## Installation
See [INSTALLATION.md](INSTALLATION.md)

## Usage
```bash
# In Claude Code
Review this design using 5F Framework
```

## License
[Your license here]
```

---

## Analytics (Optional)

To track usage internally:
1. Add telemetry to `SKILL.md` (with user consent)
2. Track metrics:
   - Number of reviews per week
   - Most common design issues found
   - RICE score distribution
   - HeyMarvin evidence coverage

Or: Use GitHub stars/clones as proxy metrics.

---

## Next Steps

**To share now:**
1. ✅ ZIP package already created (`5F-design-reviewer.zip`)
2. Upload to Slack/Drive with installation message
3. Share `INSTALLATION.md` for setup help

**To share on GitHub:**
1. Create GitHub repo
2. Push skill files
3. Add README, LICENSE
4. Share repo URL

**To maintain:**
1. Monitor user feedback
2. Update `CHANGELOG.md` for each version
3. Re-share updated ZIP or push to GitHub

---

**Questions?** See `CHANGELOG.md` for v2.0 architecture details, or read
`references/sub-agents/README.md` for how the orchestration works.
