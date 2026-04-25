# Fixture: agent-dashboard

A second fixture that catches the regressions found in v2.7.0 (delight dropped, anchors software-skewed). Run by hand alongside `refund-step.md`.

## Prompt

```
/diverge "Dashboard for all installed AI agents in our org. Need to see what each agent is doing, who's using it, and whether it's helping."
```

## Expected shape

A correct run produces, in order:

1. **Step 1 — Break down the problem**: 3 JTBD, real constraint, problem-elimination, similar problems in other fields.

2. **Step 2 — Surface vocabulary**: should fire on adjectives like "see what each agent is doing" — surface real references like a Slack people directory, F1 telemetry boards, a kitchen brigade station list, Stardew Valley villager status, a Pokémon team page. Mix software with non-software.

3. **Step 3 — 8-10 concepts**, each with the full template including BOTH:
   - **Anchor** field naming a real, Googleable thing the mechanic borrows from
   - **Delight moment** field naming a sensory instant + real-world reference

4. **Step 4 — Comparison table** with "How it dies" column.

5. **Step 5 — Hybrid combinations + day-in-the-life narratives + decision framework.**

6. **Step 6 — Output choice question.** Skill waits.

## Pass criteria (eyeball)

The set of 10 concepts must distribute across domain buckets like this:

**Anchors:**
- ≥2 from specific video game titles (Stardew, Hades, Disco Elysium, Animal Crossing, Outer Wilds, Death Stranding, etc.)
- ≥2 from arts / cinema / music / literature / mythology (Wes Anderson, Borges, Brian Eno, Yayoi Kusama, etc.)
- ≥2 from history / ritual / sport / craft / architecture (Mughal jharokha, F1 pit stop, kintsugi, Quaker meeting, etc.)
- ≥1 from domestic / social / fashion (family WhatsApp, barber shop, airport gate, etc.)
- ≤3 from software / SaaS / consumer app (Apple Home, Bloomberg, Slack — the lazy choices)

**Delight moments:**
- Same buckets, slightly relaxed minimums (≥1 game, ≥2 arts cluster, ≥1 history/sport, ≥1 domestic, ≤3 software).
- Each Delight moment is a sensory instant (sees / hears / feels), not a generic pattern label.

## Fail signals (the regressions we just shipped)

The v2.7.0 run on this prompt produced these failures — they should NOT recur:

- 8 of 10 concepts anchored in software / dashboards / operations rooms (Apple Home, Bloomberg, KDS, Slack, ESPN ticker, treemap, KPI bars).
- The only "non-software" anchor was Tamagotchi — the most predictable game reference in the bag.
- Zero concepts with a named Delight moment field. Delight got dropped.
- "Razorville Citizens" (pixel-art office) was the only attempt at metaphor; it's surface-level styling, not a Stardew/Animal Crossing/Disco Elysium-grade game mechanic.

## Verification commands

```bash
cd /Users/aditya.nawal/projects/dex/plugins/design/skills/diverge

# Confirm Anchor and Delight are required fields in SKILL.md
grep -E "^\| \*\*(Anchor|Delight moment)\*\*" SKILL.md
# Expect 2 hits.

# Confirm anchor-library.md exists and has all 10 buckets
grep -c "^## " references/anchor-library.md
# Expect ≥10 (buckets) + 1 (How to use this list) = 11.

# Confirm bucket quota table is in SKILL.md
grep -E "Video games \(specific titles\)|Arts / cinema / music / literature / mythology" SKILL.md
# Expect at least 2 hits.
```
