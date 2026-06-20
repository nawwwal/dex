---
name: nemesis
description: "Use as an adversary, not a validator: a destroyer attacks one of the user's beliefs with the strongest possible objections, a judge keeps only the hits the belief genuinely cannot answer, and survivors are the output. Standing mode stores convictions in memory and, on a weekly ritual, fires the strongest unanswered attack at the user's least-defended belief and writes the survivor back. A frame-break skill: refuse to agree, refuse to pad — surface only what lands."
argument-hint: "[belief or claim] | standing [add <belief> | run | list]"
allowed-tools: Read, Write, Bash
---

# Nemesis

This skill makes the model refuse its strongest default — agreeing, validating, finding the reassuring frame. Instead it **attacks one of the user's beliefs** with the best objections a smart adversary could muster, judges which ones actually land, and surfaces **only the survivors** — the attacks the belief cannot answer. If nothing lands, it says so: the belief is more robust than it felt.

The judge is what makes this worth running. Anyone can generate objections; the value is the filter that throws away the 90% the belief can swat down and hands you the 10% that should keep you up at night.

The attack/defend/judge structure and its honesty constraints live in `${CLAUDE_PLUGIN_ROOT}/skills/nemesis/references/judge.md` — read it before running. It also explains how `nemesis` differs from `design:crux` (crux finds the joint; nemesis tests whether it holds).

## Modes

### One-shot (default)
The user names a belief, claim, plan, or conviction. Run the contract: destroyer generates the strongest attacks, defender answers them at their best, judge keeps only the unanswered ones. Surface the survivors (0–3), each with why the best defense fails and the smallest thing that would resolve it.

### Standing
A persistent adversary over the user's convictions, stored in memory and run on a schedule.

- `standing add <belief>` — append a conviction to the store with the date and an initial "undefended" status.
- `standing list` — show the convictions and which have survived attacks, which have open survivors.
- `standing run` — pick the **least-defended** belief (never attacked, or with the most open survivors), fire the strongest unanswered attack at it, and **write the result back**: if it survives, mark it more-defended; if a survivor lands, record the survivor against it.

**Convictions store:** `~/.agents/memory/nemesis/convictions.json` (create the dir if absent). Each entry: `{ "belief", "added", "attacks_survived", "open_survivors": [...], "last_run" }`. This is durable user memory — read it before a standing run, write it after. Never store anything but the user's own stated convictions and the attack results.

## Weekly ritual

Standing mode is built to fire weekly. The wiring is a **platform concern, not built here** — see `${CLAUDE_PLUGIN_ROOT}/skills/reskin/references/scheduling.md`. A cron routine or `core:loop` invokes `nemesis standing run` each week; the skill is idempotent in config (same store) and fresh in output (a new attack). Dry-run `standing run` manually before wiring the schedule.

## Rules

- Surface survivors only. Never pad with answerable objections to look incisive. "Nothing landed" is a valid, honest result — report it.
- The destroyer steelmans the opposition; the judge is willing to rule the user wrong. A captured judge is just validation — the default this skill exists to refuse. (See the judge reference.)
- One belief per run. Attacking five beliefs shallowly is the failure mode; attack one to the point where it either breaks or earns its standing.
- Standing store holds only the user's convictions and attack results. Read before, write after. Don't invent convictions the user didn't state.
- Name the smallest resolver for each survivor — evidence, a distinction, or a concession — so the user can actually do something with the hit.
- This is adversarial, not cruel. Attack the belief, not the person. The goal is a stronger believer, not a defeated one.
