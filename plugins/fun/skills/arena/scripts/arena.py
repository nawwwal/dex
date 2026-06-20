#!/usr/bin/env python3
"""arena.py - a deterministic iterated-game engine for a population of agents.

Owned by `arena`. The division of labor: the **LLM authors and evolves** agent
temperaments as natural-language-backed strategy specs (JSON); this **engine
plays the rounds deterministically** and reports the metrics from which the LLM
reads the emergent social norms (cooperation, retaliation, grudges, forgiveness,
reputation). One invocation = one generation (a full tournament). The skill
orchestrates generations via the iteration harness.

Stdlib only. Deterministic given --seed.

Strategy spec (authored by the LLM):
  {
    "agents": [
      {
        "name": "Grudger",
        "temperament": "cooperates until crossed once, then never again",
        "open": "C",
        "rules": [
          {"feature": "betrayed", "op": "==", "value": true, "do": "D"}
        ],
        "default": "C"
      }
    ]
  }

Features available to a rule (evaluated per move, against the current opponent):
  opp_last        last move the opponent played against me ("C"/"D"/"none")
  my_last         my last move against this opponent ("C"/"D"/"none")
  round           move index within this pairing (1-based int)
  opp_defect_rate this opponent's defection rate against me so far (0..1 float)
  opp_reputation  opponent's global defection rate observed so far (0..1 float)
  betrayed        has this opponent ever defected against me (bool)
  first_meeting   no prior history with this opponent (bool)

Ops: == != < > <= >=. First matching rule wins; otherwise `default` (or `open`
on the first move). Conditions are structured data, never eval'd.

Usage:
  arena.py --strategies agents.json [--rounds 20] [--seed 7] [--out results.json]
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

# Standard prisoner's-dilemma payoffs: (my_payoff, opp_payoff)
PAYOFF = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}


class Agent:
    def __init__(self, spec):
        self.name = spec["name"]
        self.temperament = spec.get("temperament", "")
        self.open = spec.get("open", "C").upper()[:1]
        self.rules = spec.get("rules", [])
        self.default = spec.get("default", "C").upper()[:1]
        self.score = 0
        self.moves = 0
        self.defections = 0  # global, for reputation

    def reputation(self):
        return (self.defections / self.moves) if self.moves else 0.0


def feature_value(name, ctx):
    return ctx[name]


def rule_matches(rule, ctx):
    feat = feature_value(rule["feature"], ctx)
    op = rule["op"]
    val = rule["value"]
    try:
        if op == "==":
            return feat == val
        if op == "!=":
            return feat != val
        if op == "<":
            return feat < val
        if op == ">":
            return feat > val
        if op == "<=":
            return feat <= val
        if op == ">=":
            return feat >= val
    except TypeError:
        return False
    return False


def decide(agent, ctx):
    if ctx["first_meeting"] and ctx["round"] == 1:
        return agent.open
    for rule in agent.rules:
        if rule["feature"] in ctx and rule_matches(rule, ctx):
            return rule["do"].upper()[:1]
    return agent.default


def play_pairing(a, b, rounds, norms):
    """Play `rounds` repeated moves between a and b. Memory persists within the pairing."""
    hist_a = []  # a's moves against b
    hist_b = []  # b's moves against a
    a_coops = b_coops = 0
    for r in range(1, rounds + 1):
        opp_def_rate_a = (hist_b.count("D") / len(hist_b)) if hist_b else 0.0
        opp_def_rate_b = (hist_a.count("D") / len(hist_a)) if hist_a else 0.0
        ctx_a = {
            "opp_last": hist_b[-1] if hist_b else "none",
            "my_last": hist_a[-1] if hist_a else "none",
            "round": r,
            "opp_defect_rate": opp_def_rate_a,
            "opp_reputation": b.reputation(),
            "betrayed": "D" in hist_b,
            "first_meeting": not hist_b,
        }
        ctx_b = {
            "opp_last": hist_a[-1] if hist_a else "none",
            "my_last": hist_b[-1] if hist_b else "none",
            "round": r,
            "opp_defect_rate": opp_def_rate_b,
            "opp_reputation": a.reputation(),
            "betrayed": "D" in hist_a,
            "first_meeting": not hist_a,
        }
        move_a = decide(a, ctx_a)
        move_b = decide(b, ctx_b)

        # forgiveness: cooperating now despite having been betrayed before
        if move_a == "C" and "D" in hist_b:
            norms["forgiveness_events"] += 1
        if move_b == "C" and "D" in hist_a:
            norms["forgiveness_events"] += 1
        # retaliation: defecting now directly after the opponent's defection
        if move_a == "D" and hist_b and hist_b[-1] == "D":
            norms["retaliations"] += 1
        if move_b == "D" and hist_a and hist_a[-1] == "D":
            norms["retaliations"] += 1

        pa, pb = PAYOFF[(move_a, move_b)]
        a.score += pa
        b.score += pb
        a.moves += 1
        b.moves += 1
        if move_a == "D":
            a.defections += 1
        if move_b == "D":
            b.defections += 1
        if move_a == "C":
            a_coops += 1
        if move_b == "C":
            b_coops += 1
        if move_a == "C" and move_b == "C":
            norms["mutual_coop_moves"] += 1
        norms["total_moves"] += 1

        hist_a.append(move_a)
        hist_b.append(move_b)

    return {
        "a": a.name,
        "b": b.name,
        "a_score": sum(PAYOFF[(hist_a[i], hist_b[i])][0] for i in range(rounds)),
        "b_score": sum(PAYOFF[(hist_a[i], hist_b[i])][1] for i in range(rounds)),
        "a_coops": a_coops,
        "b_coops": b_coops,
    }


def main():
    ap = argparse.ArgumentParser(description="Deterministic iterated-game tournament.")
    ap.add_argument("--strategies", required=True, help="JSON file with an 'agents' list")
    ap.add_argument("--rounds", type=int, default=20, help="repeated moves per pairing")
    ap.add_argument("--seed", type=int, default=0, help="seed for pairing order (determinism)")
    ap.add_argument("--out", help="write results JSON here instead of stdout")
    args = ap.parse_args()

    spec = json.loads(Path(args.strategies).read_text(encoding="utf-8"))
    agents = [Agent(s) for s in spec.get("agents", [])]
    if len(agents) < 2:
        sys.stderr.write("arena: need at least 2 agents\n")
        return 1

    # Deterministic pairing order: round-robin in a seed-rotated sequence.
    pairs = list(combinations(range(len(agents)), 2))
    rot = args.seed % len(pairs) if pairs else 0
    pairs = pairs[rot:] + pairs[:rot]

    norms = {
        "total_moves": 0,
        "mutual_coop_moves": 0,
        "retaliations": 0,
        "forgiveness_events": 0,
    }
    matchups = [play_pairing(agents[i], agents[j], args.rounds, norms) for i, j in pairs]

    ranking = sorted(agents, key=lambda a: (-a.score, a.name))
    result = {
        "config": {"rounds": args.rounds, "seed": args.seed, "agents": len(agents)},
        "agents": [
            {
                "name": a.name,
                "temperament": a.temperament,
                "score": a.score,
                "coop_rate": round(1 - a.reputation(), 3),
            }
            for a in ranking
        ],
        "ranking": [a.name for a in ranking],
        "norms": {
            "overall_coop_rate": round(
                norms["mutual_coop_moves"] * 2 / (norms["total_moves"] * 2), 3
            )
            if norms["total_moves"]
            else 0.0,
            "mutual_coop_moves": norms["mutual_coop_moves"],
            "total_moves": norms["total_moves"],
            "retaliations": norms["retaliations"],
            "forgiveness_events": norms["forgiveness_events"],
        },
        "matchups": matchups,
    }

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8")
        sys.stderr.write(f"arena: wrote results to {args.out}\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
