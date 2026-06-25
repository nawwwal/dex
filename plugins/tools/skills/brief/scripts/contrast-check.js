#!/usr/bin/env node

function parseColor(value) {
  const hex = value.replace("#", "").trim();
  const full = hex.length === 3 ? hex.split("").map((c) => c + c).join("") : hex;
  if (!/^[0-9a-fA-F]{6}$/.test(full)) throw new Error(`Invalid color: ${value}`);
  const number = Number.parseInt(full, 16);
  return [(number >> 16) & 255, (number >> 8) & 255, number & 255];
}

function channel(value) {
  const c = value / 255;
  return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

function luminance(rgb) {
  return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);
}

function ratio(foreground, background) {
  const lighter = Math.max(luminance(foreground), luminance(background));
  const darker = Math.min(luminance(foreground), luminance(background));
  return (lighter + 0.05) / (darker + 0.05);
}

const checks = process.argv.slice(2);
if (!checks.length) {
  console.error("Usage: contrast-check.js '#foreground:#background:label'");
  process.exit(1);
}

let failed = false;
for (const check of checks) {
  const [fg, bg, label = "pair"] = check.split(":");
  const value = ratio(parseColor(fg), parseColor(bg));
  const bodyPass = value >= 4.5;
  const largePass = value >= 3;
  if (!bodyPass) failed = true;
  console.log(`${label}: ratio=${value.toFixed(2)} body=${bodyPass ? "PASS" : "FAIL"} large=${largePass ? "PASS" : "FAIL"}`);
}

process.exit(failed ? 1 : 0);
