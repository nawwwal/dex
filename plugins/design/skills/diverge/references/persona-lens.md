# Persona Lens

Personas must affect mechanisms, not just tone. Use a persona lens when audience, urgency, expertise, accessibility, or context changes design decisions.

For each persona, specify:

- Information density
- Copy style
- Default hierarchy
- Interaction model
- Error handling
- Education model
- Confirmation needs
- Power-user affordances
- Accessibility needs
- Emotional state

## Crisis user

- Information density: one issue at a time.
- Copy style: short, direct, consequence-first.
- Default hierarchy: severity -> action -> safety.
- Interaction model: big targets, no exploration, no hidden actions.
- Error handling: recovery path visible immediately.
- Education model: none during crisis; teach later.
- Confirmation needs: only for destructive or irreversible actions.
- Power-user affordances: bypass route to urgent action.
- Accessibility needs: no color-only severity, focus lands on action.
- Emotional state: urgency without panic.

## Power user

- Information density: high.
- Copy style: terse, precise, object-specific.
- Default hierarchy: speed, batch action, state, owner.
- Interaction model: keyboard, bulk, saved views, command palette.
- Error handling: detailed logs and exact failure cause.
- Education model: shortcut discovery after repeated action.
- Confirmation needs: minimal except destructive or irreversible actions.
- Power-user affordances: filters, macros, recent actions, bulk edit.
- Accessibility needs: keyboard completeness and screen-reader table semantics.
- Emotional state: mastery and control.

## Once-ever user

- Information density: low to moderate.
- Copy style: explanatory without condescension.
- Default hierarchy: what this is -> what to do -> what happens next.
- Interaction model: guided, visible, forgiving.
- Error handling: plain recovery path with no jargon.
- Education model: first-run orientation in empty state or inline helper.
- Confirmation needs: explicit success and next step.
- Power-user affordances: hidden or irrelevant.
- Accessibility needs: clear labels, large targets, predictable focus.
- Emotional state: confidence and safety.

## Skeptic

- Information density: evidence before recommendation.
- Copy style: direct, proof-oriented, no hype.
- Default hierarchy: source -> reason -> consequence -> action.
- Interaction model: review and approve, preview before commit.
- Error handling: transparent cause and data safety.
- Education model: explain value only after showing evidence.
- Confirmation needs: reversibility and audit trail.
- Power-user affordances: raw detail behind disclosure.
- Accessibility needs: proof not encoded only in visuals.
- Emotional state: trust earned through control.

## Accessibility-first user

- Information density: semantic grouping over visual compression.
- Copy style: explicit labels and state text.
- Default hierarchy: headings, landmarks, state, action.
- Interaction model: keyboard and screen-reader first.
- Error handling: programmatically announced and recoverable.
- Education model: available through text, not hover-only.
- Confirmation needs: persistent status text.
- Power-user affordances: keyboard shortcuts that are discoverable.
- Accessibility needs: contrast, focus, target size, reduced motion, text scaling.
- Emotional state: control without guessing.

## Low-bandwidth/shared-device user

- Information density: small summaries before detail fetch.
- Copy style: short, resilient-state aware.
- Default hierarchy: freshness, pending actions, safe next step.
- Interaction model: actions can queue or retry.
- Error handling: distinguish failed, pending, stale, and offline.
- Education model: no heavy tours or media.
- Confirmation needs: durable confirmation that survives refresh.
- Power-user affordances: lightweight saved state.
- Accessibility needs: works without heavy assets.
- Emotional state: certainty despite fragility.

## Expert operator

- Information density: very high, but structured.
- Copy style: technical and exact.
- Default hierarchy: state -> evidence -> action -> logs.
- Interaction model: scriptable, batchable, keyboard-first.
- Error handling: exact source, run IDs, logs, dependency links.
- Education model: shortcut reveal and advanced mode.
- Confirmation needs: audit summary, not explanatory interstitials.
- Power-user affordances: saved views, macros, command palette.
- Accessibility needs: dense but navigable semantics.
- Emotional state: competence respected.

## Admin / approver

- Information density: risk, requester, affected objects, decision.
- Copy style: consequence-first.
- Default hierarchy: permission delta -> risk -> affected users -> approve/reject.
- Interaction model: review, approve, reject, request changes, delegate.
- Error handling: blocked action explains authority and next owner.
- Education model: explain why approval is needed, not how buttons work.
- Confirmation needs: audit-ready decision summary.
- Power-user affordances: queue filters and bulk approvals only when safe.
- Accessibility needs: diffs and risk not color-only.
- Emotional state: responsibility with evidence.

## Team owner

- Information density: owner, SLA, team, status, blockers.
- Copy style: operational and handoff-ready.
- Default hierarchy: affected team -> issue -> owner -> next action.
- Interaction model: assign, mention, escalate, watch.
- Error handling: blocked handoffs are first-class states.
- Education model: lightweight explanation of ownership rules.
- Confirmation needs: visible handoff and notification status.
- Power-user affordances: team saved views.
- Accessibility needs: clear relationship labels.
- Emotional state: coordination without ambiguity.
