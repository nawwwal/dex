# Tolaria Vault List Fixture

`mcp__tolaria__list_vaults` returns:

```json
[
  {
    "label": "Work",
    "path": "/tmp/portent-evals/work-vault",
    "writable": true,
    "hasAgentInstructions": true
  },
  {
    "label": "Personal",
    "path": "/tmp/portent-evals/personal-vault",
    "writable": true,
    "hasAgentInstructions": false
  }
]
```

The user did not provide a vault label or path hint. Both paths are plausible writable Tolaria vaults for a durable note.
