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
