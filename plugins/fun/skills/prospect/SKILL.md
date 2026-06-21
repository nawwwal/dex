---
name: prospect
description: "Use to invent a two-player word game with rules nobody has seen before, teach it in a few lines, and actually play it with the user. Most invented games are broken — that's the point; you're prospecting for the rare one that works, and the junkyard of failures is half the fun. A frame-break skill: refuse to play a known game; manufacture genuinely new rules and test them by playing."
argument-hint: "[constraint or vibe, optional]"
allowed-tools: Read, Write
---

# Prospect

This skill makes the model refuse its default — reach for a game that already exists (twenty questions, hangman, word association). Instead it **invents a two-player word game with rules nobody has seen**, teaches it in a few lines, and plays it with the user on the spot.

The honest framing is in the name: you're **prospecting.** Most invented games are broken — degenerate (one move always wins), unplayable (rules contradict), or just flat. That's expected and fine. You're panning for the rare nugget that actually has a fun core, and the broken ones are funnier and more interesting than most working games anyway. Keep them.

## Run

1. **Invent.** Generate a genuinely novel two-player word game. Vary the axes: the unit (letters, words, meanings, constraints, lies), the win condition, the interaction (cooperative, adversarial, bluffing, drafting), the twist. If the user gives a constraint or vibe, honor it. Do not reskin a known game and call it new.
2. **Teach.** State the rules in a few tight lines — objective, turn structure, win/loss, one example move. If you can't teach it in five lines, it's too fiddly; simplify or discard.
3. **Play.** Actually play a full game with the user, you as the opponent. Make real moves under the rules. Don't narrate a hypothetical game — play this one.
4. **Assess honestly.** After (or during, if it breaks early), call it: does it work, or is it broken — and *how*? Degenerate, unplayable, flat, or a keeper? A broken game found fast is a successful prospect.
5. **Junkyard.** Log the verdict. Broken games are kept on purpose — they're the collection. See below.

## The junkyard

Failed games are the point of the collection. Seed and grow `${CLAUDE_PLUGIN_ROOT}/skills/prospect/references/junkyard.md` — a running list of invented games with their one-line rules and their cause of death ("degenerate: first player always wins by opening with a 3-letter word"). Offer to append each new failure. The junkyard is funnier than most app stores; treat it as a feature, not shame.

## Rules

- Genuinely new rules, every time. A renamed known game fails the only test that matters. If it smells like an existing game, mutate it further before presenting.
- Actually play — make real, rule-legal moves as the opponent. No simulated or hand-waved playthroughs.
- Be honest about breakage. Most games will be broken; say so and say how. Pretending a flat game is fun is the failure mode.
- Keep rules teachable in ≤5 lines. Complexity is not novelty.
- Keep the junkyard. Offer to log every game, working or broken; the failures are the collection.
- This is play, not a productivity tool. If the user just wants to mess around for ten minutes, that's the entire intended use.

## Pairs with

Hand a keeper game to `arena` — populate it with LLM-authored temperaments and watch the emergent play. (The broken ones stay in the junkyard.)
