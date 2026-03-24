---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

**Writing a skill IS Test-Driven Development applied to process documentation.**

**Personal skills live in agent-specific directories (`~/.claude/skills` for Claude Code, `~/.codex/skills/` for Codex)**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

**Official guidance:** Anthropic's official skill authoring documentation is at https://code.claude.com/docs/en/skills — always use this as the canonical reference for field definitions, advanced patterns, and invocation control.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (if it's enforceable with regex/validation, automate it)

## Skill Types

### Technique
Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)

### Pattern
Way of thinking about problems (flatten-with-flags, test-invariants)

### Reference
API docs, syntax guides, tool documentation (office docs)

## Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Flat namespace** — all skills in one searchable namespace

**Separate files for:**
1. **Heavy reference** (100+ lines) — API docs, comprehensive syntax
2. **Reusable tools** — Scripts, utilities, templates

**Keep inline:** Principles, code patterns (< 50 lines), everything else

## SKILL.md Structure

**Frontmatter (YAML — Claude Code runtime):**
- Core fields: `name` and `description`. For the full list, see the Full Frontmatter Reference below.
- Max 1024 characters total for frontmatter
- `name`: Use letters, numbers, and hyphens only (no parentheses, special chars)
- `description`: Third-person, describes ONLY when to use (NOT what it does)
  - Start with "Use when..." to focus on triggering conditions
  - Include specific symptoms, situations, and contexts
  - **NEVER summarize the skill's process or workflow** (see CSO section for why)
  - Keep under 500 characters
  - **YAML safety:** If the description contains a colon (`:`), wrap in double quotes or use a block scalar (`|` or `>`). Malformed YAML silently breaks the skill.
- **Keep SKILL.md under 500 lines.** Move heavy content to supporting files with descriptive links (see Orchestrator Skill pattern below).

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision non-obvious]

Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)
Before/after code comparison

## Quick Reference
Table or bullets for scanning common operations

## Implementation
Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes
Failure cases Claude hit using this skill — not generic advice.
Build from observed failures, not speculation. Update over time.
```

## Full Frontmatter Reference

All supported YAML frontmatter fields for Claude Code `SKILL.md` files:

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | No | Directory name | Lowercase, hyphens only, max 64 chars |
| `description` | Recommended | First paragraph | Claude uses this to decide when to auto-load. Start with "Use when..." |
| `argument-hint` | No | — | Shown during `/` autocomplete, e.g. `[issue-number]` |
| `disable-model-invocation` | No | `false` | `true` = only you can invoke; Claude cannot auto-trigger |
| `user-invocable` | No | `true` | `false` = hide from `/` menu; Claude-only background knowledge |
| `allowed-tools` | No | — | Tools Claude can use without per-use approval while skill is active |
| `model` | No | — | Model override when skill is active |
| `context` | No | — | `fork` = run in isolated subagent with no conversation history |
| `agent` | No | — | Subagent type when `context: fork` is set (`Explore`, `Plan`, custom) |
| `hooks` | No | — | Lifecycle hooks scoped to this skill only. Events: `PreToolUse`, `PostToolUse`, `Stop`. Types: `command`, `prompt`, `agent`. See [hooks-and-subagents.md](hooks-and-subagents.md) for examples. |

**Invocation control:**
- Default: Claude can auto-invoke AND you can slash-invoke
- `disable-model-invocation: true`: Only you can invoke
- `user-invocable: false`: Claude can auto-trigger, hidden from `/` menu
- Note: `user-invocable` only controls menu visibility. Use `disable-model-invocation: true` to block programmatic invocation.

## Advanced Patterns

### String Substitutions

| Variable | Value |
|---|---|
| `$ARGUMENTS` | All arguments passed to the skill |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g. `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing this `SKILL.md` |

If `$ARGUMENTS` is not present in content, arguments are appended as `ARGUMENTS: <value>`.

