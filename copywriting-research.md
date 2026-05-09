I’d name this skill **content design**, not copywriting.

Copywriting optimizes for persuasion. This skill should optimize for **task completion, trust, clarity, and context-sensitive persuasion only where the surface allows it**. For Razorpay, the default failure mode of AI copy will be either startup-bro hype or cute UX writing. Both are dangerous in fintech.

One important note: I checked all provided links. The Material 3 and Uber Base pages expose limited/no readable HTML in this browser, so I used their indexed official page content plus Google’s official Material UX writing codelab where needed. The Wix, Shopify, Wise, van Schneider, and GOV.UK pages were directly readable.

---

# Razorpay content design skill: research guide + framework v0.1

## 1. Skill mission

The agent’s job is not to “make copy sound good.”

The agent’s job is to produce UI language that helps Razorpay users:

1. understand what is happening
2. understand what changed
3. understand what they need to do next
4. trust the system when money, identity, risk, or compliance is involved
5. complete the task with the least ambiguity possible

The skill should treat every string as part of the interface, not decoration. Shopify states this directly: words are part of design, but each word adds noise, so content should only be added when it improves clarity. ([Polaris React][1]) GOV.UK frames content design as starting with user needs rather than what an organization wants to say. ([GOV.UK][2])

Core principle:

> **Write the minimum useful truth for the user’s current state.**

Not minimum words. Minimum useful truth.

---

## 2. Source synthesis: what the agent must learn from each reference

### Wix error writing

Wix’s strongest lesson is that bad error copy is usually a product/system failure disguised as a sentence problem. Bad errors are generic, blame users, use technical jargon, or use an inappropriate tone. Good errors explain what happened, why it happened, what was unaffected, how to fix it, and what to do if the issue cannot be fixed immediately. ([Wix UX][3])

For the agent:

* Never accept “Something went wrong” as final copy unless it is genuinely unknowable.
* Ask or infer: What failed? Who caused it? What is affected? What remains safe? What can the user do now?
* Avoid “Oops,” jokes, blame, and backend terms.
* If the product knows the cause and the copy hides it, the copy is wrong.

Wix also found that generic errors require cross-functional work: developers mapped triggers, causes, frequency, and resolution paths before writers rewrote messages. They prioritized errors by frequency and whether the error blocked the user’s flow. ([Wix UX][3])

For Razorpay, this becomes non-negotiable: **the agent should flag missing system context, not hallucinate a polished vague error.**

---

### Shopify Polaris

Shopify’s core model is lean, human, action-led content. It asks writers to add only what is necessary, remove repetition, use plain language, start with verbs, and focus on the one thing the merchant needs to know or do next. ([Polaris React][1])

For the agent:

* Every string must have a job.
* Every screen must have one dominant next action.
* Buttons should be verbs or verb+noun.
* Do not fill every available content slot just because the component supports it.

Shopify’s error guidance is directly useful: errors should explain what is wrong, be specific, avoid error jargon like “invalid,” avoid over-apology, and give detailed next-step instructions. Error messages should be placed close to the issue, and severity should be communicated through design as well as words. ([Polaris React][4])

For Razorpay:

* “Invalid IFSC” is bad.
* “Enter an 11-character IFSC” is better.
* “We couldn’t verify this IFSC. Check the code and try again.” is better when verification is the real failure.

Shopify’s naming guidance is important because AI tends to invent branded feature names. Shopify says most features do not need branded names; features should be descriptive and should reveal their purpose. Evocative names are reserved for standalone products with independent branding. ([Polaris React][5])

For Razorpay:

* Prefer **payment links**, **settlements**, **refunds**, **disputes**, **test mode**, **live mode**, **bank account verification**.
* Avoid invented names unless the feature is already officially branded.
* Do not make a feature sound more proprietary than it is.

Shopify’s grammar guidance also gives useful mechanics: sentence case for headings, buttons, cards, and subject lines; contractions for human tone; descriptive headings; no “click here”; numerals for numbers; consistent timestamp formats; and “you” for addressing the user. ([Polaris React][6])

---

### Material Design / Google

Material’s M3 content guidance says UI text should be clear to anyone and follow AP Style unless noted otherwise. ([Material Design][7]) Google’s Material UX writing codelab frames UX writing as language that supports user journeys through word choice, hierarchy, clarity, and concision. It also says UI writing should prioritize user goals over formal grammar rules when interface constraints demand it. ([Google Codelabs][8])

For the agent:

* AP Style is the grammar baseline, not a creative style.
* Interface clarity can override formal writing when needed.
* The goal is not beautiful prose. The goal is usable language.

Material’s principles: be concise but not robotic, write simply and directly, address users clearly, avoid mixing “you/your” with “I/my,” and communicate only essential details for the context. ([Google Codelabs][8])

For Razorpay:

* Use “you” for user actions.
* Use “we” only when Razorpay is responsible or will take action.
* Use “I” only for consent-style actions: “I agree to the terms.”
* Avoid mixed perspective: “Update my bank account so you can receive payouts” is broken.

Material’s tone mapping is especially useful for Razorpay. Tone should vary by journey point: onboarding, confirmations, errors, notifications, labels, and empty states. Material also says products involving payment or legal matters should move toward a more serious and detailed tone when comprehension is critical. ([Google Codelabs][8])

For Razorpay:

* Marketing banner: can be benefit-led.
* Empty state: can be encouraging.
* Payment failure: calm, precise, non-cute.
* KYC/compliance: formal, exact, no excitement.
* Destructive modal: serious, explicit, consequence-first.

Material’s alt text guidance says alt text should convey meaning, not image format; decorative images do not need meaningful alt text; avoid starting with “image of”; keep it short; and focus on the important part of the image. ([Material Design][9])

---

### Wise

Wise is useful because it is also financial-product language. Its grammar guide prioritizes active voice, sentence case, no ampersands, clear currency formatting, numerals for scanability, no emojis, and precise action verbs. ([wise.design][10])

For the agent:

* Financial copy should be plain without being lifeless.
* Use the active voice because it makes actor and action clear.
* Use numerals because people scan numbers faster in digital interfaces.
* Avoid emojis in product copy; they are hard to localize and inaccessible in many contexts.

Wise’s verb distinctions are valuable. “Edit” means modifying something that exists. “Change” means switching from one option to another. “Choose” means deciding among valid options. “Select” means picking a specific option or interacting with the UI; it is more inclusive than “click.” ([wise.design][10])

For Razorpay:

* **Edit bank account details** = modify saved details.
* **Change settlement account** = switch to another account.
* **Choose a payment method** = user preference among options.
* **Select Add new** = instruction inside the interface.
* Avoid “click” unless the experience is strictly desktop-only.

