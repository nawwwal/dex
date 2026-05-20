# Portent Vault State Fixture

## [[Agent Marketplace runtime fixes]]

```yaml
type: Project
organized: true
archived: false
related_to:
  - "[[Agent Marketplace]]"
  - "[[Dashboard microapps]]"
```

Status: HMR and local mock-mode boundaries were fixed, but PR review replies are still open.
Latest event: [[Agent Marketplace Chrome verification]].
Open tasks:

- Reply to the PR review thread about runtime mock gating.
- Confirm Fast Refresh still works after the package typecheck change.

## [[Launch Portent v0.1]]

```yaml
type: Project
organized: true
archived: false
related_to:
  - "[[Personal Knowledge Base]]"
  - "[[Alice Example]]"
```

Status: completed after the model and first skill draft landed.
Launch event: [[Portent launch shipped]].

## [[Portent launch shipped]]

```yaml
type: Event
organized: true
archived: false
belongs_to: "[[Launch Portent v0.1]]"
related_to:
  - "[[Alice Example]]"
```

The first Portent skill draft shipped with capture, organize, brief, todo, archive, and search modes.

## [[Alice Example]]

```yaml
type: Person
organized: true
archived: false
related_to:
  - "[[Knowledge graphs]]"
```

Alice asked for the first Portent version to stay simple.

## [[Knowledge graphs]]

```yaml
type: Topic
organized: true
archived: false
related_to:
  - "[[Portent object model]]"
```

Knowledge graphs are useful when object links matter more than folders.

## [[Knowledge graph notes]]

```yaml
type: Note
organized: true
archived: false
belongs_to: "[[Knowledge graphs]]"
related_to:
  - "[[Launch Portent v0.1]]"
```

Portent should expose relationships in briefs and search results without forcing synthesis.

## [[Agent Marketplace runtime verification]]

```yaml
type: Event
organized: true
archived: false
belongs_to: "[[Agent Marketplace runtime fixes]]"
related_to:
  - "[[Chrome verification]]"
```

Chrome verification passed for local mock gating on a dev host.