Use `${CLAUDE_SKILL_DIR}` for portable script references:
```yaml
Run: python ${CLAUDE_SKILL_DIR}/scripts/analyze.py $0
```

### Dynamic Context Injection

The **dynamic injection syntax** is an exclamation mark immediately followed by a backtick-quoted shell command. The skill loader runs the command before sending content to Claude — the output replaces the injection placeholder. This is preprocessing, not something Claude executes.

**Optional — verify it works in your actual invocation path before relying on it.** Injection can fail before Bash approval or depending on the invocation context. Always document a safe fallback for when injection is unavailable.

Example (angle brackets show where the backtick-quoted command goes — replace `<cmd>` with an actual shell command in a real skill):

```yaml
---
name: pr-review
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

Current PR state:
- Diff: !<gh pr diff>
- Comments: !<gh pr view --comments>
```

### Subagent Execution

Add `context: fork` to run the skill in complete isolation (no conversation history). Use `agent` to pick the execution type.

**Skills vs. Subagents — two directions:**

| Approach | System prompt | Task source | Also loads |
|---|---|---|---|
| Skill with `context: fork` | From agent type | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown | Claude's delegation | Preloaded skills + CLAUDE.md |

`context: fork` only makes sense for skills with explicit instructions — not for pure reference content.

**Key subagent frontmatter fields** (in `.claude/agents/` markdown files, not SKILL.md):

| Field | Effect | When to use |
|---|---|---|
| `skills` | Preloads skill content at startup. Subagents do NOT inherit parent skills — list explicitly. | Any subagent enforcing skill conventions |
| `isolation` | `worktree` — temp git worktree, auto-cleaned if no changes. | Risky or experimental ops |
| `memory` | Persist learnings: `user`, `project`, or `local` scope. `project` recommended default. | Cross-session agent knowledge |
| `background` | `true` — always runs as background task. | Long-running verification |
| `effort` | `max` — extended thinking (Opus 4.6 only, as of writing). | Complex multi-step reasoning |
| `hooks` | Lifecycle hooks scoped to this subagent only. | PreToolUse validation, PostToolUse linting |
| `maxTurns` | Cap agentic turns before stopping. | Prevent runaway agents |

For annotated examples, see [hooks-and-subagents.md](hooks-and-subagents.md).

### Hooks in Skills

Skills can declare lifecycle hooks that run while the skill is active — no separate settings file needed.
**Hook types:**

| Type | Use when |
|---|---|
| `command` | Deterministic rules — block tools, auto-format, validate inputs |
| `prompt` | Judgment-based check — "is the work complete?", "did Claude follow the pattern?" (Haiku by default) |
| `agent` | Need actual codebase state or test output to verify (up to 50 turns, 60s default timeout) |

**Common patterns for skills:**
| Pattern | Event | Purpose |
|---|---|---|
| Completeness guard | `Stop` + prompt/agent hook | Prevent Claude stopping before all checklist items done |
| Auto-format | `PostToolUse` + command hook | Run formatter after file edits |
| Tool validation | `PreToolUse` + command hook | Block dangerous commands for this skill's domain |

**Critical:** Stop hooks with `command` type require an infinite-loop guard (`stop_hook_active` check) — `prompt` and `agent` types handle this automatically. See [hooks-and-subagents.md](hooks-and-subagents.md) for safe, annotated examples.
**Plugin authors only:** Hook scripts can reference `${CLAUDE_PLUGIN_DATA}` — a stable per-plugin data directory. This is a hook-context variable, not YAML string substitution.

### Extended Thinking

Include the word `ultrathink` anywhere in skill content to enable extended thinking mode. Use for skills requiring deep reasoning: architecture decisions, complex debugging, multi-step planning.

### Background Knowledge Skills

Set `user-invocable: false` for skills that:
- Auto-trigger when description matches the task
- Are NOT actionable slash commands
- Function as injected context (legacy system docs, codebase conventions, team context)

