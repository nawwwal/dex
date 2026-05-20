# Tolaria Missing Path Fixture

`mcp__tolaria__list_vaults` returns:

```json
[
  {
    "label": "Work",
    "path": "/tmp/portent-evals/missing-work-vault",
    "writable": true,
    "hasAgentInstructions": true
  }
]
```

The user gave the vault hint "Work". The listed path is absent or unreadable, so Markdown fallback cannot execute safely.
