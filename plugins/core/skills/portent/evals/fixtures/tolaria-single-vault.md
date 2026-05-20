# Tolaria Single Vault Fixture

`mcp__tolaria__list_vaults` returns:

```json
[
  {
    "label": "Work",
    "path": "/tmp/portent-evals/readable-work-vault",
    "writable": true,
    "hasAgentInstructions": false
  }
]
```

The fixture represents a single readable vault. With only `list_vaults` and `open_note` available, the expected write path is direct Markdown inside `/tmp/portent-evals/readable-work-vault`.
