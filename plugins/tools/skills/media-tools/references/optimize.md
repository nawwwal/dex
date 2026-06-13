# Optimize — Compress, Convert, and Resize Media

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

## Supported Formats

### Images
PNG, JPEG, WebP, AVIF, HEIC, JPEG XL (JXL), GIF, SVG

### Videos
MP4, WebM, MOV, MKV, AVI, OGV

## Pipelines

Optimo selects a pipeline by output format:

| Format | Pipeline |
|---|---|
| `.png` | `magick.png` |
| `.svg` | `svgo.svg` |
| `.jpg` / `.jpeg` | `magick.jpg` + `mozjpegtran.jpg` (lossless JPEG without resize/conversion skips magick, runs only mozjpegtran) |
| `.gif` | `magick.gif` + `gifsicle.gif` |
| `.webp`, `.avif`, `.heic`, `.heif`, `.jxl`, etc. | `magick.<format>` |
| `.mp4`, `.m4v`, `.mov`, `.webm`, `.mkv`, `.avi`, `.ogv` | `ffmpeg.<format>` |

### Mode behavior

- **Default:** lossless-first pipeline
- `--losy` / `-l`: lossy + lossless pass where supported (note: one 's', not two)
- `--mute` / `-m`: remove audio from videos (default: `true`; use `--mute false` to keep audio)

## All CLI Options

| Flag | Short | Description |
|---|---|---|
| `--dry-run` | `-d` | Show what would change without writing files |
| `--format` | `-f` | Convert output format (`jpeg`, `webp`, `avif`, etc.) |
| `--losy` | `-l` | Enable lossy + lossless pass (note: one 's', not two) |
| `--mute` | `-m` | Remove audio tracks from videos (default: `true`; `--mute false` to keep audio) |
| `--resize` | `-r` | Resize using percentage (`50%`), max file size (`100kB`, images only), width (`w960`), or height (`h480`) |
| `--silent` | `-s` | Suppress per-file logs |
| `--data-url` | `-u` | Return optimized image as data URL (single image file only; throws for videos or directories) |
| `--verbose` | `-v` | Print debug logs (pipeline selection, command execution, errors) |

## Behavior Notes

- For non-conversion runs, if the optimized file is not smaller, the original is kept
- During conversion, output uses the new extension and the original source file is removed (unless `--dry-run`)
- Hidden files and folders (names starting with `.`) are skipped in directory mode
- Unsupported files are reported as `[unsupported]` and ignored
- Video defaults are tuned for web compatibility (`yuv420p`, fast-start MP4 where applicable)
- `--data-url` is only supported for single image files
- `--resize 100kB` is not supported for videos; use `50%`, `w960`, or `h480` instead

## Programmatic API

```js
const optimo = require('optimo')

// Single file — image
await optimo.file('/absolute/path/image.jpg', {
  dryRun: false,
  losy: false,
  format: 'webp',
  resize: '50%',
  onLogs: console.log
})

// Single file — resize to target size
await optimo.file('/absolute/path/image.jpg', {
  resize: '100kB',
  onLogs: console.log
})

// Single file — get as data URL
const { dataUrl } = await optimo.file('/absolute/path/image.png', {
  dataUrl: true,
  onLogs: console.log
})

// Single file — video
await optimo.file('/absolute/path/video.mp4', {
  losy: false,
  mute: false,
  format: 'webm',
  resize: 'w1280',
  onLogs: console.log
})

// Directory
const result = await optimo.dir('/absolute/path/images')
console.log(result)
// { originalSize, optimizedSize, savings }
```

## Git Pre-Commit Hook

Auto-optimize staged images and videos before every commit using `simple-git-hooks` + `nano-staged`:

```json
{
  "simple-git-hooks": {
    "pre-commit": "npx nano-staged"
  },
  "nano-staged": {
    "*.{png,jpg,jpeg,webp,avif,heic,gif,svg}": "npx optimo@0.0.24",
    "*.{mp4,webm,mov}": "npx optimo@0.0.24"
  }
}
```

Install hooks after adding config:
```bash
npx simple-git-hooks
```

## Install Binaries (macOS)

```bash
brew install imagemagick ffmpeg gifsicle mozjpeg
npm install -g svgo debug
```

> **Note:** `svgo` and `debug` must be installed separately — optimo@0.0.24 does not bundle them despite requiring them. `brew install svgo` installs a different binary; use `npm install -g svgo debug` instead.

After installing mozjpeg, symlink for Optimo:

```bash
ln -s /opt/homebrew/opt/mozjpeg/bin/jpegtran /usr/local/bin/mozjpegtran
```

Or add to your shell profile:

```bash
export PATH="/opt/homebrew/opt/mozjpeg/bin:$PATH"
```

## Dependency Detection

```bash
command -v magick    && echo "ImageMagick: OK" || echo "ImageMagick: MISSING (PNG/JPEG/WebP/AVIF/HEIC/JXL/GIF)"
command -v svgo      && echo "SVGO: OK"        || echo "SVGO: MISSING (SVG)"
command -v ffmpeg    && echo "FFmpeg: OK"      || echo "FFmpeg: MISSING (video)"
command -v mozjpegtran && echo "MozJPEG: OK"  || echo "MozJPEG: optional (JPEG second pass)"
command -v gifsicle  && echo "Gifsicle: OK"   || echo "Gifsicle: optional (GIF second pass)"
```
