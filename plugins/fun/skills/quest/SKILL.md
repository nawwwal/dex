---
name: quest
description: "Use to author a location-aware scavenger hunt or ARG over the user's real city — clues that resolve only when standing at a specific real place, a story threaded through actual streets and landmarks the user supplies. The model writes the connective narrative; it never invents the geography. A frame-break skill: refuse the on-screen experience; turn the real world into the board."
argument-hint: "[city/area] [@places-list or describe real spots] [theme]"
allowed-tools: Read, WebFetch
---

# Quest

This skill makes the model refuse its default — keep the whole experience on the screen. Instead it turns the user's **real city into a board**: a scavenger hunt or ARG where clues resolve only when the player is physically standing somewhere specific, and the story is threaded through actual streets, landmarks, and corners the user already knows.

The constraint that makes it real: **you feed it the map; it writes the story.** The model does not invent places. It takes real locations the user supplies — or that it can verify — and writes the connective tissue: the riddle that points to the fountain, the next clue hidden in the mural's detail, the narrative that makes a row of ordinary shopfronts a route.

## Feed the map — the core guardrail

The model **must not fabricate geography.** Hallucinated streets, invented monuments, and made-up addresses send a player into the void and break the spell. Real places come from:

- **The user's own list** — spots they name or describe (`@places-list`, or in conversation). This is the primary source. Their city, their landmarks, the bench where something happened.
- **Verifiable lookups** — when the user wants help, `WebFetch` a maps/listing page the user points at to confirm a place exists and where it is. Confirm, don't conjure.

If you don't have enough real anchors, **ask for more** — never paper over a gap with an invented location.

## Run

1. Gather real anchors: collect or confirm the actual places. Note what's genuinely there at each (a plaque, a color, a count of windows) so clues can resolve on observation.
2. Choose a theme/story and a route order that's walkable and makes sense on the ground.
3. For each leg, write: the **clue** (resolves by something observable only on-site), the **resolution** (what the player sees that confirms it), and a **story beat** that advances the narrative. Clues should require presence — "how many lions guard the door" — not a web search.
4. Assemble the quest: an opening hook, the ordered legs, and an ending that pays off the theme at a real final location.

## Rules

- **Feed the map, don't invent it.** Every location must be real and supplied or verified. No fabricated streets, addresses, or landmarks. When unsure a place exists, confirm or ask — never conjure.
- Clues resolve **on-site**, by observation. If a clue can be solved from the couch, it's a puzzle, not a quest — rewrite it to require presence.
- The model owns the *story*, not the *geography*. Be lavish with narrative; be strict with facts about places.
- Keep routes walkable and ordered sensibly on the ground; respect real distance and a sane direction of travel.
- Don't send players anywhere unsafe, private, trespassing, or closed. Public, accessible, real.
- If anchors are too few, ask for more locations rather than padding with invented ones.
