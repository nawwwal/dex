# Layered Concept Enrichment

Use this file to deepen directions without drifting into decorative lore.

## Preserve from the old skill

- JTBD
- Real constraint
- Eliminate-the-problem thinking
- Similar problems from other fields
- Kill ledger
- How each direction dies
- Day-in-the-life narratives
- Simplicity pass
- Prototype selection

## Jobs to Be Done

State 3 JTBD statements:

- Obvious: functional job.
- Emotional/social: anxiety, status, control, belonging, trust.
- Surprising: the hidden job discovered by asking what this is really about.

Format:

```md
When <situation>, I want to <motivation>, so I can <outcome>.
```

## Real constraint

Identify the real bottleneck:

- Time
- Knowledge
- Access
- Trust
- Motivation
- Coordination
- Attention
- Permission
- Data freshness
- Reversibility

Name primary and secondary constraints. These determine which layers matter.

## Eliminate the problem

Ask:

- What upstream change removes the problem?
- What can be automated safely?
- What can be prevented instead of repaired?
- What if the surface should not exist?

Output one problem-elimination statement.

## Similar problems in other fields

Use analogous problems only for transferable mechanisms. Do not transplant aesthetics.

Format:

```md
Other field:
Equivalent problem:
Mechanism:
Product translation:
Layer affected:
```

## Product model extraction

Every run should extract:

- Entities and product objects.
- Properties.
- States.
- User actions.
- System actions.
- Dependencies.
- Rules and permissions.
- Data freshness.
- Reversibility.

## Layer Diagnosis

Before generating, diagnose which layers are weak.

```md
| Layer | Current weakness | Evidence from prompt | Should diverge? | Why |
|---|---|---|---|---|
| Product mechanics | | | yes/no | |
| UX flow | | | yes/no | |
| Interaction | | | yes/no | |
| Information hierarchy | | | yes/no | |
| Copy | | | yes/no | |
| Layout | | | yes/no | |
| Typography | | | yes/no | |
| Color | | | yes/no | |
| Motion | | | yes/no | |
| Emotional design | | | yes/no | |
| Persuasion | | | yes/no | |
| Education | | | yes/no | |
| Accessibility | | | yes/no | |
| Handoff | | | yes/no | |
```

Only diverge layers that matter.

## State/action matrix

Use this for software products:

```md
| State | User meaning | System meaning | Severity | User action | System action | UI representation | Copy requirement | Edge case |
|---|---|---|---|---|---|---|---|---|
```

Use domain-specific states when available.

## Enrichment passes

Run only the passes relevant to the selected layers.

### Copy pass

- Page title
- Section heading
- CTAs
- Empty, loading, error, success states
- Confirmation copy
- Tooltip/helper text only if necessary

Quality check:
Does copy tell the user what changed, what matters, what to do next, and what consequence follows?

### Layout pass

- Top, primary, secondary, detail regions
- Persistent controls
- CTA placement
- Scroll behavior
- Responsive transformation
- Density

Quality check:
Can the user identify the primary action within 2 seconds?

### Interaction pass

- Trigger
- Input
- Feedback
- Intermediate state
- Completion
- Undo/recovery
- Failure
- Accessibility
- Power-user shortcut
- First-time affordance

Quality check:
Does it handle latency, keyboard use, screen readers, and recovery?

### Hierarchy pass

Define:

1. First read
2. Second read
3. Third read
4. Persistent context
5. Hidden detail
6. Quiet metadata
7. Removed content

Squint test:
With blurred vision, the user should first see X, then Y, then Z.

### Typography pass

Specify font strategy, scale, weight, line-height, line length, numeric style, and accessibility notes.

### Color pass

Specify palette role, semantic colors, accent usage, status usage, contrast requirements, and non-color backup signals.

### Motion pass

Specify state transitions, loading, success, error, hover/focus, and reduced-motion alternative.

### Emotional design pass

Specify before-use, during-use, and after-use emotional states plus visceral, behavioral, and reflective mechanisms.

### Persuasive design pass

Specify desired behavior, motivation, ability/friction, prompt, timing, ethical boundary, opt-out/escape, and failure mode.

### Education pass

First ask whether the UI can be made more obvious. Use education only when the UI cannot carry all meaning itself.

### Accessibility pass

Check color backup, contrast, target size, keyboard use, screen-reader legibility, reduced motion, and text scaling.

### Handoff pass

Translate the direction into:

- Objects
- States
- Events
- Components
- Data dependencies
- Permissions
- Edge cases
- Analytics
- Accessibility
- Localization
- QA scenarios

## Story mode

For selected directions:

```md
- Trigger:
- Moment of confusion or need:
- Product response:
- User action:
- Aftermath:
```

## How each direction dies

State the single most likely failure mode:

```md
<persona> cannot <required action/decision> because <specific assumption fails> after <time/context>.
```

Bad:
"Users might not like it."

Good:
"Operators stop trusting risk ranking after one stale dependency graph marks the wrong agent as safe."

## Simplicity pass

Ask:
What can be removed, combined, or hidden without killing the direction?

Output:

```md
Original:
Simplified:
What stayed because it is load-bearing:
```

If original and simplified are identical, the direction is probably bloated or under-specified.

## Prototype decision framework

Rate 1-5:

- Signal strength: will the prototype teach something new?
- Feasibility: can it be built quickly?
- Risk of skipping: what insight is lost if skipped?
- Team conviction: does the team care?
- State coverage: does it test real states?
- Handoff value: can implementation learn from it?

## Kill ledger

### Universal gates

Kill or rewrite if:

1. Direction does not name altitude.
2. Direction does not say which layers changed.
3. Direction cannot be sketched.
4. Direction cannot be prototyped.
5. Direction does not handle real states.
6. Direction has no clear user action.
7. Direction uses metaphor without execution.
8. Direction ignores constraints.
9. Direction hides complexity users need.
10. Direction is just a different visual treatment of the same mechanism but claims product-level divergence.

### Product gates

- Does the object model change?
- Does the agency model change?
- Does the automation boundary change?
- Does the trust model change?
- Does the data requirement exist?
- Does it name the business/user tradeoff?

### UX gates

- Does the decision flow change?
- Does the IA change?
- Does the interaction loop change?
- Does the state handling change?
- Does the entry point change?
- Does the recovery path change?

### UI gates

- Does the layout hierarchy change?
- Does copy become clearer or more purposeful?
- Does typography improve hierarchy/readability?
- Does color communicate meaning?
- Does motion explain state?
- Does density match use frequency?

### Copy gates

- Does every word earn its place?
- Is the CTA specific?
- Are consequences clear?
- Is error copy useful?
- Is empty state copy actionable?
- Is tone appropriate?
- Is cleverness hurting clarity?

### Emotional gates

- Is the target emotion named?
- Is the UI mechanism that creates it named?
- Is the emotion appropriate to the moment?
- Does it improve the task?

### Persuasion gates

- Is motivation real?
- Is ability improved?
- Is prompt timing justified?
- Is the nudge ethical?
- Can users decline or undo?

### Accessibility gates

- Does color have non-color backup?
- Is contrast sufficient?
- Are targets large enough?
- Is keyboard use possible?
- Are states screen-reader legible?
- Is reduced motion handled?
- Does text scale?
