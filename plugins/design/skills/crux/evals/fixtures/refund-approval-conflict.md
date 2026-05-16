# Refund Approval Conflict

Three artifacts disagree:

- Public help docs: admins approve refunds before money moves.
- Code comments in `refunds/approval.ts`: support agents approve refunds above the risk threshold.
- Product review notes: users should approve their own refund requests from the dashboard.

No artifact includes observed user behavior. The conflict is about decision rights, accountability, and auditability.
