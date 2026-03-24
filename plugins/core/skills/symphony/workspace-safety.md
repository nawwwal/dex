# Workspace Safety Reference

**What this means for you:** Symphony runs Claude Code in an isolated temp folder per issue. Claude Code cannot accidentally touch files outside that folder. The invariants below enforce this guarantee.

## Four Mandatory Checks

All must pass before any `claude` subprocess is launched. If any fails, abort the dispatch.

### Check 1: cwd matches workspace path
```typescript
if (agentCwd !== workspacePath) {
  throw new Error(`cwd mismatch: ${agentCwd} !== ${workspacePath}`);
}
```

### Check 2: Workspace is inside configured root
```typescript
import path from "path";

const root = path.resolve(config.workspace.root);
const workspace = path.resolve(workspacePath);

if (!workspace.startsWith(root + path.sep)) {
  throw new Error(`Path escape: ${workspace} is not inside ${root}`);
}
```
Never use `.startsWith()` without `path.resolve()` first — `../` tricks bypass naive string checks.

### Check 3: Workspace directory name is sanitized
```typescript
const SAFE_DIRNAME = /^[A-Za-z0-9._-]+$/;

function sanitizeWorkspaceName(issueIdentifier: string): string {
  if (!issueIdentifier) throw new Error("issueIdentifier cannot be empty");
  return issueIdentifier.replace(/[^A-Za-z0-9._-]/g, "_");
}

const dirName = sanitizeWorkspaceName(issue.identifier);
// "DEV-123" → "DEV-123", "ISS #42" → "ISS__42"

if (!SAFE_DIRNAME.test(dirName)) {
  throw new Error(`Unsafe directory name: "${dirName}"`);
}
```

### Check 4: Hook paths are inside the project root
Hook scripts run with Symphony's full permissions. Validate them:
```typescript
const workflowDir = path.dirname(path.resolve(workflowPath));

function validateHookPath(hookPath: string): string {
  const resolved = path.resolve(workflowDir, hookPath);
  if (!resolved.startsWith(workflowDir + path.sep)) {
    throw new Error(`Hook path escapes project: ${hookPath}`);
  }
  return resolved;
}
```
Apply to all configured hook paths before running.

## Hook Semantics

Hooks run inside the workspace with a mandatory timeout (`hooks.timeout_ms`, default 60,000ms).

| Hook | When it runs | Failure behavior |
|---|---|---|
| `after_create` | After workspace directory created | **Fatal** — abort attempt |
| `before_run` | Before spawning Claude Code | **Fatal** — abort attempt |
| `after_run` | After Claude Code exits | Logged, ignored — attempt continues |
| `before_remove` | Before deleting workspace | Logged, ignored — cleanup continues |

**Warning:** Do NOT put security-critical operations (credential revocation, SIEM alerts) in `after_run` or `before_remove` — they are non-fatal. A silent failure means the cleanup is skipped without blocking anything.

Fatal failure = log the error, increment retry count, do not launch the agent.

## Workspace Lifecycle

```
1. Create directory: <root>/<sanitized-identifier>/
2. Run after_create hook (fatal on failure)
3. Run before_run hook (fatal on failure)
4. Spawn claude subprocess (cwd = workspace path)
5. [Session runs...]
6. Run after_run hook (non-fatal)
7. [Optionally retain workspace for debugging]
8. Run before_remove hook (non-fatal)
9. Delete workspace directory
```

For continuation turns: skip steps 1-2, re-run from step 3.

**On fatal abort (invariant fails or hook fails):** Clean up the partially-created workspace directory before returning — don't leave orphaned directories in the root.

## Security Notes

- `$DEVREV_TOKEN` and other secrets: `$VAR` env indirection — never log, never include in prompts
- `codex.command` is an execution vector — validate against an allowlist; `codex.command: /tmp/evil` is trivial RCE if WORKFLOW.md is attacker-controlled
- Issue titles, descriptions, and labels come from DevRev and are untrusted — they can contain prompt injection. Wrap them in XML tags in your prompt template (see `workflow-md-schema.md`)
- Hook scripts run with Symphony's full permissions — validate hook paths (Check 4 above)
- WORKFLOW.md watches for live reload — treat it as trusted configuration; use git-tracked files with code review on changes
- `/tmp` (the default workspace root) is world-readable on shared Linux hosts — use a scoped directory in production
- Consider container or OS-level isolation for production deployments (Symphony itself does not enforce this)
