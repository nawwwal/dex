# Teach Skill Design

## Goal

Add a new `teach` skill to the Dex `core` plugin. The skill turns unfamiliar context into a teaching pass before execution, records concepts the user has learned as Markdown notes, rebuilds a SQLite search index from those notes through a Codex lifecycle hook, and ships a Dex eval suite that judges response quality, not only trigger behavior.

## Decisions

- Trigger explicitly with `$teach` and implicitly for requests such as "teach me", "explain this", "walk me through this", "I don't understand this", "before doing it help me understand", or "what concepts does this use".
- Store concept memory in `~/.agents/memory/teach/`.
- Store learner context in `~/.agents/memory/teach/profile.md`.
- Use Markdown notes as the canonical source of truth. Example: `~/.agents/memory/teach/event-loop.md`.
- Store the generated SQLite index next to the notes at `~/.agents/memory/teach/index.sqlite3`.
- Treat SQLite as a rebuilt index, not the canonical record. If the database is corrupted, the agent can rebuild it from Markdown.
- Use SQLite FTS5 for local full-text search across title, aliases, tags, related concepts, source context, and body. This gives practical semantic lookup through frontmatter and concept language without adding an embedding dependency.
- Ship the SQLite rebuild as a plugin-bundled Codex `Stop` hook, not as a manual skill step. The hook checks whether concept Markdown is newer than the index and rebuilds only when needed.
- Keep the hook explicitly documented as Codex plugin-hook behavior: plugin hooks are opt-in through `[features].plugin_hooks = true` and still require normal trust review.
- Include a Dex-style eval suite with routing cases, artifact cases, deterministic script checks, response look-and-feel rubrics, negative controls, and repair-regression cases.

## Runtime Behavior

When `teach` loads, it assumes the active context is unfamiliar to the user. It should first explain how the context works, what concepts are involved, what alternatives exist, and what tradeoffs matter. It should not rush into the original task until the user has a workable grasp.

Before teaching, it should read `~/.agents/memory/teach/profile.md` when present. For this user, the initial profile should say: the user is a designer moving toward design engineering, wants to understand frontend intricacies deeply, and especially wants HTML, CSS, JavaScript, TypeScript, React, rendering, browser behavior, state, component architecture, accessibility, and interaction details explained through design-to-code mechanics. Backend or tooling concepts should still be taught when relevant, but frontend examples should be the default bridge when that makes the concept easier to understand.

For code changes, if the agent introduces a clever function, abstraction, parser, state machine, cache, index, concurrency pattern, or data model, it must name the concepts it used and tell the user what they would need to read to understand the design choice.

The teaching pass should use one small grounding gate before execution. The gate can be a short confirmation or a single question that checks whether the user wants more explanation. It should not become a quiz unless the user asks for that.

## Memory Format

The learner profile uses Markdown with frontmatter:

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

Use this profile to choose examples, analogies, and reading paths. Keep it short and update it when the user states a new learning goal or stronger grasp.
```

Each concept note uses YAML frontmatter and plain Markdown:

```markdown
---
title: "SQLite FTS5"
aliases: ["full text search", "FTS"]
tags: ["sqlite", "search", "indexing"]
learned_at: "2026-05-18"
source_context: "Teach skill design"
confidence: "introduced"
related_concepts: ["inverted index", "ranking", "canonical source"]
---

# SQLite FTS5

## Concept

FTS5 is SQLite's built-in full-text search engine.

## Why It Matters

It lets local files become searchable without running a separate search service.

## How It Works

SQLite stores tokenized text in a virtual table and can rank matches with BM25.

## Alternatives

- Plain grep
- SQLite normal tables with LIKE
- Vector embeddings
- External search engines

## Tradeoffs

FTS5 is local and reliable, but it is lexical search, not embedding-based semantic search.

## What To Read Next

- SQLite FTS5 virtual tables
- Inverted indexes
- BM25 ranking

## Seen In

- Dex teach skill concept index
```

## SQLite Index

The skill includes a deterministic script at `plugins/core/skills/teach/scripts/teach_memory.py`.

The script supports:

- `ensure`: create `~/.agents/memory/teach/` and initialize `index.sqlite3`
- `index`: rebuild SQLite tables from Markdown notes
- `search <query>`: search the index
- `validate`: confirm the memory directory, database schema, and FTS5 support are usable

The database stores one row per Markdown concept and a linked FTS table. The script never treats SQLite as canonical. It must exclude `profile.md` and `README.md` from concept indexing.

The core plugin bundles a Codex hook:

- `plugins/core/hooks/hooks.json`
- `plugins/core/hooks/reindex_teach_memory.py`

The hook runs on `Stop`, uses the plugin root to locate `teach_memory.py`, and rebuilds `~/.agents/memory/teach/index.sqlite3` only when Markdown concept notes are newer than the index or the index is missing.

## Eval Suite

The `teach` eval suite must test behavior, not just routing. It covers:

- explicit trigger
- implicit trigger
- contextual trigger
- negative control
- artifact/source-backed teaching
- clever-function explanation
- Markdown memory and hook-index behavior
- response look and feel
- frontend-personalized teaching
- over-teaching regression
- execution-gate regression
- benchmark comparison against a no-skill baseline

Response-quality grading checks whether the output feels like teaching: it should build a mental model, use the active context, define unfamiliar terms once, compare alternatives through concrete tradeoffs, avoid lectures when a compact answer is enough, and ask one grounding question before execution.

## Repo Changes

Create:

- `plugins/core/skills/teach/SKILL.md`
- `plugins/core/skills/teach/scripts/teach_memory.py`
- `plugins/core/skills/teach/scripts/validate_teach_memory.py`
- `plugins/core/skills/teach/scripts/validate_teach_evals.py`
- `plugins/core/skills/teach/evals/evals.json`
- `plugins/core/skills/teach/agents/openai.yaml`
- `plugins/core/hooks/hooks.json`
- `plugins/core/hooks/reindex_teach_memory.py`

Modify:

- `README.md`
- `plugins/core/.codex-plugin/plugin.json`
- `plugins/core/.claude-plugin/plugin.json`

## Validation

Run:

- `python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/core/skills/teach`
- `python3 plugins/core/skills/teach/scripts/validate_teach_memory.py`
- `python3 plugins/core/skills/teach/scripts/validate_teach_evals.py`
- `python3 plugins/core/hooks/reindex_teach_memory.py --memory-dir /tmp/dex-teach-memory`
- `python3 plugins/core/skills/teach/scripts/teach_memory.py ensure --memory-dir /tmp/dex-teach-memory`
- `python3 plugins/core/skills/teach/scripts/teach_memory.py index --memory-dir /tmp/dex-teach-memory`
- `python3 plugins/core/skills/teach/scripts/teach_memory.py search "sqlite search" --memory-dir /tmp/dex-teach-memory`

Forward-test the implicit trigger with prompts that ask for explanation, conceptual walkthroughs, and code design choices.
