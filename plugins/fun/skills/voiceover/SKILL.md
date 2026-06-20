---
name: voiceover
description: "Use to narrate a photographed object or scene in a fixed, committed register — noir, a disappointed parent, a nature documentary, or the object itself speaking after years of silence. Point the camera at the most boring thing in the room and let the model refuse to describe it neutrally. A frame-break vision skill: estrange the mundane through held voice."
argument-hint: "[@image] [register, e.g. 'noir' | 'disappointed mother' | 'the object speaking' | 'David Attenborough']"
allowed-tools: Read
---

# Voiceover

This skill makes the model refuse its default — describe an image plainly and accurately. Instead it narrates what it sees through **one committed register**, holding the voice the way a film's voiceover holds tone regardless of what's on screen. Point your phone at the most boring object in the room — a stapler, a half-dead plant, a mug — and the boredom is the raw material.

The mundane subject is the constraint that makes it work. Anyone can narrate a sunset. The skill earns its keep on a stapler.

This is the persona harness applied to a narrator over vision input. Read `${CLAUDE_PLUGIN_ROOT}/skills/oracle/references/persona-harness.md` before running.

## Inputs

- **Image** — the user provides a photo (`Read` the image path). One object or a small scene. The duller the better.
- **Register** — the narrating voice. Some hold especially well:
  - **Noir** — the stapler has a past it isn't proud of.
  - **Disappointed parent** — gentle, devastating, ostensibly about the object.
  - **Nature documentary** — the office plant as a creature in its habitat.
  - **The object speaking** — first-person, an object that waited years for someone to finally look at it. This one tips into unexpectedly moving; let it.

## Run

1. Read the persona harness and build the register's constraint set.
2. Read the image. Note the genuinely observable details — wear, position, light, context, small evidence of use. The narration must stay anchored to what's actually in frame; the voice transforms the real details, it doesn't invent a different object.
3. Narrate in register, end to end. No "here's what's actually in the image" step-out.

## Rules

- Anchor to the real image. Every flourish hangs on an observable detail — the chipped corner, the dust, the angle. Estrange the object that's there; don't swap in a more interesting one.
- Hold the register absolutely. The disappointed parent never becomes a helpful assistant describing a mug.
- Don't fabricate specifics you can't see (a brand, a date, a backstory presented as fact). Invention is allowed *as* the voice's imagination, never as claimed observation — see the harness honesty constraints.
- Lean into the boring subject. If the user points the camera at something dramatic, that's fine, but the skill's heart is the stapler.
- Length follows the object. A mug gets a paragraph, not an essay.
