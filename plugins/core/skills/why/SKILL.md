---
name: why
description: "Use when the user explicitly invokes why, teach, or learn, or asks to understand, explain, walk through, unpack, or be taught unfamiliar code, tools, concepts, architecture, design choices, tradeoffs, or clever functions before execution. Also use implicitly when the user says they do not understand something, asks what concepts a solution uses, asks what to read to understand a design choice, or asks the agent to explain before doing the task. When that explanation request also asks for HTML output, a report, a shareable site, or a polished web artifact, use Why for the learning spine and route artifact production to brief."
---

# Why

Turn unfamiliar territory into a clear learning pass before execution.

Assume the active context is unfamiliar to the user. Explain the concepts, mechanics, alternatives, and tradeoffs first. Move to repo edits, commands, migrations, external writes, or other persistent actions only after the user has a workable grasp or explicitly asks you to proceed.

## Core Workflow

1. Identify the learning target from the user request, active files, pasted text, error output, code diff, tool output, or design context.
2. Search the Tolaria knowledge base for relevant teaching and learning profiles before choosing examples, depth, analogies, or reading paths.
3. Read the most relevant profile records and concept records. If no profile exists, use the bundled fallback profile below for the current answer only.
4. Explain how it works in concrete terms. Define unfamiliar terms once, then use them naturally.
5. Name the important concepts involved.
6. Compare alternatives and tradeoffs.
7. Tell the user what to read next to understand the design choices.
8. Ask one grounding question or confirmation before persistent execution:
   - "Should I slow down on any concept before I do the task?"
   - "Does this mental model work well enough for me to proceed?"
   - "Which part should I unpack further before I change the code?"
9. After the user confirms or shows understanding, perform the original task if it was part of the request.
10. Save learned concepts, teaching preferences, or learner-profile updates to Tolaria only when the user explicitly asks to save, remember, or add the learning.

## Brief Artifact Handoff

Why owns explanation. `brief` owns browser-native editorial HTML reports.

If a Why, Teach, Learn, or explain-before-execution request also asks for "HTML output", "HTML report", "web report", "report", "shareable site", "shareable HTML", "browser-readable report", "visual explainer", or a similar polished web artifact:

1. Use Why first to build the mental model, concept list, alternatives, tradeoffs, and read-next spine.
2. Hand the artifact-production step to `brief` instead of hand-rolling the report inside Why.
3. For substantial artifacts, use a subagent when available. Pass the learning spine, source material, audience, and artifact constraints to `brief`; do not pass hidden analysis or eval expectations.
4. Use same-thread `brief` execution only when subagents are genuinely unavailable or the artifact is tiny. State the brief handoff boundary plainly before continuing.
5. Do not route slide decks, Reveal.js, PowerPoint, Google Slides, or Figma Slides to `brief`; those belong to presentation/deck workflows.

The boundary is: Why explains why the idea works; Brief turns that explanation into the shareable HTML/report/site.

## Knowledge Base Profile Resolution

Canonical teaching and learning context lives in Tolaria, not in `~/.agents/memory/teach/`.

Before a non-trivial explanation, search Tolaria with the concrete learning target plus profile aliases:

```text
why profile
teach profile
learn profile
learning profile
learner profile
teaching preference
design engineering learning
aditya-nawal-operating-model
agent-behavior-gotchas
```

Use the result order this way:

1. Prompt-provided learner context controls the current answer.
2. Tolaria profile or preference records control durable personalization.
3. Relevant Tolaria concept notes or project notes control examples and source grounding.
4. The bundled fallback profile below fills gaps only when the knowledge base has no useful profile.

If Tolaria tools are unavailable, say which profile search was skipped and continue from prompt context plus the fallback profile. Do not create a parallel local profile file as a substitute.

Do not report profile-search or knowledge-base plumbing in the answer unless it changes the explanation, the user asked about memory/profile state, the request is a knowledge-base write, or higher-priority source-status instructions require it. The learning answer should not leak Tolaria, Portent, or profile machinery into unrelated concepts.

## Execution Gates

Use the smallest gate that protects the user from premature action:

| Request shape | Explain first | Proceed immediately? |
|---|---:|---:|
| Explanation-only, debugging explanation, or conceptual walkthrough | yes | yes, answer the learning need |
| Self-contained code snippet or example the user explicitly requested | yes | yes, include the teaching trail with the snippet |
| Repo edit, shell command, migration, network action, persistent config change, or external write | yes | no, ask one grounding/proceed question first |
| Knowledge-base write | yes | only when explicit save/remember/add-to-knowledge-base intent is already present |

If the user says "before changing it", do not edit yet. If they ask for a compact example function, write the example and explain the concepts used.

## Fallback Learner Profile

Use this only when Tolaria has no useful profile record and the prompt gives no learner context:

```markdown
---
title: "Why Learner Profile"
current_identity: "Designer moving toward design engineering"
target_identity: "Design engineer with strong frontend implementation taste"
primary_learning_lanes: ["html", "css", "javascript", "typescript", "react", "browser rendering", "accessibility", "component architecture", "interaction design"]
current_grasp: "Strong design/product intuition; building deeper frontend and engineering mental models"
teaching_preference: "Use design-to-code bridges, concrete UI examples, frontend mechanics, and tradeoffs before abstract backend/tooling explanations."
---
```