Wise also says “just,” “only,” “easy,” and “quick” can discourage users when a task is not easy for them. Shopify makes the same point in inclusive language guidance. ([Polaris React][11])

For Razorpay:

* Bad: “Just complete your KYC.”
* Better: “Complete KYC to start accepting live payments.”
* Bad: “It only takes a minute.”
* Better: “You’ll need your PAN and bank account details.”

---

### Uber Base

Uber’s Base content design system frames content as a way to motivate reliance, empower users, build trust, nurture relationships, and define new spaces. It distinguishes **voice** as the consistent brand personality and **tone** as the contextual attitude that changes by moment. It also defines a value proposition as a user-facing explanation of how a choice transforms the customer’s life, not a buzzword. ([base.uber.com][12])

For the agent:

* Voice stays stable.
* Tone changes by surface, risk, and user state.
* Value propositions must say what changes for the user, not what the feature is called.

Uber’s button guidance is also useful: button labels should indicate what happens when tapped, buttons perform actions while links navigate, primary actions should be limited, destructive actions require confirmation, and disabled buttons should be avoided when they hide the reason something cannot continue. ([base.uber.com][13])

For Razorpay:

* Prefer enabled buttons with validation feedback over silent disabled buttons.
* Use destructive labels that name the destructive act: “Delete webhook,” not “Confirm.”
* Use links for destinations: “View settlement details.”
* Use buttons for actions: “Retry payout.”

Uber’s VoiceOver guidance is strong for accessibility: accessibility labels should answer “Who are you?” or “What is your name?”, traits should explain what the element is, and hints should only be used when the result of interaction is not obvious. Hints should not contain essential information because power users may turn them off. ([base.uber.com][14])

---

### van Schneider / DESK

This article’s useful idea is that UX copy should often be understood at a glance, not “read.” It recommends cutting filler like “in order to,” “please note,” “we recommend,” “you must,” and “there is,” using progressive disclosure, and avoiding passive voice. ([House of van Schneider][15])

For the agent:

* Start with the shortest clear version.
* Remove ceremonial phrases.
* Use progressive disclosure: show what the user needs now, not everything the system knows.
* Concise does not mean robotic; it means efficient.

For Razorpay:

* Bad: “Please note that in order to receive settlements, you must complete your KYC.”
* Better: “Complete KYC to receive settlements.”
* Better with context: “Complete KYC by 12 June to keep receiving settlements.”

---

### DESK: product copy, voice, selling, humor, and joy

The additional DESK articles change the skill architecture. They make voice a functional part of UX copy, not a decorative layer to apply after clarity.

#### UX copy continues selling

DESK argues that marketing copy sells the product, but UX copy continues selling it during use. This does not mean every product string should become promotional. It means product copy should affirm that the user made the right choice, help them move forward, and validate progress at the right moments. ([UX copy sells][16])

For the agent:

* Treat in-product marketing as part of UX, not a detached campaign layer.
* Sell through use: show the user what they can now do, what changed, and why the next step is worth taking.
* Do not pitch when the user is already acting. At that point, reduce friction, answer questions, and affirm progress.
* If the copy needs paragraphs to explain a feature, flag possible product complexity instead of hiding it under prose.
* Speak to one user, not to a crowd. “Your cart is empty” is more direct than “The cart is empty.”

For Razorpay:

* In-product marketing should validate the merchant’s operational goal: accept more payment methods, reduce manual work, recover failed payments, settle faster, or understand risk.
* The pitch must be tied to a concrete product mechanism. “Enable UPI to let customers pay from supported apps” is usable. “Unlock seamless payments” is not.
* In serious money, identity, or compliance states, “selling” becomes reassurance and clarity, not hype.

#### Consistency is trust

DESK frames consistent microcopy as the glue of product UX. Voice, perspective, terminology, formatting, and CTA structure should be decided once and used consistently. Random shifts make users wary and increase cognitive load. ([Consistent microcopy][17])

For the agent:

* Track perspective: first person, second person, or neutral. Do not mix “my account,” “your account,” and “profile” without a product reason.
* Use the same product nouns every time. Do not swap synonyms to avoid repetition.
* Keep CTA grammar consistent: do not alternate between question-style CTAs and command-style CTAs unless the surface pattern changes.
* Keep capitalization, punctuation, and heading style consistent across related surfaces.
* In audits, flag inconsistent terms even when each individual string is clear.

For Razorpay:

* Prefer stable nouns: payment, refund, settlement, payout, dispute, webhook, API key, test mode, live mode, KYC.
* Decide whether the product uses “your” language or neutral labels per surface. Do not mix “Your settlements,” “My payouts,” and “Settlement details” in one flow without intent.
* Consistency is not sameness. A KYC rejection and a feature nudge can have different tone, but they should still sound like the same product.

#### Brand voice belongs inside the product

DESK argues that brand voice is not only for ads and website headlines. Product microcopy is where users repeatedly experience the brand, step by step. Voice is created through language choice, tone, and the feeling the product evokes. ([Finding your brand voice][20])

For the agent:

* Always identify the intended voice before rewriting a large surface or system.
* Voice terms must be executable. Each adjective should map to word choice, punctuation, sentence length, rhythm, humor, directness, and amount of explanation.
* Use a small set of voice adjectives, but make them specific. “Helpful” is weak unless it says what helpful does: names the next action, explains impact, removes uncertainty.
* When no brand voice is provided, infer a provisional voice from product category, risk level, and existing copy. Label the inference.
* Apply voice differently by context. Voice should survive tone shifts, but should not override clarity, safety, or legal precision.

For Razorpay:

* Current recommended voice remains clear, composed, accountable, action-led, and numerate.
* Add a voice calibration layer:
  * **Clear** → common words, exact nouns, no filler.
  * **Composed** → calm punctuation, no panic, no over-celebration in risky flows.
  * **Accountable** → name the actor: user, Razorpay, bank, customer, regulator, system.
  * **Action-led** → verbs point to the next useful step.
  * **Numerate** → exact dates, amounts, limits, timelines, IDs, and counts when useful.
* A future Razorpay audit should collect actual product strings and define a more precise brand voice from the product itself, not only external design systems.

#### Humor must be designed

DESK says humor can make products memorable, but only when context, user emotion, repetition, and clarity are handled. Humor should not appear everywhere; it works best in lower-risk moments such as loading screens, empty states, 404 pages, confirmations, help text, and placeholders. If a joke weakens comprehension, kill it. ([My best products are a joke][18])

For the agent:

* Treat humor as a contextual tool, not a voice default.
* Before using humor, classify the user’s emotional state and the cost of misunderstanding.
* Avoid humor in payment failure, KYC rejection, settlement issues, disputes, chargebacks, data loss, account suspension, or legal consent.
* Use humor only when it helps the user feel seen, reduces hesitation, or makes a low-risk moment more memorable.
* Check repetition. A funny line seen every day becomes annoying.
* Check localization. If the joke depends on idiom, slang, culture, or a pun, it probably fails.

