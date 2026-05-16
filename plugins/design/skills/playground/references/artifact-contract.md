# Artifact Contract

Every generated playground must declare metadata so the user and future agents can understand what was built, where it lives, and how much trust to place in it.

## Required Metadata

- `artifact_title`: human-readable name.
- `slug`: lowercase hyphen slug.
- `filename`: actual file name.
- `output_path`: absolute or repo-relative path returned to the user.
- `created_at`: local timestamp.
- `source_material`: files, URLs, notes, screenshots, prompts, or assumptions used.
- `asset_mode`: `none`, `inspiration-seed`, `asset-seed`, or `provided-assets`.
- `open_method`: how to open or inspect it.
- `what_this_proves`: what the artifact makes testable, visible, or decidable.
- `what_this_does_not_prove`: fidelity gaps, fake data, inferred behavior, missing source, or production limits.

## Default File Naming

Use:

```text
playground-<slug>-YYYYMMDD-HHMM.html
```

## Default Location

Ask only if the user has a preferred location. Otherwise:

1. Use a local notes/artifacts folder already used by the repo if one exists.
2. If none exists, use `notes/playgrounds/`.

## Return Contract

When finished, return:

- Artifact path.
- Open method.
- What the playground proves.
- What it does not prove.
- How to copy or export feedback back into the agent.
