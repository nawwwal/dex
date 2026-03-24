# 5F Design Reviewer - Installation Guide

## Quick Install

**For Claude Code users:**

```bash
# 1. Download the skill
git clone https://github.com/YOUR-USERNAME/5F-design-reviewer.git

# 2. Copy to your Compass skills folder
cp -r 5F-design-reviewer ~/.claude/plugins/cache/compass/compass/unknown/skills/

# 3. Reload Claude Code
# In Claude Code, type: /reload
```

---

## Alternative: Manual Installation

**If you received a ZIP file:**

1. Download `5F-design-reviewer.zip`
2. Unzip the file
3. Copy the `5F-design-reviewer/` folder to:
   - **Mac/Linux:** `~/.claude/plugins/cache/compass/compass/unknown/skills/`
   - **Windows:** `%USERPROFILE%\.claude\plugins\cache\compass\compass\unknown\skills\`
4. Restart Claude Code or run `/reload`

---

## Verify Installation

Type this in Claude Code:

```
Show me available skills
```

You should see `reviewing-designs-5f` in the list.

---

## First Use

Try it out:

```
Review this design using 5F Framework
```

Then share:
- Figma design URL, OR
- Screenshot of design

Claude will:
1. Ask 6 clarifying questions
2. Offer mood selection (Strategic/Creative/Critical)
3. Launch 3 sub-agents for analysis
4. Return prioritized recommendations with RICE scores

---

## Requirements

- **Claude Code** installed
- **Optional:** HeyMarvin MCP for evidence-backed user stories
  - Without HeyMarvin: Research gaps will be flagged
  - With HeyMarvin: User stories include actual research quotes

---

## Troubleshooting

### "Skill not found"
- Check the folder is in the correct location
- Folder name must be `5F-design-reviewer`
- Run `/reload` in Claude Code

### "Sub-agent failed"
- Check `references/sub-agents/` folder exists
- All 5 sub-agent files must be present:
  - `5f-reviewer.md`
  - `prioritizer-strategist.md`
  - `story-generator.md`
  - `ORCHESTRATION-GUIDE.md`
  - `README.md`

### "HeyMarvin unavailable"
- This is normal if you don't have HeyMarvin MCP configured
- Agent 3 will flag all gaps as "Research needed"
- Design review still works without HeyMarvin

---

## Support

- **Documentation:** See `CHANGELOG.md` for v2.0 features
- **Architecture:** Read `references/sub-agents/README.md`
- **Examples:** Check `references/EXAMPLE-*.md` files

---

**Version:** 2.0 (2026-03-09)
**License:** Internal use at Razorpay (or specify your license)