For Razorpay:

* Humor can live at the edge: low-risk onboarding, low-stakes empty states, harmless loading states, lightweight feature education.
* Humor should never obscure a financial status, legal requirement, or recovery action.
* In fintech, the best “wit” is often precise understatement, not jokes.

#### Joy is momentum and confidence

DESK’s “joy” article is not about making copy cute. It defines useful product joy as positive language, confidence-building, active voice, and step-by-step encouragement. The product should make users feel capable and ready to continue. ([Product joy][19])

For the agent:

* Use positive language to motivate action, but do not shame users into compliance.
* Affirm useful progress after the user completes a step.
* Use active voice to create forward motion.
* In onboarding, use help text to reduce hesitation and build confidence.
* Avoid patronizing celebration. Not every successful action needs applause.

For Razorpay:

* “Joy” in Razorpay should usually mean reduced anxiety, clear progress, and confidence that money, identity, or data is handled correctly.
* Good: “KYC submitted. We’ll review your details and notify you when live payments are available.”
* Bad: “You’re almost there!” when approval is still uncertain.
* Good: “Add UPI to let customers pay from supported apps.”
* Bad: “Don’t miss out on effortless growth.”

Skill implication:

The skill needs a dedicated `voice-system.md` reference and an `in-product-marketing.md` reference. Marketing copy inside the product should be grounded in DESK’s idea that UX copy continues selling, but constrained by Razorpay’s risk model. Voice should be part of the classifier, not a late polish pass.

---

### Razorpay public website marketing voice

Razorpay’s public website gives the skill a stronger native marketing model than borrowed Gamma-style examples. The pattern is not “quirky and imaginative.” It is **operator aspiration made concrete through money movement, speed, scale, trust, and control**.

Marketing copy should be aspirational by default. Its job is to make founders, entrepreneurs, merchants, and operators feel that a larger business outcome is within reach: starting faster, selling more, collecting sooner, reducing manual work, scaling payouts, or running finance with more confidence. The proof/mechanism requirement is not meant to flatten that aspiration. It is the anchor that keeps aspiration from becoming interchangeable startup hype.

Observed source surfaces:

* Homepage: all-in-one finance platform, product-suite navigation, category breadth, and AI-native expansion. ([Razorpay homepage][21])
* Payment Gateway: trusted gateway, easiest integration, highest success rates, 100+ payment methods, developer-friendly APIs, and platform integrations. ([Payment Gateway][22])
* Payment Links and Payment Pages: no-code setup, instant collection, shareability, branded pages, automation, and industry use cases. ([Payment Links][23], [Payment Pages][24])
* RazorpayX: business banking, payouts, scale, operational control, success rates, cost reduction, and customer proof. ([RazorpayX][25])
* Magic Checkout: high-energy growth marketing with conversion, RTO reduction, one-click checkout, proof numbers, and playful product confidence. ([Magic Checkout][26])

The marketing voice works through six repeatable lanes:

1. **Platform authority** → Razorpay as the financial operating layer.
   * Mechanic: all-in-one framing, category breadth, “one platform,” “one dashboard,” “one provider.”
   * Use for: homepage, suite pages, high-level product positioning.
   * Avoid: vague “future of finance” unless tied to actual product surface.

2. **Speed to value** → users can start, collect, pay, settle, or integrate quickly.
   * Mechanic: “in minutes,” “single click,” “instantly,” “no coding,” “go live faster.”
   * Use for: activation, onboarding, no-code products, developer setup, payment collection.
   * Avoid: speed claims where compliance, bank, or approval timelines can block the user.

3. **Scale proof** → numbers create trust.
   * Mechanic: payment methods, businesses served, unicorn adoption, TPV, success rates, processed volume, cost/time saved.
   * Use for: landing pages, adoption nudges, enterprise proof, sales surfaces.
   * Avoid: unsupported “best,” “largest,” “fastest,” or “most trusted” claims without source or context.

4. **Operational control** → finance teams get visibility and precision.
   * Mechanic: dashboards, APIs, webhooks, reports, approval workflows, bulk actions, real-time tracking.
   * Use for: payouts, banking, reconciliation, reports, finance-ops surfaces.
   * Avoid: emotional benefits without naming the control gained.

5. **Growth outcome** → payment products help merchants sell, convert, recover, or expand.
   * Mechanic: conversion lift, fewer RTOs, more payment methods, easier collections, fewer manual steps.
   * Use for: Magic Checkout, Payment Links, Payment Pages, UPI, Optimizer, product adoption.
   * Avoid: “unlock growth” unless the copy names the mechanism: fewer failed payments, faster checkout, abandoned-cart recovery, more payment methods.

6. **Trust and compliance** → regulated money movement needs proof and boundaries.
   * Mechanic: RBI authorization, licensed banks, security policy, test/live mode, partner-bank disclaimers, compliance terms.
   * Use for: banking, cards, current accounts, payment aggregation, security, checkout trust.
   * Avoid: implying Razorpay is a bank where the legal surface says partner banks provide the account.

Marketing headline lanes for Razorpay:

| Lane | Meaning | Execution | Avoid |
| --- | --- | --- | --- |
| Platform | Razorpay unifies multiple money jobs | “Manage payments, payouts, banking, payroll, and credit from one platform” | Abstract “all your financial dreams in one place” |
| Speed | Razorpay reduces setup or transaction time | “Create a payment link and collect in seconds” | “Effortless” without saying what effort disappeared |
| Scale | Razorpay is proven at volume | “Accept 100+ payment methods” / “Process 50k payouts with one OTP” | Unverified superlatives |
| Control | Razorpay gives operators visibility and levers | “Track every payment link from the dashboard” | Generic “stay in control” |
| Growth | Razorpay improves revenue or conversion mechanics | “Reduce checkout drop-offs with saved addresses and one-click payment” | “Unlock growth” |
| Trust | Razorpay makes money movement safer and more credible | “Custom URLs help customers recognise your payment page” | Casual confidence in legal/banking contexts |

Aspiration ladder:

| Level | Role | Example shape | Risk |
| --- | --- | --- | --- |
| Functional | Names what the product does | “Create and share payment links” | Clear but flat |
| Outcome-led | Names the business result | “Start collecting payments without a website” | Strong default |
| Aspirational | Names the future the user wants | “Take your first sale live in minutes” | Best for marketing when mechanism is true |
| Proof-led aspiration | Pairs future with evidence | “Grow checkout conversion with a 5X faster, one-click flow” | Strongest when sourced |
| Empty hype | Future without mechanism | “Unlock limitless growth” | Reject |

