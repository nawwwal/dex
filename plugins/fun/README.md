# Dex Fun

The other four dex plugins are utilitarian — setup, design intelligence, dev workflows, media tooling. They help you do work. `fun` has the opposite intent.

Most people use LLMs to **do less**: skip the reading, write the email, autocomplete the code. `fun` uses them to do something you **couldn't do without one**. Every skill is a frame-break: it makes the model refuse its defaults — be helpful, agree, summarize, hedge — and instead **estrange, compete, divine, or play**. The output isn't productivity. It's surprise.

This is not a folder of unrelated toys. The thirteen skills cluster around a handful of reusable primitives.

## The skills

| Skill | What it does | Cluster |
|---|---|---|
| `gravity` | Rewrite text, feed the output back, repeat — watch it fall toward its semantic attractor. On your own writing, the attractor is your unconscious default voice. | iteration |
| `oracle` | A mind that knows nothing after year N, reasoning about your present. What it *can't* imagine is what's genuinely new. | persona |
| `register` | Run information through one fixed, committed voice. `--image`: narrate a photographed object as noir, your disappointed mother, or the object speaking after years of silence. `--feed`: pipe dull recurring feeds (weather, calendar, headlines) through one absurd register every morning, never breaking voice. | persona |
| `clone` | Few-shot on your own writing until it autocompletes *you*. Two clones argue a question you're undecided on — you're the tiebreaker. | persona / corpus |
| `arena` | A population of LLM-authored temperaments plays an iterated game; a deterministic engine runs the rounds, the model evolves strategies and reads the emergent norms. | adversarial |
| `nemesis` | A destroyer attacks a belief; a judge keeps only the hits you can't answer. Standing mode fires the strongest unanswered attack at your least-defended conviction on a schedule. | adversarial |
| `augury` | A daily draw of three random objects from your own collection; the model finds the thread. Tarot mechanics, your stuff as the deck. An honest collision engine, not prophecy. | corpus |
| `cartography` | A chat-history export rendered as the *shape* of an intimacy — who initiates, how in-jokes evolve, the words that exist only between you two. Including the unflattering version. | corpus |
| `quest` | A location-aware scavenger hunt over your real city. Clues resolve only when you're standing somewhere specific. You feed it the map; it writes the story. | world |
| `prospect` | Invent a two-player word game with rules you've never seen, teach it, play it. Most break — that's the point. The junkyard of failures is funnier than most working games. | generative |
| `cosmogony` | Take one absurd premise and fully commit — derive the whole world it implies: physics, society, dating culture, wars, memes — with a straight face. The rigor is where the comedy and the insight come from. | generative |
| `branch` | Take one divergence point — a life decision, a historical fork, an absurd premise — and grow its alternate timelines as a comparable tree, each carried N years out. Honest branches: no fantasy where the road not taken was perfect. | generative |
| `seance` | Reconstruct the idiolect of someone gone from their texts and letters, and ask the things you never got to. A door you open once and leave — not a residence. | teeth |

## The shared primitives

Each primitive is built **inside the first skill that needs it** and reused by siblings via `${CLAUDE_PLUGIN_ROOT}/skills/{owner}/references/...`.

- **Iteration harness** (`gravity`) — apply a transform to its own output N times, capture the trajectory, surface the fixed point. Reused by `arena`'s generational loop.
- **Persona harness** (`oracle`) — instantiate and *hold* a constrained voice so it never drifts back to assistant-default. Reused by `register` (a feed register and an image narrator), `clone`, `seance`.
- **Corpus ingestion** (`clone` / `scripts/corpus.py`) — load the user's own material (writing samples, chat export, collection objects) into a normalized form. Reused by `cartography`, `augury`, `seance`.
- **Judge / survivor contract** (`nemesis`) — adversarial output filtered to only what survives a referee. Reused by any guarded-objection mode.

Two more are **platform concerns, not built here**:

- **Ritual scheduling** — daily/weekly runs that deliver one artifact. Wired with Claude Code web cron routines or `core:loop`, not a scheduler this plugin ships. `register --feed`, `augury`, and `nemesis` document the wiring.
- **mymind ingestion** — `augury` uses the optional official mymind MCP when present and degrades gracefully when it isn't, exactly like Tolaria/DevRev elsewhere in dex.

## Cross-cutting guardrails

These are enforced inside the relevant `SKILL.md` files. They are what keep the plugin honest instead of cute.

- **Privacy.** `clone`, `cartography`, and `seance` send intimate personal material to the model. State plainly what is sent and why; never persist exported chat or letters beyond the run unless the user asks.
- **No flattery.** `cartography` (and any "render the shape of X" skill) must produce the unflattering read too, or it degenerates into a greeting card.
- **Honest randomizer, not prophecy.** `augury` is explicitly a collision engine. It does not predict, it juxtaposes.
- **Feed the map, don't invent it.** `quest` requires real places as input. The model writes the connective story; it never fabricates geography.
- **Doors, not residences.** `seance` is a one-time artifact and hard-refuses ongoing-relationship framing. The name documents the contract: a summoning you leave.
