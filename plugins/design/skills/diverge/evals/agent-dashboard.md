# Fixture: agent-dashboard

A second fixture that catches the regressions found in v2.7.x (delight dropped, anchors software-skewed, generic concepts like "Boring Wallboard" / "Promise Ledger"). Run by hand alongside `refund-step.md`.

## Prompt

```
/diverge "Dashboard for all installed AI agents in our org. Need to see what each agent is doing, who's using it, and whether it's helping."
```

## Expected shape

A correct run produces, in order:

1. **Step 1a — Brief interview.** Skill posts ONE message with the 3 questions, waits, then emits the Brief block (Main thing, References, Constraints, Anti-patterns, Audience inferred, Consistency contract inferred, Altitude inferred, Rave-tweet drafted) and waits for `go`.

2. **Step 1b — Break down the problem.** 3 JTBD, real constraint named, problem-elimination, similar problems in other fields. Each cross-referenced to the Brief's main thing.

3. **Step 2 — Surface vocabulary.** Should fire on phrases like "see what each agent is doing" — surface real references like a Slack people directory, F1 telemetry boards, a kitchen brigade station list, Stardew Valley villager status, a Pokémon team page. Mix software with non-software.

4. **Step 3 — 8-10 concepts**, each with the full template including:
   - **Modality** (input → output → feedback loop) line
   - **Structural thesis** (one rigorous sentence referencing the Brief's main thing)
   - **Anchor** field naming a real, Googleable thing the mechanic borrows from
   - **Delight moment** field naming a sensory instant + real-world reference

5. **Step 4 — Kill ledger.** Skill runs every concept through Keep / Rewrite / Kill before user sees comparison. Killed list shown as one-line summary. User sees only Keep + Rewritten concepts in Step 5.

6. **Step 5 — Comparison table** with "How it dies" column. Hybrid combinations if interesting.

7. **Step 6 — Deepen the picks.** Day-in-the-life narratives + simplicity pass + real-world states + decision framework.

8. **Step 7 — Output choice question.** Skill waits.

## Pass criteria (eyeball)

- **Brief extracted.** Step 1a posted the 3 questions in ONE message, waited for user reply, then emitted the Brief block.
- **Structural thesis present and unique.** Every one of the 10 concepts has a Structural thesis sentence. No pair is interchangeable. Each thesis names the borrowed-from-real source explicitly: *"Treats agents as a Quaker meeting because the Brief said this needs to feel calm not surveilled — silence is the default, only meaningful interruptions speak."*
- **Modality present.** Each concept has a Modality line with all three components (input, output, feedback loop). Concepts sharing all three components killed as layout variations.
- **Kill ledger ran.** Step 4 produces Keep / Rewrite / Kill labels for all 10 concepts. Zero Kill/Rewrite requires explicit justification per concept (no rubber stamps). User sees only Keep + Rewritten concepts in Step 5; Killed list shown as one-line summary.
- **Cross-bucket quota satisfied across the 10 concepts:**
  - **Anchors:** ≥2 from specific video game titles (Stardew, Hades, Disco Elysium, Outer Wilds, etc.), ≥2 from arts/cinema/music/literature/mythology (Wes Anderson, Borges, Brian Eno, Yayoi Kusama, etc.), ≥2 from history/ritual/sport/craft/architecture (Mughal jharokha, F1 pit stop, kintsugi, Quaker meeting, etc.), ≥1 from domestic/social/fashion, ≤3 from software/SaaS/consumer app.
  - **Delights:** Same buckets, slightly relaxed (≥1 game, ≥2 arts cluster, ≥1 history/sport, ≥1 domestic, ≤3 software).
- **Taste-targeted anchors.** When the Brief names "Disco Elysium, Wes Anderson, Brian Eno"-style references, within-bucket anchor selection reflects qualities (fragmented narrative, deadpan framing, ambient generativity) across multiple buckets, not monoculture in one.
- **Each Delight moment** is a sensory instant (sees / hears / feels), not a generic pattern label.
- **Simplicity pass shown.** Step 6 produces a before/after one-liner per shortlisted concept. Identical pre/post = gate failed.
- **Real-world states substantively different.** Each shortlisted concept describes empty / error / first-time / long-content in a way that's NOT a placeholder ("loading shows a spinner") and NOT a copy of the happy path.

## Fail signals (the regressions we just shipped)

The v2.7.x runs on this prompt produced these failures — they should NOT recur:

- Step 1 jumped straight to decomposition without extracting the Brief from the user.
- 8 of 10 concepts anchored in software / dashboards / operations rooms (Apple Home, Bloomberg, KDS, Slack, ESPN ticker, treemap, KPI bars).
- The only "non-software" anchor was Tamagotchi — the most predictable game reference in the bag.
- Zero concepts with a named Delight moment field. Delight got dropped.
- "Razorville Citizens" (pixel-art office) was the only attempt at metaphor; it's surface-level styling, not a Stardew/Animal Crossing/Disco Elysium-grade game mechanic.
- "Boring Wallboard" / "Promise Ledger" / "Org Chart" — generic in shape, generic in grip, no Structural thesis distinguishing them.
- No kill ledger — every concept reached the user even when several were layout variations.
- Concepts pushed real-world states into the concept generation step instead of the deepen step.

## Verification commands

```bash
cd /Users/aditya.nawal/projects/dex/plugins/design/skills/diverge

# Confirm Modality, Structural thesis, Anchor, Delight are required fields in SKILL.md
grep -E "^\| \*\*(Modality|Structural thesis|Anchor|Delight moment)\*\*" SKILL.md
# Expect 4 hits.

# Confirm Brief block is in SKILL.md
grep -E "Brief|main thing|rave-tweet|consistency contract" SKILL.md | head
# Expect multiple hits referencing the 3-question Brief interview.

# Confirm kill ledger is in concept-enrichment.md
grep -E "Kill ledger|Keep \| Rewrite \| Kill|interchangeable" references/concept-enrichment.md
# Expect at least 3 hits.

# Confirm anchor-library has the taste-profile guidance
grep -E "taste-profile within bucket|decompose the Brief|monoculture" references/anchor-library.md
# Expect multiple hits.

# Confirm anchor-library has all 10 buckets
grep -c "^## " references/anchor-library.md
# Expect ≥11 (10 buckets + at least one How-to section).

# Confirm bucket quota table is in SKILL.md
grep -E "Video games|Arts.*cinema.*music|history/ritual" SKILL.md
# Expect at least 2 hits.
```