This creates a Razorpay-specific version of the Gamma sample:

* **Aspirational** should be the marketing default: “Turn every chat into a checkout,” “The payment stack India runs on,” “Every business banking need. One provider.”
* **Descriptive** should carry mechanism: “Create and share payment links over WhatsApp, SMS, or email,” “Make up to 50k payouts in bulk using one OTP.”
* **Proof-led** should use numbers: “100+ payment methods,” “40% growth in conversion rate,” “50% reduction in RTO,” “70% of India’s Unicorns.”
* **Operator-led** should name the workflow: collect, reconcile, settle, refund, approve, track, automate, route, verify.

Important correction:

Razorpay’s public marketing pages sometimes use words the product-copy rules restrict, such as “seamless,” “effortless,” and “supercharged.” The skill should not blindly ban those in marketing mode. Instead:

* In product UI and high-risk states, avoid them unless they are plainly true and non-essential.
* In marketing mode, allow them only when paired with a mechanism, proof point, or concrete outcome.
* In legal, KYC, banking, failure, refund, settlement, and destructive flows, keep the stricter product-copy rules.

For the agent:

* Before writing marketing copy, classify the lane: platform, speed, scale, control, growth, or trust.
* Choose the aspiration level: functional, outcome-led, aspirational, proof-led aspiration, or reject as empty hype.
* Choose one primary lane per headline. Do not cram all six into one line.
* If using a claim, attach proof or mechanism.
* If using aspiration, make the desired future vivid, then tie it to money movement or operational outcome.
* If using playful confidence, keep it at the edge of product, not at the point of risk.

---

### GOV.UK

GOV.UK’s key lesson is that content design is not copy production. It starts with user needs, chooses the right format, removes duplication, and keeps content accurate, current, and useful. ([GOV.UK][2])

For the agent:

* Do not write before identifying the user need.
* Consider whether content should be split, removed, moved, or reformatted.
* Duplicated guidance creates mistrust.
* Content must be maintained, not merely shipped.

For Razorpay:

* If the same rule appears in tooltip, banner, help text, and modal with slightly different words, users will distrust the product.
* The agent should identify duplicate or conflicting strings during audits.

---

# 3. Razorpay writing position

## Default voice

**Clear, composed, accountable, action-led, numerate.**

Mechanics:

* **Clear** → use common words, exact nouns, and visible outcomes.
* **Composed** → no panic, jokes, exclamation marks, or drama in serious flows.
* **Accountable** → say who needs to act: you, Razorpay, bank, customer, or system.
* **Action-led** → lead with what the user can do next.
* **Numerate** → use exact dates, amounts, limits, counts, durations, payment IDs, settlement IDs, and error codes when useful.

Avoid:

* “Oops”
* “Uh-oh”
* “Something went wrong” as default
* “Unlock”
* “Supercharge”
* “Seamless”
* “Hassle-free”
* “Powerful”
* “Effortless”
* “Leverage”
* “Experience the future of payments”
* “Don’t worry” when money is affected
* “Just” and “simply” in compliance, risk, or setup flows
* Puns in errors, KYC, payments, disputes, refunds, settlements, chargebacks, or risk reviews

The Gamma headline sample is useful as a warning. Clever copy like “Love at first site” or “A great deck isn’t rocket science” works only in low-risk marketing contexts. Razorpay’s product surfaces deal with money movement, compliance, and operational continuity. The safer rule is: **cleverness belongs at the edge of the product, never at the point of risk.**

---

# 4. Context model the agent must use before writing

Before generating copy, the agent must classify the request across these dimensions.

## A. Surface

* Button
* Link
* Form label
* Placeholder
* Helper text
* Inline validation
* Toast/snackbar
* Banner/alert
* Modal/dialog
* Empty state
* Tooltip
* Table header
* Filter/search copy
* Navigation
* Success confirmation
* Failure state
* Onboarding
* In-product marketing banner
* Permission/consent
* Legal/compliance notice
* Alt text/accessibility label
* Email/SMS/push notification
* Developer/API documentation copy

## B. User role

* Founder/merchant
* Finance operator
* Support operator
* Developer
* Admin/owner
* Risk/compliance reviewer
* Customer/end payer
* Partner/platform user

## C. Risk level

* **Low**: cosmetic, preference, navigation
* **Medium**: setup, configuration, reversible changes
* **High**: payments, refunds, payouts, settlements, KYC, bank accounts, disputes, chargebacks, permissions
* **Critical**: data loss, money loss, legal commitment, account suspension, irreversible actions

## D. User state

* First time
* Returning
* Blocked
* Reviewing
* Confirming
* Recovering from failure
* Taking destructive action
* Waiting for external action
* Comparing options

## E. System state

* Success
* Pending
* Failed
* Partially completed
* Blocked by user input
* Blocked by Razorpay
* Blocked by bank/network/regulator/third party
* Unknown fallback

## F. Required next action

* No action
* Retry
* Edit
* Change
* Choose
* Select
* Upload
* Verify
* Contact support
* Wait
* Review
* Confirm
* Delete/remove/cancel

---

# 5. Tone map for Razorpay

Use two axes:

1. **Risk:** low → critical
2. **Detail need:** brief → explicit

| Surface/context           |        Tone | Detail level | Example behavior                         |
| ------------------------- | ----------: | -----------: | ---------------------------------------- |
| Navigation, tabs, filters |     Neutral |        Brief | Use exact nouns                          |
| Buttons                   |      Direct |        Brief | Verb or verb+noun                        |
| Tooltips                  |     Helpful | Brief-medium | Explain unfamiliar concept               |
| Empty states              |     Helpful |       Medium | Explain why empty + next action          |
| Success toasts            |       Quiet |        Brief | Confirm completed action                 |
| Marketing banner          | Benefit-led |       Medium | Show concrete user outcome               |
| Setup/onboarding          |  Supportive |       Medium | Explain value + next step                |
| Form validation           |  Corrective |        Brief | State fix, not fault                     |
| Payment failure           |        Calm |       Medium | State status + next action               |
| Payout/settlement issue   |     Serious |  Medium-high | State impact, cause, resolution          |
| KYC/compliance            |      Formal |         High | State requirement, documents, timelines  |
| Destructive modal         |     Serious |         High | State consequence before action          |
| Legal consent             |      Formal |         High | State commitment clearly                 |
| System outage             | Accountable |         High | State impact, safety, next update/action |

---

# 6. Component-level framework

## 6.1 Buttons

Button copy should say what action happens.

Formula:

> **Verb** or **verb + object**

Use:

* Save
* Continue
* Create payment link
* Retry payout
* Upload PAN
* Verify bank account
* Download report
* Delete webhook

Avoid:

