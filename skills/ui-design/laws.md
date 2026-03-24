# Laws of UX

Framework-agnostic psychological principles that govern how users perceive and interact with interfaces.

## Fitts's Law

The time to reach a target is proportional to the distance to it and inversely proportional to its size. Larger, closer targets are faster to click.

- Minimum touch target: **44×44px** (WCAG 2.5.5 AAA; WCAG 2.5.8 AA minimum is 24×24px — 44px is the recommended baseline) — not 32px (Fitts's cognitive minimum, not an accessibility standard)
- Expand small visual elements with `::before` / `::after` pseudo-elements (hit target expansion without visual change)
- Place primary actions within easy reach of the natural cursor/thumb rest zone

## Hick's Law

The time to make a decision increases with the number and complexity of choices.

- Limit choices per screen or menu
- Use progressive disclosure — show advanced options only when needed
- Group related actions together to reduce decision surface

## Miller's Law

Working memory can hold 7 ± 2 items at a time.

- Chunk related items into groups of 5–9
- Use visual grouping (proximity, borders, whitespace) to define chunks
- Don't present more than 7 primary navigation items

## Doherty Threshold

Productivity increases when a system responds within 400ms.

- Target interaction response under 400ms
- Use optimistic UI for async operations (show the expected result immediately, roll back on failure)
- Use skeleton screens for initial page loads

## Postel's Law

Be liberal in what you accept, conservative in what you output.

- Accept messy input: normalize phone numbers, trim whitespace, case-insensitive matching
- Output in a consistent, clean format regardless of input format

## Jakob's Law

Users spend most of their time on other sites, so they expect yours to work the same way.

- Favor familiar patterns (navigation, checkout, forms) over novel interaction designs
- Innovation should be in value, not basic interaction patterns

## Aesthetic-Usability Effect

Aesthetically pleasing designs are perceived as easier to use, even when they aren't.

- Good visual design creates goodwill that makes users more tolerant of minor usability issues
- Poor aesthetics creates skepticism that amplifies usability problems

## Law of Proximity

Objects near each other are perceived as related.

- Tight spacing within a group (8–12px between related items)
- Generous spacing between groups (24–48px)
- Related form fields should be visually adjacent

## Law of Similarity

Objects that look alike are perceived as related.

- Elements with the same function should have the same visual treatment
- Differentiate elements with different functions even if they are adjacent

## Law of Common Region

Elements within a bounded area are perceived as grouped.

- Use card backgrounds, borders, or whitespace to define groups
- Avoid using borders for purely decorative purposes — they imply relationship

## Von Restorff Effect (Isolation Effect)

When multiple similar objects are present, the one that differs from the rest is most likely to be remembered.

- Make the primary CTA visually distinct from secondary actions
- Use one accent color — applying it to too many elements negates the effect

## Serial Position Effect

Users best remember the first and last items in a list.

- Place the most important navigation items first or last
- Bury rarely-used or destructive actions in the middle

## Peak-End Rule

Users judge an experience mostly by its peak and ending moments.

- Success states matter — a satisfying "Payment confirmed" animation is worth building
- Error resolution (successfully recovering from an error) should feel good

## Tesler's Law (Law of Conservation of Complexity)

Every system has inherent complexity that cannot be reduced — it can only be transferred between the user and the system.

- Make the system absorb complexity, not the user
- Smart defaults, pre-filled fields, and inference reduce user burden

## Goal-Gradient Effect

People speed up as they get closer to a goal.

- Show progress indicators: step X of Y, percentage complete, visual progress bar
- Breaking a long form into steps increases completion rates

## Zeigarnik Effect

People remember uncompleted tasks better than completed ones.

- Show incomplete state explicitly — a partially-filled profile or setup progress creates a pull to finish
- "You're 80% done. Add a bank account to complete your profile." works.

## Law of Prägnanz (Good Figure / Simplicity)

People perceive complex images in the simplest form.

- Reduce visual noise — every element should earn its place
- Simplified layouts are understood faster and remembered longer

## Pareto Principle

80% of users use 20% of the features.

- Make the critical 20% of actions prominently accessible
- Progressively disclose the remaining 80%

## Cognitive Load

Reduce the mental effort required to use the interface.

- Remove extraneous elements that don't serve the current user goal
- Use familiar patterns, clear labels, and consistent behavior

## Law of Uniform Connectedness

Elements connected by visual lines, borders, or frames are perceived as related.

- Use visual connectors (step lines, progress paths) to show sequential relationships
- Avoid connecting elements that aren't actually related