### Invocation Control Matrix

| Frontmatter | You can `/invoke` | Claude can auto-invoke | In `/` menu | Description in context |
|---|---|---|---|---|
| (default) | Yes | Yes | Yes | Always |
| `disable-model-invocation: true` | Yes | No | Yes | No |
| `user-invocable: false` | No | Yes | No | Always |

### Skill Context Budget

Skill **descriptions** (not full content) load into context. Budget: **2% of context window**, **16,000-character fallback**.

- Run `/context` to check if skills are being excluded
- Override: `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var
- To reduce budget use: `user-invocable: false` (hides from menu) or `disable-model-invocation: true` (removes from context)

## Claude Search Optimization (CSO)

**Critical for discovery:** Future Claude needs to FIND your skill

### 1. Rich Description Field

Claude reads the description to decide which skills to load. Make it answer: "Should I read this right now?"

**CRITICAL: Description = When to Use, NOT What the Skill Does**

Testing revealed: descriptions that summarize the workflow become a shortcut Claude takes instead of reading the full skill. Keep descriptions as triggering conditions only.

```yaml
# ❌ BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ✅ GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks in the current session
```

**Rules:**
- Start with "Use when..."
- Describe the *problem*, not language-specific symptoms
- Write in third person (injected into system prompt)
- **NEVER summarize the skill's process or workflow**
- If description contains `:`, wrap in quotes to avoid YAML parse errors

### 2. Keyword Coverage

Use words Claude would search for:
- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Tools: Actual commands, library names, file types

### 3. Descriptive Naming

Use active voice, verb-first:
- ✅ `creating-skills` not `skill-creation`
- ✅ `condition-based-waiting` not `async-test-helpers`

Gerunds (-ing) work well: `creating-skills`, `testing-skills`, `debugging-with-logs`

### 4. Token Efficiency

**Target word counts:**
- Getting-started workflows: <150 words each
- Frequently-loaded skills: <200 words total
- Other skills: <500 words

Move details to `--help`, use cross-references, eliminate redundancy. Verify with `wc -w skills/path/SKILL.md`.

### 5. Cross-Referencing Other Skills

Use explicit requirement markers. Distinguish **mention** (awareness) from **invoke** (required action):

```markdown
# Mention — awareness only:
Related: superpowers:test-driven-development covers the RED-GREEN-REFACTOR cycle.

# Invoke — required:
**REQUIRED SUB-SKILL:** Invoke superpowers:test-driven-development before writing any test.
```

- ❌ Bad: `See skills/testing/test-driven-development` (unclear if required)
- ❌ Bad: `@skills/tdd/SKILL.md` (`@` syntax force-loads, burns context immediately)

## Flowchart Usage

**Use flowcharts ONLY for:**
- Non-obvious decision points
- Process loops where you might stop too early
- "When to use A vs B" decisions

**Never use for:** Reference material (→ Tables), code examples (→ Markdown blocks), linear instructions (→ Numbered lists)

For graphviz style rules, see `graphviz-conventions.dot` in the superpowers plugin's `skills/writing-skills/` directory.

## Code Examples

**One excellent example beats many mediocre ones.** Choose the most relevant language. A good example is complete, runnable, well-commented explaining WHY, and ready to adapt.

Don't: implement in 5+ languages, create fill-in-the-blank templates, write contrived examples.

## File Organization

Skills are folders, not files. Think of the structure as **progressive disclosure** — tell Claude what files exist in SKILL.md, and it reads them when relevant.

### Self-Contained Skill
```
defense-in-depth/
  SKILL.md    # Everything inline
```
When: All content fits, no heavy reference needed

### Skill with Reusable Tool
```
condition-based-waiting/
  SKILL.md    # Overview + patterns
  example.ts  # Working helpers to adapt
