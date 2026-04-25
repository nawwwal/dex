# Fixture: calibrate-bar

A third fixture exercising **Step 1 (Brief interview)** specifically. The other two fixtures (`refund-step.md`, `agent-dashboard.md`) verify the full pipeline; this one isolates the Brief extraction so regressions there are caught early.

## Prompt

```
/diverge "Internal tool for our design system team. Need to track which Blade components are most/least used across Razorpay dashboards, and flag when a team builds a custom component that already exists in Blade."
```

## Expected Step 1a — the 3-question interview

The skill MUST post exactly one message containing the 3 required questions before generating anything else. Expected verbatim shape:

```
Before I diverge, three quick things. Answer in any format — bullets, fragments, vibes.

1. The main thing — if you could only get ONE thing right about this, what is it? (one sentence)
2. References — name 3-5 products / installations / games / films / artworks you admire. Anything that raises your bar; doesn't have to relate to this problem.
3. Constraints and anti-patterns — what cannot change (design system, brand, downstream consumers) and what's already been tried that didn't work / what would feel deeply wrong.

Reply 'go' once done.
```

The skill then waits. It does NOT proceed to vocabulary, decomposition, or concepts until the user replies.

## Sample user reply

```
1. main thing — make designers feel like they're contributing to a shared system, not policing each other.
2. references — github contributor graphs, the SF Symbols app, observable notebooks, the Figma community page, IndieWeb webrings.
3. constraints — must use Blade, must not require teams to file tickets, can't be another standalone app (live inside our existing internal tools portal). anti-patterns: leaderboards, shame metrics, anything that feels like a compliance dashboard.
```

## Expected Brief block

After the user replies, the skill emits a Brief block. Expected fields:

```
Brief

Main thing: Make designers feel like they're contributing to a shared system, not policing each other.
References: GitHub contributor graphs, SF Symbols app, Observable notebooks, Figma community page, IndieWeb webrings.
Constraints: Must use Blade. Must not require teams to file tickets. Must live inside the existing internal tools portal — not a standalone app.
Anti-patterns: Leaderboards, shame metrics, compliance-dashboard feel.
Audience (inferred): Razorpay product designers and FE engineers across dashboard teams; secondary: Blade core team.
Consistency contract (inferred): Blade components and tokens, dashboard nav, login state. Must be a route inside the existing tools portal.
Altitude (inferred): Underlying issue (cultural — feeling of contribution vs surveillance), not surface (the problem isn't "tracking is ugly").
Rave-tweet (drafted): "the new blade usage thing on dashboard.razorpay shows me where my work shows up across the org. it's a contribution graph, not a cop."

Reply 'go' to lock, or correct any line.
```

The skill then waits again. It does NOT proceed to Step 1b (decomposition) or Step 2 (vocabulary) until the user replies `go` or corrects fields.

## Pass criteria

- **Single-message interview.** All 3 questions posted in ONE message, not three separate prompts. The literal phrase "Reply 'go' once done." appears.
- **Skill waits.** No tool calls fire between the interview message and the user's reply.
- **Brief block emitted with all 8 fields.** Main thing, References, Constraints, Anti-patterns, Audience, Consistency contract, Altitude, Rave-tweet — all present, even if some are inferred.
- **Inferred fields marked.** Audience, Consistency contract, Altitude carry `(inferred)` or `(uncertain)` markers when not directly given by the user.
- **Rave-tweet under 30 words and concrete.** Names the product or surface. Does not use "elevate", "seamless", "unleash", "next-gen", "delight" as verbs.
- **Consistency contract derived from Constraints, not invented.** If the user says "must use Blade", contract names Blade. Does not introduce a stack the user didn't mention.
- **Altitude inference reasoned.** Output names whether the prompt is asking about surface fixes, the underlying issue, or both — and the inference must follow from the words in the user's prompt.
- **Skill waits for `go`.** Step 2 does not start until the user explicitly confirms.

## Fail signals

- Skill posts the questions and then immediately starts generating without waiting.
- Skill posts the questions one at a time over multiple messages.
- Brief block missing one or more of the 8 fields.
- Rave-tweet is marketing fluff ("Elevate your design system to the next level with seamless component tracking!").
- Consistency contract invents a stack the user didn't mention (e.g., "Tailwind tokens" when the Brief said Blade).
- Skill proceeds to Step 1b without waiting for `go`.
- Skill skips the Brief on `skip brief` but does NOT mark the output as DEGRADED at the top.

## Skip-brief variant

Re-run the same prompt, but instead of answering, reply `skip brief`. Expected behavior:

- Skill self-generates a Brief (using its inference of main thing, references it would associate with the prompt, plausible constraints).
- Output is marked **DEGRADED** at the top.
- Skill proceeds to Step 1b without waiting further.

Pass: the DEGRADED marker is visible in the output, and the skill doesn't pretend the user provided the Brief.

## Verification commands

```bash
cd /Users/aditya.nawal/projects/dex/plugins/design/skills/diverge

# Confirm the 3-question interview literal text is in SKILL.md
grep -E "main thing|References — name|Constraints and anti-patterns|Reply 'go'" SKILL.md
# Expect 4 hits.

# Confirm Brief block fields exist
grep -E "Audience \(inferred\)|Consistency contract \(inferred\)|Altitude \(inferred\)|Rave-tweet \(drafted\)" SKILL.md
# Expect 4 hits.

# Confirm DEGRADED marker for skip brief is documented
grep -E "skip brief|DEGRADED" SKILL.md
# Expect at least 2 hits.
```
