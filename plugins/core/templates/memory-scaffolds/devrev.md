---
date: 2026-03-16
tags: [devrev, conventions, tooling, ways-of-working]
type: knowledge-base
status: active
source: https://docs.google.com/document/d/1Axt5asxigA42pm8igNd4MxBHxrip7BUz/edit
---

# DevRev Conventions — Razorpay Ways of Working

> Source: DevRev Ways of Working v1.0 (27 Feb 2026). All DEPA PODs.
> the user's user ID: `don:identity:dvrv-in-1:devo/2sRI6Hepzz:devu/11830` (DEVU-11830)

---

## Golden Rules

- **Every work item must be linked to a Part (POD).** Enhancements → POD. Issues → Enhancement or POD. Unlinked items break dashboards.
- **Always set task type to Design** (`ctype__task_type`) when creating issues as a designer. Default is "Engineering" — must be overridden.
- **DevRev is the single source of truth.** No parallel tracking in spreadsheets or Slack.
- **Always link every PR/commit to a DevRev issue** (Task/Bug/Story).

---

## Terminology (DevRev → Razorpay)

| DevRev Term | Razorpay Equivalent | Description |
|---|---|---|
| **Product** | Group | Top-level business unit (e.g., Payments Platform, Magic Checkout) |
| **Capability** | Sub Group | Functional area within a Group |
| **Feature** | POD (Part) | Atomic engineering team unit. All issues anchored here. |
| **Enhancement** | Project / Milestone / Epic | Large deliverable tracked in Roadmap (≡ Jira Epic). Must link to Part. |
| **Issue** | Story / Task / Bug / Oncall / PSE | Day-to-day work item tracked in Sprints. Sub-type defines nature. |
| **Vista** | Saved View / Dashboard | Filtered, saved list of objects shareable across teams. |
| **Sprint Board** | Sprint | 2-week time-boxed board. Default: Tue 9AM → Mon 7PM. |
| **Ticket** | Internal Item | Internal approvals (IT Support, Compliance, CARCA) — NOT merchant tickets. |
| **Incident** | Incident | Tracked in Incident Management. Auto-created from #potential_outages. |

---

## Enhancement vs Issue — When to Use

**Enhancement (Epic):** Use when work spans multiple sprints, requires a Product/Design/Tech Spec, is tied to an OKR or quarterly commitment, and needs Roadmap visibility.

**Issue (Story/Task/Bug):** Use for execution-level work completable within one sprint. Does not need Roadmap visibility.

---

## Issue Sub-Types and Mandatory Fields

| Sub-Type | What It Tracks | Mandatory Fields |
|---|---|---|
| **Story** | User-facing functionality from a Product Spec | Acceptance Criteria, Part, Owner, Priority |
| **Task** | Technical tasks, infrastructure, non-story work | Task Type, Part, Owner, Priority |
| **Dependency** | Cross-team dependencies blocking another team | Impact Details, Requester Team, Requested Quarter, Requested Timeline |
| **Bug** | Defects in any environment | Report Team, Environment, Part, Priority |
| **Oncall** | Unplanned on-call / merchant-impacting ops work | Oncall Category, Part |
| **PSE** | Issues escalated from TS/CS to Engineering | PSE POD, FD ID, Merchant ID, Merchant Category, Reported Team, Severity |
| **Incident RCA** | Root Cause Analysis for production incidents | Linked Incident |
| **Incident-AI** | Action items from Incident RCA | Linked to Incident RCA, Owner, Priority, Target Close Date |

**Common mandatory fields across all sub-types:** Title, Priority, Owner, Part (POD).

---

## Enhancement Stage Lifecycle

| Stage | Description | Who Moves It |
|---|---|---|
| **Backlog** | Created, not committed to a quarter | PM/EM |
| **Prioritised** | Committed to quarter plan | PM + EM jointly |
| **Conceptualisation** | Product and Design readiness in progress | PM/Designer |
| **Implementation** | Tech Spec complete; dev and testing underway | EM/TL |
| **Production Deployed** | Code deployed to production | EM/DevOps |
| **Early Access** | Limited availability to select merchants | PM |
| **GTM Done** | Generally available to all customers | PM |
| **Deprioritised** | Moved out of quarter | PM + EM |
| **Cancelled** | No longer required | PM + EM |

Moving to **Prioritised** requires: Forecasted Close Date, Planned Quarter, ARD Required, Product/Design/Tech Spec Required, OKR, Efforts-Dev.

**Stage IDs discovered via API:**
> ⚠️ Last verified: 2026-03-16. Re-verify before any sprint batch operation by running `devrev.get_valid_stage_transitions` or calling DevRev MCP. IDs can change if Razorpay's DevRev config is modified.

- `custom_stage/61` = Backlog
- `custom_stage/44` = In Progress
- `custom_stage/26` = Completed (for task/story subtype)
- `custom_stage/42` = Done (for other subtypes; stage_diagram/862 for tech_doc has different rules)

---

## Hierarchy

