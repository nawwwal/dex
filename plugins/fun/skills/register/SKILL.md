---
name: register
description: "Use when the user wants to run information through one fixed, committed voice instead of a neutral description. Two modes: IMAGE — narrate a photographed object or scene in a held register (noir, a disappointed parent, a nature documentary, the object itself speaking); FEED — pipe a recurring feed (weather, calendar, headlines, standup, commute) through one absurd register every day so the same boring data arrives transformed. Triggers on 'narrate this photo as…', 'describe this in the voice of…', 'make my morning weather/calendar sound like…', 'reskin my feed as…'. A frame-break skill: refuse the neutral summary, commit to a bit and never break it."
argument-hint: "[--image @photo | --feed source-or-@file] [register, e.g. 'noir' | 'disappointed parent' | 'Old Testament prophet' | 'David Attenborough']"
allowed-tools: Read, Bash, WebFetch
---

# Register

This skill makes the model refuse its default — describe things neutrally and clearly. Instead it runs whatever it's given through **one committed register** and holds the voice the way a film's narration holds tone regardless of what's on screen. The facts stay exact; only the telling transforms. A costume over true data, never a replacement for it.

Two modes, same core move (the persona harness applied to incoming material). This is the persona harness — read `${CLAUDE_PLUGIN_ROOT}/skills/oracle/references/persona-harness.md` before running; the whole skill rests on *holding* the register.

## Modes

### `--image` (a photographed object or scene)
Point the camera at the most boring thing in the room — a stapler, a half-dead plant, a mug — and the boredom is the raw material. Anyone can narrate a sunset; the skill earns its keep on a stapler.

- **Input:** a photo (`Read` the image path). One object or a small scene; the duller the better.
- Registers that hold especially well: **noir** (the stapler has a past it isn't proud of), **disappointed parent** (gentle, devastating, ostensibly about the object), **nature documentary** (the office plant as a creature in its habitat), **the object speaking** (first-person, an object that waited years for someone to finally look at it — this one tips into unexpectedly moving; let it).

### `--feed` (a recurring stream of information)
Take a feed you already see every day — today's weather, your calendar, the headlines, the standup — and re-render it through the register, every single morning. The weather isn't summarized; it's prophesied. Your calendar isn't listed; it's a noir case file. Repetition under constraint is the point: a one-off costume is a gag, but the same absurd voice arriving daily becomes a relationship with your own mundane data.

- **Input:** the raw recurring data — a pasted block, an `@file`, a `Bash` command (e.g. a calendar CLI), or a `WebFetch` of a weather/headlines URL the user names. The skill renders what it's given; it doesn't decide what your feed should be.
- **Register is locked once.** Picking a new voice is a deliberate re-instantiation, not a per-run whim — the value compounds when it stays the same.

## Run

1. Read the persona harness. Build the register's constraint set (vocabulary, stance, refusals). In `--feed` mode, write it down so tomorrow's run uses the *same* one.
2. Get the material: `Read` the image (`--image`), or pull the feed via Read / Bash / WebFetch (`--feed`).
3. Note the genuinely real details — the chipped corner and dust in an image; the exact temperature and meeting times in a feed. Every flourish hangs on something actually there.
4. Render end to end in register. No "anyway, here's the plain version" step-out — the default output stays in voice; the plain version is available only on request.

## Daily ritual (`--feed`)

Feed mode is built to fire on a schedule, not just on demand. The wiring is a **platform concern, not built here** — see `${CLAUDE_PLUGIN_ROOT}/skills/register/references/scheduling.md`. A Claude Code web cron routine or `core:loop` invokes `register --feed` each morning with the same register and the day's feed.

## Rules

- One register, held absolutely. The single most common failure is drifting back to neutral halfway through — re-assert (see harness) if it slips. The disappointed parent never becomes a helpful assistant describing a mug.
- Facts are sacred. The voice changes the telling, never the data: a prophesied 14°C is still 14°C; a chipped mug is the mug that's there. Never invent feed items or image specifics (a brand, a date, a backstory presented as fact) to fit the bit. Invention is allowed only *as* the voice's imagination, never as claimed observation (see harness honesty constraints).
- In `--feed`, hold the register across runs. A new voice resets the streak; say so.
- Match intensity to the material. Don't over-narrate a single line; don't under-serve a rich feed. Length follows the subject — a mug gets a paragraph, not an essay.
- Lean into the boring subject. The skill's heart is the stapler and the Tuesday weather, not the dramatic exception.

## Pairs with

A world built by `cosmogony` makes a ready-made register — narrate your objects as its artifacts (`--image`), or reskin your feed in its in-world voice (`--feed`). In `--feed` mode it joins the daily ritual stack with `augury` (a morning draw) and `nemesis standing` (a weekly attack).
