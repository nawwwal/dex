# Portent Setup

Use this when Tolaria, Portent, qmd, the `portent` qmd collection, qmd local models, MCP wiring, or global agent instructions are missing, stale, or broken.

Goal: make the setup feel like a guided conversation, not a sysadmin checklist. Detect first, explain plainly, ask before installing or overwriting, then do the smallest repair that restores retrieval and writeback.

## Detection

Check what works:

```bash
test -f ~/.agents/AGENTS.md
test -d "<vault_path>"
which qmd
qmd status
qmd collection list
node --version
npm ls -g @tobilu/qmd --depth=0
```

Use Tolaria MCP when visible:

1. `mcp__tolaria__list_vaults`
2. `mcp__tolaria__get_vault_context` for the selected vault
3. `mcp__qmd__status`

Report in plain language:

```text
I found Tolaria, but qmd has no `portent` collection.
Your notes are safe. I need to index the Markdown vault so agents can search it well.
Set that up now?
```

Do not run installs, clone repositories, create vaults, remove collections, or download models without user confirmation.

## Readiness Check

Run this before setup and after setup:

1. Global instructions:
   - `~/.agents/AGENTS.md` exists.
   - It names the default Portent vault path.
   - It names the qmd collection, usually `portent`.
   - It says not to rediscover the vault on every run.
2. Vault:
   - The configured vault path exists and is readable.
   - The vault has `AGENTS.md`.
   - The vault has `brain-log.md`, `agent-behavior-gotchas.md`, and `portent-index.md` or equivalent orientation notes.
3. qmd:
   - `qmd status` works.
   - The configured vault is indexed as collection `portent`.
   - There are no pending embeddings.
   - Local embedding/reranking/generation models work, or degraded mode is explicitly reported.
4. MCP:
   - Tolaria MCP can list or open the configured vault when available.
   - qmd MCP is visible when the runtime supports it, otherwise qmd CLI works.
   - Codex/Claude MCP config points to the expected servers; report missing MCPs instead of silently falling back.
5. Hooks:
   - `plugins/core/.codex-plugin/plugin.json` points to `./hooks/hooks.json`.
   - `plugins/core/hooks/hooks.json` registers `UserPromptSubmit`.
   - `plugins/core/hooks/portent_context_receipt.py --self-test` passes.
   - Hook output names the configured vault, qmd collection, source-read rule, Tolaria writeback role, and writeback audit.
6. Writeback:
   - A harmless smoke note can be opened or refreshed in Tolaria.
   - Direct Markdown edits inside the vault are possible.
   - qmd can find the edited source after refresh.

If any check fails, report:

```text
Ready: no
Broken: <specific check>
Smallest fix: <one action>
Needs confirmation: yes/no
```

## Persist The Default Vault

Do this once during setup, not every agent run.

If the user confirms the vault path, add or update a short section in `~/.agents/AGENTS.md`:

```markdown
### Portent Knowledge Loop

Use `<vault_path>` and qmd collection `<collection_name>` as the default knowledge base. Do not rediscover the vault on every run.

Use qmd for retrieval. Use Tolaria MCP for note opening, refresh, UI context, and writeback. If qmd is unavailable, search Markdown directly inside `<vault_path>` and say qmd is degraded.
```

Do not overwrite unrelated global instructions. Patch the smallest existing Portent section if one exists; otherwise append a compact section.

## Missing Tolaria

If Tolaria MCP is not visible:

1. Try tool discovery.
2. If still unavailable, ask whether the user wants help setting up Tolaria.
3. Point them to the Tolaria app/repo from the existing note `[[tolaria]]`: `http://tolaria.md/` or `https://github.com/refactoringhq/tolaria`.
4. Ask them to open or create the Markdown vault folder they want agents to use.
5. Persist that vault path in `~/.agents/AGENTS.md`.
6. Continue after the configured local vault path is readable. Tolaria MCP can be repaired later if direct Markdown and qmd are working.

## Missing Portent Vault

If there is a vault but no Portent structure:

1. Explain that Portent is the object model: typed notes, relationships, and lifecycle fields.
2. Ask whether this vault should become the agent knowledge base.
3. If yes, create only the minimum starter files:
   - `AGENTS.md`
   - `README.md`
   - `portent.md`
   - `portent-index.md`
   - `brain-log.md`
   - `agent-behavior-gotchas.md`
4. Use `references/portent-spec.md` for object types and relationships.

Prefer updating an existing vault over cloning a new one. Clone or copy a template only when the user wants a fresh knowledge base.

## Missing qmd

If `qmd` is missing:

1. Ask before installing.
2. Install the current qmd package with npm when Node is available:

```bash
npm install -g @tobilu/qmd
```

3. Verify:

```bash
qmd --help
qmd status
```

If npm or Node is missing, stop and report the missing prerequisite. Do not install system packages unless the user explicitly asks.

## Missing Or Stale Collection

Use one active collection named `portent` for the selected Tolaria vault:

```bash
qmd collection add "<vault_path>" --name portent --mask "*.md"
qmd update
qmd embed -c portent
qmd status
```

If old duplicate collections exist, ask before removal:

```bash
qmd collection remove "<old_name>"
qmd cleanup
```

After direct Markdown edits, refresh the app and index:

```bash
qmd update -c portent
qmd embed -c portent
```

Use `mcp__tolaria__refresh_vault` when available.

## Missing Local Models

`qmd status` should show local models for embedding, reranking, and generation. If vectors are missing or model-backed query fails:

```bash
qmd embed -c portent
qmd query -c portent $'intent: setup smoke test\nlex: "agent-behavior-gotchas"\nvec: agent behavior rules in the knowledge base' --no-rerank
```

If model download fails, retry once with a narrower embed batch:

```bash
qmd embed -c portent --max-docs-per-batch 50 --max-batch-mb 8
```

If it still fails, keep lexical retrieval working with `qmd search` and tell the user semantic retrieval is degraded.

## Smoke Test

This smoke test intentionally exercises all qmd modes. Normal task retrieval should choose the mode that fits instead of running every command.

Before calling setup complete:

```bash
qmd search -c portent 'Agent Behavior Gotchas' -n 5
qmd vsearch -c portent 'reusable agent behavior corrections in the knowledge base' -n 5
qmd query -c portent $'intent: find agent behavior rules\nlex: "agent-behavior-gotchas"\nvec: reusable agent behavior corrections\nhyde: The knowledge base stores reusable agent behavior corrections in agent-behavior-gotchas and logs material maintenance in brain-log.'
qmd get qmd://portent/agent-behavior-gotchas.md:1:40
```

Expected result: `search`, `vsearch`, and `query` find a relevant note, `get` reads source text, and Tolaria can open or refresh the note. If retrieval works but writeback does not, say so; Portent needs both.
