# Pre-Repair Log Snapshot Fixture

This fixture is the baseline behavior snapshot for `benchmark-against-log-snapshot`.

## User request

Use portent after /wrap. We committed `feat: add Portent skill`, left one next step to release core later, and changed README plus plugins/core/skills/portent/SKILL.md.

## Pre-repair output

The old log workflow wrote a session note to:

```text
~/.claude/log/2026-05-21-portent-skill.md
```

It also appended a carry-forward task to:

```text
~/.claude/TASKS.md
```

## Pre-repair frontmatter

```yaml
---
type: session
date: 2026-05-21
project: dex
decisions-count: 1
tasks-count: 1
---
```

## Pre-repair body

- Changed README and plugins/core/skills/portent/SKILL.md.
- Commit: `feat: add Portent skill`.
- Next step: release core later.

## Baseline scoring notes

- canonical_destination: fails because the canonical write target is a legacy Claude log path.
- type_accuracy: fails because `type: session` is not a Portent object type.
- lifecycle: fails because organized/archived lifecycle fields are absent.
- relationships: fails because project context is a loose string, not `belongs_to` or `related_to`.
- legacy_avoidance: fails because it writes to both `~/.claude/log` and `~/.claude/TASKS.md`.