```
Enhancement (Quarterly) → Story (Sprint, 1–2 weeks) → Task (Daily, 1 day)
```

- Enhancement spans multiple sprints. Story fits within one sprint. Task fits within one day — break down if larger.
- Link Stories to Enhancement via "Linked Enhancement" field when creating.
- Auto-link: create Issues from inside an Enhancement's page.
- Manual link: open issue → click + (link) icon → search and confirm.

---

## Sprint Conventions

- **Duration:** 2 weeks (14 days). Starts **Tuesday 9AM**, ends **Monday 7PM**.
- **Spillovers:** Issues not closed auto-carry to next sprint.
- **Sprint Calendar:** Fixed — refer to Sprint Calendar spreadsheet. Never start mid-cycle.
- **Planning capacity:** 80–90% bandwidth per person. 10–20% for meetings, ad-hocs.
- Sprint board naming: `[Group]-[SubGroup]-[POD]` (e.g., `Cross Border-Import-Import Core`)
- All DEPA teams use the same sprint as the POD they work with.

---

## Bug Severity SLAs

| Priority | Description | Resolution SLA |
|---|---|---|
| P0 — Critical | Production down / major payment flow broken | 4 business days |
| P1 — High | Significant issue, workaround available | 10 business days |
| P2 — Medium | Moderate issue, workaround available | 4 weeks |
| P3 — Low | Minor / cosmetic / edge case | 8 weeks |

P0 bugs must be resolved before any new feature work. P1 takes priority over P2/P3 in current sprint.

---

## Daily Update Format (Sprint Check-in)

```
Progress: [What was completed yesterday]
Planned Items: [What is planned for today]
Blockers/Risk/Callout: [Any open dependencies or blockers]
Help Needed: [Any help required]
```

---

## Weekly Update Format (Key Projects)

```
Current RAG: 🟢 On Track / 🟡 At Risk / 🔴 Blocked
Progress: [What was completed this week]
Next Week Milestones: [What the team will do next sprint]
Blockers/Risk/Callout: [Any open dependencies or escalations needed]
Help Needed: [Any help required from leadership]
```

Escalate to Group EM or TPM when:
- Enhancement At Risk (🟡) for 3+ days without mitigation plan
- Cross-team Dependency open >5 business days without resolution
- Sprint carry-over rate >30% for 2 consecutive sprints on a Key Project
- Forecasted Close Date needs to move by >2 weeks

---

## Core Vistas Every POD Should Maintain

| Vista Name | Object Type | Key Filters |
|---|---|---|
| Q[X] FY[YY] Roadmap | Enhancement | Type=Enhancement, Part=[POD], Quarter=[Current] |
| Sprint Board - [POD] | Issue | Type=Issue, Part=[POD], Sprint=[Current] |
| Active Bug Tracker - [POD] | Issue | Sub-Type=Bug, Part=[POD], Stage≠Closed |
| PSE Tracker - [POD] | Issue | Sub-Type=PSE, Engineering POD=[POD], Date=Last 90 days |
| Dependency Tracker - [POD] | Issue | Sub-Type=Dependency, Part=[POD], Stage≠Closed |

Vista naming: `[POD Name] - [Type] Tracker`
Always share Roadmap Vistas with **Viewer-only** access for leadership.

---

## DOs and DON'Ts

✅ **DO:**
- Link every issue to a Part (POD) or Enhancement
- Keep Enhancement stages updated in real time
- Use correct Sub-Type when creating issues
- Post weekly status updates on all prioritised Projects
- Fill all mandatory fields for PSE tickets (FD ID, MID, Engineering POD)
- Use Dependency Sub-Type for cross-team dependencies
- Close stale issues and clean up backlog every sprint
- Update Incident mandatory fields within 1 hour of resolution
- Use List View for bulk updates during sprint planning

❌ **DON'T:**
- Leave Enhancements in 'Prioritised' when work has already started
- Create issues without a Sub-Type — breaks reporting
- Wait for leadership reviews to communicate project risks
- Create PSE issues without FD ID — breaks SLA tracking
- Track dependencies informally in Slack without a DevRev record
- Share Vistas with Editor access to leadership
- Leave old issues open indefinitely
- Leave Incident fields blank

---

## Scheduling Rules

- **Never set due dates on weekends (Sat/Sun).** Always use the nearest preceding weekday (Fri).
- Working days are Mon–Fri only.
- All sprints start Tuesday 9AM, end Monday 7PM.

## Process Constraints

- Canary deployments at Razorpay require a developer — designers cannot do canary deploys independently.

---

## Key Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| Global search | Cmd/Ctrl + K |
| Quick issue create | + button (top-right, blue) |
| Inline stage update | Click Stage chip in List View |
| Filter by me | Owner = Me filter in any Vista |
| Updates/mentions | Updates bell icon |

---

## Connections

→ [[memory/patterns|Patterns]] — Stage IDs discovered via API
→ [[memory/projects|Projects]] — DevRev issue links per project
