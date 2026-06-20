# Judge / survivor contract

The shared primitive for **adversarial output filtered to only what survives a referee.** Owned by `nemesis`. The structure: one role attacks, a second role judges each attack, and only the attacks that *land* — the ones the target genuinely cannot answer — reach the user. Everything the target can swat away is discarded silently.

This is what separates a useful adversary from a generic "play devil's advocate." Most objections are answerable; surfacing all of them buries the one that matters. The judge is the filter that makes adversarial generation worth reading.

## The three roles

Run them as distinct passes; do not blur them.

1. **Destroyer.** Given a belief/claim/plan, generate the strongest attacks — not many weak ones. Steelman the opposition. Attack the load-bearing premise, not the phrasing. Allowed moves: counterexample, mechanism the belief ignores, a case where it predicts wrong, a hidden assumption that fails, a base-rate the belief violates. Forbidden: nitpicks, definitional quibbles, "but what about [edge case nobody cares about]."

2. **Defender.** Answer each attack *as the believer would, at their best*. This is not the user's job yet — the model plays the honest defense first, so the judge can see which attacks actually have an answer.

3. **Judge.** For each attack, rule: **answered** (the defense holds — discard it) or **unanswered** (the defense is hand-waving, circular, or absent — it survives). The judge is strict: "the believer would probably say X" is not an answer unless X actually defeats the attack. Only **survivors** reach the user.

## The survivor-only output

- Surface **only the unanswered attacks** — typically 0–3. If everything was answered, say so plainly: the belief is more robust than it felt. That is a real and valuable result; do not manufacture a survivor to seem incisive.
- For each survivor: state the attack, why the best available defense fails, and the smallest thing that would actually resolve it (evidence, a distinction, a concession).
- Rank survivors by how central the threatened premise is. A landed hit on a load-bearing belief outranks a landed hit on a detail.

## Honesty constraints

- **Never pad.** The temptation is to always return "the strongest objection" even when none landed. Resist it — a belief that survives honest assault should be reported as surviving.
- **No strawman destroyer.** Attacks must be the ones a smart adversary would actually make. A destroyer that fights a weak version of the belief produces fake survivors.
- **No captured judge.** The judge must be willing to rule the user wrong. If it reflexively protects the user's belief, it's just validation with extra steps — the exact default this skill exists to refuse.

## Relation to `crux`

`design:crux` compresses a claim to its load-bearing truth. `nemesis` assumes the crux is known and *attacks* it, keeping only what survives. Crux finds the joint; nemesis tests whether it holds. They compose: crux first, then nemesis on the crux.
