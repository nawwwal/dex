# Agent Protocol Reference (Claude Code)

## Claude Code as the Coding Agent

Symphony uses Claude Code CLI as its subprocess coding agent.

**Correct invocation:**
```bash
claude --print --output-format stream-json --max-turns <N> --dangerously-skip-permissions
```

> **`--dangerously-skip-permissions`** disables all tool-use confirmation prompts — required for unattended operation. Without OS-level isolation, the agent can read/write/exec anything the Symphony process can. Use `allowed_tools` in WORKFLOW.md codex config to restrict tool access.
>
> **`--max-turns`** — verify this flag exists in your installed version with `claude --help | grep max-turns`. If missing, check the Claude Code changelog.
>
> **`--dangerously-skip-permissions` is likely to be renamed** — Anthropic has signaled intent to replace it with a scoped permission model. Check the changelog if this flag stops working.

Prompt is passed via **stdin**:
```typescript
// Use proc.stdin.end(renderedPrompt) — simpler and handles backpressure correctly
const proc = spawn(config.codex?.command ?? "claude", [
  "--print",
  "--output-format", "stream-json",
  "--max-turns", String(config.agent.max_turns),
  "--dangerously-skip-permissions",
], {
  cwd: workspacePath,       // MUST be the per-issue workspace (see workspace-safety.md)
  stdio: ["pipe", "pipe", "pipe"],
  env: { ...process.env },  // WARNING: $DEVREV_TOKEN is inherited. Scope if needed.
});

// ⚠️ PROMPT INJECTION RISK: issue fields come from DevRev and are untrusted.
// Wrap them in delimiters in your prompt_template, e.g.:
// <issue_description>{{issue.description}}</issue_description>
// See workflow-md-schema.md for the safe template pattern.
proc.stdin.end(renderedPrompt);

// Always drain stderr — unread pipe buffers block the subprocess on long runs
proc.stderr.on("data", (chunk) => {
  console.error(`[${issue.identifier}] stderr:`, chunk.toString().trim());
});
```

**PATH note for daemons:** When running as systemd/launchd/supervisor, PATH is minimal. `claude` may not resolve. Either set PATH explicitly in `env`, or use an absolute path: `which claude` at install time and store the result in `codex.command`.

**Do NOT:**
- Pass prompt as a positional arg — doesn't work for multi-line prompts
- Split line parsing without buffering — chunks can split a JSON object across `data` events

## Startup Sequence (First Turn)

```
1. Prepare workspace (see workspace-safety.md)
2. Build prompt: render WORKFLOW.md prompt_template with issue fields
   ⚠️  Wrap untrusted fields in XML tags (see prompt injection note above)
3. Spawn claude subprocess (cwd = workspace path)
4. Write rendered prompt to stdin via proc.stdin.end(prompt)
5. Stream and parse newline-delimited JSON events from stdout (buffer across chunks)
```

**session_id note:** Symphony uses `"<pid>-<turn_number>"` as its internal correlation ID for structured logs. This is NOT the session_id Claude Code emits in stream events — Claude Code emits its own UUID from the API. Capture both separately if needed.

## Continuation Turns

When a worker exits cleanly (exit code 0), the orchestrator checks the issue's current DevRev stage:

- **Stage is in `terminal_states`** → mark complete, release from running set
- **Stage is NOT in `terminal_states`** → schedule continuation turn (1,000ms delay)

Continuation turns:
- Spawn a **new subprocess** in the same workspace
- **First turn only** receives the full task prompt
- **Subsequent turns** receive continuation guidance (e.g. "Continue from where you left off.")
- Reuse same workspace directory — prior session's file changes persist
- Continue until `agent.max_turns` — exhausting max_turns is a **continuation** (not failure); orchestrator reschedules with fixed 1s delay, not exponential backoff

## Three Timeout Layers

| Timeout | Config key | Default | What it covers |
|---|---|---|---|
| `read_timeout_ms` | `codex.read_timeout_ms` | 5,000ms | Per request/response during startup |
| `turn_timeout_ms` | `codex.turn_timeout_ms` | 3,600,000ms | Total wall time for one full turn |
| `stall_timeout_ms` | `agent.stall_timeout_ms` | 300,000ms | No stdout for this long → Stalled |

Stall detection runs in the orchestrator reconcile step. Check `LiveSession.last_event_at_ms` (updated on every stdout event) against `now - stall_timeout_ms`.

## Token Accounting

Parse `usage` from Claude Code stream events. **Buffer lines across chunks** — a single JSON object can be split across two `data` events:

```typescript
let buffer = "";
let threadInputTotal = 0;
let threadOutputTotal = 0;

proc.stdout.on("data", (chunk) => {
  buffer += chunk.toString();
  const lines = buffer.split("\n");
  buffer = lines.pop()!; // retain incomplete last line for next chunk
  for (const line of lines.filter(Boolean)) {
    try {
      const event = JSON.parse(line);
      // event.usage.thread contains running totals (not per-event deltas)
      // Note: usage.thread shape is undocumented — verify against your Claude Code version
      if (event.usage?.thread) {
        threadInputTotal = event.usage.thread.input_tokens;
        threadOutputTotal = event.usage.thread.output_tokens;
      }
      // Update stall detection timestamp on any event
      session.last_event_at_ms = Date.now();
    } catch {}
  }
});
```

Update `LiveSession.token_counts` and accumulate into `OrchestratorRuntimeState.token_totals`.

## Tool Failures

- **Unsupported dynamic tool call**: return a failure result and continue — NEVER stall the turn
- **User-input-required event**: hard failure — Claude Code cannot prompt for input in unattended mode. Log and terminate with `Failed` state.

## Optional: devrev_graphql Tool

Expose raw DevRev GraphQL access to the agent using Symphony's `$DEVREV_TOKEN`:
- One operation per call; reject multi-operation documents
- Return `{ success: boolean, data?: unknown, error?: string }`
- Never expose the token to the agent's output stream
- No rate-limiting is enforced by default — a prompt-injected agent could spam mutations
