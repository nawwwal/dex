# Test 3: Layout divergence

## Prompt

```md
/diverge "Give me layout divergence for a settings page with account, billing, team, API keys, and security."
```

## Expected

The skill should select UX-level or UI-level layout divergence, not product-level divergence.

Output should include:

- Same product mechanics held constant.
- Different layout topologies.
- Hierarchy rationale.
- Responsive behavior.
- Density tradeoffs.
- State handling.
- No fake product concepts.

Good layout directions may include:

- Split settings nav with detail pane
- Search-first settings command page
- Security/billing priority dashboard
- Account setup checklist
- Table/detail for API keys and team members
- Mobile grouped settings flow

## Pass criteria

- Product objects stay constant: account, billing, team, API keys, security.
- Each direction names layout topology, regions, CTA placement, scroll behavior, responsive behavior, density, and tradeoff.
- It uses hierarchy and squint-test language.
- It handles empty/error/loading or permission denied for at least relevant sections.
- It does not invent new product mechanics.
