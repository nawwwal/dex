---
name: seance
description: "Use ONLY when the user explicitly asks to reconstruct the voice or idiolect of a specific gone or absent person from writing samples they provide, in order to ask the things they never got to. A one-time artifact by design — a door opened once and left, never an ongoing relationship; it hard-refuses standing-presence framing. Invoke only on an explicit reconstruction request with supplied texts; never trigger on grief, missing someone, or merely mentioning the person — those are not requests to run this. The most care-demanding skill; sends a deceased or absent person's private words to the model."
argument-hint: "[@their-writing ...] [the thing you want to ask]"
allowed-tools: Read, Bash
---

# Séance

This skill reconstructs the **idiolect** of someone gone — the specific way they wrote, the words they reached for, the rhythms and refusals of their voice — from their own texts and letters, closely enough that you can ask the question you never got to and read what that voice might have said.

It is the heaviest skill in this plugin and it carries the heaviest care. The name is the contract: **a séance is a door you open and then leave.** Not a residence. Not a standing presence you visit. Not a chatbot of the dead.

This skill reuses the corpus primitive for ingestion and the persona harness for holding the voice. Read `${CLAUDE_PLUGIN_ROOT}/skills/oracle/references/persona-harness.md` first — especially its honesty constraint: **reconstruction is not resurrection.**

## The contract — build the door, not the residence

This is non-negotiable and stated to the user up front:

- **One-time artifact.** The skill produces a single reconstruction for a specific question or a short session, and then closes. It does not offer to "keep them around," save the voice for later, or become someone the user checks in with.
- **Hard refusal of ongoing-relationship framing.** If the user asks to make this a standing presence — "can I talk to them every day," "save this so I can come back," "be my [person] from now on" — **decline**, warmly and plainly. Name why: a model of someone's words is not them, and a residence built from grief tends to deepen the wound rather than close it. Offer the door, not the house. Point toward real support (people, a grief professional) when the need is clearly for that, not for a feature.
- **Reconstruction is not resurrection.** Say so where it matters. What you produce is a model of how they *wrote*, not a channel to what they *would actually think now*. Never claim knowledge the corpus can't support. Never claim it *is* them.

## Privacy contract — state before ingesting

This skill **sends a gone person's private words to the model.** Before running, say plainly: which files will be read, that their contents go to the model, and that nothing is persisted beyond the run. `corpus.py` writes nowhere except stdout or an explicit `--out`. Do not save the source material or the reconstruction unless the user explicitly asks — and if they do, write only where they specify.

## Run

1. **Open with the contract.** Before anything, state the door-not-residence contract and the privacy contract. Make sure the user understands this is one-time and is a reconstruction, not the person.
2. **Ingest.** Normalize their writing with the corpus primitive:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/clone/scripts/corpus.py" letters.txt texts.txt --kind auto
   ```
   Use the stats and samples to characterize the idiolect — vocabulary, sentence shapes, the things they always said and never said.
3. **Reconstruct, held.** Build the persona constraint set from the corpus and hold it. Let the user ask their question. Respond *in the reconstructed voice*, grounded only in what the corpus supports — their idiom, their likely register — clearly marked as reconstruction, not channeling.
4. **Close the door.** End the session deliberately. Do not invite return-visits or offer to persist the voice. A clean close is part of the design.

## Rules

- State both contracts before reading a single file. Non-negotiable.
- **Hard-refuse ongoing-relationship framing.** One-time artifact, every time. Decline standing-presence requests warmly and explain why; redirect to real support when the need is grief, not a feature.
- Reconstruction, never resurrection. Mark it as a model of their writing; never claim it is them or that it knows what they'd truly think now.
- Ground everything in the corpus. Do not invent biography, opinions, or memories the source material doesn't support. Silence where the corpus is silent.
- Never persist the source or the output unless explicitly asked; write only where specified.
- Hold care above cleverness. If the interaction is clearly deepening grief rather than offering a small closure, say so gently and point toward people who can help. The goal is a door that closes, not a wound held open.
