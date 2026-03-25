---
name: media-optimizer
description: "Optimize images and videos — compress, convert, resize."
disable-model-invocation: true
---

# Media Optimizer

Optimize and convert images and videos using [Optimo](https://optimo.microlink.io/) — format-specific compression pipelines on top of ImageMagick and FFmpeg.

## Tool

```bash
npx optimo@0.0.24 <file-or-directory>
```

Check for newer versions: `npm view optimo version`

> **Node.js requirement:** Optimo requires Node >= 24. Verify with `node --version`. If on an older version, upgrade Node first or use `nvm install 24 && nvm use 24`.
>
> **Security:** Pin to an exact version in production. Avoid running on untrusted files — ImageMagick and FFmpeg have active CVEs.

## Prerequisites

| Format | Required binary |
|---|---|
| PNG, JPEG, WebP, AVIF, HEIC, JXL, GIF | `magick` (ImageMagick) |
| SVG | `svgo` |
| JPEG second pass | `mozjpegtran` or `jpegtran` (optional) |
| GIF second pass | `gifsicle` (optional) |
| MP4, WebM, MOV, MKV, AVI, OGV | `ffmpeg` |

**Partial install behavior:** SVG works with only `svgo` installed. Video fails gracefully if `ffmpeg` is absent. JPEG second-pass is skipped if neither mozjpegtran nor jpegtran is found.

> `svgo` and `debug` are peer deps not bundled by optimo — install with `npm install -g svgo debug`.

## Recommended Workflow

1. **Dry run first** — confirm target files without changes
2. **Test single file** — run on one file before scaling to directories
3. **Convert intentionally** — use `--format` only when format conversion is the goal
4. **Resize explicitly** — use `--resize` only when dimension/size control is required
5. **Debug issues** — use `--verbose` when diagnosing unsupported files or binary errors
6. **Verify & commit** — check outputs in version control before committing

## Common Commands

```bash
# Dry run — preview what would change
npx optimo@0.0.24 public/ --dry-run

# Optimize a single file
npx optimo@0.0.24 image.png

# Optimize entire directory
npx optimo@0.0.24 public/media

# Convert format
npx optimo@0.0.24 image.png --format webp
npx optimo@0.0.24 image.heic --format jpeg

# Lossy mode for maximum compression
npx optimo@0.0.24 image.jpg --losy

# Resize options
npx optimo@0.0.24 image.png --resize 50%      # by percentage
npx optimo@0.0.24 image.png --resize 100kB    # to target file size (images only)
npx optimo@0.0.24 image.png --resize w960     # by width
npx optimo@0.0.24 image.png --resize h480     # by height

# Video
npx optimo@0.0.24 clip.mp4
npx optimo@0.0.24 clip.mov --format webm
npx optimo@0.0.24 clip.mp4 --mute false       # keep audio (muted by default)

# Debug
npx optimo@0.0.24 image.heic --dry-run --verbose
```

> Full flag reference, pipelines, JS API, and git pre-commit hook: [`references/optimo.md`](references/optimo.md)
