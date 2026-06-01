#!/usr/bin/env node

function parseHex(value) {
  const hex = value.replace(/^#/, "").trim();
  if (!/^[0-9a-fA-F]{3}$|^[0-9a-fA-F]{6}$/.test(hex)) {
    throw new Error(`Invalid hex color: ${value}`);
  }
  const full = hex.length === 3 ? hex.split("").map((x) => x + x).join("") : hex;
  return [0, 2, 4].map((index) => parseInt(full.slice(index, index + 2), 16) / 255);
}

function luminance(hex) {
  const [r, g, b] = parseHex(hex).map((channel) =>
    channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4
  );
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrast(foreground, background) {
  const a = luminance(foreground);
  const b = luminance(background);
  const lighter = Math.max(a, b);
  const darker = Math.min(a, b);
  return (lighter + 0.05) / (darker + 0.05);
}

const pairs = process.argv.slice(2);

if (pairs.length === 0) {
  console.error("Usage: node scripts/contrast-check.js '#ffffff:#030303:body' '#c1ff84:#030303:eyebrow'");
  process.exit(2);
}

let failed = false;

for (const pair of pairs) {
  const [foreground, background, label = `${foreground} on ${background}`] = pair.split(":");
  const ratio = contrast(foreground, background);
  const bodyPass = ratio >= 4.5;
  const largePass = ratio >= 3;
  if (!bodyPass) failed = true;
  console.log(`${label}: ${ratio.toFixed(2)}:1 body=${bodyPass ? "PASS" : "FAIL"} large=${largePass ? "PASS" : "FAIL"}`);
}

process.exit(failed ? 1 : 0);
