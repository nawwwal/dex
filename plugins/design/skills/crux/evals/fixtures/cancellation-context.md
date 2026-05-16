# Cancellation Context

Project vocabulary:

- A `workspace` is the customer's operating container.
- A `subscription` is the billable contract attached to a workspace.
- A `user account` is an identity inside one or more workspaces.

Current implementation:

- Support can cancel a subscription for an entire workspace.
- There is no partial cancellation for a single module.
- Deleting a user account does not cancel billing.

Product proposal:

"Accounts should be cancellable" was written in a planning note, but it does not specify whether the team means workspace cancellation, subscription cancellation, user deletion, or module-level partial cancellation.
