---
name: cartography
description: "Use when the user explicitly supplies a chat-history export and asks to map or analyze the relationship in it — who initiates, how in-jokes evolve, where the temperature spikes, the words that exist only between these two people, the rhythms of silence and repair — including the unflattering read, not just the warm one. Invoke only on an explicit request to map/analyze a supplied conversation export; it sends the user's private conversation to the model, so do not trigger on a casual mention of a friendship or person. A frame-break skill: refuse the flattering summary; map an intimacy honestly."
argument-hint: "[@chat-export] [other person's name]"
allowed-tools: Read, Bash
---

# Cartography

This skill makes the model refuse its default — the warm, flattering summary ("you two have such a special bond!"). Instead it reads a chat history as terrain and maps its **shape**: who reaches first, how the in-jokes mutated, where the temperature spiked and cooled, the private vocabulary that exists nowhere else, the patterns of silence and repair. A friendship has a structure, and the structure is legible in the logs.

The honest version includes the parts a greeting card omits. An intimacy map that only flatters is worthless — it tells you what you wanted to hear. The skill must surface the asymmetries too: who carries the thread, who lets it drop, whose bids go unanswered.

This skill reuses the corpus primitive for ingestion. Read `${CLAUDE_PLUGIN_ROOT}/skills/clone/scripts/corpus.py` usage.

## Privacy contract — state this before ingesting

This skill **sends a private conversation to the model.** Before running, say plainly: which export will be read, that its contents go to the model, and that nothing is persisted beyond the run unless the user asks. `corpus.py` writes nowhere except stdout or an explicit `--out`. Do not save the export or the map to disk unless asked. The other person did not consent to analysis — keep the read for the user's own understanding, not for ammunition.

## Ingest

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/clone/scripts/corpus.py" chat-export.txt --kind chat
```

It detects common export formats (WhatsApp-style lines, JSON arrays, generic `Name: text`) and returns normalized messages plus per-author stats (message counts, average length, vocabulary). Use the stats as evidence, not decoration.

## Map these dimensions

- **Initiation balance** — who starts conversations, who responds. Asymmetry is signal.
- **Temperature** — where intensity, warmth, conflict, or distance spike across time. Name the inflection points.
- **In-joke evolution** — a phrase's first appearance, how it mutated, what it stands in for now.
- **Private lexicon** — words and constructions that exist only between these two. The dialect of the relationship.
- **Silence and repair** — the gaps, who breaks them, how ruptures get mended (or don't).
- **Rhythm** — the cadence: rapid-fire vs. slow burn, daily vs. seasonal.

## Report

- **The shape** — the relationship's structure in plain language, anchored to specific messages and the corpus stats.
- **The unflattering read** — mandatory. The asymmetry, the unanswered bids, the place one person performs and the other manages, the in-joke that's become a wall. State it with care but state it. If you genuinely find none, say what you looked for and why it's clean — don't skip the section.

## Rules

- State the privacy contract before reading anything. Non-negotiable.
- **Always produce the unflattering read.** A map that only flatters is the failure mode this skill exists to refuse. (No-flattery guardrail.)
- Anchor every claim to evidence — a quoted message, a stat, a dated shift. No vibes presented as findings.
- Never persist the export or the map unless asked. Write only where the user specifies.
- This is the user's own understanding of their relationship, not a dossier on the other person. Don't produce leverage, scorekeeping, or "who's right" verdicts.
- Hold care and honesty together. The unflattering read is delivered to help, not to wound.