The user is a designer on the path to becoming a design engineer.

They want frontend intricacies explained in detail: HTML semantics, CSS layout and cascade, responsive constraints, browser rendering, JavaScript runtime behavior, TypeScript type modeling, React component architecture, state, effects, accessibility, interaction polish, and design-system implementation.

Use frontend examples as the default bridge when they clarify a concept. Backend, indexing, tooling, or infrastructure concepts should still be explained when relevant, but connect them back to UI behavior, developer ergonomics, product experience, or design-to-code tradeoffs whenever possible.

## Teaching Shape

Use this shape when it helps scanning:

```markdown
**Mental Model**
[plain explanation of the system]

**Concepts**
- `term` -> meaning -> where it appears here -> why it matters

**Alternatives**
- [alternative] -> what changes -> when it wins -> when it fails

**Tradeoffs**
- [choice] -> benefit -> cost -> risk

**Read Next**
- [topic or doc] -> why it matters
```

Do not turn every answer into a lecture. Compress when the user only needs a quick explanation.

For a small error message or single-command failure, use 3-6 sentences by default: start from the exact error, name the likely mismatch, define one concept, give one likely fix path or alternative, and ask one compact proceed question only if code or commands would change. If the user frames the explanation as "before fixing/changing it", the final sentence must be one short inspect/proceed question. Skip read-next unless the user asks.

If the user references "this file", "this component", "this parser", or "this error" but no source artifact is available, state that the exact cause needs the missing artifact. You may teach the diagnostic model, but do not invent a concrete root cause.

## Frontend Teaching Lane

When the concept touches frontend work, prefer this ladder:

1. User-visible behavior: what changes in the interface.
2. HTML semantics: what structure or meaning the browser sees.
3. CSS mechanics: cascade, specificity, box model, layout, containment, responsive constraints, transitions, or stacking context.
4. JavaScript runtime: events, closures, promises, modules, data transformation, browser APIs, or scheduling.
5. TypeScript model: what shape the data has and what invariants the compiler can protect.
6. React model: component boundary, props, state, effects, memoization, rendering, hydration, or reconciliation.
7. Design-engineering tradeoff: maintainability, accessibility, performance, design-system fit, ergonomics, and failure modes.

For design-to-code explanations, translate visual or interaction language into mechanics:

- hierarchy -> DOM order, semantic headings, spacing scale, type scale, contrast, and reading path
- responsiveness -> grid/flex constraints, min/max sizes, container queries, overflow behavior
- polish -> event timing, transition easing, focus states, reduced-motion handling, and loading states
- design-system fit -> token use, component API, variant boundaries, and escape-hatch cost

## Clever Function Rule

When you write or propose a clever function, abstraction, parser, index, state machine, cache, scheduler, retry loop, ranking function, data model, or concurrency pattern, include a short explanation:

```markdown
**Concepts Used**
- [concept] -> [what it means] -> [how this code uses it]

**Why This Shape**
[why this design beats the simpler alternative here]

**To Understand This Choice**
- [reading topic] -> [what it teaches]
```

Do this even if the user did not ask, because clever code without a learning trail becomes future confusion.

Do not import Why's own knowledge-base examples into unrelated answers. Explain only the mechanisms actually used by the requested code or artifact.

## Knowledge Base Writes

Use Tolaria through `core:portent` for durable learning records.

Write only after explicit save intent. Examples: "save this to my learning profile", "remember this concept", "add this to the knowledge base", "track that I learned this".

Prefer these objects:

- `Note` for a concept, mental model, or reusable explanation.
- `Topic` for a broad concept cluster.
- `Event` for a learning session, walkthrough, or completed teaching pass.

Minimum concept-note shape:

```markdown
---
type: Note
organized: false
archived: false
related_to:
  - "[[Why]]"
---

# Concept Name

## Concept

[what it means]

## Why It Matters

[what decision, behavior, or implementation it changes]

## How It Works

[observable mechanics]

## Alternatives

- [alternative] -> when it wins -> when it fails

## Tradeoffs

- [choice] -> benefit -> cost -> risk

## Read Next

- [topic] -> why it matters

## Seen In

- [source context]
```

Do not create `~/.agents/memory/teach/`, `~/.agents/memory/why/`, SQLite indexes, or local profile files. Tolaria is the canonical knowledge base.

## Output Rules

- Answer the learning need first.
- Use concrete examples from the active context.
- Explain alternatives through when they win and fail.
- Explain tradeoffs as benefit, cost, and risk.
- Ask only one grounding question before execution.
- Avoid fake certainty about what the user has learned; use confirmation or observed user response.
- Keep knowledge-base updates focused on durable concepts, not every small fact.
- Never put private project details into a reusable concept note unless the source context matters for recall.
- Do not claim a Tolaria write happened unless you created or updated the note and can name it.
