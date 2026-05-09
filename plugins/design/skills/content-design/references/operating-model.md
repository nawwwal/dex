# Operating Model

Use this file to run the content-design workflow end to end. The skill's job is to produce interface language that helps a user understand state, consequence, and next action.

Core rule: write the minimum useful truth. Minimum useful truth means the copy says what happened, what it means, what the user can do next, and what can be trusted. It does not mean the fewest possible words.

## Runtime workflow

1. Classify the request before writing.
2. Identify the product truth available: actor, cause, affected object, impact, recovery path, proof, and constraints.
3. Choose the surface pattern from `surface-playbook.md`.
4. Choose the risk and tone behavior from `risk-and-tone.md`.
5. Apply voice from `voice-system.md`; do not use voice to hide missing facts.
6. Write the copy.
7. Run the quality gates in `quality-rubric.md`.
8. Return final copy with assumptions or missing context only when it changes correctness or trust.

## Output modes

- Write: create new copy from context.
- Rewrite: improve existing copy while preserving product truth.
- Audit: identify weak joints, risk, inconsistency, and replacements.
- Systematize: create a voice table, string table, vocabulary, or flow rule set.
- Diagnose: stop and name missing context before writing high-risk copy.
- Marketing: use in-product persuasion rules and Razorpay lanes.
- Accessibility/localization check: inspect labels, disappearing content, variables, idioms, and screen-reader behavior.

## Missing-context gate

Stop before final copy when the missing fact changes user safety, financial truth, legal meaning, or product behavior.

Ask for or list:

- What failed or changed?
- Who owns the issue: user, Razorpay, bank, customer, regulator, partner, or system?
- What object is affected: payment, payout, refund, settlement, KYC, account, webhook, API key, report, or document?
- What remains safe or unaffected?
- What can the user do now?
- What timeline, amount, ID, limit, or date should be shown?

If a fallback is needed, make it honest: state the failed action and safe recovery without inventing cause.

## Copy decision rules

- Do not accept "Something went wrong" when the product knows what failed.
- Do not polish vague copy. Replace vagueness with state, actor, consequence, and action.
- Do not use synonyms for variety in financial nouns. Repetition is safer than term drift.
- Do not make a pending state sound complete.
- Do not use marketing language in risk, compliance, legal, failure, destructive, or money-movement states.
- Do not invent branded feature names.

## Progressive disclosure

Show the user what they need for the current decision. Move secondary detail into helper text, expandable content, documentation, or support paths only when it is not required to act safely.

Keep essential information visible. Do not hide required instructions in tooltips, placeholders, toasts, or accessibility hints.

