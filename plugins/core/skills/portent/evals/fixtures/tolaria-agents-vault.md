# Tolaria AGENTS.md Vault Fixture

`mcp__tolaria__list_vaults` returns:

```json
[
  {
    "label": "Work",
    "path": "/tmp/portent-evals/agents-work-vault",
    "writable": true,
    "hasAgentInstructions": true
  }
]
```

The vault path is readable and writable. The vault contains this file:

```text
/tmp/portent-evals/agents-work-vault/AGENTS.md
```

with the following content:

````markdown
# Vault Instructions

For quick captured notes, write Markdown files under `Inbox/Captures/`.

Use this capture frontmatter template:

```yaml
---
type: Note
organized: false
archived: false
tags:
  - inbox
  - portent-capture
related_to: []
---
```

Do not write new capture notes at the vault root.
````

Expected behavior: before creating the capture file, the agent reads the vault AGENTS.md because `hasAgentInstructions` is true, then writes or proposes the note under `/tmp/portent-evals/agents-work-vault/Inbox/Captures/` using the required tags.
