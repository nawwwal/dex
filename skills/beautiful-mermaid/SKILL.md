---
name: beautiful-mermaid
description: "Use when creating Mermaid diagrams with consistent visual style, exporting Mermaid to styled SVG, or previewing diagrams in the terminal."
---

# Beautiful Mermaid diagrams

## Workflow

1. Confirm the diagram type and the desired output:
   - **Markdown Mermaid** (raw ` ```mermaid ` block)
   - **SVG** (rendered, styled)
   - **Terminal preview** (ASCII)

2. Write correct Mermaid source first (clarity > cleverness):
   - Keep node labels short.
   - Prefer explicit direction (`TD`, `LR`) and stable IDs.
   - Avoid deeply nested subgraphs unless necessary.

3. If you need **SVG or terminal output**, use `beautiful-mermaid` in the repo/app where the diagram lives.
   - Install: `npm i -D beautiful-mermaid`
   - Inspect available exports (API can evolve):
     - `node -e "import('beautiful-mermaid').then(m=>console.log(Object.keys(m)))"`

4. Render using the most appropriate export that exists in the installed version:
   - Prefer a single-call helper if available (commonly named `renderMermaid` / `renderSVG`).
   - Otherwise use a renderer class (commonly `MermaidToSVG`).

5. (Optional) Format and validate if the exports exist:
   - Look for functions commonly named `formatMermaid` and `validateMermaid`.

## Patterns (pick the one that matches installed exports)

### (Optional) Format and validate

```js
import { formatMermaid, validateMermaid } from "beautiful-mermaid";

const raw = `graph TD;A-->B`;
const pretty = await formatMermaid(raw);
await validateMermaid(pretty);
```

### A) Render SVG via `renderMermaid(...)` (if present)

```js
import { renderMermaid } from "beautiful-mermaid";

const mermaid = `graph TD; A[Start] --> B[Done]`;
const svg = await renderMermaid(mermaid, {
  // Prefer passing a theme name/object if supported by your version.
});
```

### B) Render SVG via `renderSVG(...)` (if present)

```js
import { renderSVG } from "beautiful-mermaid";

const mermaid = `sequenceDiagram\n  Alice->>Bob: Hello`;
const svg = await renderSVG(mermaid, {
  // Prefer passing a theme name/object if supported by your version.
});
```

### C) Render SVG via `MermaidToSVG` (if present)

```js
import { MermaidToSVG } from "beautiful-mermaid";

const mermaid = `stateDiagram-v2\n  [*] --> Active`;
const renderer = new MermaidToSVG({
  // Prefer setting `theme` / `config` if supported by your version.
});
const svg = await renderer.render(mermaid);
```

### D) Terminal preview via `renderMermaidAscii(...)` (if present)

```js
import { renderMermaidAscii } from "beautiful-mermaid";

const mermaid = `graph LR; A --> B --> C`;
const ascii = await renderMermaidAscii(mermaid, { width: 80 });
console.log(ascii);
```

## Helper CLI (optional)

Use the bundled script to render to SVG (best-effort across versions):

- `node skills/beautiful-mermaid/scripts/render.mjs --in diagram.mmd --out diagram.svg`
- `node skills/beautiful-mermaid/scripts/render.mjs --in diagram.mmd` (prints SVG to stdout)
- `node skills/beautiful-mermaid/scripts/render.mjs --help`

## References

If you need upstream API details or theme names, read:
- `references/upstream-readme.md`
*** Add File: skills/beautiful-mermaid/agents/openai.yaml
interface:
  display_name: "Beautiful Mermaid"
  short_description: "Create themed Mermaid diagrams (SVG/ASCII)"
  default_prompt: "Use $beautiful-mermaid to generate a Mermaid diagram and (if needed) render it to a themed SVG for embedding in Markdown/HTML."
