# Ritual scheduling

The shared pattern for skills that deliver **one artifact on a recurring schedule** — `register --feed` (daily), `augury` (daily), `nemesis` (weekly). This is a **platform concern; this plugin does not ship a scheduler.** The skills ship their generative core and document the wiring here.

## Two ways to fire a ritual

1. **Claude Code web cron routines** — the cloud platform supports scheduled sessions. Create a routine that opens a session and invokes the skill with a fixed prompt (the register and feed for `register --feed`, the draw config for `augury`, the conviction set for `nemesis`). See the Claude Code on the web docs: https://code.claude.com/docs/en/claude-code-on-the-web
2. **`core:loop`** — the dex `loop` skill runs a prompt or slash command on a recurring interval. Suitable for a long-lived local session. Example: `/loop 24h /register --feed weather "Old Testament prophet"`.

## What the skill must guarantee for a ritual to work

- **Deterministic invocation surface.** The skill takes its full configuration as arguments (register, feed source, draw size, conviction store path) so a cron prompt can pass them with no human in the loop.
- **Stable state across runs.** `register --feed` reuses the same register; `nemesis` reads/writes the same conviction store under `~/.agents/memory/`; `augury` draws from the same collection. The run is idempotent in config, fresh in output.
- **Graceful no-op.** If the feed/collection/source is empty or unreachable on a given day, the skill says so in one line and exits cleanly — a ritual that crashes on an empty day breaks the streak.

## Dry-run before wiring cron

Always run the skill once manually with the exact arguments the routine will use, confirm the artifact is produced, then wire the schedule. Never debug a skill through the cron surface.
