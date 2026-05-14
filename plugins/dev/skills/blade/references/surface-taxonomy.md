# Blade Surface Taxonomy

Use this reference to classify the job before choosing components. Blade is a layered design system, not just a component list.

## Source-truth ladder

| Source | Proves | Does not prove |
| --- | --- | --- |
| Consumer app root and installed `@razorpay/blade` | Which Blade version the app actually runs. | Latest public docs behavior. |
| Blade MCP | Exact props, slots, triggers, providers, icons, tokens, examples, and constraints. | Whether the interaction feels right in product context. |
| Public Storybook / `index.json` | Canonical names, docs/stories presence, broad surface area. | Complete API contract or installed app version. |
| Local app examples | Established integration patterns in that repo. | That the pattern is still preferred, Blade-compliant, or allowed for new motion/polish work. |

## Layers

| Layer | Owns | Agent move |
| --- | --- | --- |
| Patterns | Page/workflow structure such as lists, creation flows, detail views, forms, settings, confirmations, dashboard shells, and generative UI. | Check pattern docs before assembling many components by hand. |
| Components | Semantic units: actions, inputs, navigation, overlays, feedback, data display, typography, accessibility, layout primitives, AI/chat, and charts. | Choose a semantic owner before layout. |
| Motion | Physical change: opacity, position, edge entry, shadow, scale, continuity, sequence, parent-trigger coordination, branded motion. | Use one primitive for one physical property; keep semantic components owning meaning. |
| Tokens and utils | Spacing, size, typography, border, elevation, motion time, breakpoints, theme. | Use tokens/utilities for values before hardcoded CSS. |
| Interaction quality | Fit checks for density, frequency, typography, surface detail, transition feel, hit area, and reduced motion. | Use `interaction-quality.md` when Blade-compliant UI still feels wrong. |
| Coverage tooling | Adoption and drift signals in the measured DOM. | Product quality, auth state, focus behavior, or interaction fit. |

## Semantic ownership test

A Blade primitive owns a UI region when it defines what the thing is, what it can do, how it is reached, how it reports state, and how it behaves under keyboard, focus, loading, error, and motion.

Layout primitives may own geometry: spacing, grid/flex, width, overflow, z-index, layering, and ref boundaries. They must not own meaning or recreate interaction/motion when Blade has a semantic primitive for that responsibility.

If the intended owner is `Box`, `div`, CSS module, `motion.div`, or a custom component, stop and remap the responsibility to Blade. If Blade lacks the exact parameter, document the limitation and choose the closest Blade-native behavior.

## Ownership domains

| Domain | Blade owns | Layout code may own |
| --- | --- | --- |
| Surface | Cards, overlays, sheets, alerts, popovers, tooltips, carousel items, dashboard shells. | Size, placement, local layering, decorative internals. |
| Action | Buttons, icon buttons, links, menus, confirmation flows, disclosure controls. | Alignment and grouping around the action owner. |
| Input | Text/select/date/file inputs, checkbox, radio, switch, labels, hints, validation, grouped forms. | Form section layout after labels/errors are owned by Blade. |
| Navigation | Top/side/bottom nav, breadcrumbs, tabs, pagination, route affordance. | Router wrappers that preserve Blade state and focus behavior. |
| Feedback | Alert, toast, progress, skeleton, spinner, empty state, badge/tag/indicator when representing state. | Placement and spacing of feedback components. |
| Data display | Table, ListView, charts, Amount, InfoGroup, Code, status labels, loading/empty states. | Cell composition and surrounding page layout. |
| Motion | Blade motion primitive or component-owned transition. | Stable dimensions and DOM/ref boundaries around the Blade motion primitive. |

Every recommendation in this file is a candidate. MCP confirms the contract.
