---
date: 2026-03-20
tags: [razorpay, context, setup]
type: knowledge-base
status: active
---

# Razorpay — Company Context

## Team Structure
- **R1 Design** — ~23-member product design team
  - Led by Varghese Mathew (Design Lead)
  - Akanksha Khanna runs weekly standups
  - Pingal Kakati runs sprint planning + design walkthroughs
  - Prarthana Gogoi — designer on Website addition flow + Dashboard Whitelabeling
  - Gopi Bhatnagar — designer on Malaysia Onboarding + Duit Now; did comm design for Agent Marketplace FTX
  - Caren Felicia J — organized B2B Design Principles (Mar 17, 2026)
  - Annamalai Lakshmanan — led dashboard → live-ready for FTX + Agentic Integration prototype
- **i18n Product** — Internationalization group spanning US, MY, SG markets
  - PMs: Raghav Iyengar, Shubham Agarwal, Shashwat Gupta, Dhruv Mittal, Manoj W
  - Arkaprabha C runs weekly DEPA review
- **AI Squad** — AI tools and unblocking
  - Abhinav Krishna (lead), Sudarshan Srinivas
- **Blade Design System** — Component library team
  - Saurav Rastogi, RK (reviewer), Saurabh Soni
  - Kamlesh Chandnani — Director of Engineering (Blade DS + Frontend)
  - **Blade 3.0 (Spark) is LIVE on Production** as of ~Mar 12, 2026

## Slack Channel Directory
| Channel | Purpose |
|---------|---------|
| #r1-design | R1 design team coordination |
| #international-product-design | Cross-market i18n design |
| #design-system | [[work/non-blade-migration/index|Blade DS]] discussions |
| #product-agent-marketplace | [[work/agent-marketplace/index|Agent marketplace]] product (Nexus / Agent Studio). Aravinth runs status updates here. |
| #ai-squad-design | AI tools for design |
| #launchpad-experiments | Non-tech people (PMs, designers, Ops) experiment with building in Razorpay repos. Facilitated by Kamlesh + Abhinav. Akanksha is the design lead. Key reference for vibe-coding setup, access process, and prod deployment SOP. |
| #tech_it | IT helpdesk. Raise GitHub access requests, Cursor access, MakeMeAdmin. Tag manager + Kaushik Bhat (kb) for approval. |
| #product-design-bulletin | **Mandatory ritual channel** — all R1 design projects must be posted here at key milestones (see bulletin protocol below). |
| #mcp-dev | MCP + AI integration discussions across Razorpay engineering (added Mar 2026) |

## #product-design-bulletin Protocol

Active since September 2024. **All design projects must post**, including small ones (MOTO, Alipay+, smaller checkout changes).

**When to post:**
- Design doc / experience doc is ready + first-line reviewed (80–90% complete is fine, don't wait for perfect)
- Figma file reaches ~80% + first-line reviewed
- Prototype or demo video is ready
- Important updates: design review changes, PRD updates, dev handoff changes, phased releases

**Post format — main thread starter:**
```
[Group/BU] Project Name

<Customer + business context — why we're doing this>
<Key design decisions or approach>
<Links: Figma, PRD, Prototype>
<Tag DEPA group — designer, EM, PM, analytics + reviewer stakeholders>
<Attach 1-2 key screen images>
```
**Always include:** Figma link + PRD link (even for small projects). Prototype if available. Project Status. Blade Score **only for dashboard and onboarding projects** — never for checkout projects (SG Checkout, MY Checkout, Alipay+, NIPL UPI, MOTO, PayNow, etc.).

**Updates go in the same thread** — do NOT create new top-level posts for updates on the same project. Check "Also send to #product-design-bulletin" on thread replies.

**Tone rules:**
- Business context first — why did this project exist? Committed clients, merchant pipeline, revenue blocked? Lead with this.
- Design focused — explain what decisions were made and why. UX rationale, approach, tradeoffs.
- Zero engineering language — no dev phases, timelines, API names, flags, PR merges. The audience is the design org.
- Never compare to or mention other teams' timelines negatively.

**Tag pattern:** `// @Pingal @Varghese @[PM] @[EM] @[key reviewers]`

**the user's posting history:** 1 post (Curlec AutoKYC Phase 2, Dec 2025). Missing: Agent Studio/Marketplace (now publicly launched Mar 12!), MOTO SG, Alipay+. All three need posts ASAP.

## Vibe-Coding Setup Knowledge

### Standard Repo Access List
Post in #tech_it with GitHub username + manager approval + tag kb:
- github.com/razorpay/dashboard
- github.com/razorpay/frontend-care
- github.com/razorpay/razor-analytics-plugins
- github.com/razorpay/razor-analytics
- github.com/razorpay/frontend-universe
- github.com/razorpay/blade
- github.com/razorpay/passport-nodejs (easy to miss)

### Key Reference Documents
- Akanksha's guide (UI migration using Cursor): https://docs.google.com/document/d/1yl2P1Jo_Eo8zDxQ7DawAoNTAZ1D9SKoei-w1t2e4m_I/edit
- Hemlata's setup SOP: https://docs.google.com/document/d/1skMdJJMW9g0UfrBv2eTlKXfu0xInQhevpCP2TGg4dkY/edit
- the user's Designer-to-Prod SOP (living doc): https://docs.google.com/document/d/1B01AFkkpiAIdBPV-Cq3deuHl-G_Md-RFy3pbeMsYFrY/edit
- Repo ownership/access lookup: 403.concierge.razorpay.com

## Tools
- **[[memory/devrev|DevRev]]** — Issue tracking, sprint management (ENH for enhancements, ISS for issues, TKT for tickets)
- **Figma** — Design tool (+ Figma Make for code prototyping)
- **Slack** — Primary communication
- **Google Workspace** — Docs, Sheets, Calendar, Drive
- **Reclaim.ai** — Auto calendar blocking (focus time, lunch)
- **PostHog** — Product analytics (being onboarded)

## Recent Milestones (as of Mar 2026)
- **FTX 2026** (Feb 28) — Razorpay's first-ever live production demo. the user led Agent Studio design. Varghese: "handling it like a senior designer."
- **Agent Studio launched** (Mar 12) — Razorpay's AI-native platform on Anthropic Claude Agent SDK. Covered by Business Standard.
- **Blade Spark (3.0) live** (~Mar 12) — R1 designers did regression QA across Onboarding + Dashboard.

## Critical Constraints
- Canary deployments at Razorpay require a developer — designers cannot do canary deploys independently.

## Office
- BLR-Arena — Main Bangalore office
- Meeting rooms follow naming convention: BLR-Arena-{Floor}FL-MR-{Number} {Person Name} ({Capacity})
