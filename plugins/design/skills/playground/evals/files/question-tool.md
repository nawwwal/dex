# Question Tool Fixture

The question tool asks a user to choose between two implementation paths.

Current layout:
- Title: "Choose an implementation path"
- Body: one paragraph of context
- Options: two stacked cards with title, description, risk label, and estimated effort
- Footer: Cancel and Continue

Known issue:
- Users miss the risk label because it looks decorative.
- The Continue button is enabled before a choice is selected.
- The cards feel like final recommendations instead of comparable options.

Desired playground:
- Explore density, comparison layout, risk emphasis, and selected-state treatment.
- Export the chosen layout changes back to the agent.
