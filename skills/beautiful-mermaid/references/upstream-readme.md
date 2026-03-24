# beautiful-mermaid (upstream notes)

Source README: https://github.com/lukilabs/beautiful-mermaid

## What it is

`beautiful-mermaid` is a JS/TS library for rendering Mermaid diagrams with attractive theming (and, in some versions, ASCII rendering for terminals).

## Exports you may see (version-dependent)

Depending on the published package version, you may find exports such as:

- `renderMermaid(mermaidSource, options?)` → returns rendered SVG
- `renderMermaidAscii(mermaidSource, options?)` → returns terminal-friendly ASCII output
- `renderSVG(mermaidSource, options?)` → returns rendered SVG
- `MermaidToSVG` → class-based renderer
- Theme helpers / theme objects (e.g., light/dark defaults)
- Shiki theme loading helpers (e.g., `loadShikiTheme(...)`)

Because the API surface can change across versions, prefer inspecting installed exports:

```bash
node -e "import('beautiful-mermaid').then(m=>console.log(Object.keys(m)))"
```

## Install

```bash
npm i -D beautiful-mermaid
```

## Basic rendering patterns (choose based on exports)

```js
import { renderMermaid } from "beautiful-mermaid";
const svg = await renderMermaid("graph TD; A-->B");
```

```js
import { renderSVG } from "beautiful-mermaid";
const svg = await renderSVG("graph TD; A-->B");
```

```js
import { MermaidToSVG } from "beautiful-mermaid";
const svg = await new MermaidToSVG({}).render("graph TD; A-->B");
```

## Themes

Upstream mentions multiple built-in themes. Some commonly referenced theme display names include:

- Default
- Zinc
- Dark
- Tokyo Night
- Tokyo Storm
- Tokyo Light
- Catppuccin Latte
- Nord
- Nord Light
- Dracula
- GitHub
- GitHub Dark
- Solarized
- Solar Dark
- One Dark

Names may be exposed as IDs or display names depending on version. If you need exact identifiers, prefer checking the package exports or upstream README.
