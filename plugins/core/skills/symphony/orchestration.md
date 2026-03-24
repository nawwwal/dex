# Orchestration Reference

## Poll Tick Sequence (EXACT ORDER — deviating from this breaks correctness)

```
1. Reconcile running issues
   ├── For each running issue: refresh state from DevRev (mcp__plugin_compass_devrev__get_issue)
   ├── Detect stalls (now - last_event_at_ms > stall_timeout_ms)
   └── Cancel stalled workers; log Stalled

2. Validate dispatch config preflight
   └── If WORKFLOW.md is invalid, block new dispatches — keep reconciling

3. Fetch candidate issues from DevRev

4. Sort candidates:
   └── priority ASC (lower number = higher priority)
       → created_at ASC (oldest first)
       → identifier ASC (tiebreak)

5. For each candidate (within concurrency slots):
   ├── Check dispatch eligibility
   └── Dispatch if eligible
```

**Critical:** Reconcile ALWAYS runs before fetch. A common mistake is checking concurrency first — always reconcile first.

## Dispatch Eligibility Checklist

All must pass before dispatch:

- [ ] Valid fields (id, identifier, title, state present)
- [ ] State is in `active_states` (not in `terminal_states`)
- [ ] Not already in `claimed` or `running` sets
- [ ] Global concurrency slot available (`running.size < max_concurrent_agents`)
- [ ] Per-state concurrency slot available (`running_by_state[state] < max_concurrent_agents_by_state[state]`)
- [ ] Blocker check: if issue has any `blocked_by` entries, ALL referenced issues must be in `terminal_states`

If any check fails, skip the issue this tick.

**Note:** The blocker check applies to any issue with `blocked_by` entries — not just issues in specific states. Teams using `Backlog`, `Queued`, or custom state names are covered.

## Continuation Decision (after Claude Code exits cleanly)

After exit code 0, the orchestrator checks whether to reschedule or declare success:

```
If issue's current DevRev stage is in terminal_states:
  → Mark complete; release from running set
Else:
  → Schedule continuation turn (fixed 1,000ms delay, attempt resets to 1)
```

This is the explicit decision point that determines continuation vs. completion. Never assume exit code 0 = done.

**max_turns exhaustion** is a continuation case, not a failure — treated as a clean exit, not exponential backoff.

## Issue Claim States (Internal — separate from DevRev tracker states)

```
Unclaimed → Claimed → Running → Released
                    ↘ RetryQueued → Released
```

- **Unclaimed**: not in any set
- **Claimed**: in `claimed` set, workspace being prepared
- **Running**: in `running` set, Claude Code active
- **RetryQueued**: in `retry_queue`, due_at_ms in the future
- **Released**: removed from all sets

**`completed` set semantics:** Persists for the process lifetime. A re-opened issue (stage moved back to active by a human) will be blocked from re-dispatch until the process restarts. This is intentional — restart recovery clears in-memory state and re-dispatches all eligible work.

## Concurrency

```typescript
interface ConcurrencyConfig {
  max_concurrent_agents: number;                        // global cap
  max_concurrent_agents_by_state: Record<string, number>; // per-state cap (lowercase keys)
}

// Check both before dispatching:
const globalOk = running.size < config.max_concurrent_agents;
const stateKey = issue.state.toLowerCase();
const stateLimit = config.max_concurrent_agents_by_state[stateKey] ?? Infinity;
const stateOk = (runningByState.get(stateKey) ?? 0) < stateLimit;
```

## Retry Backoff

**Failure retry** (exponential):
```
delay = min(10000 × 2^(attempt - 1), max_retry_backoff_ms)
```
Default `max_retry_backoff_ms`: 300,000ms (5 min)

**Continuation retry** (clean exit, not failure):
- Fixed 1,000ms delay, attempt resets to `1`
- Applies when: clean exit AND issue not in terminal_states AND turn count < max_turns

## DevRev MCP Tool Mapping

| Symphony operation | DevRev MCP tool | Key args |
|---|---|---|
| Fetch candidate issues | `mcp__plugin_compass_devrev__list_issues` | `stage` filter (not `state`), pagination |
| Fetch single issue | `mcp__plugin_compass_devrev__get_issue` | `id` |
| Reconcile state refresh | `mcp__plugin_compass_devrev__get_issue` | batch via parallel calls |
| Check valid transitions | `mcp__plugin_compass_devrev__get_valid_stage_transitions` | `id` — call before update_issue |
| Update state / claim | `mcp__plugin_compass_devrev__update_issue` | `id`, `stage` |
| Add comment (audit trail) | `mcp__plugin_compass_devrev__add_comment` | `id`, `body` |

**Note:** DevRev uses `stage` not `state` in MCP tool args. Always call `get_valid_stage_transitions` before `update_issue` — invalid transitions fail silently or with cryptic errors.

**If `mcp__plugin_compass_devrev__` prefix changes** (plugin renamed): update all entries in this table. It is the single source of DevRev tool names.

## Failure Model

| Failure class | Recovery |
|---|---|
| WORKFLOW.md / config invalid | Block new dispatches; keep service alive; keep reconciling |
| Worker failure | Exponential backoff retry |
| DevRev candidate fetch failure | Skip tick; retry next tick |
| Reconciliation state refresh failure | Keep current workers; retry next tick |
| Dashboard / log failure | Do NOT crash orchestrator |

## Restart Recovery

- No durable database. State is in-memory only.
- On restart: fetch all terminal-state issues → cleanup sweep → fresh poll → re-dispatch eligible work.
- Previously-running issues with non-terminal DevRev state get re-dispatched as fresh (no continuation).
- **In practice:** if Symphony restarts while issues are being processed, Claude Code re-runs from the beginning. Design your prompt template to be idempotent (check existing work, don't duplicate commits).

## OrchestratorRuntimeState Shape

```typescript
interface OrchestratorRuntimeState {
  running: Map<string, LiveSession>;          // issueId → session
  claimed: Set<string>;                       // issueIds being prepared
  retry_attempts: Map<string, number>;        // issueId → attempt count
  retry_queue: RetryEntry[];                  // pending retries with due_at_ms
  completed: Set<string>;                     // issueIds finished this process lifetime
  token_totals: { input: number; output: number };
  rate_limit_snapshot: { requests_remaining: number; reset_at_ms: number } | null;
}

interface LiveSession {
  session_id: string;           // Symphony-internal: "<pid>-<turn_number>" (not Claude Code's UUID)
  pid: number;
  token_counts: { input: number; output: number };
  turn_count: number;
  last_event_at_ms: number;    // updated per stdout event; used by reconcile stall detection
}

interface RetryEntry {
  issue_id: string;
  attempt: number;
  due_at_ms: number;
  timer_handle: ReturnType<typeof setTimeout>;
  error: string;
}
```
