#!/usr/bin/env node
/**
 * blade-score.js — Measures Blade design system coverage on a live page.
 *
 * Vendors the canonical calculateBladeCoverage algorithm from the Blade Chrome extension:
 * razorpay/blade packages/blade-coverage-extension/background-scripts/blade-coverage-script.js
 *
 * Usage:
 *   node blade-score.js <url> [options]
 *
 * Options:
 *   --threshold <n>        Fail (exit 1) if coverage is below n percent
 *   --no-navbars           Exclude sidenav / top-nav from the count
 *   --headed               Run with a visible browser window
 *   --json                 Output JSON instead of human-readable text
 *   --storage-state <path> Playwright storage state file for auth (cookies + localStorage)
 *   --settle-ms <n>        Wait n ms after page load before measuring (default: 1000)
 *   --timeout-ms <n>       Navigation timeout in ms (default: 30000)
 *
 * Exit codes:
 *   0 — success (or no --threshold passed)
 *   1 — coverage below --threshold
 *   2 — setup / dependency error
 *   3 — navigation / auth timeout
 */

'use strict';

const path = require('path');

// Resolve playwright from the consuming project first, then globally.
// This prevents the dex plugin from requiring a separate playwright install.
function resolveDep(name) {
  const searchBases = [
    process.cwd(),
    path.join(__dirname, '..', '..', '..', '..', '..', '..'),
  ];
  for (const base of searchBases) {
    try {
      return require(path.join(base, 'node_modules', name));
    } catch (_) {}
  }
  try {
    return require(name);
  } catch (_) {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Canonical calculateBladeCoverage — vendored from blade-coverage-extension.
// Runs inside the browser via page.evaluate(). __INCLUDE_NAVBARS__ is
// replaced with true/false before evaluation.
// ---------------------------------------------------------------------------
const BLADE_COVERAGE_FN = `
(function(includeNavbars) {
  var bladeElementExceptions = [
    '[data-blade-component="table-cell"] > div',
    '[data-blade-component="table-header-cell"] > div',
    '[data-blade-component="table-footer-cell"] > div'
  ];

  function isElementHidden(element) {
    if (element.parentElement && isElementHidden(element.parentElement)) return true;
    if (!(element instanceof HTMLElement)) return false;
    if (element.hidden) return true;
    var style = getComputedStyle(element);
    return style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0';
  }

  function isElementEmpty(element) {
    if (!element) return true;
    return element.childNodes.length === 0;
  }

  function isMediaElement(element) {
    return ['img', 'video', 'audio', 'source', 'picture'].includes(element.tagName.toLowerCase());
  }

  function isInsideNavElement(element) {
    var SIDENAV = 'sidenav';
    var TOPNAV  = 'top-nav';
    var bc = element.getAttribute('data-blade-component');
    if (bc === SIDENAV || bc === TOPNAV) return true;
    if (element.closest('[data-blade-component=' + SIDENAV + ']') ||
        element.closest('[data-blade-component=' + TOPNAV  + ']')) return true;
    return false;
  }

  function shouldIgnoreElement(element) {
    if (isInsideNavElement(element)) return true;
    var bc = element.getAttribute('data-blade-component');
    if (bc && ['box'].includes(bc)) return true;
    return false;
  }

  var allDomElements    = document.querySelectorAll('body *');
  var bladeNodeElements = [];
  var totalNodeElements = [];
  var nonBladeNodeElements = [];

  allDomElements.forEach(function(elm) {
    if (isElementHidden(elm)) return;
    if (isElementEmpty(elm)) return;
    if (isMediaElement(elm)) return;

    var closestSvg = elm.closest('svg');

    // Blade SVG icons: include the root <svg> if it has data-blade-component
    if (elm.tagName.toLowerCase() === 'svg' && elm.hasAttribute('data-blade-component')) {
      if (!includeNavbars && shouldIgnoreElement(elm)) return;
      bladeNodeElements.push(elm);
      totalNodeElements.push(elm);
      return;
    }
    // Skip internals of icon SVGs
    if (closestSvg && closestSvg.getAttribute('data-blade-component') === 'icon') return;
    // Skip non-Blade SVG descendants
    if (closestSvg && !elm.hasAttribute('data-blade-component')) return;

    // Skip table-cell inner divs
    if (bladeElementExceptions.some(function(sel) { return elm.matches(sel); })) return;

    if (!includeNavbars && shouldIgnoreElement(elm)) return;

    totalNodeElements.push(elm);
    if (elm.hasAttribute('data-blade-component')) {
      bladeNodeElements.push(elm);
    } else {
      nonBladeNodeElements.push(elm);
    }
  });

  var totalNodes = totalNodeElements.length;
  var bladeNodes = bladeNodeElements.length;
  var bladeCoverage = totalNodes === 0 ? 0 : Number((bladeNodes / totalNodes * 100).toFixed(2));

  return { bladeCoverage: bladeCoverage, totalNodes: totalNodes, bladeNodes: bladeNodes };
})(__INCLUDE_NAVBARS__)
`;

// ---------------------------------------------------------------------------
// Argument parsing
// ---------------------------------------------------------------------------
const argv = process.argv.slice(2);
let url           = null;
let threshold     = null;
let includeNavbars = true;
let headed        = false;
let jsonOutput    = false;
let storageState  = null;
let settleMs      = 1000;
let timeoutMs     = 30000;

for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  if (arg.startsWith('http://') || arg.startsWith('https://')) {
    url = arg;
  } else if (arg === '--threshold') {
    threshold = parseFloat(argv[++i]);
  } else if (arg === '--no-navbars') {
    includeNavbars = false;
  } else if (arg === '--headed') {
    headed = true;
  } else if (arg === '--json') {
    jsonOutput = true;
  } else if (arg === '--storage-state') {
    storageState = argv[++i];
  } else if (arg === '--settle-ms') {
    settleMs = parseInt(argv[++i], 10);
  } else if (arg === '--timeout-ms') {
    timeoutMs = parseInt(argv[++i], 10);
  }
}

if (!url) {
  console.error('Usage: node blade-score.js <url> [--threshold 95] [--no-navbars] [--headed] [--json] [--storage-state path] [--settle-ms 1000] [--timeout-ms 30000]');
  process.exit(2);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  const playwright = resolveDep('playwright');
  if (!playwright) {
    console.error('Error: playwright not found in project or globally.\nRun: npm install playwright && npx playwright install chromium');
    process.exit(2);
  }

  const { chromium } = playwright;
  let browser;

  try {
    browser = await chromium.launch({ headless: !headed });
    const contextOpts = storageState ? { storageState } : {};
    const context = await browser.newContext(contextOpts);
    const page    = await context.newPage();

    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: timeoutMs });
    } catch (err) {
      await browser.close();
      console.error(`Navigation failed: ${err.message}`);
      process.exit(3);
    }

    if (settleMs > 0) {
      await new Promise(r => setTimeout(r, settleMs));
    }

    const script = BLADE_COVERAGE_FN.replace('__INCLUDE_NAVBARS__', includeNavbars ? 'true' : 'false');
    const result = await page.evaluate(script);
    await browser.close();

    const pass    = threshold === null || result.bladeCoverage >= threshold;
    const verdict = threshold !== null ? (pass ? 'PASS' : `FAIL (threshold: ${threshold}%)`) : null;

    if (jsonOutput) {
      console.log(JSON.stringify({ url, ...result, threshold, pass }));
    } else {
      console.log(`Blade Coverage: ${result.bladeCoverage}%`);
      console.log(`Blade Nodes:    ${result.bladeNodes} / ${result.totalNodes}`);
      if (verdict) console.log(`Verdict:        ${verdict}`);
    }

    process.exit(pass ? 0 : 1);
  } catch (err) {
    if (browser) await browser.close().catch(() => {});
    console.error(`Error: ${err.message}`);
    process.exit(2);
  }
}

main();
