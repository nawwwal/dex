# Quality Rubric

Use this file before returning final copy, especially for high-risk financial, legal, compliance, or marketing claims.

Score each criterion from 0 to 2.

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Clarity | Ambiguous | Understandable with effort | Immediately clear |
| Specificity | Generic | Some context | Exact object, cause, state, or action |
| Actionability | No next step | Implied next step | Clear next step |
| Tone fit | Wrong for risk | Mostly acceptable | Matches surface and severity |
| Brevity | Bloated | Slightly long | No wasted words |
| Trust | Hype, blame, or vagueness | Neutral | Accurate and confidence-building |
| Accessibility | Screen-reader hostile | Acceptable | Descriptive and navigable |
| Consistency | Invents or swaps terms | Mostly aligned | Uses stable vocabulary and perspective |
| Localization | Idioms, puns, fragile fragments | Minor issues | Easy to translate |
| Legal/compliance safety | Overpromises or implies wrong actor | Slightly loose | Precise and defensible |

## Shipping thresholds

- Low-risk UI: 14/20 minimum.
- Medium-risk UI: 16/20 minimum.
- High-risk UI: 17/20 minimum.
- Critical, legal, payment, compliance, data-loss, or irreversible-action copy: 18/20 minimum and must pass legal/product review if required.

## Automatic fail gates

Reject or rewrite copy that:

- Hides a known cause behind generic failure language.
- Uses humor in high-risk or critical flows.
- Uses vague CTAs like Submit, Proceed, OK, or Confirm when the action has a real name.
- Says "invalid" without telling the user how to fix it.
- Calls a pending state complete.
- Overpromises approval, settlement, refund, payment success, availability, or speed.
- Puts essential information only in a tooltip, placeholder, toast, or accessibility hint.
- Uses unsupported marketing claims.
- Changes product nouns or perspective inconsistently.
- Weakens localization or accessibility.

## Audit questions

- What is the user trying to finish?
- What changed in the system?
- What does the user need to know now?
- What can the user do next?
- What actor owns the next step?
- What amount, date, timeline, ID, or limit would reduce uncertainty?
- What term must stay consistent across the flow?
- What claim needs mechanism, proof, or source verification?

## Bad-copy detectors

- Generic failure: "Something went wrong."
- Cute failure: "Oops, your payout hit a snag."
- Startup hype: "Unlock seamless payment experiences."
- Passive fog: "The document was not able to be verified."
- Blame language: "You entered the wrong IFSC."
- Vague CTA: "Proceed."
- Legal softness: "You're almost ready" when approval is pending.

