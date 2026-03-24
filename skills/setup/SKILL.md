---
name: setup
description: "Smart onboarding for dex vault system. Reads Slack/DevRev (with consent), generates personalized CLAUDE.md, scaffolds memory structure. Run once after installing the dex plugin."
---

# /dex:setup — Smart Onboarding

Generate a personalized vault system for the current user. Detective-first, question-last.

## Phase 1 — Local Detection (no external calls)

Check what already exists:

```
READ ~/.claude/CLAUDE.md       → if exists, extract identity (name, role, team)
READ ~/.claude/memory/          → list which files already exist
READ ~/.claude/settings.json    → check for leftover vault hooks that might double-fire
CHECK prerequisites:
  - python3 (required): which python3
  - jq (required): which jq
  - node (required): which node
  - Compass plugin installed (required): check enabledPlugins in settings.json for "compass@"
  - Figma MCP (optional): check for figma in enabledPlugins, warn if missing
```

If prerequisites missing: **STOP and print remediation steps.** Do not proceed with partial setup.

Report what was found:
> "Found: [existing files]. Missing prerequisites: [list with install commands]."

## Phase 2 — Ask Consent for External Reads

Before reading any external service, ask explicitly:

> "I can read your Slack and DevRev to personalize your setup — your name, team, active projects, communication style. This is optional. Allow Slack/DevRev reading? [Yes/No]"

- If **Yes**: proceed to read Slack MCP (display_name, channel list, 5 recent messages) and DevRev MCP (assigned issues, squad, role)
- If **No**: skip to Phase 3 with generic questions

## Phase 3 — Infer + Confirm

Only ask about things that couldn't be detected or inferred.

If external reads happened:
> "Based on your Slack profile, you're [name] on [team]. Correct?"
> "Your active DevRev issues are about [topics]. Main focus right now?"

If no external reads:
> "What's your full name?"
> "What's your role and team?"
> "What are you currently working on?"

Always ask:
> "Any project you want Claude to always remember?"
> "What's your GitHub username?"
> "What timezone are you in?"

## Phase 4 — Generate Files

Using the template at `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.template`:

1. **Replace template variables**:
   - `{{USER_NAME}}` → discovered/provided name
   - `{{ROLE}}` → discovered/provided role
   - `{{TEAM}}` → discovered/provided team
   - `{{GITHUB_USERNAME}}` → provided GitHub username
   - `{{LOCATION}}` → provided location
   - `{{TARGET_LEVEL}}` → provided career target (or remove section if not applicable)
   - `{{TIMEZONE}}` → provided timezone
   - `{{LEAVE_NOTE}}` → remove this line entirely for new users

2. **Write to `~/.claude/CLAUDE.md`** — but NEVER overwrite without asking:
   > "~/.claude/CLAUDE.md already exists. Overwrite? [Yes/No/Merge]"

3. **Create user-state directories** (skip if exists):
   ```
   mkdir -p ~/.claude/memory ~/.claude/career ~/.claude/log
   mkdir -p ~/.claude/sessions ~/.claude/config ~/.claude/work
   mkdir -p ~/.claude/archive ~/.claude/agent-memory
   mkdir -p ~/.claude/people ~/.claude/projects
   ```

4. **Scaffold memory files** from `${CLAUDE_PLUGIN_ROOT}/templates/memory-scaffolds/`:
   - Copy each file to `~/.claude/memory/` if it doesn't already exist
   - For pre-filled files (terms.md, razorpay-context.md, devrev.md, blade-taste.md, agent-onboarding.md, agent-protocol.md): copy as-is (shared Razorpay knowledge)
   - For slack-channels.md: if Slack MCP was read, populate with discovered channels; otherwise copy empty template
   - For voice.md: if Slack messages were read, extract 3-5 tone examples; otherwise copy empty template
   - For goals.md: if DevRev was read, populate with discovered active issues; otherwise copy empty template
   - **NEVER overwrite** existing files. Print: "Skipped [file] (already exists)"

5. **Create TASKS.md** at `~/.claude/TASKS.md` if it doesn't exist (empty template)

## Phase 5 — Migration Check

Scan `~/.claude/settings.json` for vault hooks that now live in the dex plugin:

```python
# Check for hooks referencing $HOME/.claude/hooks/
# These would double-fire with plugin hooks
```

If found:
> "I found vault hooks in your settings.json that now live in the dex plugin.
> Remove them to prevent double-firing? (SUPERSET notification hooks will be kept.)"

If confirmed: remove vault hook entries, keep any SUPERSET notify.sh entries.

## Phase 6 — Report

```
Setup complete!

Generated:
  ~/.claude/CLAUDE.md (personalized for [name])
  ~/.claude/memory/ (20 files scaffolded)
  ~/.claude/career/, log/, sessions/, config/, work/, archive/, agent-memory/, people/, projects/

Prerequisites verified:
  python3 ✓ | jq ✓ | node ✓ | Compass ✓ | Figma MCP: [✓/⚠ not found]

Next steps:
  1. Review ~/.claude/CLAUDE.md — customize the Identity section
  2. Optional: install Figma MCP for design skills
  3. Start a new session to activate all hooks
```
