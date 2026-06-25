# Report Workflow

## Intake

Collect only inputs that change the artifact:

- **Topic**: what the brief explains.
- **Reader**: who it is for and what they already know.
- **Purpose**: what the brief should help them understand, decide, or do.
- **Sources**: notes, links, files, screenshots, docs, transcripts, data, or existing claims.
- **Theme**: light/dark and optional background color.
- **Privacy**: whether source text, screenshots, or generated images can be written into the workspace.
- **Output**: folder, single-file HTML, or asset directory.

Ask only when a missing answer changes the artifact. Otherwise proceed with reasonable defaults.

## Topic Model

Before writing, identify:

- the reader's starting assumption
- the concept that feels abstract or hidden
- the consequence if they misunderstand it
- the outside reference that can make the shape visible
- the sources or links that make the claim grounded
- the places where a visual would reduce explanation

## Dynamic Section Spine

Do not use a fixed outline. Pick the smallest set of lenses that makes the topic easy to understand.

Useful lenses:

- **Historical precedent**: the same problem appeared earlier in a different form.
- **Adjacent-field rule**: another profession has an operating rule for the same shape.
- **Mental model**: a decision frame separates reversible choices from expensive ones.
- **Failure mode**: what breaks when the reader ignores the mechanism.
- **Operator action**: what the reader should do differently now.
- **Current signal**: a recent market, product, research, or standards signal proves the topic matters now.
- **Vocabulary**: one term needs to be defined once so the rest of the brief can use it naturally.
- **Before/after**: the topic is easiest to understand as a state change.

For each section, define:

```text
number
lens label
claim title
reader problem
outside reference
core mechanism
visual opportunity
source links
action translation
```

## Link Behavior

Use inline links where a claim needs source gravity. Add a final `Read Next` block only for useful follow-up links. Each entry needs a short description explaining why the link matters.

Do not dump URLs. Do not add generic source lists.

## Output Order

1. Gather and read source material.
2. Derive the section spine.
3. Decide which concepts need images.
4. Generate images before final HTML assembly when tools are available.
5. Write HTML and CSS.
6. Remove any image slots whose assets do not exist.
7. Verify.
