# Portent Retrieval

qmd is the retrieval plane. Tolaria search is not.

Use the configured vault path from global `~/.agents/AGENTS.md` as already resolved. Use Tolaria for vault discovery only when the configured path is unreadable, another vault is named, multiple vaults are plausible, or a Tolaria operation fails because the vault target is ambiguous. Use qmd for finding and reading knowledge.

## Mode Selection

Use one or two retrieval modes well. Do not run every qmd mode by default.

| Need | Use | Why |
| --- | --- | --- |
| Known filename, note title, quote, PR, issue, channel, person, error text, or exact phrase | `qmd search` | Exact anchors should stay exact. |
| Vague memory, behavior, preference, team context, or concept that may be phrased differently | `qmd vsearch` | Semantic recall catches meaning when words do not match. |
| Cross-note synthesis, historical state, current plate, ambiguous project context, or a high-stakes answer | `qmd query` | Hybrid retrieval can combine `lex`, `vec`, and `hyde`, then rerank. |
| Any factual answer, brief, or writeback based on retrieved context | `qmd get` or `qmd multi-get` | Snippets are leads; source text is evidence. |

Default paths:

- Known anchor: `search` -> `get`.
- Vague memory: `vsearch` -> `get`.
- Complex task: `query` -> `get`/`multi-get`.
- Weak, partial, or contradictory result: try another mode or a better angle.

## Fast Path

1. Check qmd only when health matters:

```bash
qmd status
```

2. Choose the retrieval mode that fits.

Search exact anchors:

```bash
qmd search -c portent '"<exact phrase>" <project> <person> <repo> <channel>' -n 10
```

Search semantic meaning:

```bash
qmd vsearch -c portent 'natural language version of the question and likely related concepts' -n 10
```

Search with hybrid intent:

```bash
qmd query -c portent $'intent: find the current source-backed state for <topic>
lex: "<exact phrase>" <project> <person> <repo> <channel>
vec: natural language version of the question
hyde: A likely answer would mention the current decision, blocker, owner, and source note.'
```

3. Read source:

```bash
qmd get qmd://portent/path.md:40:80
qmd multi-get 'events/2026-06-*.md' -l 80
```

4. Answer from retrieved text. Name unchecked sources when relevant.

## Query Angles

Use at least three angles before saying no context:

- exact anchors: PR, issue, repo, person, title, channel, meeting name, error text
- aliases: old project names, teammate names, shorthand, feature labels
- maps/logs: `portent-index`, `brain-log`, `agent-behavior-gotchas`, active project/task maps
- broad semantic query: what the user means, not only their words
- recent notes: today/week event notes when the state is time-sensitive

## qmd Syntax

- `lex`: exact and keyword search. Best for names, quoted phrases, PRs, issues, channels, filenames.
- `vec`: semantic search. Best when the words may differ.
- `hyde`: hypothetical answer. Best for behavior, history, preference, synthesis, or "what should I know" questions.
- `vsearch`: standalone vector search. Use it when exact anchors are weak or the user is asking from memory.
- `query`: hybrid search with expansion and reranking. Use it when the task needs synthesis, broad recall, or a better ranking than the first pass gave you.
- `get`/`multi-get`: source reading. Use these before answering from snippets.

Put the strongest signal first. Use `candidateLimit`/`-C` and `minScore` only after recall is good enough.

## Degraded Retrieval

If qmd MCP is absent, use qmd CLI.

If qmd CLI is broken or stale:

1. Say qmd is degraded.
2. Use direct Markdown search inside the resolved vault path.
3. Read matching files directly.
4. Continue the task.
5. Use `references/setup.md` only if the user wants repair/setup.

Do not switch to Tolaria full-text search as the default fallback. It misses too much.

## No Context Contract

"No context" is valid only after naming what was checked:

- qmd queries attempted, or why qmd was unavailable
- Markdown paths/patterns searched
- key maps/logs checked
- live sources not checked

If you skipped retrieval because the task was trivial or local-only, say `Portent skipped: <reason>`.
