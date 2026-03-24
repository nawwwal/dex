---
name: agent-development
description: Use when asked to "create an agent", "add an agent", "write a subagent", "agent frontmatter", "agent examples", "agent tools", "agent colors", "autonomous agent", or when needing guidance on agent structure, system prompts, or triggering conditions for Claude Code plugins.
---

# Agent Development for Claude Code Plugins

## Overview

Agents are autonomous subprocesses that handle complex, multi-step tasks independently. Markdown files with YAML frontmatter define their structure, triggering conditions, and behavior.

**Key distinction:** Agents are for autonomous work; commands/skills are for user-initiated actions.

## When to Use

- Creating a new agent for a Claude Code plugin
- Writing or refining agent frontmatter (name, description, model, color, tools)
- Designing system prompts for agent behavior
- Debugging agent triggering conditions
- Understanding agent file structure and organization

**When NOT to use:** For creating skills (use `superpowers:writing-skills`) or commands (user-initiated actions with no autonomous triggering).

## Agent File Structure

### Complete Format

```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions — simple one-liner, no multi-line, no XML tags].
model: sonnet
color: blue
tools: Read, Write, Grep
---

You are [agent role description]...

**Your Core Responsibilities:**
1. [Responsibility 1]
2. [Responsibility 2]

**Analysis Process:**
[Step-by-step workflow]

**Output Format:**
[What to return]
```

## Frontmatter Fields

### name (required)

Agent identifier used for namespacing and invocation.

**Format:** lowercase, numbers, hyphens only
**Length:** 3-50 characters
**Pattern:** Must start and end with alphanumeric

**Good examples:**
- `code-reviewer`
- `test-generator`
- `api-docs-writer`
- `security-analyzer`

**Bad examples:**
- `helper` (too generic)
- `-agent-` (starts/ends with hyphen)
- `my_agent` (underscores not allowed)
- `ag` (too short, < 3 chars)

### description (required)

Defines when Claude should trigger this agent. **This is the most critical field.**

**CRITICAL: Must be a simple one-liner.** Multi-line descriptions and XML-like tags (`<example>`, `<commentary>`) inside YAML frontmatter break the YAML parser and cause the agent to silently fail to load. The agent will not appear in the available agents list.

**Format:**
```yaml
description: Use this agent when [specific triggering conditions — one line].
```

**Good examples:**
```yaml
# ✅ Simple, one-line, specific triggers
description: Use when the user needs to log into a website, authenticate with a service, or handle a multi-step login flow.
description: World-class UX expert specializing in user experience and accessibility. Use when reviewing user experience aspects of landing pages or marketing content.
```

**Bad examples:**
```yaml
# ❌ Multi-line with <example> tags — BREAKS YAML PARSER, agent won't load
description: Use this agent when... Examples:
 <example>
 Context: User needs help
 user: "help me"
 </example>
```

**Best practices:**
- Keep it to one line — put detailed triggering examples in the system prompt body instead
- Start with "Use when..." or describe expertise then "Use when..."
- Be specific about triggering conditions
- Be specific about when NOT to use the agent

### model (required)

Which model the agent should use.

**Options:**
- `sonnet` - Claude Sonnet (balanced, recommended)
- `opus` - Claude Opus (most capable, expensive)
- `haiku` - Claude Haiku (fast, cheap)
- `inherit` - Use same model as parent

**Recommendation:** Use `sonnet` — this is what all working agents use in practice. While `inherit` is documented, `sonnet` is the proven default.

### color (required)

Visual identifier for agent in UI.

**Options:** `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`

**Guidelines:**
- Choose distinct colors for different agents in same plugin
- Use consistent colors for similar agent types
- Blue/cyan: Analysis, review
- Green: Success-oriented tasks
- Yellow: Caution, validation
- Red: Critical, security
- Magenta: Creative, generation

### tools (optional)

Restrict agent to specific tools.

**Format:** Plain text, comma-separated (NOT JSON arrays — JSON arrays may cause parsing issues)

```yaml
# ✅ CORRECT: plain text comma-separated
tools: Read, Write, Bash

# ❌ WRONG: JSON array format — may break agent loading
tools: ["Read", "Write", "Bash"]
```

