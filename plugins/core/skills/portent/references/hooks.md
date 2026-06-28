# Portent Hooks

Hooks keep the knowledge loop present. They do not replace the skill.

Use hooks for three things:

1. **Prompt receipt**: inject the already-resolved default vault, qmd-first retrieval rule, no Tolaria search rule, capture-first writeback rule, context-hunger reminder, and correction-writeback reminder at `UserPromptSubmit`.
2. **Setup doctor**: check the hook file and manifest during setup so agents know whether the receipt is installed.
3. **Future stop audit**: if `Stop` hooks are added later, keep them tiny: remind the agent to write durable context before final response. Do not run vault scans or qmd retrieval inside the stop hook.

Do not put retrieval inside hooks. Prompt hooks are hot-path and run before the agent knows the real task. Retrieval belongs in `references/retrieval.md`; writeback belongs in `references/writeback.md`.

The current shipped hook is `plugins/core/hooks/portent_context_receipt.py`, registered from `plugins/core/hooks/hooks.json` on `UserPromptSubmit`.

Readiness checks:

- `plugins/core/.codex-plugin/plugin.json` points to `./hooks/hooks.json`.
- `hooks.json` registers `UserPromptSubmit`.
- `portent_context_receipt.py --self-test` passes.
- The emitted receipt names the configured vault, says not to call `list_vaults` just to confirm it, names the qmd collection, qmd source-read rule, Tolaria writeback role, capture-first default, context-hunger question, correction-writeback rule, duplicate-note avoidance, and "no update needed" audit.

If hooks are disabled or unavailable, do not fail Portent. Say hooks are degraded and use the skill manually.
