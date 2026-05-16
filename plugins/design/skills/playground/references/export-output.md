# Export Output

The export is the bridge from playground interaction back to agent action. Natural-language prompt output is the default because the next agent should be able to act without reopening the playground.

## Export Modes

- Instruction: implementation prompt with chosen settings, rationale, source context, and non-default decisions.
- Critique: approved, rejected, and commented feedback packet with anchors and severity.
- Reproduction: steps, state, event path, expected behavior, observed behavior, and blockers.
- Config: JSON state for repeatable replay or import.
- Handoff: design, motion, copy, responsive, or implementation notes.

## Rules

- Natural-language prompt is default.
- Mention only non-default or user-approved choices.
- Include enough context to act without seeing the playground.
- Raw JSON is available as secondary export, not the only output.
- Rejected items must not leak into the action prompt unless clearly labeled as rejected context.
- Review-mode exports must include approved suggestions, rejected suggestions labeled separately, unresolved comments, anchors or target line references, and source assumptions.
- Include source notes and assumptions when factual claims, measurements, or inferred behavior are used.

## Output Shape

Use a readable prompt with these parts when applicable:

```text
Goal:
Source context:
Selected decisions:
Non-default settings:
Approved changes:
Rejected context:
Open questions:
Implementation or follow-up prompt:
```