**Default:** If omitted, agent has access to all tools

**Best practice:** Limit tools to minimum needed (principle of least privilege)

**Common tool sets:**
- Read-only analysis: `Read, Grep, Glob`
- Code generation: `Read, Write, Grep`
- Testing: `Read, Bash, Grep`
- Full access: Omit field entirely

**Note:** The `allowed-tools` field (e.g., `allowed-tools: Bash(agent-browser:*)`) is NOT recognized by the agent loader and will be silently ignored. Do not use it.

## System Prompt Design

The markdown body becomes the agent's system prompt. Write in second person, addressing the agent directly.

### Structure

**Standard template:**
```markdown
You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Additional responsibilities...]

**Analysis Process:**
1. [Step one]
2. [Step two]
3. [Step three]
[...]

**Quality Standards:**
- [Standard 1]
- [Standard 2]

**Output Format:**
Provide results in this format:
- [What to include]
- [How to structure]

**Edge Cases:**
Handle these situations:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
```

### Best Practices

✅ **DO:**
- Write in second person ("You are...", "You will...")
- Be specific about responsibilities
- Provide step-by-step process
- Define output format
- Include quality standards
- Address edge cases
- Keep under 10,000 characters

❌ **DON'T:**
- Write in first person ("I am...", "I will...")
- Be vague or generic
- Omit process steps
- Leave output format undefined
- Skip quality guidance
- Ignore error cases

## Creating Agents

### Method 1: AI-Assisted Generation

Use this prompt pattern (extracted from Claude Code):

```
Create an agent configuration based on this request: "[YOUR DESCRIPTION]"

Requirements:
1. Extract core intent and responsibilities
2. Design expert persona for the domain
3. Create comprehensive system prompt with:
   - Clear behavioral boundaries
   - Specific methodologies
   - Edge case handling
   - Output format
4. Create identifier (lowercase, hyphens, 3-50 chars)
5. Write description with triggering conditions
6. Include 2-3 <example> blocks showing when to use

Return JSON with:
{
  "identifier": "agent-name",
  "whenToUse": "Use this agent when... Examples: <example>...</example>",
  "systemPrompt": "You are..."
}
```

Then convert to agent file format with frontmatter.

See `examples/agent-creation-prompt.md` for complete template.

### Method 2: Manual Creation

1. Choose agent identifier (3-50 chars, lowercase, hyphens)
2. Write one-line description with triggering conditions
3. Select model (use `sonnet`)
4. Choose color for visual identification
5. Define tools as plain text comma-separated (if restricting access)
6. Write system prompt with structure above
7. Save as `agents/agent-name.md`
8. Create symlink if needed: `ln -sf <source> ~/.claude/agents/agent-name.md`
9. **Restart Claude Code session** for the agent to appear

## Validation Rules

### Identifier Validation

```
✅ Valid: code-reviewer, test-gen, api-analyzer-v2
❌ Invalid: ag (too short), -start (starts with hyphen), my_agent (underscore)
```

**Rules:**
- 3-50 characters
- Lowercase letters, numbers, hyphens only
- Must start and end with alphanumeric
- No underscores, spaces, or special characters

### Description Validation

**Length:** 10-500 characters (one line)
**Must include:** Triggering conditions
**Must NOT include:** Multi-line content, `<example>` tags, or any XML-like markup
**Best:** 100-300 characters with clear "Use when..." trigger

### System Prompt Validation

**Length:** 20-10,000 characters
**Best:** 500-3,000 characters
**Structure:** Clear responsibilities, process, output format

## Agent Organization

### Plugin Agents Directory

```
plugin-name/
└── agents/
    ├── analyzer.md
    ├── reviewer.md
    └── generator.md
```

All `.md` files in `agents/` are auto-discovered.

### Namespacing

Agents are namespaced automatically:
- Single plugin: `agent-name`
- With subdirectories: `plugin:subdir:agent-name`

## Runtime Behavior

**Agents are loaded at session start.** If you create or modify an agent file during a session, it will NOT be available until the user starts a new Claude Code session. This is a common source of confusion during development.

