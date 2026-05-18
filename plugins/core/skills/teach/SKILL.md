---
name: teach
description: "Use when the user explicitly invokes teach or asks to learn, understand, explain, walk through, unpack, or be taught unfamiliar code, tools, concepts, architecture, design choices, tradeoffs, or clever functions before execution. Also use implicitly when the user says they do not understand something, asks what concepts a solution uses, asks what to read to understand a design choice, or asks the agent to explain before doing the task."
---

# Teach

Turn unfamiliar territory into a clear learning pass before execution.

Assume the active context is unfamiliar to the user. Teach the concepts, mechanics, alternatives, and tradeoffs first. Move to the requested task only after the user has a workable grasp or explicitly asks you to proceed.

## Core Workflow

1. Identify the learning target from the user request, active files, pasted text, error output, code diff, tool output, or design context.
2. Read `~/.agents/memory/teach/profile.md` when present and use it to choose examples, analogies, learning depth, and reading paths.
3. Explain how it works in concrete terms. Define unfamiliar terms once, then use them naturally.
4. Name the important concepts involved.
5. Compare alternatives and tradeoffs.
6. Tell the user what to read next to understand the design choices.
7. Ask one grounding question or confirmation before execution:
   - "Should I slow down on any concept before I do the task?"
   - "Does this mental model work well enough for me to proceed?"
   - "Which part should I unpack further before I change the code?"
8. After the user confirms or shows understanding, perform the original task if it was part of the request.
9. Record learned concepts in `~/.agents/memory/teach/` when the concept is durable enough to matter later.
10. Let the bundled Codex hook rebuild the SQLite index after concept notes change. If hooks are disabled or the user asks for an immediate search, run the index command manually.

## Learner Profile

Personalization lives in:

```text
~/.agents/memory/teach/profile.md
```

If the file exists, read it before choosing examples or depth. If it does not exist and the user provides learning context, create it. Do not index `profile.md` as a concept note.

Seed this user's profile with:

```markdown
---
title: "Teach Learner Profile"
updated_at: "2026-05-18"
current_identity: "Designer moving toward design engineering"
target_identity: "Design engineer with strong frontend implementation taste"
primary_learning_lanes: ["html", "css", "javascript", "typescript", "react", "browser rendering", "accessibility", "component architecture", "interaction design"]
current_grasp: "Strong design/product intuition; building deeper frontend and engineering mental models"
teaching_preference: "Use design-to-code bridges, concrete UI examples, frontend mechanics, and tradeoffs before abstract backend/tooling explanations."
---

# Teach Learner Profile

The user is a designer on the path to becoming a design engineer.

They want frontend intricacies explained in detail: HTML semantics, CSS layout and cascade, responsive constraints, browser rendering, JavaScript runtime behavior, TypeScript type modeling, React component architecture, state, effects, accessibility, interaction polish, and design-system implementation.

Use frontend examples as the default bridge when they clarify a concept. Backend, indexing, tooling, or infrastructure concepts should still be explained when relevant, but connect them back to UI behavior, developer ergonomics, product experience, or design-to-code tradeoffs whenever possible.
```

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

## Memory Contract

Canonical concept memory lives in:

```text
~/.agents/memory/teach/
```

Use one Markdown file per concept:

```text
~/.agents/memory/teach/<slug>.md
```

Use this note format:

```markdown
---
title: "SQLite FTS5"
aliases: ["full text search", "FTS"]
tags: ["sqlite", "search", "indexing"]
learned_at: "2026-05-18"
source_context: "Teach skill"
confidence: "introduced"
related_concepts: ["inverted index", "BM25", "canonical source"]
---

# SQLite FTS5

## Concept

FTS5 is SQLite's built-in full-text search engine.

## Why It Matters

It makes local concept notes searchable without running a separate service.

## How It Works

SQLite stores tokenized text in a virtual table and ranks matches with BM25.

## Alternatives

- Plain grep
- SQLite `LIKE`
- Vector embeddings
- External search services

## Tradeoffs

FTS5 is local and reliable, but it is lexical search. Semantic usefulness comes from good titles, aliases, tags, related concepts, and body wording.

## What To Read Next

- SQLite FTS5 virtual tables
- Inverted indexes
- BM25 ranking

## Seen In

- Dex teach skill concept index
```

Use `confidence` values:

- `introduced`: user has seen the concept and basic meaning.
- `practiced`: user applied the concept in a task.
- `comfortable`: user can likely recognize or explain it later.

Do not overwrite a user's existing concept note blindly. Read it first, preserve useful existing material, then add a dated `## Seen In` or `## Notes` entry.

## SQLite Index

The SQLite index is generated, not canonical:

```text
~/.agents/memory/teach/index.sqlite3
```

Indexing is normally handled by the bundled Codex `Stop` hook in the Core plugin. Codex plugin hooks run only when `[features].plugin_hooks = true` is enabled and the hook is trusted through the normal `/hooks` review flow; when hooks are disabled, Markdown notes remain canonical and usable.

If the user asks for immediate search before the hook runs, or if the hook is disabled, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" index
```

For a health check, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" validate
```

For search, run:

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/teach_memory.py" search "query words"
```

If `$CLAUDE_SKILL_DIR` is not available, resolve the script relative to the loaded skill directory.

## Search Semantics

SQLite FTS5 is lexical search. It is not vector embedding search.

Make it semantically useful by writing strong frontmatter:

- `title`: canonical concept name.
- `aliases`: common names, abbreviations, and phrases the user might search.
- `tags`: domain and mechanism words.
- `related_concepts`: neighboring ideas.
- body: plain-language explanation with concrete examples.

If the user later asks for embedding search, keep Markdown as canonical and add embeddings as a derived index.

## Output Rules

- Answer the learning need first.
- Use concrete examples from the active context.
- Explain alternatives through when they win and fail.
- Explain tradeoffs as benefit, cost, and risk.
- Ask only one grounding question before execution.
- Avoid fake certainty about what the user has learned; use confirmation or observed user response.
- Keep memory updates focused on durable concepts, not every small fact.
- Never put private project details into a reusable concept note unless the source context matters for recall.
- Do not claim the hook ran unless you saw hook output or verified `index.sqlite3` was refreshed.
