# PMB CLI Reference

Use this reference when a task needs detailed PMB command knowledge. Prefer MCP tools during an agent session; use CLI commands for terminal capture, import, project tracking, inspection, maintenance, and workspace operations.

Sources checked:

- https://docs.pmbai.dev/reference/cli/write
- https://docs.pmbai.dev/reference/cli/read
- https://docs.pmbai.dev/reference/cli/manage
- Local `pmb --help` command surface.

## Choose The Interface

| Need | Prefer |
| --- | --- |
| Start work with relevant context | `prepare` |
| Specific memory question | `recall` or `pmb recall` |
| Broad topic summary | `overview` or `pmb overview` |
| Named project state | `project_overview` |
| Session recovery | `session_brief` or `pmb session brief` |
| Durable in-session write | `record_batch` |
| One current attribute value | `record_keyed_fact` |
| Terminal capture | `pmb note`, `pmb fact`, `pmb learn`, `pmb remember` |
| File or folder auto-capture | `pmb watch` |
| Existing source ingestion | `pmb import` |
| Code/project knowledge | `pmb index project`, `pmb track changes`, `pmb track modules`, `pmb track install` |
| Resume note | `pmb resume save`, `pmb resume show`, `pmb resume install` |
| Memory health and repair | `pmb doctor`, `pmb stats`, `pmb reindex`, `pmb regraph`, `pmb repair-keyed` |
| Reversible cleanup | `pmb forget`, `pmb delete`, `pmb restore`, `pmb forget-topic` |
| Backup before risky work | `pmb snapshot create`, `pmb export` |

## Write Memory

### In-Agent Writes

Use one `record_batch` near the end of a substantive turn. Write atomic entries, not a transcript dump.

| Item type | Use when | Good content shape |
| --- | --- | --- |
| `fact` | Stable truth | "Project X uses Y for Z." |
| `lesson` | Reusable correction, rule, or failure to avoid | "When doing X, first check Y because Z." |
| `goal` | Future or ongoing intent | title plus `pending` or `in_progress` |
| `plan` | Multi-step future intent | clear title and scope |
| `activity` | Completed work, decision, or failure | include `kind`: `completed`, `decision`, or `failure` |
| `milestone` | Named checkpoint in a longer chain | chain name, title, and state |

Use `record_keyed_fact` when there is exactly one current value for an attribute, such as a default workspace, preferred backend, active project, or current owner.

Use `update_goal` instead of writing a new fact when an existing goal changes status or progress.

### Terminal Capture

Use the terminal commands when the user or shell session needs to add memory outside the active agent flow.

```bash
pmb note "decided to use Postgres for JSONB" --pin
pmb fact "the staging DB is read-only"
pmb learn "always run make fmt before committing"
pmb learn "rerunning command X broke Y; use Z instead" --failed
pmb remember "deploy command" "make deploy ENV=prod"
pmb watch ~/notes/daily.md
```

Notes:

- `pmb note` is the quick scratchpad command. Use `--pin` for must-keep memory and `--ttl 30d` for temporary memory.
- `pmb learn` is procedural memory. Use it for corrections, durable rules, and failures.
- `pmb fact` is for standalone truth.
- `pmb remember` stores a question/answer pair.
- `pmb watch` auto-captures new paragraphs from a file or folder; use `--once` when wiring it into scheduled jobs.

### Imports

Use `pmb import SOURCE PATH` to seed PMB from existing exports or note folders. Run `--dry-run` first when the input is large or unfamiliar.

```bash
pmb import chatgpt ~/Downloads/conversations.json --dry-run
pmb import claude ~/Downloads/claude-export/ --dry-run
pmb import mem0 mem0_dump.json --dry-run
pmb import markdown ~/notes/ --dry-run

pmb import chatgpt ~/Downloads/conversations.json
pmb import claude ~/Downloads/claude-export/
pmb import mem0 mem0_dump.json
pmb import markdown ~/notes/
```

Import guidance:

- Default chat imports keep user-role content to reduce noise; pass `--roles user,assistant` only when assistant responses are useful source material.
- Treat bulk imports as source ingestion, then inspect recall quality before deleting the source.
- After import, inspect with `pmb stats`, `pmb audit`, `pmb overview "<topic>"`, and targeted `pmb recall "<question>"`.

### Project Tracking

Use project tracking to make code repositories searchable by purpose and change intent.

```bash
pmb index project .
pmb track changes --max-commits 5
pmb track modules --limit 50
pmb track install
```

Command roles:

- `pmb index project` records file and symbol structure. It is idempotent and should be run before module summaries.
- `pmb track changes` reads new git commits, summarizes why they changed, and links memory to touched files. It is cursor-based and idempotent per repository.
- `pmb track modules` writes one-line module purpose summaries for indexed files.
- `pmb track install` installs a non-blocking post-commit hook and should not clobber an existing hook.

Before installing hooks, inspect any existing `.git/hooks/post-commit` or repository hook configuration. If a repository uses a custom hook path, install or bridge PMB in that path instead of assuming `.git/hooks`.

### Distillation And Consolidation

Use distillation to extract durable lessons/failures from a session. Use consolidation to merge recent low-level entries into higher-signal memory.

