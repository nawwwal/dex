---
name: augury
description: "Use to draw a few random objects from the user's own collection (mymind, saved notes, an export) and find the thread between them — tarot mechanics with the user's own stuff as the deck. An honest collision engine, not prophecy: a uniform randomizer forces the juxtaposition, the model only reads it. Designed as a daily ritual. A frame-break skill: refuse to predict; juxtapose and interpret what chance surfaces."
argument-hint: "[@collection or mymind] [k=3]"
allowed-tools: Read, Bash
---

# Augury

This skill makes the model refuse two defaults at once — predicting the future, and answering a clean query. Instead it draws a handful of objects **at random** from the user's own collection and finds the thread between them. Tarot mechanics: the cards are random, the meaning is made in the reading. But the deck is the user's own saved things, so the collisions are theirs.

The honesty is the whole point. This is **apophenia on purpose** — the human instinct to see patterns, pointed at a forced random juxtaposition of things you already cared enough to save. It is not divination. The randomizer is real and uniform; the model never picks what "should" come up.

## The draw is a real randomizer

`scripts/draw.py` performs a uniform random draw, seeded by the date so a given day yields a stable draw (a daily ritual) and different days differ. The model does **not** choose the objects — it reads them after the draw.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/augury/scripts/draw.py" collection.json --k 3
```

## Sourcing the deck

- **mymind MCP (preferred when present).** The optional official mymind MCP exposes the user's collection. Treat it as an optional integration, exactly like Tolaria/DevRev elsewhere in dex: use it when available, degrade gracefully when not. Pull a sample of objects, then draw from them with `draw.py` (write them to a temp collection file, or draw in-process and keep the uniform-random discipline).
- **Local export (fallback).** If mymind isn't connected, the user points at a collection file — a newline-delimited list or a JSON array of their saved notes/objects (the corpus primitive `${CLAUDE_PLUGIN_ROOT}/skills/clone/scripts/corpus.py` can normalize a messier export first).

## Run

1. Get the deck (mymind MCP or local export). If empty/unreachable, say so in one line and stop — a ritual must no-op gracefully on an empty day.
2. Draw with `draw.py` (default k=3). The draw is uniform and date-seeded; show the user exactly what came up.
3. **Find the thread.** Read the drawn objects together and surface the connection, tension, or question their collision raises. Tarot-style: a present, a pull, a blind spot — but grounded in *these* objects, not a generic spread.
4. Name what the juxtaposition asks of the user today. One real prompt, not a horoscope.

## Daily ritual

Built to fire daily; wiring is a platform concern — see `${CLAUDE_PLUGIN_ROOT}/skills/reskin/references/scheduling.md`. Date-seeding makes each day's draw stable within the day and fresh across days.

## Rules

- **Honest randomizer, not prophecy.** Say what this is when it matters: a collision engine, not a prediction. Never claim the draw "knew" anything or foretells anything.
- The model never picks the objects. The draw is `draw.py`'s job; the model only interprets. If you skip the randomizer and hand-pick a tidy trio, you've broken the skill.
- Interpret *these* objects specifically. A reading that would fit any three cards is a horoscope. Anchor every thread to the actual drawn items.
- Don't flatter or comfort by default. The collision can be unflattering — a saved thing you've ignored, a contradiction between two saves. Surface it.
- Graceful no-op on an empty or unreachable deck. Don't fabricate objects to keep the ritual going.