* Submit
* Done
* Proceed
* Yes
* Confirm
* Click here
* Let’s go
* Make it happen

Rules:

* One primary action per context.
* Destructive final actions must name the destruction.
* Do not use “Confirm” when the actual action is delete, cancel, deactivate, refund, or remove.
* Use “Continue” only when the next step is generic and obvious.
* Use “Save changes” when changes persist.
* Use “Apply” when settings affect the current view but do not persist globally.

Examples:

| Weak       | Better                  |
| ---------- | ----------------------- |
| Submit     | Create payment link     |
| Confirm    | Delete webhook          |
| Done       | Save changes            |
| Proceed    | Continue to KYC         |
| Click here | View settlement details |

---

## 6.2 Links

Links navigate. Buttons act.

Formula:

> **View / Learn / Open / Go to + destination**

Use:

* View settlement details
* Learn about chargebacks
* Open API logs
* Go to KYC settings
* Download invoice

Avoid:

* Click here
* Here
* Know more
* Read more, when destination is specific
* Learn more, repeated multiple times on one screen

Rule: link text must make sense out of context for screen-reader users.

---

## 6.3 Form labels

Labels identify the information needed.

Use nouns, not instructions.

Good:

* PAN
* GSTIN
* Account holder name
* IFSC
* Business website
* Refund amount
* Webhook URL

Avoid:

* Enter your PAN
* Please provide IFSC
* Type business website here
* Your good name

Rule: labels should remain meaningful after the field is filled.

---

## 6.4 Placeholder text

Placeholders are hints, not labels.

Use placeholders only for examples or formatting.

Good:

* `https://example.com/webhook`
* `RAZR0000001`
* `name@company.com`

Avoid:

* Enter your email address
* Required
* Your website goes here

Rule: never put essential instructions only in placeholder text. It disappears when the user types.

---

## 6.5 Helper text

Helper text prevents errors before they happen.

Formula:

> Constraint + reason, only if useful.

Good:

* Use the bank account linked to your business.
* Upload a PDF, PNG, or JPG under 5 MB.
* Settlements are sent to this account after verification.

Avoid:

* Please ensure all details are correct.
* This is important.
* This helps us serve you better.

Rule: helper text should not repeat the label.

---

## 6.6 Inline validation

Validation should say how to fix the field.

Formula:

> **Enter / Use / Select / Upload + valid requirement**

Good:

* Enter a 10-digit mobile number
* Use an email address with `@`
* Enter an amount between ₹1 and ₹5,00,000
* Upload a file under 5 MB
* Select a settlement account

Avoid:

* Invalid mobile number
* Wrong email
* Bad request
* Not valid
* This field has an error

Rule: do not blame the user. Describe the requirement.

---

## 6.7 Error banners

Use for issues that affect the screen, flow, or account state.

Anatomy:

1. **Heading:** effect on the user
2. **Body:** cause + what is affected + next action
3. **CTA:** one-step recovery

Formula:

> Couldn’t + action
> Cause/impact. Next action.

Example:

**Couldn’t verify bank account**
The account number and IFSC do not match bank records. Check the details and try again.
CTA: **Edit bank details**

For unknown errors:

**Couldn’t load settlements**
Refresh the page to try again. If this keeps happening, contact support.
CTA: **Refresh**

For Razorpay-owned errors:

**Couldn’t create payment link**
There’s an issue on our end. Your details are saved. Try again in a few minutes.
CTA: **Try again**

Rules:

* Say what failed.
* Say what did not happen.
* Say whether money/data is safe if relevant.
* Say what to do next.
* Give support path if user cannot fix it.
* Avoid “Oops,” “sorry” loops, and blame.

---

## 6.8 Toasts/snackbars

Use for temporary, low-detail feedback.

Formula:

> Completed action
> Failed action + retry, if recoverable

Good:

* Payment link created
* Refund initiated
* Webhook deleted
* Report downloaded
* Couldn’t download report. Try again.

Avoid:

* Success!
* Done!
* Your action was successful
* Oops, something went wrong

Rules:

* No heading.
* No long explanation.
* No critical information that disappears.
* Do not use toast for KYC rejection, settlement failure, account suspension, or payment-risk states.

---

## 6.9 Modals/dialogs

Use when the user must make a decision before continuing.

Anatomy:

1. **Title:** decision or consequence
2. **Body:** what will happen, what cannot be undone, what remains unaffected
3. **Primary CTA:** exact action
4. **Secondary CTA:** safe exit

Destructive formula:

> Delete [object]?
> This will [specific consequence]. This cannot be undone.
> CTA: Delete [object]
> Secondary: Cancel

Example:

**Delete webhook?**
Razorpay will stop sending events to this URL. Existing event logs will not be deleted.
Primary: **Delete webhook**
Secondary: **Cancel**

Rules:

* Do not use “Are you sure?” as the title.
* Do not hide consequences in body text.
* Do not use “Confirm” for destructive actions.
* Never make both buttons semantically vague.

---

## 6.10 Empty states

Use empty states to explain why there is no data and what to do next.

Formula:

> No [objects] yet
> [Why this is empty / what will appear here].
> CTA: [Create/connect/start]

Examples:

**No payment links yet**
Create a payment link to accept payments without a website.
CTA: **Create payment link**

**No settlements found**
Settlements for the selected date range will appear here.
CTA: **Change date range**

Rules:

* Do not celebrate emptiness.
* Do not use generic “Nothing to see here.”
* Mention filters/date ranges if they may be hiding data.
* For financial records, avoid implying data does not exist when a filter may be active.

---

## 6.11 Tooltips

Use tooltips for short explanations of unfamiliar terms or constraints.

Good:

* **Settlement cycle:** The time between payment capture and payout to your bank account.
* **Test mode:** Use test API keys to simulate payments without moving money.

Avoid:

* Long instructions
* Marketing copy
* Legal disclosures
* Critical warnings
* Anything required to complete the task

Rule: tooltips are optional help, not required reading.

---

## 6.12 In-product marketing banners

This is where copy may be more persuasive, but it must stay concrete.

Formula:

> Outcome-led headline
> Specific benefit or eligibility
> Action CTA

Good:

**Accept UPI payments from more customers**
Enable UPI to let customers pay directly from supported apps.
CTA: **Enable UPI**

Weak:

**Unlock seamless payment experiences**
Supercharge your business with powerful payment capabilities.
CTA: **Get started**

Rules:

* One concrete benefit.
* One audience.
* One CTA.
* No hype without a mechanism.
* No “faster/easier/better” unless you say what gets faster/easier/better.

---

## 6.13 Success confirmations

Confirm what happened and, if useful, what happens next.

Good:

**KYC submitted**
We’ll review your details and notify you when live payments are available.