```bash
pmb distill --dry-run --backend claude
pmb distill --backend claude

pmb consolidate --dry-run --backend claude --since-days 14
pmb consolidate --backend claude --since-days 14
```

Run dry runs first. Inspect proposed writes for correctness, duplicates, and privacy before committing them.

### Resume Notes

Use resume notes when a repository should carry a local "where we are now" snapshot generated from typed PMB memory.

```bash
pmb resume save
pmb resume save --path .pmb/resume.md
pmb resume show
pmb resume install
```

`pmb resume install` enables automatic refresh at turn end. Hand-written additions below PMB's marker line are preserved across regenerations.

## Retrieve Memory

### In-Agent Retrieval

Use the narrowest read that answers the task:

- `prepare`: first context bundle for a non-trivial task.
- `recall`: specific question.
- `overview`: broad topic state.
- `project_overview`: named project state.
- `session_brief`: continuity after compaction, interruption, or long sessions.
- `find_lessons`: procedural rules, corrections, and failure memory.
- `list_goals`: open or pending goals.

When a surfaced lesson applies, act on it and then call `mark_lesson_followed` with a one-line note.

### Terminal Search And Inspection

```bash
pmb recall "what port did we choose" -k 5
pmb recall "release workflow for core plugin" --rerank
pmb why "what port did we choose"
pmb overview "authentication"
pmb timeline --days 7
pmb insights
pmb digest week
pmb audit
pmb lessons
pmb reminders --within 7
pmb list -n 20 --type decision
pmb stats
```

Command roles:

- `pmb recall` returns ranked memory hits with source, confidence, freshness, and markers for lessons/failures.
- `pmb why` explains ranking behavior.
- `pmb overview` returns a structured topic summary: facts, decisions, lessons, goals, and timeline.
- `pmb timeline` is chronological, useful when sequence matters.
- `pmb insights` shows analytics such as totals, type breakdown, growth, top topics, lessons, and goals.
- `pmb digest` recaps recent memory for a day, week, month, or day count.
- `pmb audit` shows a grouped, read-only view of what PMB knows.
- `pmb lessons` lists procedural memory.
- `pmb reminders` surfaces due or overdue goals.
- `pmb list` inspects recent events by count or type.
- `pmb stats` checks workspace size and type counts.

### Code And Graph Reads

```bash
pmb history path/to/file.ts
pmb correlate path/to/file.ts
pmb graph stats
pmb graph top
pmb graph neighbors "auth"
```

Use `history` for file-level change memory, `correlate` for files that change together, and `graph` when entity relationships matter.

## Manage Memory

### Health And Runtime

```bash
pmb doctor
pmb stats
pmb warmup
pmb daemon status
pmb daemon restart
```

Use `doctor` for setup/runtime diagnosis, `stats` for workspace counts, `warmup` to load recall dependencies ahead of time, and `daemon` commands when recall latency or hook delivery depends on the persistent process.

### Export, Snapshot, And Sync

```bash
pmb export --format json --out memory.json
pmb export --format markdown --out memory.md
pmb snapshot create --note "before cleanup"
pmb snapshot list
pmb snapshot restore <snapshot-id>
pmb workspaces
pmb workspace init --remote git@github.com:me/pmb-memory.git
pmb workspace status
pmb workspace push
pmb workspace pull
pmb workspace clone <url> <name>
pmb workspace export bundle.pmb
pmb workspace import bundle.pmb restored-name
```

Create a snapshot before bulk cleanup, model changes, large imports, or repair commands. Use export when the user needs a readable copy. Workspace sync and export/import are deliberate network or bundle operations; run them only when requested or clearly needed.

### Deletion, Cleanup, And Repair

Prefer reversible operations first.

```bash
pmb forget <ulid>
pmb delete <ulid>
pmb restore <ulid>
pmb forget-topic "topic name" --dry-run
pmb forget-topic "topic name" --yes
pmb forget-auto --dry-run
pmb pin <ulid>
pmb tag <ulid> important project-x
pmb untag <ulid> project-x
pmb ttl <ulid> 30d
pmb ttl <ulid> clear
pmb prune-expired
pmb decay
pmb declutter
pmb dedupe
pmb compact
pmb reindex
pmb regraph
pmb repair-keyed
pmb feedback <ulid> helpful
```

Rules:

- Use `forget` or normal `delete` for reversible archive behavior.
- Use hard deletion only after explicit user approval.
- Use `forget-topic --dry-run` before archiving a topic.
- Use `pin` for memory that should keep maximum importance and avoid automatic archival.
- Use `tag` and `untag` for local organization.
- Use `ttl` for time-bound memory and `prune-expired` to archive expired entries.
- Use `reindex` when embeddings need rebuilding with the active model.
- Use `regraph` when entity associations need rebuilding.
- Use `repair-keyed` when current-value facts conflict.
- Use `feedback` when recall quality should influence future ranking.

## Safe Workflow

1. Read first with `prepare`, `recall`, `overview`, or the relevant CLI inspection command.
2. Write the smallest durable memory that will help a future session.
3. For bulk imports or cleanup, run dry-run or snapshot first.
4. Verify with targeted recall or overview.
5. Do not claim PMB was read, updated, imported, or repaired unless the command or MCP tool actually ran.
