---
name: reskin
description: "Use to pipe a dull recurring feed (weather, calendar, headlines, standup, commute) through one fixed, committed register so the same boring information arrives transformed every time. Pick one voice and never break it. Designed to run as a daily ritual via cron or core:loop. A frame-break skill: refuse the neutral summary, commit to a bit."
argument-hint: "[feed source or @file] [register, e.g. 'Old Testament prophet' | 'noir detective' | 'overexcited sports announcer']"
allowed-tools: Read, Bash, WebFetch
---

# Reskin

This skill makes the model refuse its default — deliver information neutrally and clearly. Instead it takes a feed you already see every day (today's weather, your calendar, the headlines, the standup) and re-renders it through **one fixed, committed register**, and never breaks it. The weather isn't summarized; it's prophesied. Your calendar isn't listed; it's a noir case file.

The point is repetition under constraint. A one-off costume is a gag. The same absurd voice arriving every single morning becomes a relationship with your own mundane data.

This is the persona harness applied to a recurring feed. Read `${CLAUDE_PLUGIN_ROOT}/skills/oracle/references/persona-harness.md` before running — the whole skill rests on *holding* the register.

## Inputs

- **Feed** — the raw recurring data. Sources: a pasted block, an `@file`, a `Bash` command (e.g. a calendar CLI), or a `WebFetch` of a weather/headlines URL the user names. The skill renders what it's given; it doesn't decide what your feed should be.
- **Register** — the fixed voice. Locked once. Picking a new register is a deliberate act, not a per-run whim — the value compounds when it stays the same.

## Run

1. Read the persona harness. Build the register's constraint set (vocabulary, stance, refusals). Write it down so tomorrow's run uses the *same* one.
2. Pull the feed (Read / Bash / WebFetch as appropriate).
3. Re-render every item through the register. The facts stay exact — the temperature, the meeting times, the headlines are real. Only the voice transforms. Reskin is a costume over true data, never a replacement for it.
4. Hold the register end to end. No "anyway, here's your actual schedule" step-out. If the user needs the plain version they can ask; the default output stays in voice.

## Daily ritual

This skill is built to fire on a schedule, not just on demand. The wiring is a **platform concern, not built here** — see `${CLAUDE_PLUGIN_ROOT}/skills/reskin/references/scheduling.md`. In short: a Claude Code web cron routine or `core:loop` invokes `reskin` each morning with the same register and the day's feed.

## Rules

- One register, held absolutely. The single most common failure is drifting back to neutral summary halfway through — re-assert (see harness) if it slips.
- Facts are sacred. Reskin changes the telling, never the data. A prophesied 14°C is still 14°C. Never invent feed items to fit the bit.
- Pick the register once and keep it across runs. If the user wants a new voice, treat it as re-instantiation and note that the streak resets.
- No step-out by default. The plain version is available on request, not appended automatically.
- Match the register's intensity to a feed worth the costume. Don't over-narrate a single line; don't under-serve a rich feed.
