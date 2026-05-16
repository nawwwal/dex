# Design Review Narrative Fixture

The current connector setup screen explains every available integration before asking the user what they need.

The main critique:
- The page teaches inventory before intent.
- Users need to decide which connector unblocks their current workflow.
- The review should help stakeholders see why a triage-first flow is faster.

Evidence:
- Users scan connector names but miss setup requirements.
- Support tickets mention confusion around "connected" versus "ready".
- Engineering needs a decision on whether setup state belongs on the connector card or a separate detail page.

Likely objections:
- Sales wants the page to show the breadth of integrations.
- Engineering does not want to build a new wizard.
- Design worries that hiding connectors behind questions reduces discoverability.
