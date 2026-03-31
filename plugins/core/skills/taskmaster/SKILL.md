---
name: taskmaster
description: |
  Original Taskmaster-style stop hook that keeps work moving
  until an explicit parseable done signal is emitted.
argument-hint: "(auto-triggered, no arguments)"
disable-model-invocation: true
author: blader
version: 4.2.0
---

# Taskmaster

This plugin mirrors the original Taskmaster completion contract for Claude
Stop hooks: the run is not done until an explicit parseable done signal is
present in the assistant output.

## How It Works

1. **Agent tries to stop** and the Stop hook fires.
2. **The hook checks** the latest assistant output and transcript for the
   parseable completion token:
   `TASKMASTER_DONE::<session_id>`
3. **Token missing**:
   - block stop
   - return the shared Taskmaster compliance prompt
   - force same-session continuation until the work is actually complete
4. **Token present**: allow stop and clear the session counter.

## Parseable Done Signal

When the work is genuinely complete, the agent must include this exact line
in its final response (on its own line):

```text
TASKMASTER_DONE::<session_id>
```

This gives external automation a deterministic completion marker to parse.

## Configuration

- `TASKMASTER_MAX` (default `0`): max warning count before suppression in the
  stop hook. `0` means unlimited warnings.

Fixed behavior (not configurable):
- Done token prefix: `TASKMASTER_DONE`
- Shared compliance prompt text lives in `hooks/taskmaster-compliance-prompt.sh`
- Stop-hook enforcement lives in `hooks/check-completion.sh`

## Setup

Register the Stop hook and let it run automatically:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/skills/taskmaster/hooks/check-completion.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```
