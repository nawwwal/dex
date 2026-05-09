# Council Router

Use this file first. Do not load all mode files before routing.

## Defaults

- `mode=auto`
- `depth=standard`
- `goal=findings`

If the user supplied flags, honor them unless they are clearly inconsistent with the prompt.

## Step 1: Extract the topic

- Treat the free-text part of `$ARGUMENTS` as the investigation topic.
- Keep the topic wording close to the user's phrasing.
- If the topic is empty, ask a single routing question before doing anything else.

## Step 2: Infer the mode from the prompt

Infer the mode without asking questions when the message is clear.

| Mode | Strong signals |
|---|---|
| `code` | files, dirs, modules, APIs, tests, refactor, implementation, code review, regression |
| `research` | how do others, best practice, compare, evaluate, alternatives, state of the art, what exists, survey |
| `opinion` | what do you think, second opinion, should we, expert view, perspectives, debate, which approach |
| `system` | architecture, hooks, lifecycle, integrations, plugins, ownership, blast radius, cross-system behavior |
| `workflow` | process, handoff, review flow, bottleneck, repeated churn, operating model, automation gap |

Prefer `research` over `code` when the question is about external information, alternatives, or best practices rather than investigating existing code.

Prefer `opinion` over `research` when the user wants perspectives on a decision rather than factual information gathering.

Prefer `system` over `code` when the request spans multiple parts of the repo or asks about interactions, ownership, or lifecycle.

## Step 3: Infer the goal from the prompt

| Goal | Strong signals |
|---|---|
| `findings` | audit, investigate, analyze, map, understand, what is going on, research |
| `risks` | fragile, what could break, failure mode, adversarial, risk review, threat, blind spot |
| `decision` | compare, choose, should we, which direction, recommend a path, what do you think |
| `actions` | what should we do, prioritize, next steps, fix plan, action plan |

If multiple goals are implied, choose the most decision-heavy one:
`decision` > `actions` > `risks` > `findings`

## Step 4: Infer the depth

| Depth | Use when |
|---|---|
| `quick` | single file, single skill, narrow slice, fast contrarian pass, one immediate question |
| `standard` | normal investigation, medium scope, moderate uncertainty |
| `deep` | full audit, architecture review, inconsistency hunt, cross-system review, comprehensive research |

Bias toward `quick` when the blast radius is narrow and the user wants speed.
Bias toward `deep` only when the topic is broad enough to justify wider fan-out.

## Step 5: Decide whether to ask questions

Ask structured questions only if at least one of these is still unclear:

- the `mode`
- the desired `goal`
- the breadth of the review
- the final output shape

Question budget:

- `0` if the prompt already routes cleanly
- `1` for mild ambiguity
- `2-3` for meaningful ambiguity

Never ask questions that can be answered by one or two reconnaissance reads.

If you ask questions, load `$CLAUDE_SKILL_DIR/references/questions.md`.

## Step 6: Do a lean reconnaissance pass

Before spawning agents, spend 1-3 tool calls to ground the investigation:

- map the obvious files, dirs, or artifacts involved
- identify constraints or adjacent systems
- collect enough context to shape non-overlapping lenses

For `research` mode, the reconnaissance pass should include 1-2 quick web searches to map the landscape before assigning deeper research to agents.

For `opinion` mode, the reconnaissance pass should identify what the decision is, what constraints exist, and what the stakes are, so agents can be briefed with the right personas.

Do not try to answer the whole question in reconnaissance.

## Step 7: Load only the selected references

Load exactly these:

1. one mode file from `$CLAUDE_SKILL_DIR/references/modes/`
2. `$CLAUDE_SKILL_DIR/references/depths.md`
3. `$CLAUDE_SKILL_DIR/references/synthesis.md`

Use `$CLAUDE_SKILL_DIR/references/examples.md` only if the request is still hard to classify or the prompting shape is unclear.

## Investigation Context Object

After routing, store the working context in this shape:

```json
{
  "investigation_context": {
    "topic": "...",
    "mode": "code|research|opinion|system|workflow",
    "depth": "quick|standard|deep",
    "goal": "findings|risks|decision|actions",
    "scope_note": "...",
    "constraints": ["..."],
    "assumptions": ["..."]
  }
}
```

Keep it compact. It is for routing and synthesis, not for writing the final report.
