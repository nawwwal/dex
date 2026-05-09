# Content Design Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-fledged `content-design` skill for Dex that writes, rewrites, audits, and systematizes product UI copy, in-product marketing copy, Razorpay voice, risk-sensitive fintech copy, and source-grounded copy decisions.

**Architecture:** Create `plugins/design/skills/content-design/` as a progressive-disclosure skill. `SKILL.md` is the runtime router and operating contract; detailed knowledge lives in one-hop `references/`; behavior confidence comes from `evals/` that test real copy outcomes, not from storing a large research dump.

**Tech Stack:** Markdown skill files, Dex plugin skill conventions, Python smoke validator, `quick_validate.py`, `rg`, `zsh`.

---

## File Structure

Create these files:

- `plugins/design/skills/content-design/SKILL.md`  
  Runtime router: classify request, load references, write/audit copy, run gates, return output.

- `plugins/design/skills/content-design/references/operating-model.md`  
  The end-to-end workflow: classify, decide, write, check, cite, and escalate.

- `plugins/design/skills/content-design/references/context-model.md`  
  Surface, role, product area, risk, user state, system state, voice lane, marketing lane, and next action.

- `plugins/design/skills/content-design/references/voice-system.md`  
  Razorpay voice as executable mechanics, including founder/startup/entrepreneur support.

- `plugins/design/skills/content-design/references/in-product-marketing.md`  
  Marketing copy inside product and Razorpay marketing lanes from public webpages.

- `plugins/design/skills/content-design/references/surface-playbook.md`  
  Buttons, links, labels, placeholders, helper text, validation, banners, toasts, modals, empty states, tooltips, success, pending, notifications, and developer/API copy.

- `plugins/design/skills/content-design/references/risk-and-tone.md`  
  Risk tiers, detail level, seriousness, humor allowance, and no-overpromise rules.

- `plugins/design/skills/content-design/references/errors-and-recovery.md`  
  Known/unknown failure handling, recovery anatomy, missing-context gate, and high-risk error behavior.

- `plugins/design/skills/content-design/references/accessibility-and-localization.md`  
  Alt labels, link labels, disappearing instructions, critical-state persistence, idioms, variables, and translation risk.

- `plugins/design/skills/content-design/references/source-map.md`  
  Rule-to-source mapping from DESK, Razorpay webpages, Shopify, Material, Wise, Uber Base, Wix, and GOV.UK.

- `plugins/design/skills/content-design/references/quality-rubric.md`  
  Scorecard for clarity, specificity, actionability, voice fit, trust, accessibility, localization, and legal/compliance safety.

- `plugins/design/skills/content-design/evals/payment-failure.md`  
  Merchant and payer-facing payment failure behavior.

- `plugins/design/skills/content-design/evals/razorpay-marketing.md`  
  Razorpay marketing copy with platform, speed, scale, control, growth, trust, and founder/startup lanes.

- `plugins/design/skills/content-design/evals/voice-system.md`  
  Brand voice mechanics, not vague adjectives.

- `plugins/design/skills/content-design/evals/destructive-modal.md`  
  Consequence-first modal and CTA copy.

- `plugins/design/skills/content-design/evals/missing-context.md`  
  Refuse to hallucinate high-risk facts.

- `plugins/design/skills/content-design/evals/consistency-audit.md`  
  Term, perspective, capitalization, and CTA grammar consistency.

- `plugins/design/skills/content-design/evals/accessibility-localization.md`  
  Link labels, alt labels, variables, idioms, and ephemeral critical copy.

- `plugins/design/skills/content-design/evals/in-product-marketing.md`  
  Product nudges, adoption prompts, empty-state conversion, and claim proof.

- `plugins/design/skills/content-design/scripts/validate_content_design_skill.py`  
  Deterministic smoke validator for required files, reference links, eval coverage, and core section names.

Modify these files:

- `copywriting-research.md`  
  Keep as source research. It already includes DESK voice additions and Razorpay public website marketing voice. Add founder/startup/entrepreneur support language if it is not present after implementation.

Do not create:

- `README.md`
- install guide
- changelog
- deeply nested references
- broad marketing-writing skill outside product/content-design scope

---

## Grounding Rules

The implementation must preserve these mechanics from `copywriting-research.md`:

- Minimum useful truth: users should know what happened, what it means, what to do next, and why the product feels trustworthy.
- Full coverage: UI copy, content design, in-product marketing, voice, errors, forms, CTAs, empty states, pending states, success states, notifications, developer/API copy, accessibility, localization, and audits.
- Razorpay marketing lanes: platform authority, speed to value, scale proof, operational control, growth outcome, trust/compliance.
- Marketing aspiration rule: marketing copy should be aspirational by default; proof and mechanism are anchors, not replacements for ambition.
- Razorpay founder/startup/entrepreneur lane: support people building businesses by making money movement feel accessible, credible, and operationally manageable.
- Voice is not polish. Voice is a classifier input and output constraint.
- Marketing claims must name mechanism or proof.
- Humor is allowed only when context, risk, repetition, and localization allow it.
- Internet/source lookup is fallback and refresh path: use bundled references first, browse when the source is missing, current-sensitive, user asks for citations, or factual claims need verification.

---

### Task 1: Write Failing Structural Validator

**Files:**
- Create: `plugins/design/skills/content-design/scripts/validate_content_design_skill.py`
- Test target: `plugins/design/skills/content-design/SKILL.md`

- [ ] **Step 1: Write the failing validator**

Create `plugins/design/skills/content-design/scripts/validate_content_design_skill.py` with this content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "references/operating-model.md",
    "references/context-model.md",
    "references/voice-system.md",
    "references/in-product-marketing.md",
    "references/surface-playbook.md",
    "references/risk-and-tone.md",
    "references/errors-and-recovery.md",
    "references/accessibility-and-localization.md",
    "references/source-map.md",
    "references/quality-rubric.md",
    "evals/payment-failure.md",
    "evals/razorpay-marketing.md",
    "evals/voice-system.md",
    "evals/destructive-modal.md",
    "evals/missing-context.md",
    "evals/consistency-audit.md",
    "evals/accessibility-localization.md",
    "evals/in-product-marketing.md",
]

SKILL_REQUIRED_PATTERNS = [
    r"name:\s*content-design",
    r"description:.*UI copy",
    r"## Runtime Workflow",
    r"## Reference Map",
    r"## Output Modes",
    r"## Quality Gates",
    r"## Source Grounding",
]

REFERENCE_REQUIRED_HEADINGS = {
    "references/voice-system.md": [
        "Razorpay voice",
        "founders",
        "startups",
        "entrepreneurs",
        "Term",
        "execution",
        "avoid",
    ],
    "references/in-product-marketing.md": [
        "Platform authority",
        "Speed to value",
        "Scale proof",
        "Operational control",
        "Growth outcome",
        "Trust and compliance",
        "founder",
        "aspirational",
        "Aspiration ladder",
    ],
    "references/source-map.md": [
        "DESK",
        "Razorpay",
        "Shopify",
        "Material",
        "Wise",
        "Wix",
        "GOV.UK",
    ],
}