```
When: Tool is reusable code, not just narrative

Prefer giving Claude reusable assets (templates, reference files, scripts) over describing what to generate.

### Skill with Heavy Reference
```
pptx/
  SKILL.md       # Overview + workflows
  pptxgenjs.md   # 600 lines API reference
  ooxml.md       # 500 lines XML structure
  scripts/       # Executable tools
```
When: Reference material too large for inline

### Orchestrator Skill
```
my-skill/
  SKILL.md        # Overview and navigation ONLY (≤500 lines)
  reference.md    # Detailed API docs — loaded when needed
  examples.md     # Usage examples — loaded when needed
  scripts/
    helper.py     # Executable utility — executed, not loaded into context
```
When: Multiple concerns push SKILL.md past 500 lines, or different parts of reference are needed in different situations.

**Key rules:**
- SKILL.md = navigation layer only; describe each file and when to load it
- Use standard relative markdown links: `For API details, see [reference.md](reference.md)`
- Supporting `.md` files are **not auto-loaded** — Claude reads them based on prose descriptions
- Scripts in `scripts/` are **executed**, not loaded into context
- Use `${CLAUDE_SKILL_DIR}/scripts/helper.py` for CWD-independent script references
- `user-invocable: false` + thin SKILL.md = pure background knowledge pattern

## The Iron Law (Same as TDD)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over. Edit skill without testing? Same violation.

**No exceptions:**
- Not for "simple additions" or "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Delete means delete

**Testing & Bulletproofing:** See [testing-guide.md](testing-guide.md) for:
- Testing methodology by skill type (technique, pattern, reference, discipline-enforcing)
- Pressure scenario design and rationalization tables
- RED-GREEN-REFACTOR for Skills (how to run the full cycle)
- Bulletproofing against rationalization

## Anti-Patterns

### ❌ Narrative Example
"In session 2025-10-03, we found empty projectDir caused..."
**Why bad:** Too specific, not reusable

### ❌ Multi-Language Dilution
example-js.js, example-py.py, example-go.go
**Why bad:** Mediocre quality, maintenance burden

### ❌ Code in Flowcharts
**Why bad:** Can't copy-paste, hard to read

### ❌ Generic Labels
helper1, helper2, step3, pattern4
**Why bad:** Labels should have semantic meaning

### ❌ Stating the Obvious
Documenting Claude's defaults (e.g. "write clean code", "handle errors").
**Why bad:** Burns context on behavior Claude already does. Focus on what Claude gets wrong.

### ❌ Railroading
Over-specifying every step for a reusable skill.
**Why bad:** Prevents Claude from adapting. Skills are invoked in varying contexts — leave room for judgment.

## Skill Creation & Review

**Checklists and review process:** See [review-checklists.md](review-checklists.md) for:
- Creation Review checklist (run before committing a new skill)
- Existing Skill Audit checklist (run against any skill to surface improvements)
- Full Skill Creation Checklist (TDD Adapted) with RED/GREEN/REFACTOR phases

## Discovery Workflow

How future Claude finds your skill:

1. **Encounters problem** ("tests are flaky")
2. **Finds SKILL** (description matches)
3. **Scans overview** (is this relevant?)
4. **Reads patterns** (quick reference table)
5. **Loads example** (only when implementing)

**Optimize for this flow** — put searchable terms early and often.

## Miscellaneous Reference

**Priority order** (higher wins on name conflict):
1. Enterprise (managed settings)
2. Personal (`~/.claude/skills/`)
3. Project (`.claude/skills/`)
4. Plugin (`<plugin>/skills/`)

**Skill vs command:** Skill wins when a skill and `.claude/commands/` entry share the same name.

**Plugin namespace:** `plugin-name:skill-name` format prevents conflicts with personal/project skills.

**Permission syntax:** `Skill(name)` exact match, `Skill(name *)` prefix match.

**Live reload:** Skills in `--add-dir` directories reload without session restart.

**Monorepo support:** Claude discovers skills from nested `.claude/skills/` directories as you work in subdirectories.

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).
Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills.
