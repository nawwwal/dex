# Layered Divergence Axes

Use these axes to select what changes. A direction must name its altitude and changed layers. If the layer does not change, mark it `unchanged`.

## A. Product-level axes

### 1. Organizing object

Meaning:
What primary object structures the experience?

Options:
User-first, task-first, issue-first, object-first, timeline-first, workflow-first, business-impact-first, owner/team-first, risk-first, outcome-first.

What changes in UI:
Navigation, page title, grouping, search, filters, empty states, default sort, object labels.

Example:
Connector-first shows Slack, Gmail, Shopify. Agent-risk-first shows agents at risk because Slack auth expired.

Avoid:
Same card grid with a different sort order.

### 2. User agency

Meaning:
Who initiates and controls the work?

Options:
User initiates, system suggests, user confirms, system batches, system acts safely, system blocks risky action, system acts silently and reports.

What changes in UI:
CTA design, approval flows, audit logs, undo, confidence indicators, permission boundaries.

Avoid:
"AI does it" without trust, reversibility, or evidence.

### 3. Product posture

Meaning:
Is the product helping, preventing, repairing, teaching, monitoring, or deciding?

Options:
Assistive, preventive, repair-oriented, educational, monitoring, decision-support, autonomous, auditing.

What changes in UI:
Primary screens, timing, notifications, explanations, CTAs, empty states.

Avoid:
A dashboard that pretends to be all of these at once.

### 4. Automation boundary

Meaning:
Where does the system stop and ask the human?

Options:
Manual, recommended, semi-automated, auto-safe, auto-with-review, auto-blocking, fully autonomous.

What changes in UI:
Review queue, approvals, logs, confidence, undo, override, escalation.

Avoid:
Invisible automation with no explanation.

### 5. Trust model

Meaning:
How does the product earn belief?

Options:
Evidence trail, before/after diff, simulation preview, human approval, audit log, confidence score, source citation, reversible action, role permission.

What changes in UI:
Detail panels, diff views, preview states, logs, footnotes, provenance.

Avoid:
Magic recommendations.

## B. UX-level axes

### 6. Information architecture

Meaning:
How information is organized.

Options:
Inventory, queue, timeline, map, matrix, inspector, wizard, feed, command palette, exception inbox, canvas, report.

What changes in UI:
Navigation, page topology, grouping, breadcrumbs, tabs, panels.

Avoid:
Renaming tabs and pretending it is strategy.

### 7. Primary decision

Meaning:
What decision does the surface optimize?

Options:
What matters, what changed, what should I fix, what should I ignore, what can I automate, what is safe, what is risky, what happens next, who owns this.

What changes in UI:
Above-the-fold content, CTA, ranking, severity, labels, explanatory copy.

Avoid:
Displaying everything equally.

### 8. Disclosure model

Meaning:
When information appears.

Options:
Always visible, progressive disclosure, on hover/focus, on selection, on error, on threshold, on user maturity, on role permission.

What changes in UI:
Panels, drawers, tooltips, accordions, inspector, advanced mode.

Avoid:
Hiding information users need for trust.

### 9. Flow structure

Meaning:
How the user moves through the task.

Options:
Single-screen action, step-by-step, branching flow, checklist, review-and-commit, compare-and-choose, diagnose-and-repair, draft-preview-publish, ask-approve-act.

What changes in UI:
Step order, progress, confirmation, backtracking, save states, validation.

Avoid:
Stepper because "flows need steppers."

### 10. Education model

Meaning:
How users learn the interface.

Options:
Self-evident UI, inline hint, empty state education, progressive onboarding, targeted toast, learn-by-doing sandbox, social discovery, help center, keyboard shortcut reveal.

What changes in UI:
Tooltips, first-run state, empty states, shortcuts, contextual nudges.

Avoid:
Blocking popovers that point at obvious things.

## C. Interaction-level axes

### 11. Input model

Meaning:
How the user expresses intent.

Options:
Click/tap, drag, swipe, keyboard, command palette, natural language, voice, gesture, bulk select, inline edit, upload/import, constraint sliders.