**Debugging checklist when agent doesn't appear:**
1. Verify the file exists: `ls -la ~/.claude/agents/agent-name.md`
2. If symlink, verify target exists: `readlink ~/.claude/agents/agent-name.md`
3. Check YAML frontmatter parses correctly (no multi-line descriptions, no `<` tags)
4. Check `tools` field uses plain text format, not JSON arrays
5. Start a new Claude Code session and check available agents

## Testing Agents

### Test Triggering

Create test scenarios to verify agent triggers correctly:

1. Write agent with specific triggering examples
2. Use similar phrasing to examples in test
3. Check Claude loads the agent
4. Verify agent provides expected functionality

### Test System Prompt

Ensure system prompt is complete:

1. Give agent typical task
2. Check it follows process steps
3. Verify output format is correct
4. Test edge cases mentioned in prompt
5. Confirm quality standards are met

## Quick Reference

### Minimal Agent

```markdown
---
name: simple-agent
description: Use this agent when [specific one-line triggering condition].
model: sonnet
color: blue
tools: Read, Write, Bash
---

You are an agent that [does X].

Process:
1. [Step 1]
2. [Step 2]

Output: [What to provide]
```

### Frontmatter Fields Summary

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| name | Yes | lowercase-hyphens | code-reviewer |
| description | Yes | One-line text | Use when reviewing code for bugs. |
| model | Yes | sonnet/opus/haiku/inherit | sonnet |
| color | Yes | Color name | blue |
| tools | No | Plain text, comma-separated | Read, Write, Bash |

### Best Practices

**DO:**
- ✅ Keep description as a simple one-liner with triggering conditions
- ✅ Use `tools: Read, Write, Bash` (plain text comma-separated)
- ✅ Use `sonnet` for model (proven default)
- ✅ Choose appropriate tools (least privilege)
- ✅ Write clear, structured system prompts
- ✅ Test agent triggering in a NEW session after creating the file

**DON'T:**
- ❌ Put `<example>` tags or multi-line content in the YAML description (breaks parser)
- ❌ Use JSON arrays for tools field (e.g., `["Read", "Bash"]`)
- ❌ Use `allowed-tools` field (not recognized)
- ❌ Expect new agents to appear without restarting the session
- ❌ Give all agents same color
- ❌ Write vague system prompts

## Additional Resources

### Reference Files

For detailed guidance, consult:

- **`references/system-prompt-design.md`** - Complete system prompt patterns
- **`references/triggering-examples.md`** - Example formats and best practices
- **`references/agent-creation-system-prompt.md`** - The exact prompt from Claude Code

### Example Files

Working examples in `examples/`:

- **`agent-creation-prompt.md`** - AI-assisted agent generation template
- **`complete-agent-examples.md`** - Full agent examples for different use cases

### Utility Scripts

Development tools in `scripts/`:

- **`validate-agent.sh`** - Validate agent file structure and frontmatter

## Implementation Workflow

To create an agent for a plugin:

1. Define agent purpose and triggering conditions
2. Choose creation method (AI-assisted or manual)
3. Create `agents/agent-name.md` file
4. Write frontmatter with all required fields
5. Write system prompt following best practices
6. Include 2-4 triggering examples in description
7. Validate with `scripts/validate-agent.sh`
8. Test triggering with real scenarios
9. Document agent in plugin README

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generic name like `helper` or `agent` | Use specific, descriptive names: `code-reviewer`, `test-generator` |
| Multi-line description with `<example>` tags | Keep description as a one-liner. Put examples in system prompt body |
| `tools: ["Read", "Bash"]` (JSON array) | Use plain text: `tools: Read, Bash` |
| Using `allowed-tools` field | Not recognized by agent loader. Remove it |
| Agent not appearing after creation | Agents load at session start. Restart Claude Code session |
| Broken symlink in `~/.claude/agents/` | Verify target exists: `readlink` + `ls` the target path |
| Vague system prompt ("help with code") | Specify responsibilities, process steps, output format |
| Granting all tools when only Read needed | Apply principle of least privilege via `tools` field |
| Same color for all agents in a plugin | Pick distinct colors matching agent purpose |
| First-person system prompt ("I will...") | Write in second person ("You are...", "You will...") |
| Missing output format in system prompt | Define exact structure the agent should return |