**Refund initiated**
The customer should receive ₹2,500 within 5–7 working days.

Avoid:

* Great job!
* You’re all set! when the process is pending
* Success! Your request has been taken

Rule: success copy must not overstate completion. If something is pending, say pending.

---

## 6.14 Pending states

Pending states must reduce anxiety.

Formula:

> Current status + expected next step/timeline + whether user action is needed

Good:

**Bank account verification in progress**
This usually takes up to 2 working days. You do not need to do anything right now.

**Refund processing**
The refund has been sent to the customer’s bank. Bank processing can take 5–7 working days.

Avoid:

* Almost there!
* Hang tight!
* Processing...
* Your request is underway

Rule: for money movement, pending copy must identify the actor currently responsible: Razorpay, bank, user, customer, or regulator.

---

## 6.15 KYC and compliance copy

KYC copy must be exact, calm, and non-casual.

Good:

**Complete KYC to accept live payments**
You’ll need your PAN, business details, and bank account information.

**PAN verification failed**
The name on the PAN does not match your business details. Check the PAN or update your business name.

Avoid:

* Just finish KYC
* You’re almost ready to go live!
* Something’s off with your docs
* We need a few things

Rules:

* State requirement.
* State reason only when useful.
* State documents needed.
* State timeline if known.
* Do not make compliance feel optional if it is mandatory.
* Do not promise approval.

---

## 6.16 Payment failure copy

Payment failure copy must distinguish payer-facing and merchant-facing copy.

Merchant-facing:

**Payment failed**
The customer’s bank declined the payment. Ask the customer to try another payment method.

Payer-facing:

**Payment failed**
Your bank declined the payment. Try another payment method or contact your bank.

Avoid:

* Transaction unsuccessful due to issuer failure
* Payment could not be processed
* Oops, your payment hit a snag

Rules:

* Say who declined/blocked if known.
* Do not expose technical gateway jargon unless the user is a developer.
* Do not imply Razorpay can fix bank-side failures.
* Provide a next action.

---

## 6.17 Refund copy

Refund copy must separate initiation, processing, success, and failure.

Examples:

**Refund initiated**
The customer should receive ₹1,200 within 5–7 working days.

**Refund failed**
The customer’s bank could not process the refund. Try again or contact support.

**Refund already processed**
This payment was refunded on 12 June.

Rules:

* Use exact amount where possible.
* Use exact date where possible.
* Say “initiated” when money has not reached the customer.
* Avoid “refunded” until the state is final.

---

## 6.18 Settlement and payout copy

Settlement copy must be operationally precise.

Examples:

**Settlement delayed**
Your settlement of ₹48,320 is delayed because bank account verification is pending. Complete verification to receive future settlements.

**Payout failed**
The bank account on file is closed. Update your bank details and we’ll retry the payout.

Rules:

* Mention amount if available.
* Mention expected settlement date if available.
* Distinguish “settlement created,” “settlement processing,” “settlement delayed,” and “settlement paid.”
* Say what user action affects future settlements versus current settlement.

---

## 6.19 Developer/API copy

Developer copy can include technical terms, but must pair them with action.

Good:

**Webhook delivery failed**
Your endpoint returned `500`. Fix the endpoint and retry the event.

**Invalid API key**
Use a live mode key to create live payments.

Avoid:

* Authentication failed
* Bad request
* Invalid credentials
* Entity validation failed

Rules:

* Preserve error codes when useful.
* Explain the likely cause.
* State exact fix.
* Distinguish test mode and live mode.
* Do not over-simplify if precision matters.

---

## 6.20 Accessibility labels and alt text

Alt text formula:

> Meaningful object/action, not visual decoration.

Good:

* Search payments
* Download settlement report
* Payment success illustration, if the image conveys success
* QR code for payment link

Avoid:

* Image of search icon
* IMG_2024.png
* Screenshot
* Beautiful dashboard illustration

Rules:

* If the image is decorative, use empty alt text.
* Do not start with “image of.”
* For icons that trigger actions, describe the action, not the icon.
* Accessibility hints should not contain essential information.

---

# 7. The agent’s operating prompt

Use this as the base instruction for the skill.

```text
You are Razorpay’s content design agent.

You write UI copy for fintech product experiences. Your priority is task completion, clarity, trust, accessibility, and context-fit. You do not write decorative copy unless the surface is explicitly marketing or brand-led.

Before writing, classify the surface, user role, user state, system state, risk level, and required next action.

Default voice:
clear, composed, accountable, action-led, numerate.

Rules:
1. Write for the user’s current task, not the company’s desire to sound impressive.
2. Prefer plain, specific language over cleverness.
3. Use sentence case.
4. Use active voice.
5. Use “you” for the user. Use “we” only when Razorpay is responsible or will act. Use “I” only for consent.
6. Do not mix “you/your” and “I/my” in the same phrase.
7. Avoid jokes, puns, emojis, exclamation marks, and hype in product UI.
8. Avoid “Oops,” “Something went wrong,” “invalid,” “failed due to technical issue,” and “please try again later” unless no better system context exists.
9. For errors, state what happened, what is affected, why if known, and what the user can do next.
10. For money, identity, compliance, legal, risk, data loss, or irreversible actions, use a serious and explicit tone.
11. For buttons, use verb or verb+noun.
12. For links, describe the destination.
13. For validation, state the fix.
14. For destructive actions, name the object and consequence.
15. For pending states, identify who or what the user is waiting for.
16. For accessibility labels, describe the action or meaning, not the visual asset.
17. Do not invent branded names.
18. Do not overpromise speed, approval, success, or availability.
19. If information is missing, make a reasonable assumption and label it. If the missing information changes the correctness of the copy, flag it.
20. Output copy that can ship, not generic advice.
```

---

# 8. Agent input schema

The agent should request or infer this context.

```json
{
  "surface": "banner | modal | toast | button | form_label | helper_text | validation | empty_state | tooltip | marketing_banner | accessibility_label | email | sms | push | developer_error",
  "product_area": "payments | payment_links | settlements | refunds | payouts | kyc | disputes | subscriptions | webhooks | api_keys | dashboard | reports",
  "user_role": "merchant | founder | finance_ops | developer | admin | customer | support_agent",
  "user_state": "first_time | returning | blocked | confirming | recovering | waiting | reviewing",
  "system_state": "success | failed | pending | blocked | partially_complete | unknown",
  "risk_level": "low | medium | high | critical",
  "cause": "known cause, if any",
  "affected_object": "payment | refund | settlement | account | webhook | report | document",
  "affected_amount": "optional",
  "affected_date_or_timeline": "optional",
  "next_action": "retry | edit | upload | verify | contact_support | wait | confirm | delete | none",
  "constraints": "character limit, localization, legal wording, design limitations",
  "existing_copy": "copy to rewrite, if any"
}
```