What changes in UI:
Affordances, target sizes, shortcuts, focus states, mobile behavior.

Avoid:
Adding chat if the actual action model is still buttons.

### 12. Feedback model

Meaning:
How the product responds.

Options:
Immediate inline feedback, toast, status chip, progress indicator, preview, simulation, activity log, undo snackbar, confirmation, haptic/audio, silent success.

What changes in UI:
Motion, copy, timing, persistence, state transitions.

Avoid:
Toast spam.

### 13. Error and recovery model

Meaning:
How failure is handled.

Options:
Prevent, warn, block, explain, retry, roll back, escalate, degrade gracefully, assign owner, contact support, learn from failure.

What changes in UI:
Error copy, disabled states, retry buttons, logs, repair flows, fallback UI.

Avoid:
"Something went wrong."

### 14. Power-user model

Meaning:
How repeated use gets faster.

Options:
Shortcuts, command palette, batch actions, saved views, templates, macros, defaults, recent actions, bulk edit, advanced filters.

What changes in UI:
Keyboard hints, density, table controls, saved configurations.

Avoid:
Designing only for first-time comprehension.

## D. UI presentation axes

### 15. Layout topology

Meaning:
The structural arrangement of the screen.

Options:
Single column, split pane, master/detail, table/detail, dashboard grid, timeline, kanban, matrix, canvas, map, inspector sidebar, command center, modal, bottom sheet, full-page flow.

What changes in UI:
Regions, scrolling, panel behavior, density, primary action placement.

Avoid:
Three equal cards by default.

### 16. Information hierarchy

Meaning:
The order and emphasis of content.

Options:
Outcome-first, action-first, status-first, risk-first, timeline-first, comparison-first, explanation-first, data-first, recommendation-first.

What changes in UI:
Headlines, row structure, CTA prominence, labels, grouping, empty states.

Avoid:
Making everything equally visible.

### 17. Density

Meaning:
How much information appears per unit of attention.

Options:
One thing, sparse, comfortable, dense, power-dense, progressive density, role-based density.

What changes in UI:
Spacing, row height, columns, text length, shortcuts, default disclosure.

Avoid:
Mistaking whitespace for clarity.

### 18. Component grammar

Meaning:
Which components carry the experience.

Options:
Cards, rows, tables, chips, pills, forms, drawers, panels, inline editors, checklists, progress bars, diff views, charts, toasts, badges, accordions.

What changes in UI:
Affordance, scannability, action density, accessibility.

Avoid:
Cards around everything.

### 19. Responsive behavior

Meaning:
How the surface adapts across screen sizes and contexts.

Options:
Stack, collapse, prioritize, transform into list, transform into carousel, move actions to bottom bar, keep table with horizontal scroll, summarize first/detail later, mobile-specific flow.

What changes in UI:
Breakpoints, navigation, density, action placement, hidden content.

Avoid:
Removing important functionality on mobile.

## E. Copywriting axes

### 20. Copy function

Meaning:
What the words are doing.

Options:
Orient, explain, label, instruct, warn, reassure, persuade, confirm, recover, celebrate, teach.

What changes in UI:
Headlines, CTAs, helper text, error messages, empty states, confirmations.

Avoid:
Decorative copy that does not help the user decide or act.

### 21. Tone

Meaning:
The emotional posture of the words.

Options:
Clinical, warm, direct, calm, urgent, expert, friendly, dry, formal, plainspoken, celebratory, apologetic.

What changes in UI:
Verb choice, sentence length, pronouns, humor, reassurance, warning style.

Avoid:
Same tone for onboarding, errors, and destructive actions.

### 22. CTA framing

Meaning:
How action is named.

Options:
Verb-first, outcome-first, risk-aware, time-bound, confirming consequence, reversible, commitment-heavy, low-friction.

What changes in UI:
Button labels, confirmation dialogs, destructive action copy.

Examples:
Bad: Submit. Better: Save changes. Better for billing: Charge $29 and subscribe. Better for destructive action: Delete 23 files.

Avoid:
OK, Submit, Continue when consequence matters.

### 23. Error copy model

Meaning:
How failure is explained.

