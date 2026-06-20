---
name: arena
description: "Use to study emergent social norms by running a population of LLM-authored temperaments through an iterated game on a deterministic engine, then evolving strategies across generations and reading the norms that emerge — reputation, grudges, retaliation, forgiveness, stable cooperation or collapse. A frame-break skill: refuse the single optimal answer; watch a society of strategies discover its own rules. The model authors the minds; Python plays the rounds."
argument-hint: "[game: ipd] [agents N] [generations G]"
allowed-tools: Read, Write, Bash
---

# Arena

This skill makes the model refuse its default — reason about a game as one optimizer looking for the best move. Instead it populates a world with **many temperaments**, lets a deterministic engine play them against each other, and reads the **norms that emerge** from the population: who gets a reputation, who holds grudges, who forgives, whether cooperation stabilizes or collapses into mutual defection.

The division of labor is the whole design. **The model authors the minds** — distinct temperaments described in natural language and encoded as strategy specs. **Python plays the rounds** — `scripts/arena.py`, deterministic and seedable, so the dynamics are real consequences of the strategies, not a story the model talked itself into. Then the model **reads the results and evolves** the next generation.

The generational loop is the iteration harness. Read `${CLAUDE_PLUGIN_ROOT}/skills/gravity/references/iteration-harness.md` — here the "transform" is one generation (play + evolve) and the attractor is an emergent social norm.

## The engine

`scripts/arena.py` runs **one generation** (a full round-robin tournament) and emits metrics. Strategy specs are structured JSON the model authors (full schema in the script header). Each agent has an opening move, ordered condition→action rules over per-opponent memory (`opp_last`, `betrayed`, `opp_defect_rate`, `opp_reputation`, `round`, `first_meeting`), and a default. Conditions are data, never `eval`'d.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/arena/scripts/arena.py" \
  --strategies agents.json --rounds 20 --seed 7 --out gen1.json
```

`strategies.example.json` ships six classic temperaments (Saint, Defector, TitForTat, Grudger, ForgivingTFT, Suspicious) — use it to smoke-test, then author your own.

The default game is iterated prisoner's dilemma — the cleanest substrate for reputation and reciprocity. The engine is structured for richer games (ultimatum haggling, gossip/reputation nets, heist-with-ratting); when you add one, keep the same contract: deterministic engine, model-authored strategies, metrics the model reads.

## Run

1. **Author the population.** Write `agents.json` — N distinct temperaments (default 6; keep small, every move is real compute downstream). Each gets a natural-language temperament *and* an encoded rule set. Make them genuinely different: a forgiver, a grudge-holder, a probe, a zealot.
2. **Play a generation.** Run the engine with a fixed seed. Read the results: ranking, per-agent score and cooperation rate, and the `norms` block (overall cooperation, mutual-cooperation moves, retaliations, forgiveness events).
3. **Read the norms.** What stabilized? Did reciprocity win? Did one defector poison the well? Did a reputation system effectively punish betrayal? Name the *emergent* social fact, not just the leaderboard.
4. **Evolve.** Author the next generation informed by what happened — strategies that exploit the incumbents, or that the incumbents failed to handle. Re-run. Continue until norms stop shifting (a stable equilibrium or a stable cycle of regime changes) or for the requested G generations (default 3; small).
5. **Report the trajectory of norms** across generations — the society's history, not just its final state.

## Rules

- The engine is the source of truth. Never narrate dynamics you didn't run. If you claim cooperation collapsed, the metrics must show it.
- Keep N and G small by default (6 agents, 3 generations). This is a real tournament times real generations; respect the cost.
- Temperaments must be genuinely distinct and genuinely encoded — a population of near-identical TitForTats teaches nothing. Variety is the experiment.
- Read *emergent norms*, not just winners. "TitForTat topped the board" is a result; "reciprocity plus a clean-reputation second chance suppressed defection until a probe exploited the forgivers" is a norm.
- Use a fixed seed per generation so results are reproducible and the evolution is honest.
- Author strategies as the documented spec; don't hand the engine free-form prose it can't execute.