---

# 9. Output format for the skill

The agent should return:

```text
Recommended copy

[Surface-specific final copy]

Why this works

- User state:
- Risk level:
- Tone:
- What changed:
- Next action:
- Accessibility/localization notes:

Alternatives

1. Shorter:
2. More explicit:
3. Softer, if needed:

Do not use

- [bad version]
- [why it fails]
```

For simple requests, the agent can skip rationale and provide only final copy plus one alternate.

---

# 10. Content quality rubric

Score each string from 0–2.

| Criterion               | 0                         | 1                          | 2                                |
| ----------------------- | ------------------------- | -------------------------- | -------------------------------- |
| Clarity                 | Ambiguous                 | Understandable with effort | Immediately clear                |
| Specificity             | Generic                   | Some context               | Exact object/cause/action        |
| Actionability           | No next step              | Implied next step          | Clear next step                  |
| Tone fit                | Wrong for risk            | Mostly fine                | Matches surface and severity     |
| Brevity                 | Bloated                   | Slightly long              | No wasted words                  |
| Trust                   | Hype, blame, or vagueness | Neutral                    | Accurate and confidence-building |
| Accessibility           | Screen-reader hostile     | Acceptable                 | Descriptive and navigable        |
| Consistency             | Invents terms             | Mostly aligned             | Uses approved vocabulary         |
| Localization            | Idioms/puns               | Minor issues               | Easy to translate                |
| Legal/compliance safety | Overpromises              | Slightly loose             | Precise and defensible           |

Shipping threshold:

* Low-risk UI: minimum 14/20
* High-risk UI: minimum 17/20
* Critical/legal/payment/compliance: minimum 18/20 and must pass legal/product review if required

---

# 11. Bad-copy detectors

The agent should automatically reject or rewrite copy with these patterns.

## Generic failure

Bad:

> Something went wrong.

Ask:

* What failed?
* What was affected?
* Can the user retry?
* Is data/money safe?
* Who owns the issue?

Better:

> Couldn’t load settlements. Refresh the page to try again.

---

## Cute failure

Bad:

> Oops! Your payout hit a snag.

Why it fails:

* Too casual for money movement.
* Does not state status or fix.

Better:

> Payout failed. Update your bank details and try again.

---

## Startup hype

Bad:

> Unlock seamless payment experiences.

Why it fails:

* No concrete outcome.
* Sounds interchangeable with every fintech product.

Better:

> Accept payments through UPI, cards, and netbanking.

---

## Passive fog

Bad:

> The document was not able to be verified.

Better:

> We couldn’t verify the document.

Even better if cause is known:

> The GSTIN does not match your business name.

---

## Blame language

Bad:

> You entered the wrong IFSC.

Better:

> Enter a valid IFSC.

Better with system context:

> We couldn’t verify this IFSC. Check the code and try again.

---

## Vague CTA

Bad:

> Proceed

Better:

> Continue to verification

---

## Legal softness

Bad:

> You’re almost ready to accept payments.

When KYC is still pending, this overpromises.

Better:

> KYC under review. We’ll notify you when live payments are available.

---

# 12. Razorpay vocabulary rules

## Preferred action verbs

| Use             | Meaning                                 |
| --------------- | --------------------------------------- |
| Create          | Make something new                      |
| Save            | Persist changes                         |
| Edit            | Modify existing details                 |
| Change          | Switch from one option/state to another |
| Choose          | Decide among valid options              |
| Select          | Pick a UI option                        |
| Verify          | Confirm through system/document check   |
| Retry           | Attempt the same action again           |
| Remove          | Detach from current context             |
| Delete          | Permanently remove                      |
| Cancel          | Stop a scheduled/requested action       |
| Deactivate      | Turn off without deleting               |
| Download        | Save file locally                       |
| View            | Navigate to details                     |
| Contact support | Escalate when user cannot resolve       |

## Avoid or restrict

| Avoid              | Use instead                     |
| ------------------ | ------------------------------- |
| Click              | Select                          |
| Submit             | Name the action                 |
| Proceed            | Continue to [next step]         |
| Invalid            | State the requirement           |
| Failed transaction | Payment failed                  |
| Successful         | Say what succeeded              |
| Utilize            | Use                             |
| Enablement         | Setup / activation              |
| Kindly             | Please, or remove               |
| As per             | Based on / under                |
| The same           | It / this / the object          |
| At the earliest    | By [date] / as soon as possible |
| Do the needful     | State exact action              |

---

# 13. Razorpay mechanics: grammar and style

Recommended defaults:

* Use **sentence case** for all UI text.
* Use **active voice**.
* Use **contractions** in normal product UI: “can’t,” “you’re,” “we’ll.”
* Avoid contractions in legal, compliance, and policy-heavy copy if seriousness or precision improves.
* Use numerals for amounts, counts, dates, limits, and durations.
* Use exact currency values when relevant: `₹2,500`, `₹5,00,000`.
* Use “working days” when banks or compliance timelines are involved.
* Avoid exclamation marks in product UI.
* Avoid emojis in product UI.
* Avoid ampersands unless part of a legal name or fixed brand term.
* Avoid periods in short labels, buttons, tabs, and single-line helper text.
* Use periods in body copy, legal copy, multi-sentence messages, and critical explanations.
* Use AP Style as baseline, with Razorpay overrides for Indian financial/product vocabulary.

One style decision Razorpay should explicitly make: **Oxford comma**. Shopify recommends it consistently, while Wise recommends it only when needed for clarity. ([Polaris React][6]) My recommendation for Razorpay: use the Oxford comma in product and legal/compliance copy because lists often contain financial or operational conditions. In marketing copy, avoid long inline lists instead of debating comma style.

---

# 14. Research plan for the next iteration

The agent should not stop at external inspiration. It should learn Razorpay’s own language system.

## Phase 1: Copy audit

Collect real strings from:

* Dashboard home
* Payment links
* KYC
* Settlements
* Refunds
* Disputes/chargebacks
* Webhooks/API keys
* Reports
* Settings
* Error states
* Empty states
* Notifications
* Emails/SMS

For each string, tag:

* Surface
* Product area
* User role
* Risk level
* State
* Trigger
* Current copy
* User confusion risk
* Support-ticket connection
* Proposed rewrite

## Phase 2: Error inventory

For every error, map:

* Error key
* Trigger
* Cause
* Owner: user / Razorpay / bank / regulator / network / unknown
* Frequency
* Blocking level
* User-visible impact
* Existing message
* Recovery path
* Proposed message
* Need for engineering/product fix

This follows Wix’s insight: generic errors are not just writing problems; they often require developer mapping and product decisions. ([Wix UX][3])