EVAL_REQUIRED_SECTIONS = [
    "## Prompt",
    "## Expected behavior",
    "## Pass criteria",
    "## Fail signals",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = read("SKILL.md")
    for pattern in SKILL_REQUIRED_PATTERNS:
        if not re.search(pattern, skill, re.IGNORECASE | re.DOTALL):
            fail(f"SKILL.md missing pattern: {pattern}")

    for ref, required_terms in REFERENCE_REQUIRED_HEADINGS.items():
        text = read(ref).lower()
        for term in required_terms:
            if term.lower() not in text:
                fail(f"{ref} missing required term: {term}")

    for path in REQUIRED_FILES:
        if not path.startswith("evals/"):
            continue
        text = read(path)
        for section in EVAL_REQUIRED_SECTIONS:
            if section not in text:
                fail(f"{path} missing eval section: {section}")

    linked_refs = set(re.findall(r"`(references/[^`]+\.md)`", skill))
    expected_refs = {path for path in REQUIRED_FILES if path.startswith("references/")}
    missing_links = sorted(expected_refs - linked_refs)
    if missing_links:
        fail("SKILL.md does not link references: " + ", ".join(missing_links))

    print("PASS: content-design skill structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run validator to verify it fails**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
```

Expected:

```text
FAIL: missing required files: SKILL.md, references/operating-model.md, ...
```

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/content-design/scripts/validate_content_design_skill.py
git commit -m "test: add content design skill validator"
```

---

### Task 2: Add Behavior Evals Before Skill Instructions

**Files:**
- Create: `plugins/design/skills/content-design/evals/payment-failure.md`
- Create: `plugins/design/skills/content-design/evals/razorpay-marketing.md`
- Create: `plugins/design/skills/content-design/evals/voice-system.md`
- Create: `plugins/design/skills/content-design/evals/destructive-modal.md`
- Create: `plugins/design/skills/content-design/evals/missing-context.md`
- Create: `plugins/design/skills/content-design/evals/consistency-audit.md`
- Create: `plugins/design/skills/content-design/evals/accessibility-localization.md`
- Create: `plugins/design/skills/content-design/evals/in-product-marketing.md`

- [ ] **Step 1: Write failing eval files**

Create `plugins/design/skills/content-design/evals/payment-failure.md`:

```markdown
# Payment Failure Eval

## Prompt

```md
Use $content-design to rewrite this merchant dashboard banner:
"Something went wrong. Try again later."

Context: Customer payment failed because the issuing bank declined it.
```

## Expected behavior

The skill should classify this as high-risk payment failure copy for a merchant-facing dashboard surface. It should state the payment failed, name the bank as actor, give the merchant a useful next action, and avoid implying Razorpay can fix a bank decline.

## Pass criteria

- Uses a direct heading such as `Payment failed`.
- Body says the customer's bank declined or blocked the payment.
- Next action asks the merchant to ask the customer to try another payment method or view payment details.
- Does not use `Something went wrong`, `Oops`, or `try again later`.
- Explains why the rewrite works in terms of risk, actor, and next action.

## Fail signals

- Treats the bank decline as a Razorpay system issue.
- Uses cute language.
- Tells the merchant to retry when retry is not the right recovery.
- Omits the affected object or next action.
```

Create `plugins/design/skills/content-design/evals/razorpay-marketing.md`:

```markdown
# Razorpay Marketing Eval

## Prompt

```md
Use $content-design to write three homepage headline options for a Razorpay product that helps founders accept payments without a website.

Audience: startups, entrepreneurs, and first-time founders.
Product facts: payment links can be shared over WhatsApp, SMS, email, and social channels. No coding required.
```

## Expected behavior

The skill should use Razorpay marketing lanes, especially speed to value, founder/startup support, and growth outcome. The copy should be aspirational by default, then anchor that aspiration in product mechanism or proof. It should not imitate Gamma-style whimsy.

## Pass criteria

- Includes at least one founder/startup/entrepreneur-aware option.
- Includes at least one aspirational headline that names the future the founder wants.
- Names the mechanism: share payment links over WhatsApp, SMS, email, or social channels.
- Uses Razorpay-style money movement language: accept, collect, get paid, payments, customers.
- Avoids unsupported claims such as `best`, `effortless`, `seamless`, or `fastest` unless paired with mechanism or proof.
- Provides a recommended option and explains the lane used.

## Fail signals

- Produces generic startup hype.
- Says only `unlock growth` without mechanism.
- Uses playful Gamma-style lines that do not sound like Razorpay.
- Ignores the founder/startup audience.
```

Create `plugins/design/skills/content-design/evals/voice-system.md`:

```markdown
# Voice System Eval

## Prompt

```md
Use $content-design to define the voice for Razorpay copy in a founder onboarding flow.
Use the format: Term -> meaning -> execution -> avoid.
```

## Expected behavior

The skill should treat voice as mechanics, not adjectives. It should connect Razorpay's voice to founders, startups, entrepreneurs, money movement, trust, speed, and operational confidence.

## Pass criteria

- Defines 4-6 voice terms.
- Each term uses `Term -> meaning -> execution -> avoid`.
- Includes founder/startup/entrepreneur support as a real voice lane.
- Maps each term to observable writing choices.
- Explains how voice changes between marketing, onboarding, and high-risk finance states.

## Fail signals

- Uses vague adjectives without execution.
- Treats voice as final polish.
- Ignores risk level.
- Produces a manifesto instead of rules.
```

Create `plugins/design/skills/content-design/evals/destructive-modal.md`:

```markdown
# Destructive Modal Eval

## Prompt

```md
Use $content-design to write a modal for deleting a webhook endpoint.
Context: Razorpay will stop sending events to this URL. Existing event logs stay available.
```

## Expected behavior

The skill should write consequence-first modal copy with specific CTAs and safe-exit language.

## Pass criteria

- Title names the object: `Delete webhook?`.
- Body states Razorpay will stop sending events to the URL.
- Body states existing event logs will not be deleted.
- Primary CTA is `Delete webhook`.
- Secondary CTA is `Cancel`.
- Does not use `Are you sure?`, `Confirm`, or `OK`.

## Fail signals

- Hides consequence in vague body text.
- Uses a generic destructive CTA.
- Adds humor.
- Omits what remains unaffected.
```

Create `plugins/design/skills/content-design/evals/missing-context.md`:

```markdown
# Missing Context Eval

## Prompt

```md
Use $content-design to write an error message for a failed settlement.
```

## Expected behavior

The skill should not pretend to know why the settlement failed. It should ask for or list the missing system facts and provide only a safe unknown-cause fallback.

## Pass criteria

- States that settlement failure needs cause, owner, affected amount/date, and recovery path before final copy can safely ship.
- Offers likely cause options: bank verification pending, bank issue, Razorpay issue, regulator/compliance issue, unknown.
- Provides a safe fallback that does not invent cause.
- Mentions that financial copy must not hallucinate system truth.

## Fail signals

- Invents a cause.
- Says `try again later` as final copy without context.
- Uses casual reassurance.
- Omits safety/impact questions.
```

Create `plugins/design/skills/content-design/evals/consistency-audit.md`:

```markdown
# Consistency Audit Eval

## Prompt

```md
Use $content-design to audit these strings:
- My payouts
- Your payout settings
- Settlement dashboard
- Transfer successful
- Payment sent
```

## Expected behavior

The skill should flag perspective drift, term drift, and state-name ambiguity.

## Pass criteria

- Identifies `My` vs `Your` perspective inconsistency.
- Distinguishes payout, settlement, transfer, and payment instead of treating them as synonyms.
- Recommends one naming system.
- Explains why consistency builds trust and reduces cognitive load.

## Fail signals

- Only rewrites each string individually.
- Uses synonyms to make copy sound varied.
- Ignores financial object distinctions.
```

Create `plugins/design/skills/content-design/evals/accessibility-localization.md`:

```markdown
# Accessibility and Localization Eval

## Prompt

```md
Use $content-design to review this UI copy:
Button: Click here
Tooltip: You can only do this if your settlement is delayed.
Toast: Your KYC was rejected because your PAN name did not match. Upload a corrected PAN by 12 June.
Alt: Image of search icon
```

## Expected behavior

The skill should flag vague link/button text, essential instructions hidden in tooltip/toast, and visual-format alt text.

## Pass criteria

- Replaces `Click here` with an action or destination.
- Moves critical KYC rejection copy out of a disappearing toast.
- Flags tooltip as wrong place for essential eligibility information.
- Changes alt text to the action or meaning.
- Checks localization risks and variables.

## Fail signals

- Treats accessibility as only alt text.
- Leaves critical content in a toast.
- Keeps `Image of`.
```

Create `plugins/design/skills/content-design/evals/in-product-marketing.md`:

```markdown
# In-Product Marketing Eval

## Prompt

```md
Use $content-design to write an in-dashboard nudge for enabling UPI.
Context: Merchant accepts card payments but has not enabled UPI. UPI lets customers pay from supported apps.
```

## Expected behavior

The skill should write a concrete product nudge, not a campaign slogan. It should persuade through mechanism and next action.

## Pass criteria

- Headline states an outcome such as accepting UPI payments from more customers.
- Body names the mechanism: customers pay from supported UPI apps.
- CTA is `Enable UPI` or equivalent.
- Does not use unsupported hype.
- Explains why the nudge is appropriate in-product.

## Fail signals

- Uses `Unlock seamless payment experiences`.
- Omits what UPI enables.
- Adds pressure without eligibility or value.
- Writes a generic ad headline.
```

- [ ] **Step 2: Run validator to verify evals are still not enough**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
```

Expected:

```text
FAIL: missing required files: SKILL.md, references/operating-model.md, ...
```

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/content-design/evals
git commit -m "test: add content design behavior evals"
```

---

### Task 3: Add Reference Files From Research

**Files:**
- Create all `plugins/design/skills/content-design/references/*.md`
- Modify: `copywriting-research.md` only if founder/startup support language needs strengthening

- [ ] **Step 1: Write references with source-grounded sections**

Create `references/voice-system.md` with these required sections:

```markdown
# Voice System

Use voice as a product behavior, not a polish pass.

## Razorpay voice

Default voice: clear, composed, accountable, action-led, numerate, and founder-supportive.

## Founder, startup, and entrepreneur lane

Razorpay often speaks to people building businesses: founders, entrepreneurs, operators, and finance teams. The copy should make money movement feel possible, credible, and manageable without turning into startup hype.

Term -> meaning -> execution -> avoid:

- Founder-supportive -> respects people building under uncertainty -> name the next concrete business action, reduce setup anxiety, show what can start now -> "change the world" hype
- Operator-clear -> helps a busy business owner know what to do -> use exact product objects, dashboard actions, timelines, and outcomes -> abstract productivity claims
- Ambitious but grounded -> supports growth without fantasy -> connect growth to payment methods, conversion, recovery, settlement, or automation -> "unlock limitless growth"
- Trust-building -> makes money movement feel safe -> name proof, compliance boundary, actor, or control -> casual reassurance without facts
- Fast-to-value -> shows how quickly value starts -> use "no coding", "in minutes", "single click" only when true -> speed claims blocked by KYC, bank, or approval steps

## Voice by context

- Marketing: more ambitious, proof-led, and outcome-led.
- Onboarding: supportive, specific, confidence-building.
- Product UI: concise, action-led, state-aware.
- High-risk finance: calm, exact, actor-aware.
- Legal/compliance: formal, precise, no cleverness.

## Humor gate

Use humor only in low-risk moments where it does not carry essential meaning. Never use humor for payment failure, KYC rejection, settlement issues, refunds, chargebacks, disputes, account suspension, data loss, or legal consent.
```

Create `references/in-product-marketing.md` with these required sections:

```markdown
# In-Product Marketing

In-product marketing is still interface copy. It may persuade, but it must not break task clarity, eligibility, trust, or risk fit.

## Marketing is aspirational

Marketing copy should project a desirable future for the user. For Razorpay, that future usually means starting a business faster, accepting the first payment, selling across channels, reducing manual finance work, scaling payouts, increasing conversion, or operating with more confidence.

Mechanism and proof are anchors, not substitutes for aspiration. Do not reduce every headline to a feature description.

## Razorpay marketing lanes

### Platform authority
Meaning: Razorpay is the financial operating layer.
Execution: all-in-one framing, one platform, one dashboard, one stack, product breadth.
Avoid: abstract "future of finance" without product proof.

### Speed to value
Meaning: users can start, collect, pay, settle, or integrate quickly.
Execution: no coding, in minutes, single click, instantly, go live faster.
Avoid: speed claims when KYC, approval, bank, or compliance can block the user.

### Scale proof
Meaning: numbers create trust.
Execution: payment methods, processed volume, success rate, businesses served, cost/time saved.
Avoid: unverified superlatives.

### Operational control
Meaning: finance teams get visibility and levers.
Execution: dashboards, APIs, webhooks, reports, approval workflows, bulk actions, tracking.
Avoid: emotional benefits without naming the control gained.

### Growth outcome
Meaning: payment products help merchants sell, recover, convert, or expand.
Execution: conversion lift, fewer RTOs, more payment methods, easier collections, fewer manual steps.
Avoid: "unlock growth" without mechanism.

### Trust and compliance
Meaning: regulated money movement needs proof and boundaries.
Execution: RBI authorization, licensed banks, security policy, partner-bank disclaimers, test/live mode.
Avoid: implying Razorpay is a bank where partner banks provide the account.

## Aspiration ladder

| Level | Role | Example shape | Risk |
| --- | --- | --- | --- |
| Functional | Names what the product does | Create and share payment links | Clear but flat |
| Outcome-led | Names the business result | Start collecting payments without a website | Strong default |
| Aspirational | Names the future the user wants | Take your first sale live in minutes | Best for marketing when mechanism is true |
| Proof-led aspiration | Pairs future with evidence | Grow checkout conversion with a 5X faster, one-click flow | Strongest when sourced |
| Empty hype | Future without mechanism | Unlock limitless growth | Reject |

## Founder and entrepreneur marketing

Write to the person trying to start, run, or scale a business. Favor concrete enablement:

- Start accepting payments without a website.
- Share a payment link over WhatsApp, SMS, email, or social channels.
- Track payments from the dashboard.
- Automate reminders.
- Get paid with less setup.
- Take a first product, service, or idea live without waiting for a full website or engineering setup.

Avoid founder theater:

- Build the future, when no concrete business action follows.
- Supercharge your hustle.
- Unlock limitless growth.
- Make entrepreneurship effortless.

## Claim-proof rule

Allow "seamless", "effortless", "faster", "best", "more", and "supercharged" only when paired with mechanism, proof, or source. In product UI and high-risk states, prefer concrete mechanism over these words.
```

Create the remaining references by splitting `copywriting-research.md`:

- `operating-model.md`: lines around mission, runtime workflow, output modes, and source fallback.
- `context-model.md`: surface, role, product area, risk, user state, system state, voice lane, marketing lane, next action.
- `surface-playbook.md`: component-level rules and examples.
- `risk-and-tone.md`: tone map and high-risk product rules.
- `errors-and-recovery.md`: Wix-derived error anatomy, generic failure detector, payment/refund/settlement failure behavior.
- `accessibility-and-localization.md`: alt labels, link text, tooltips, placeholders, toast persistence, internationalization.
- `source-map.md`: source-to-rule mapping.
- `quality-rubric.md`: scoring table and shipping thresholds.

- [ ] **Step 2: Run validator to verify SKILL.md is still missing**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
```

Expected:

```text
FAIL: missing required files: SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/content-design/references copywriting-research.md
git commit -m "feat: add content design reference system"
```

---

### Task 4: Add SKILL.md Router

**Files:**
- Create: `plugins/design/skills/content-design/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Create `plugins/design/skills/content-design/SKILL.md` with this content:

```markdown
---
name: content-design
description: "Product content and UX writing for software interfaces, fintech flows, Razorpay copy, in-product marketing, UI microcopy, voice systems, error messages, empty states, buttons, labels, helper text, onboarding, KYC, payments, payouts, refunds, settlements, notifications, developer/API copy, accessibility labels, and copy audits. Use when drafting, rewriting, critiquing, or systematizing product copy."
---

# Content Design

Write product language as interface behavior.

The job is not to make copy sound nicer. The job is to help the user understand what is happening, what changed, why it matters, what to do next, and why the product can be trusted.

## Runtime Workflow

1. Classify the request before writing.
2. Load only the references needed for that request.
3. Decide whether enough product truth exists to write safely.
4. Write copy in the right surface, risk, state, and voice lane.
5. Run quality gates.
6. Return shippable copy, useful variants, assumptions, and source notes when needed.

If the user asks for high-risk financial, legal, compliance, payment, refund, payout, settlement, KYC, data-loss, or irreversible-action copy and the cause/impact/recovery path is missing, flag the missing context before final copy.

## Reference Map

- Runtime and source behavior: `references/operating-model.md`
- Classification schema: `references/context-model.md`
- Brand voice, founder/startup support, humor, and joy: `references/voice-system.md`
- Razorpay marketing lanes and in-product persuasion: `references/in-product-marketing.md`
- Component and surface rules: `references/surface-playbook.md`
- Risk, seriousness, and tone mapping: `references/risk-and-tone.md`
- Errors, recovery, missing system context: `references/errors-and-recovery.md`
- Accessibility and localization: `references/accessibility-and-localization.md`
- Rule provenance and external research fallback: `references/source-map.md`
- Output scoring: `references/quality-rubric.md`

Load `references/source-map.md` when the user asks where a rule came from, when a claim may be current-sensitive, or when the bundled references do not cover the request. Browse official/current sources when the source map is insufficient.

## Output Modes

- `write`: generate copy from a brief.
- `rewrite`: improve existing copy.
- `audit`: identify issues and recommend replacements.
- `systematize`: create a voice, vocabulary, string table, or content rules for a flow.
- `variants`: produce shorter, clearer, stricter, softer, more explicit, or more voice-forward versions.
- `diagnose`: identify missing product or system context before writing.
- `marketing`: write in-product or Razorpay-style marketing copy using source-backed lanes.
- `accessibility-check`: check labels, hints, alt text, disappearing instructions, and critical state visibility.
- `localization-check`: check idioms, variables, sentence fragments, cultural references, and translation risk.

## Classification

Before writing, identify:

- surface
- product area
- user role
- risk level
- user state
- system state
- required next action
- voice lane
- marketing lane, if any
- source/proof requirement

Infer when safe. Ask only when the missing fact changes correctness, risk, legality, or trust.

## Quality Gates

Reject or rewrite copy that:

- hides a known cause behind generic failure language
- uses humor in high-risk flows
- uses vague CTAs like `Submit`, `Proceed`, `OK`, or `Confirm` when the action has a real name
- says `invalid` without telling the user how to fix it
- calls a pending state complete
- overpromises approval, settlement, refund, payment success, availability, or speed
- puts essential information only in a tooltip, placeholder, toast, or accessibility hint
- uses unsupported marketing claims
- changes product nouns or perspective inconsistently
- weakens localization or accessibility

## Source Grounding

Use bundled references first. Use internet research when:

- the skill does not cover the surface or industry
- Razorpay public marketing voice may have changed
- current regulation, payment policy, platform rules, or brand guidance matters
- the user asks for citations
- a factual or comparative claim needs proof

Prefer official product, design-system, docs, policy, and company pages. Do not invent source authority.

## Default Output

For simple copy requests:

```text
Recommended copy

[final copy]

Alternative

[one useful variant]

Assumptions
- [only if needed]
```

For complex or high-risk requests:

```text
Recommended copy

[surface-specific copy]

Why this works
- Surface:
- User state:
- Risk level:
- Voice lane:
- What changed:
- Next action:
- Source/rule grounding:

Variants
1. Shorter:
2. More explicit:
3. More voice-forward, if safe:

Do not use
- [bad pattern]: [why it fails]
```
```

- [ ] **Step 2: Run structural validator**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
```

Expected:

```text
PASS: content-design skill structure is valid
```

- [ ] **Step 3: Run official skill validator**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/content-design
```

Expected:

```text
Valid skill: plugins/design/skills/content-design
```

If the exact success text differs, accept a zero exit code and no error diagnostics.

- [ ] **Step 4: Commit**

```bash
git add plugins/design/skills/content-design/SKILL.md
git commit -m "feat: add content design skill router"
```

---

### Task 5: Add OpenAI Skill Metadata

**Files:**
- Create: `plugins/design/skills/content-design/agents/openai.yaml`

- [ ] **Step 1: Add metadata**

Create `plugins/design/skills/content-design/agents/openai.yaml`:

```yaml
interface:
  display_name: "Content Design"
  short_description: "Write product copy with voice and trust"
  default_prompt: "Use $content-design to write or audit product UI copy with the right voice, risk level, and source grounding."
```

- [ ] **Step 2: Run official skill validator**

Run:

```bash
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/content-design
```

Expected: zero exit code.

- [ ] **Step 3: Commit**

```bash
git add plugins/design/skills/content-design/agents/openai.yaml
git commit -m "feat: add content design skill metadata"
```

---

### Task 6: Forward-Test the Skill With Subagents

**Files:**
- Modify: `plugins/design/skills/content-design/SKILL.md`
- Modify references or evals only where forward tests reveal actual failures.

- [ ] **Step 1: Run forward tests**

Dispatch fresh subagents with raw prompts. Do not tell them the expected answer.

Prompt 1:

```text
Use $content-design at /Users/aditya.nawal/projects/dex/plugins/design/skills/content-design to rewrite this payment failure banner: "Something went wrong. Try again later." Context: customer bank declined the payment. Surface: merchant dashboard.
```

Prompt 2:

```text
Use $content-design at /Users/aditya.nawal/projects/dex/plugins/design/skills/content-design to write three Razorpay-style homepage headlines for founders who want to accept payments without a website. Facts: payment links can be shared on WhatsApp, SMS, email, and social channels. No coding required.
```

Prompt 3:

```text
Use $content-design at /Users/aditya.nawal/projects/dex/plugins/design/skills/content-design to define a Razorpay voice table for founder onboarding. Use Term -> meaning -> execution -> avoid.
```

Prompt 4:

```text
Use $content-design at /Users/aditya.nawal/projects/dex/plugins/design/skills/content-design to audit: My payouts, Your payout settings, Settlement dashboard, Transfer successful, Payment sent.
```

Prompt 5:

```text
Use $content-design at /Users/aditya.nawal/projects/dex/plugins/design/skills/content-design to write an error message for a failed settlement. No other context is available.
```

- [ ] **Step 2: Compare outputs against evals**

For each output, check:

```text
- Did it classify context before writing?
- Did it load or apply the right reference area?
- Did it write shippable copy?
- Did marketing mode produce aspiration, not only feature description?
- Did it avoid generic failure, unsupported claims, and vague CTAs?
- Did it use founder/startup/entrepreneur language when relevant?
- Did it ask for missing high-risk facts instead of hallucinating?
- Did it explain decisions mechanically, not aesthetically?
```

- [ ] **Step 3: Patch skill based on failures**

Only patch the file that owns the failure:

- Trigger/routing failure -> `SKILL.md`
- Voice/founder failure -> `voice-system.md`
- Marketing/Razorpay failure -> `in-product-marketing.md`
- Error recovery failure -> `errors-and-recovery.md`
- Surface anatomy failure -> `surface-playbook.md`
- Source/proof failure -> `source-map.md`
- Eval mismatch -> eval file

- [ ] **Step 4: Re-run validators**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/content-design
git diff --check -- plugins/design/skills/content-design copywriting-research.md
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add plugins/design/skills/content-design copywriting-research.md
git commit -m "test: forward-test content design skill"
```

---

### Task 7: Update Design Plugin Description If Needed

**Files:**
- Modify: `plugins/design/.codex-plugin/plugin.json`
- Modify: `plugins/design/.claude-plugin/plugin.json`

- [ ] **Step 1: Update plugin descriptions only if the new skill is not discoverable enough**

If current plugin descriptions omit content design, update the description text:

```json
"description": "Design thinking, content design, crux finding, presentation narrative, visual handoffs, and divergence"
```

For Codex long description:

```json
"longDescription": "Dex design workflows for content design, crux finding, presentation narrative, visual handoffs, visual explanations, and divergent concept exploration."
```

- [ ] **Step 2: Validate JSON**

Run:

```bash
jq empty plugins/design/.codex-plugin/plugin.json plugins/design/.claude-plugin/plugin.json
```

Expected: no output and zero exit code.

- [ ] **Step 3: Commit**

```bash
git add plugins/design/.codex-plugin/plugin.json plugins/design/.claude-plugin/plugin.json
git commit -m "docs: advertise content design skill"
```

---

### Task 8: Final Verification

**Files:**
- All created/modified files.

- [ ] **Step 1: Run full verification**

Run:

```bash
python3 plugins/design/skills/content-design/scripts/validate_content_design_skill.py
python3 /Users/aditya.nawal/.agents/skills/.system/skill-creator/scripts/quick_validate.py plugins/design/skills/content-design
jq empty plugins/design/.codex-plugin/plugin.json plugins/design/.claude-plugin/plugin.json
git diff --check
```

Expected:

```text
PASS: content-design skill structure is valid
```

`quick_validate.py`, `jq`, and `git diff --check` should exit cleanly.

- [ ] **Step 2: Inspect final tree**

Run:

```bash
find plugins/design/skills/content-design -maxdepth 3 -type f | sort
```

Expected file list includes:

```text
plugins/design/skills/content-design/SKILL.md
plugins/design/skills/content-design/agents/openai.yaml
plugins/design/skills/content-design/evals/accessibility-localization.md
plugins/design/skills/content-design/evals/consistency-audit.md
plugins/design/skills/content-design/evals/destructive-modal.md
plugins/design/skills/content-design/evals/in-product-marketing.md
plugins/design/skills/content-design/evals/missing-context.md
plugins/design/skills/content-design/evals/payment-failure.md
plugins/design/skills/content-design/evals/razorpay-marketing.md
plugins/design/skills/content-design/evals/voice-system.md
plugins/design/skills/content-design/references/accessibility-and-localization.md
plugins/design/skills/content-design/references/context-model.md
plugins/design/skills/content-design/references/errors-and-recovery.md
plugins/design/skills/content-design/references/in-product-marketing.md
plugins/design/skills/content-design/references/operating-model.md
plugins/design/skills/content-design/references/quality-rubric.md
plugins/design/skills/content-design/references/risk-and-tone.md
plugins/design/skills/content-design/references/source-map.md
plugins/design/skills/content-design/references/surface-playbook.md
plugins/design/skills/content-design/references/voice-system.md
plugins/design/skills/content-design/scripts/validate_content_design_skill.py
```

- [ ] **Step 3: Confirm working tree scope**

Run:

```bash
git status --short
```

Expected: only intended files are changed if final commits were not made, or clean if all task commits were made.

---

## Confidence Strategy

The skill will not be effective because it knows many rules. It will be effective only if:

1. `SKILL.md` routes requests to the right reference.
2. The references are split by actual decision mode, not by source article.
3. Evals cover the hardest behavior: marketing with proof, founder/startup voice, high-risk failure copy, consistency audits, and missing context.
4. Forward tests verify the agent can produce copy from the knowledge base without seeing the expected answer.

If forward tests produce generic copy, the fix is not more research. The fix is sharper routing, stricter output shapes, and better eval fail signals.

## Plan Self-Review

- Spec coverage: covers full product copy, voice, in-product marketing, Razorpay public marketing voice, founder/startup/entrepreneur lane, source grounding, accessibility, localization, and high-risk fintech copy.
- Placeholder scan: no unfinished placeholder markers or unspecified implementation steps.
- Type/path consistency: all paths are under `plugins/design/skills/content-design/` except the existing source research file and plugin manifests.
- Risk: the plan is large, but the split is necessary because the user explicitly rejected a narrow v1. Progressive disclosure keeps runtime context controlled.
