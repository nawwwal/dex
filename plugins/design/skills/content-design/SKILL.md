---
name: content-design
description: "Product content and UX writing for software interfaces, fintech flows, Razorpay copy, in-product marketing, UI copy, aspirational marketing copy, voice systems, error messages, empty states, buttons, labels, helper text, onboarding, KYC, payments, payouts, refunds, settlements, notifications, developer/API copy, accessibility labels, and copy audits. Use when drafting, rewriting, critiquing, or systematizing product copy."
---

# Content Design

Write product language as interface behavior.

The job is not to make copy sound nicer. The job is to help the user understand what is happening, what changed, why it matters, what to do next, and why the product can be trusted. Marketing mode is different: it should project a desirable future, then anchor that aspiration in product mechanism, proof, or source.

## Runtime Workflow

1. Classify the request before writing.
2. Load only the references needed for that request.
3. Decide whether enough product truth exists to write safely.
4. Write copy in the right surface, risk, state, voice lane, and marketing aspiration level.
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
- `marketing`: write in-product or Razorpay-style marketing copy using source-backed aspirational lanes.
- `accessibility-check`: check labels, hints, alt text, disappearing instructions, and critical state visibility.
- `localization-check`: check idioms, variables, sentence fragments, cultural references, and translation risk.

Marketing outputs must include an aspirational option when the surface is a homepage, campaign, product marketing page, adoption banner, empty state, or founder-facing growth prompt. Recommend an aspirational or proof-led aspirational option by default, then show the product mechanism that makes the promise credible.

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
- aspiration level, if marketing
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
- makes marketing merely descriptive when the surface asks for aspiration
- returns only functional or feature-descriptive marketing options when a founder, startup, entrepreneur, homepage, or campaign surface asks for aspiration
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
- Marketing lane / aspiration level:
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