## Phase 3: Vocabulary matrix

Build a Razorpay-approved word list:

* Product nouns
* Action verbs
* State names
* Error terms
* Compliance terms
* Developer terms
* Customer-facing terms
* Words to avoid
* Words allowed only in marketing

## Phase 4: Component examples

For every UI component, create:

* Purpose
* Anatomy
* Character guidance
* Tone level
* Good examples
* Bad examples
* Razorpay-specific edge cases

## Phase 5: Testing

Test copy with:

* comprehension checks
* first-click/task completion
* support-ticket reduction
* form completion rate
* error recovery rate
* time to resolution
* translation/localization review
* accessibility review with screen readers

Material’s codelab recommends reading copy aloud, asking others to explain it back, surveying copy in UI context, and using comprehension/task/tone evaluation for deeper testing. ([Google Codelabs][8])

## Phase 6: Voice and in-product marketing system

Build a voice system from real Razorpay product language, not only external references.

For each product area, collect:

* Existing headings, helper text, errors, empty states, modals, success states, and nudges
* Voice adjectives that actually describe the current language
* Voice adjectives Razorpay wants to move toward
* Perspective choices: you/your, we, I/my, neutral nouns
* CTA grammar: verb, verb+noun, question, destination
* Humor allowance by surface and risk level
* Repeated terms and inconsistent synonyms
* Product promises that need proof or eligibility rules

Create:

* A voice calibration table: term → meaning → execution → avoid
* An in-product marketing playbook: adoption nudges, upgrade prompts, activation checklists, feature education, empty-state conversion, plan/limit prompts
* A Razorpay marketing lane map from public webpages: platform authority, speed to value, scale proof, operational control, growth outcome, trust/compliance
* A claim-proof rule: no “best,” “faster,” “easier,” “more,” “seamless,” or “effortless” unless the copy names the mechanism or the product team provides proof
* A humor gate: allowed moments, banned moments, repetition limit, localization check
* A consistency audit: product nouns, perspective, CTA grammar, punctuation, capitalization
* A webpage-mining workflow: when marketing voice is missing or stale, inspect current Razorpay public pages before inventing a voice model

---

# 15. First version of the actual skill

```text
Skill name:
RazorpayContentDesignWriter

Purpose:
Generate, rewrite, audit, and systematize Razorpay UI copy across product surfaces.

Primary behavior:
Given a UI copy request, classify the context, identify the user need, choose the voice/tone/risk lane, write copy that is clear and action-led, and explain only the decisions needed for review.

Default output:
- Final recommended copy
- 1 shorter variant
- 1 more explicit variant for high-risk states
- 1 more voice-forward variant when the surface permits it
- Notes on assumptions, if any

Hard constraints:
- No generic errors when cause is knowable
- No jokes in high-risk states
- No invented feature names
- No vague CTAs
- No “click here”
- No “invalid” without a fix
- No success copy for pending states
- No overpromising approval, time, money movement, or availability
- No essential information inside tooltip, placeholder, or accessibility hint only
- No voice, humor, or marketing claim that weakens clarity, context-fit, localization, or trust
- No “best,” “faster,” “easier,” “more,” “seamless,” or “effortless” claim without a mechanism or proof

Optimization target:
The user should know what happened, what it means, what to do next, and why the product feels trustworthy without rereading.
```

The central shift: make the agent behave less like a copywriter and more like a product designer who uses language as the interface.

[1]: https://polaris-react.shopify.com/content/fundamentals "https://polaris-react.shopify.com/content/fundamentals"
[2]: https://www.gov.uk/guidance/content-design/what-is-content-design "  Content design: planning, writing and managing content - What is content design? - Guidance - GOV.UK
"
[3]: https://wix-ux.com/when-life-gives-you-lemons-write-better-error-messages-46c5223e1a2f "https://wix-ux.com/when-life-gives-you-lemons-write-better-error-messages-46c5223e1a2f"
[4]: https://polaris-react.shopify.com/content/error-messages "Error messages — Shopify Polaris React"
[5]: https://polaris-react.shopify.com/content/naming "Naming — Shopify Polaris React"
[6]: https://polaris-react.shopify.com/content/grammar-and-mechanics "Grammar — Shopify Polaris React"
[7]: https://m3.material.io/foundations/content-design/overview?utm_source=chatgpt.com "Content design - Material Design 3 - Write effective content"
[8]: https://codelabs.developers.google.com/codelabs/material-communication-guidance "Material's Communication Principles: Intro to UX Writing  |  Google Codelabs"
[9]: https://m3.material.io/foundations/content-design/alt-text?utm_source=chatgpt.com "Alt text – Material Design 3"
[10]: https://wise.design/foundations/grammar-and-style "Wise Design - Grammar and style"
[11]: https://polaris-react.shopify.com/content/inclusive-language "Inclusive language — Shopify Polaris React"
[12]: https://base.uber.com/6d2425e9f/p/6d2425e9f/p/4245c4-content-design?utm_source=chatgpt.com "Content design · Base design system"
[13]: https://base.uber.com/6d2425e9f/p/756216-button/b/336373?utm_source=chatgpt.com "Button · Base design system - Uber"
[14]: https://base.uber.com/6d2425e9f/p/72ae38-voiceover?utm_source=chatgpt.com "VoiceOver · Base design system"
[15]: https://vanschneider.com/blog/ux-writing/how-to-write-concisely/ "How to write concisely - DESK Magazine"
[16]: https://vanschneider.com/blog/ux-writing/ux-copy-sells/ "UX copy sells - DESK Magazine"
[17]: https://vanschneider.com/blog/ux-writing/the-glue-to-your-product-ux-consistent-microcopy/ "The glue to your product UX: Consistent microcopy - DESK Magazine"
[18]: https://vanschneider.com/blog/ux-writing/best-products-joke/ "My best products are a joke - DESK Magazine"
[19]: https://vanschneider.com/blog/ux-writing/how-to-write-ux-copy-that-makes-your-product-a-joy-to-use/ "How to write UX copy that makes your product a joy to use - DESK Magazine"
[20]: https://vanschneider.com/blog/ux-writing/finding-your-brand-voice/ "Finding your brand voice - DESK Magazine"
[21]: https://razorpay.com/ "Razorpay - India's All-in-One Finance Platform"
[22]: https://razorpay.com/payment-gateway/ "Best Payment Gateway in India to Accept Online Payments"
[23]: https://razorpay.com/payment-links/?source=know_more "Razorpay Payment Links"
[24]: https://razorpay.com/payment-pages/?source=know_more "Razorpay Payment Pages"
[25]: https://razorpay.com/x/ "RazorpayX - The All-In-One Business Banking Suite"
[26]: https://razorpay.com/magic/ "Razorpay Magic Checkout"
