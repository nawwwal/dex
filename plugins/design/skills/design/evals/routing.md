# Design Router Eval Cases

These cases verify that `/design` stays a thin router and does not fall back to stale embedded instructions.

| # | Prompt | Expected route |
|---|---|---|
| 1 | "Check this Razorpay dashboard page for Blade score and component adherence." | `design:blade` |
| 2 | "Run Blade coverage on this feature and tell me what is non-compliant." | `design:blade` |
| 3 | "Use Dialkit interaction primitives to make this control feel better." | `interface-craft` |
| 4 | "Open the critique toolbar and handle pending feedback annotations." | `agentation` |
| 5 | "Inspect localhost, click through the flow, and capture screenshots." | `agent-browser` |
| 6 | "Pressure-test this claim before we build anything." | `design:first-principles-questioning` |
| 7 | "Find the crux in this PRD." | `design:first-principles-questioning` |
| 8 | "What assumptions are hiding in this strategy?" | `design:first-principles-questioning` |
| 9 | "Does this qi carry the dao, or are we decorating around confusion?" | `design:first-principles-questioning` |
| 10 | "What must be true for this to work?" | `design:first-principles-questioning` |
| 11 | "What would prove this wrong?" | `design:first-principles-questioning` |
| 12 | "Find the weak joint in this idea." | `design:first-principles-questioning` |
| 13 | "What hidden premise is this strategy depending on?" | `design:first-principles-questioning` |
| 14 | "What is named badly here?" | `design:first-principles-questioning` |
| 15 | "What is the simplest vessel for this principle?" | `design:first-principles-questioning` |
| 16 | "Write a PRD for this feature." | not `design:first-principles-questioning`; route to a writing/product-doc workflow if available |
| 17 | "Summarize this PRD." | not `design:first-principles-questioning`; route to summarization/writing workflow |
| 18 | "Rewrite this problem statement clearly." | not `design:first-principles-questioning`; route to writing/editing workflow unless the user asks to pressure-test it |
| 19 | "Turn these notes into a strategy doc." | not `design:first-principles-questioning`; route to writing/product strategy workflow |
| 20 | "Create a launch plan from this PRD." | not `design:first-principles-questioning`; route to planning/writing workflow |
| 21 | "Make this UI prettier." | not `design:first-principles-questioning`; use polish/interface route |
| 22 | "Brainstorm alternate concepts for the connector health dashboard." | `design:diverge` |
| 23 | "Give me different directions for this modal without changing the product goal." | `design:diverge` |
| 24 | "Polish the transition and interaction feel on this drawer." | `web-animation-design` and/or `make-interfaces-feel-better` |
| 25 | "Design audio feedback and earcons for success and failure states." | `create-sound` or available sound skill |
| 26 | "Write a GLSL shader with SDF procedural graphics." | `design:shader` |
| 27 | "Create an engineer handoff for these components, screens, and states." | `visual` |
| 28 | "Create a motion handoff for this drawer transition." | `visual` |
| 29 | "Review this UI for density, hierarchy, typography, a11y, and state handling." | `design:interface-review` |
| 30 | "Do a Figma design critique of this screen." | `design:interface-review` |
