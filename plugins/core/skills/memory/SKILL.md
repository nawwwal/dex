---
name: memory
description: Use when a task depends on persistent PMB memory, project facts, lessons, goals, decisions, session continuity, user preferences, or durable memory updates across agent sessions
---

# Memory

PMB is the persistent memory layer. Use it to start informed, keep work continuous, and leave durable state for future sessions.

## Start Pattern

- If PMB context is already injected and enough for the task, proceed.
- If the task depends on prior state, call `prepare` once with the user's request.
- Use `recall` for a specific question.
- Use `overview` for a broad topic.
- Use `project_overview` for a named project.
- Use `session_brief` after compaction, interruption, or a long gap.

## Write Pattern

Use `record_batch` before the final response when the work creates durable memory:

| Type | Use for |
| --- | --- |
| `fact` | Stable truth |
| `lesson` | Reusable rule, correction, or failure to avoid |
| `goal` | Ongoing or future work |
| `activity` | Lightweight work log |
| `milestone` | Checkpoint in a larger chain |

Use `record_keyed_fact` for attributes with one current value.

Use `list_goals` and `update_goal` when the task changes goal state.

Use `find_lessons` and `mark_lesson_followed` when lessons are surfaced.

## Boundaries

- Do not record secrets, raw credentials, private tokens, or unsupported guesses.
- Do not store noisy transcript detail when a concise fact, lesson, goal, activity, or milestone is enough.
- If PMB is unavailable, say so and continue from visible context only.
- Do not claim PMB was checked or updated unless it was.

## Final Response

Mention PMB reads or writes only when useful to the user: what was recalled, what was recorded, or what was unavailable.
