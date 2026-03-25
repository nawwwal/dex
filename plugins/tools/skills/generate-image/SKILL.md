---
name: generate-image
description: "AI image generation and editing via CLI scripts."
disable-model-invocation: true
---

# generate-image

Shared image generation skill. Two surfaces: natural language (Claude runs inline code)
and script (deterministic CLI for other skills).

## Models

| Nickname | Model ID | When to use |
|----------|----------|-------------|
| **nano banana 2** | `gemini-3.1-flash-image-preview` | Default — always use this unless explicitly asked for pro |
| **nano banana pro** | `gemini-3-pro-image-preview` | Only when user explicitly says "pro", "higher quality", or "nano banana pro" |

"Nano banana 2" and "nano banana pro" are shorthand nicknames for these models.
If the user says "nano banana", default to nano banana 2 (Flash).

Never use `gemini-2.5-flash-image` or any `gemini-2.x` / `gemini-1.x` image model.

## Invocation

### Natural language (Claude writes and runs inline code)

Use when: contextual decisions needed, multi-turn generation, prompt refinement required.

```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from env

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],  # or ["TEXT", "IMAGE"]
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # optional
            image_size="2K"       # optional
        ),
    )
)

for part in response.parts:
    if part.thought:
        continue
    elif part.inline_data is not None:
        part.as_image().save("output.png")
    elif part.text:
        print(part.text)
```

### Script (deterministic, called by other skills)

```bash
python ~/.claude/skills/generate-image/scripts/generate.py \
  --prompt "..." \
  [--model gemini-3.1-flash-image-preview] \
  [--aspect-ratio 16:9] \
  [--size 2K] \
  [--modalities IMAGE] \
  [--thinking minimal] \
  [--google-search] \
  [--image-search] \
  [--input-image /path/to/source.png] \
  [--output ./output.png] \
  [--output-dir ./images]
```

Output: JSON to stdout — `{ "path": "...", "text": "...", "model": "...", "usage": {...} }`
Errors: message to stderr + exit code 1

## Params

| Flag | Values | Default |
|------|--------|---------|
| `--model` | `gemini-3.1-flash-image-preview`, `gemini-3-pro-image-preview` | `gemini-3.1-flash-image-preview` |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`, `21:9`, `4:5`, `5:4`, `1:4`, `4:1`, `1:8`, `8:1` | model default |
| `--size` | `512`, `1K`, `2K`, `4K` | `1K` |
| `--modalities` | `IMAGE`, `TEXT,IMAGE` | `IMAGE` |
| `--thinking` | `minimal`, `High` | `minimal` |
| `--google-search` | flag | off |
| `--image-search` | flag — Flash model only | off |
| `--input-image` | file path | none (text-to-image mode) |
| `--output` | file path | `./gemini-image-{timestamp}.png` |
| `--output-dir` | directory | current directory |

## Full reference

- Aspect ratios by use case, model limits, MIME types, streaming: read `$CLAUDE_SKILL_DIR/PARAMS.md`
- How other skills should invoke this: read `$CLAUDE_SKILL_DIR/EXAMPLES.md`

## Required packages

```
google-genai>=1.55.0
Pillow>=10.0.0
```
