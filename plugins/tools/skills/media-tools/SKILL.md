---
name: media-tools
description: "Generate, edit, compress, convert, and resize images and video. Use for AI image generation/editing, WebP/AVIF conversion, compression, resizing, or when playground/brief needs optimized media. Replaces generate-image and media-optimizer."
disable-model-invocation: true
---

# media-tools

Unified media skill. Two operation families: **generate** (AI images via Gemini) and **optimize** (compress, convert, resize via Optimo).

Replaces `generate-image` and `media-optimizer`. Do not invoke those legacy skill names.

## Routing

| User intent | Path | Reference |
|---|---|---|
| Generate, edit, or create AI images | generate | `references/generate.md` |
| Compress, convert format, resize images or video | optimize | `references/optimize.md` |
| Generate then optimize (e.g. illustration -> WebP for a brief) | generate -> optimize | both references |

When `playground` or `brief` needs generated or optimized media, route here first. Return to the requesting skill only for artifact integration.

Do not use `brief`, `playground`, or `codex` as the primary handler for raw media work.

## Quick surfaces

### Generate (deterministic CLI)

Before generating, state the chosen path, default model, and invocation surface: `generate`, `gemini-3.1-flash-image-preview`, and `scripts/generate.py` unless you are explicitly using inline `google-genai` code for a conversational edit.

```bash
python $CLAUDE_SKILL_DIR/scripts/generate.py \
  --prompt "..." \
  [--model gemini-3.1-flash-image-preview] \
  [--aspect-ratio 16:9] \
  [--size 2K] \
  [--input-image /path/to/source.png] \
  [--output ./output.png]
```

Output: JSON to stdout — `{ "path", "text", "model", "usage" }`. Errors: stderr + exit 1.

For natural-language generation (prompt refinement, multi-turn editing), read `references/generate.md` and run inline `google-genai` code.

### Optimize (Optimo, pinned)

```bash
npx optimo@0.0.24 <file-or-directory> [--dry-run] [--format webp] [--resize w960]
```

Always dry-run on directories before writing. Read `references/optimize.md` for pipelines, prerequisites, and full flags.

## Full reference

- Models, params, cross-skill invocation, inline code: `$CLAUDE_SKILL_DIR/references/generate.md`
- Optimo pipelines, prerequisites, programmatic API: `$CLAUDE_SKILL_DIR/references/optimize.md`

## Required packages (generate only)

```
google-genai>=1.55.0
Pillow>=10.0.0
```
