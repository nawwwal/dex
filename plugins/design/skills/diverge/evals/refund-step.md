# Test 2: Copy divergence

## Prompt

```md
/diverge "Diverge on copy for a destructive delete modal that removes a project and 23 files."
```

## Expected

The skill should select Copy-level mode.

Output should include:

- Copy diagnosis
- User mental state
- Copy roles
- 8-12 copy directions grouped by tone/function
- Labels, CTAs, helper text, errors, empty states, success states
- Behavioral effect of each
- "Too clever" and "too vague" kills

## Pass criteria

- Multiple copy strategies, not one rewritten modal.
- Consequence-first CTA examples, such as `Delete 23 files`.
- Reassuring but not soft.
- No generic "Are you sure?"
- Error and success copy included.
- Ethical friction included.
- Tone variants included.
- Localization notes included.
- CTA describes outcome, not vague action.

## Fail signals

- Uses "Submit", "Continue", "OK", or "Confirm" as primary destructive CTA.
- Uses humor for destructive action.
- Fails to name consequences.
- Adds friction without explaining why.