Options:
What happened, why it happened, who can fix it, what to do next, whether data is safe, whether retry helps, whether support is needed.

What changes in UI:
Error text, helper links, retry copy, severity labels.

Avoid:
Blaming the user.

### 24. Empty state copy model

Meaning:
How absence is explained.

Options:
First-run orientation, no-results recovery, permission-limited absence, filtered-empty state, success-empty state, waiting-for-data state.

What changes in UI:
Message, CTA, secondary action, illustration, explanation.

Avoid:
"No data yet" with no next step.

## F. Visual-system axes

### 25. Typography strategy

Meaning:
How type creates hierarchy and personality.

Options:
Single tuned family, sans + mono, display + body, editorial serif + utility sans, condensed for density, variable font axis, numeric/tabular data style.

What changes in UI:
Type scale, font roles, line-height, weight, tracking, line length.

Rules:
Product UI usually benefits from one well-tuned family or a restrained sans + mono pairing. Brand/editorial surfaces can use more expressive pairings. Type must improve hierarchy and readability.

Avoid:
One font everywhere with no hierarchy or too many fonts that obscure hierarchy.

### 26. Color strategy

Meaning:
How color communicates.

Options:
Semantic status, single accent, brand-led palette, neutral-first, risk-coded, role-coded, data-coded, emotional temperature, high-contrast utility, quiet monochrome.

What changes in UI:
Status chips, CTA, warnings, backgrounds, charts, selection states.

Rules:
Color must have consistent meaning. Never rely on color alone. Check contrast. Accent should carry action or meaning.

Avoid:
Purple-to-blue AI gradients. Red/yellow/green with no consequence model.

### 27. Motion strategy

Meaning:
How movement explains state.

Options:
State transition, spatial continuity, progress, feedback, causality, attention shift, celebration, error recovery, loading, reduced-motion alternative.

What changes in UI:
Transitions, duration, easing, loading states, hover/focus, success/error feedback.

Rules:
Motion must explain what changed, where something went, or what action succeeded. Respect reduced-motion settings.

Avoid:
Motion as decoration.

### 28. Shape and containment

Meaning:
How visual boundaries group information.

Options:
No containers, spacing only, dividers, cards, panels, tables, outlines, filled regions, elevation, layered surfaces, common regions.

What changes in UI:
Grouping, scan path, perceived depth, touch targets.

Avoid:
Nested cards.

### 29. Icon / illustration strategy

Meaning:
How non-text visuals support meaning.

Options:
No icons, utility icons, status icons, product-specific symbols, diagrammatic illustration, character illustration, abstract visual system, data visualization.

What changes in UI:
Recognition, emotion, empty states, onboarding, errors.

Avoid:
Generic icon tiles above every heading.

## G. Emotional and persuasive axes

### 30. Emotional design layer

Meaning:
Which emotional layer is being designed.

Options:
Visceral first impression, behavioral ease/control, reflective pride/trust/memory after use.

What changes in UI:
Visual language, interaction smoothness, copy, success states, reminders, history, shareability.

Avoid:
"Make it delightful" without naming the emotional moment.

### 31. Emotional target

Meaning:
The feeling the interface should create.

Options:
Relief, confidence, calm, urgency, safety, mastery, curiosity, pride, control, trust, momentum.

What changes in UI:
Hierarchy, tone, pacing, feedback, friction, confirmation, success moment.

Example:
Relief shows one clear next action, confirms data safety, reduces options, and lowers visual noise.

### 32. Persuasive behavior model

Meaning:
How the design ethically encourages behavior.

Use:
Motivation, ability, prompt.

For every persuasive direction, specify motivation, ability/friction, prompt timing, ethical boundary, and opt-out/undo.

Avoid:
Dark patterns, fake urgency, manipulative scarcity, guilt loops, addictive streaks for serious workflows.

### 33. Memory model

Meaning:
What the user remembers after the interaction.

Options:
Peak moment, end state, first success, recovery from error, moment of trust, moment of control, moment of mastery.

What changes in UI:
Success message, final confirmation, summary, share state, audit log, milestone.

Avoid:
Celebrating trivial actions.
