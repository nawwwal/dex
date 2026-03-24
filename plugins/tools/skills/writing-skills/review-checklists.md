# Skill Review Checklists

Referenced from [SKILL.md](SKILL.md). Load this file when reviewing a newly written skill or auditing an existing one.

## Creation Review (run before committing a new skill)

### Discovery
- [ ] Description starts with "Use when..." — triggering conditions only, no workflow summary
- [ ] Description under 500 chars, written in third person
- [ ] If description contains `:`, wrapped in double quotes or block scalar
- [ ] Name is lowercase, hyphens only, verb-first gerund preferred (`creating-skills`)
- [ ] Keywords throughout: error messages, symptoms, synonyms, tool names

### Frontmatter
- [ ] Only fields from the Full Frontmatter Reference used (no invented fields)
- [ ] `allowed-tools` set if skill needs specific tool access without per-use approval
- [ ] `user-invocable: false` if skill should only auto-trigger, not appear in `/` menu
- [ ] `disable-model-invocation: true` if skill should only be user-invoked (never auto)
- [ ] `context: fork` + `agent` set if skill should run in isolation

### Skill Quality
- [ ] Common Mistakes section built from observed failures — not generic advice or speculation?
- [ ] Skill avoids over-specification? (gives Claude info, leaves room for judgment)
- [ ] No obvious defaults stated? (e.g. "write clean code", "use descriptive names")
- [ ] Reusable assets (templates, reference files) in folder rather than reconstructed each time?

**Plugin-packaged skills additionally:**
- [ ] Durable data stored in `${CLAUDE_PLUGIN_DATA}` (stable per-plugin data directory), not skill dir?
- [ ] On-demand hooks used for scoped guardrails, not added to global settings.json?

### Content
- [ ] SKILL.md is under 500 lines
- [ ] Heavy content moved to supporting files with descriptive relative links
- [ ] `$ARGUMENTS` / `${CLAUDE_SKILL_DIR}` used where appropriate
- [ ] Dynamic injection (`!<command>` syntax) considered for live data (optional — verify it works in your invocation path first)
- [ ] `ultrathink` included if skill requires deep reasoning
- [ ] No narrative storytelling, no multi-language examples, no code in flowcharts

### Orchestration (multi-file skills only)
- [ ] SKILL.md names each supporting file and says when to load it
- [ ] Markdown reference files at top level; scripts under `scripts/`
- [ ] File structure diagram in SKILL.md

### Reference Integrity
- [ ] Every linked file (`[reference.md](reference.md)`, `@file.md`) exists in the skill directory
- [ ] Every referenced skill name (`superpowers:test-driven-development`, `tdd`) resolves in the current environment
- [ ] Every referenced script (`${CLAUDE_SKILL_DIR}/scripts/x.py`) exists

### TDD Gate
- [ ] Baseline test run WITHOUT skill — failure documented verbatim
- [ ] Test run WITH skill — compliance confirmed
- [ ] At least one refactor cycle completed (new rationalization found and countered)

---

## Existing Skill Audit (run against any skill to surface improvements)

### Discovery Health
- [ ] Description starts with "Use when..."?
- [ ] Description avoids summarizing the workflow?
- [ ] Triggering conditions concrete and searchable?

### Frontmatter Health
- [ ] Any outdated or invented fields present? (clean up to Claude Code official list)
- [ ] Should `allowed-tools` reduce approval friction?
- [ ] Is `context: fork` appropriate for this skill's isolation needs?
- [ ] Should this be `user-invocable: false` (background knowledge, not a command)?

### Content Health
- [ ] SKILL.md under 500 lines? What can move to supporting files?
- [ ] Supporting files properly referenced with descriptive links?
- [ ] `${CLAUDE_SKILL_DIR}` used for portable script references?
- [ ] Could dynamic injection (`!<command>` syntax) inject live context the skill currently asks Claude to fetch manually? (optional)
- [ ] Rationalization table and red flags list present? (discipline-enforcing skills only)

### Reference Integrity
- [ ] Every linked file exists in the skill directory?
- [ ] Every referenced skill name resolves in the current environment?
- [ ] Any `@` force-load references that should be converted to prose links?

### Testing
- [ ] Documented test scenarios exist?
- [ ] Last tested recently? Model behavior changes — re-test after major model updates.

---

## Skill Creation Checklist (TDD Adapted)

Use TodoWrite to create todos for each item below before starting.

### RED Phase — Write Failing Test
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill — document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

### GREEN Phase — Write Minimal Skill
- [ ] Name uses only letters, numbers, hyphens
- [ ] YAML frontmatter uses only Claude Code fields (max 1024 chars)
- [ ] Description starts with "Use when..." and includes specific triggers/symptoms
- [ ] Description written in third person, YAML-safe (quote if it contains `:`)
- [ ] Keywords throughout for search (errors, symptoms, tools)
- [ ] Clear overview with core principle
- [ ] Address specific baseline failures identified in RED
- [ ] Code inline OR link to separate file
- [ ] One excellent example (not multi-language)
- [ ] Run scenarios WITH skill — verify agents now comply
- [ ] Considered advanced frontmatter: `allowed-tools`, `model`, `context: fork`, `user-invocable`, `disable-model-invocation`
- [ ] `$ARGUMENTS` / `${CLAUDE_SKILL_DIR}` used where skill takes user input or references bundled files
- [ ] SKILL.md under 500 lines (heavy content moved to supporting files)

### REFACTOR Phase — Close Loopholes
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table from all test iterations
- [ ] Create red flags list
- [ ] Re-test until bulletproof

### Quality Checks
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference
- [ ] Reference integrity: every linked file and skill exists

### Deployment
- [ ] Commit skill to git and push to your fork (if configured)
- [ ] Consider contributing back via PR (if broadly useful)

---

## STOP: Before Moving to Next Skill

**After writing ANY skill, you MUST STOP and complete the deployment process.**

**Do NOT:**
- Create multiple skills in batch without testing each
- Move to next skill before current one is verified
- Skip testing because "batching is more efficient"

Deploying untested skills = deploying untested code. It's a violation of quality standards.
