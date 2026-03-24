#!/usr/bin/env node
import fs from "node:fs/promises";

function usage(exitCode = 0) {
  const msg = `
Render Mermaid to SVG using beautiful-mermaid (best-effort).

Usage:
  node render.mjs --in <input.mmd> [--out <output.svg>]
  node render.mjs --in <input.mmd>            # writes SVG to stdout

Notes:
  - Requires 'beautiful-mermaid' installed in the current project:
      npm i -D beautiful-mermaid
  - The library API can vary by version; this script probes common exports.
`.trim();
  // eslint-disable-next-line no-console
  console.log(msg);
  process.exit(exitCode);
}

function getArg(name) {
  const idx = process.argv.indexOf(name);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

if (process.argv.includes("--help") || process.argv.includes("-h")) usage(0);

const inPath = getArg("--in");
const outPath = getArg("--out");
if (!inPath) usage(1);

const mermaidSource = await fs.readFile(inPath, "utf8");

let mod;
try {
  mod = await import("beautiful-mermaid");
} catch (e) {
  // eslint-disable-next-line no-console
  console.error(
    "Failed to import 'beautiful-mermaid'. Install it first: npm i -D beautiful-mermaid",
  );
  process.exit(1);
}

async function render() {
  if (typeof mod.renderMermaid === "function") {
    return await mod.renderMermaid(mermaidSource);
  }
  if (typeof mod.renderSVG === "function") {
    return await mod.renderSVG(mermaidSource);
  }
  if (typeof mod.MermaidToSVG === "function") {
    const renderer = new mod.MermaidToSVG({});
    if (typeof renderer.render !== "function") {
      throw new Error("MermaidToSVG exists but has no .render(...) method");
    }
    return await renderer.render(mermaidSource);
  }

  const keys = Object.keys(mod || {}).sort().join(", ");
  throw new Error(
    `No known renderer export found. Available exports: ${keys || "(none)"}`,
  );
}

const svg = await render();

if (outPath) {
  await fs.writeFile(outPath, svg, "utf8");
} else {
  // eslint-disable-next-line no-console
  process.stdout.write(svg);
}

