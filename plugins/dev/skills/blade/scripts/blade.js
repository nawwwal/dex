#!/usr/bin/env node
/**
 * blade.js - Blade coverage, static drift audit, and final gate.
 *
 * Coverage vendors the canonical calculateBladeCoverage algorithm from the Blade
 * Chrome extension:
 * razorpay/blade packages/blade-coverage-extension/background-scripts/blade-coverage-script.js
 */

'use strict';

const childProcess = require('child_process');
const fs = require('fs');
const path = require('path');

const EXIT = {
  OK: 0,
  COVERAGE_FAIL: 1,
  SETUP_FAIL: 2,
  NAVIGATION_FAIL: 3,
  DRIFT_FAIL: 4,
};

const SOURCE_EXTENSIONS = new Set([
  '.css',
  '.scss',
  '.sass',
  '.less',
  '.js',
  '.jsx',
  '.ts',
  '.tsx',
]);

const SKIP_DIRS = new Set([
  '.git',
  '.next',
  '.turbo',
  '.vite',
  'build',
  'coverage',
  'dist',
  'node_modules',
  'out',
]);

const BLADE_IMPORT_RE = /@razorpay\/blade\/components/;

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

    if (elm.tagName.toLowerCase() === 'svg' && elm.hasAttribute('data-blade-component')) {
      if (!includeNavbars && shouldIgnoreElement(elm)) return;
      bladeNodeElements.push(elm);
      totalNodeElements.push(elm);
      return;
    }
    if (closestSvg && closestSvg.getAttribute('data-blade-component') === 'icon') return;
    if (closestSvg && !elm.hasAttribute('data-blade-component')) return;
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

const DRIFT_RULES = [
  {
    id: 'hardcoded-color',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(^|[^A-Za-z0-9_])#[0-9A-Fa-f]{3,8}\b/g,
    message: 'Hardcoded color. Use Blade semantic tokens or component color props.',
  },
  {
    id: 'important-override',
    severity: 'high',
    file: /\.(css|scss|sass|less)$/,
    regex: /!important\b/g,
    message: 'CSS !important override. This usually means custom CSS is fighting Blade APIs.',
  },
  {
    id: 'data-testid-styling',
    severity: 'high',
    file: /\.(css|scss|sass|less)$/,
    regex: /\[data-testid=['"][^'"]+['"]\]/g,
    message: 'CSS targets data-testid. Test ids are not a styling API and often couple to Blade internals.',
  },
  {
    id: 'role-button-styling',
    severity: 'high',
    file: /\.(css|scss|sass|less)$/,
    regex: /\[role=['"]button['"]\]|button(?=[\s,.#:[\]>])/g,
    message: 'CSS targets native/internal button selectors. Prefer Blade props or a stable wrapper.',
  },
  {
    id: 'raw-button',
    severity: 'high',
    file: /\.(tsx?|jsx?)$/,
    regex: /<button\b/g,
    message: 'Raw button element. Use Blade Button or IconButton unless this is a documented exception.',
  },
  {
    id: 'raw-input',
    severity: 'high',
    file: /\.(tsx?|jsx?)$/,
    regex: /<(input|select|textarea)\b/g,
    message: 'Raw form control. Use Blade TextInput, SelectInput, TextArea, Checkbox, Radio, or Switch.',
  },
  {
    id: 'clickable-div-span',
    severity: 'high',
    file: /\.(tsx?|jsx?)$/,
    regex: /<(div|span)\b[^>]*\bonClick=/g,
    message: 'Clickable div/span. Use a semantic Blade interactive component or add a documented a11y exception.',
  },
  {
    id: 'custom-card-surface',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(card|tile|panel|surface|metric|summary)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom card-like surface. Check Blade Card before keeping this.',
  },
  {
    id: 'custom-alert-surface',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(alert|banner|strip|notice|warning)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom alert/banner-like surface. Check Blade Alert before keeping this.',
  },
  {
    id: 'custom-navigation',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(sidebar|sidenav|side-nav|nav|navigation)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom navigation surface. Check Blade SideNav, TopNav, Tabs, or TabNav before keeping this.',
  },
  {
    id: 'custom-menu-dropdown',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(menu|dropdown|popover)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom menu/dropdown surface. Check Blade Menu, Dropdown, or Popover before keeping this.',
  },
  {
    id: 'custom-table-list',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(table|list-view|listview|row)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom data-list surface. Check Blade Table, List, or ListView before keeping this.',
  },
  {
    id: 'custom-stepper',
    severity: 'high',
    file: /\.(css|scss|sass|less|tsx?|jsx?)$/,
    regex: /(?:className=|class=|\.)(["'`]?[-_a-zA-Z0-9 ]*)\b(step|stepper|setup|progress)[-_a-zA-Z0-9 ]*\b/g,
    message: 'Custom step/progress surface. Check Blade StepGroup, Accordion, or ProgressBar before keeping this.',
  },
  {
    id: 'manual-currency-format',
    severity: 'medium',
    file: /\.(tsx?|jsx?)$/,
    regex: /\u20B9|\.toLocaleString\(/g,
    message: 'Manual amount formatting. Check Blade Amount and i18n formatting before keeping this.',
  },
  {
    id: 'raw-heading',
    severity: 'medium',
    file: /\.(tsx?|jsx?)$/,
    regex: /<h[1-6]\b/g,
    message: 'Raw heading element. Use Blade Heading unless this is outside Blade mode.',
  },
];

const SEMANTIC_IMPORT_RULES = [
  {
    id: 'missing-menu-import',
    severity: 'medium',
    terms: /\b(profile|account|avatar)[-_ ]?(menu|dropdown)|\b(log out|logout)\b/i,
    imports: ['Menu'],
    message: 'Profile/account action language found. Prefer Blade Menu over Dropdown unless this is selection-like.',
  },
  {
    id: 'missing-alert-import',
    severity: 'medium',
    terms: /\b(test mode|banner|strip|notice|warning|activation pending)\b/i,
    imports: ['Alert'],
    message: 'Banner/status language found. Check Blade Alert before custom surfaces.',
  },
  {
    id: 'missing-sidenav-import',
    severity: 'medium',
    terms: /\b(sidebar|side nav|sidenav|navigation|nav item)\b/i,
    imports: ['SideNav'],
    message: 'Navigation language found. Check Blade SideNav/TopNav/TabNav before custom nav.',
  },
  {
    id: 'missing-stepgroup-import',
    severity: 'medium',
    terms: /\b(setup step|stepper|onboarding step|current step|guided setup)\b/i,
    imports: ['StepGroup'],
    message: 'Step-flow language found. Check Blade StepGroup before custom step rows.',
  },
  {
    id: 'missing-card-import',
    severity: 'medium',
    terms: /\b(metric|summary|overview|panel|card|tile)\b/i,
    imports: ['Card'],
    message: 'Card-like language found. Check Blade Card before custom Box/CSS surfaces.',
  },
  {
    id: 'missing-chart-import',
    severity: 'medium',
    terms: /\b(donut|chart|payment method split|method split)\b/i,
    imports: ['DonutChart', 'BarChart', 'LineChart', 'AreaChart'],
    message: 'Chart language found. Check Blade chart components before CSS placeholders.',
  },
];

function printUsage() {
  console.error(`Usage:
  node blade.js score <url> [--threshold 95] [--no-navbars] [--headed] [--json] [--state path] [--profile name-or-path] [--session name] [--settle-ms 1000] [--timeout-ms 30000]
  node blade.js audit [path] [--json]
  node blade.js gate <url> [path] [--threshold 95] [--no-navbars] [--headed] [--json] [--state path] [--profile name-or-path] [--session name] [--settle-ms 1000] [--timeout-ms 30000]`);
}

function parseArgs(argv) {
  if (argv.includes('--help') || argv.includes('-h')) {
    printUsage();
    process.exit(EXIT.OK);
  }

  const args = [...argv];
  let command = args[0];
  if (!command || command.startsWith('-') || command.startsWith('http://') || command.startsWith('https://')) {
    command = 'score';
  } else {
    args.shift();
  }

  const options = {
    command,
    url: null,
    auditPath: null,
    threshold: command === 'gate' ? 95 : null,
    includeNavbars: true,
    headed: false,
    jsonOutput: false,
    state: null,
    profile: null,
    session: null,
    keepOpen: false,
    agentBrowserBin: 'agent-browser',
    settleMs: 1000,
    timeoutMs: 30000,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('http://') || arg.startsWith('https://')) {
      options.url = arg;
    } else if (arg === '--threshold') {
      options.threshold = parseFloat(args[++i]);
    } else if (arg === '--no-navbars') {
      options.includeNavbars = false;
    } else if (arg === '--headed') {
      options.headed = true;
    } else if (arg === '--json') {
      options.jsonOutput = true;
    } else if (arg === '--agent-browser-bin') {
      options.agentBrowserBin = args[++i];
    } else if (arg === '--session') {
      options.session = args[++i];
    } else if (arg === '--profile') {
      options.profile = args[++i];
    } else if (arg === '--state') {
      options.state = args[++i];
    } else if (arg === '--keep-open') {
      options.keepOpen = true;
    } else if (arg === '--settle-ms') {
      options.settleMs = parseInt(args[++i], 10);
    } else if (arg === '--timeout-ms') {
      options.timeoutMs = parseInt(args[++i], 10);
    } else if (!arg.startsWith('-')) {
      options.auditPath = arg;
    } else {
      throw new Error(`Unknown flag: ${arg}`);
    }
  }

  if (!['score', 'audit', 'gate'].includes(options.command)) {
    throw new Error(`Unknown command: ${options.command}`);
  }
  if ((options.command === 'score' || options.command === 'gate') && !options.url) {
    throw new Error(`${options.command} requires a URL`);
  }
  if (options.threshold !== null && (Number.isNaN(options.threshold) || options.threshold < 0)) {
    throw new Error('--threshold must be a non-negative number');
  }

  options.auditPath = path.resolve(options.auditPath || process.cwd());
  return options;
}

function collectFiles(root) {
  const files = [];
  const stack = [root];

  while (stack.length > 0) {
    const current = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch (_) {
      continue;
    }

    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (!SKIP_DIRS.has(entry.name)) stack.push(fullPath);
      } else if (entry.isFile() && SOURCE_EXTENSIONS.has(path.extname(entry.name))) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

function lineAndColumn(content, index) {
  let line = 1;
  let column = 1;
  for (let i = 0; i < index; i++) {
    if (content.charCodeAt(i) === 10) {
      line++;
      column = 1;
    } else {
      column++;
    }
  }
  return { line, column };
}

function readBladeImports(content) {
  if (!BLADE_IMPORT_RE.test(content)) return new Set();
  const imports = new Set();
  const importRe = /import\s*\{([\s\S]*?)\}\s*from\s*['"]@razorpay\/blade\/components['"]/g;
  let match;
  while ((match = importRe.exec(content)) !== null) {
    match[1]
      .split(',')
      .map((item) => item.trim().split(/\s+as\s+/)[0].trim())
      .filter(Boolean)
      .forEach((item) => imports.add(item));
  }
  return imports;
}

function pushIssue(issues, root, filePath, content, index, rule, evidence) {
  const position = lineAndColumn(content, index);
  issues.push({
    id: rule.id,
    severity: rule.severity,
    filePath: path.relative(root, filePath),
    line: position.line,
    column: position.column,
    message: rule.message,
    evidence: evidence.trim().slice(0, 180),
  });
}

function auditPath(root) {
  if (!fs.existsSync(root)) {
    throw new Error(`Audit path does not exist: ${root}`);
  }

  const files = collectFiles(root);
  const issues = [];

  for (const filePath of files) {
    const ext = path.extname(filePath);
    let content;
    try {
      content = fs.readFileSync(filePath, 'utf8');
    } catch (_) {
      continue;
    }

    for (const rule of DRIFT_RULES) {
      if (!rule.file.test(ext)) continue;
      rule.regex.lastIndex = 0;
      let match;
      while ((match = rule.regex.exec(content)) !== null) {
        pushIssue(issues, root, filePath, content, match.index, rule, match[0]);
      }
    }

    if (/\.(tsx?|jsx?)$/.test(ext) && BLADE_IMPORT_RE.test(content)) {
      const imports = readBladeImports(content);
      for (const rule of SEMANTIC_IMPORT_RULES) {
        if (!rule.terms.test(content)) continue;
        if (rule.imports.some((importName) => imports.has(importName))) continue;
        const index = content.search(rule.terms);
        pushIssue(issues, root, filePath, content, Math.max(index, 0), rule, RegExp.lastMatch || rule.id);
      }
    }
  }

  const counts = issues.reduce(
    (acc, issue) => {
      acc[issue.severity] = (acc[issue.severity] || 0) + 1;
      return acc;
    },
    { high: 0, medium: 0 },
  );

  return {
    path: root,
    filesScanned: files.length,
    issueCount: issues.length,
    counts,
    issues,
  };
}

async function runScore(options) {
  const session = options.session || `blade-${process.pid}-${Date.now()}`;
  const env = {
    ...process.env,
    AGENT_BROWSER_DEFAULT_TIMEOUT: String(options.timeoutMs),
  };

  try {
    runAgentBrowser(options, ['--session', session, ...browserLaunchFlags(options), 'open', options.url], {
      env,
    });

    if (options.settleMs > 0) {
      runAgentBrowser(options, ['--session', session, 'wait', String(options.settleMs)], { env });
    }

    const script = BLADE_COVERAGE_FN.replace('__INCLUDE_NAVBARS__', options.includeNavbars ? 'true' : 'false');
    const evalOutput = runAgentBrowser(
      options,
      ['--session', session, 'eval', '--stdin', '--json'],
      {
        env,
        input: script,
      },
    );
    const parsed = JSON.parse(evalOutput);
    if (!parsed.success) {
      throw new Error(parsed.error || 'agent-browser eval failed');
    }
    const result = parsed.data && parsed.data.result;
    if (!result || typeof result.bladeCoverage !== 'number') {
      throw new Error('agent-browser eval did not return Blade coverage data');
    }

    const pass = options.threshold === null || result.bladeCoverage >= options.threshold;
    return {
      exitCode: pass ? EXIT.OK : EXIT.COVERAGE_FAIL,
      result: {
        url: options.url,
        ...result,
        threshold: options.threshold,
        pass,
      },
    };
  } catch (err) {
    const message = err.message || String(err);
    const exitCode = /not found|ENOENT|command not found/i.test(message) ? EXIT.SETUP_FAIL : EXIT.NAVIGATION_FAIL;
    return { exitCode, error: `agent-browser failed: ${message}` };
  } finally {
    if (!options.keepOpen && !options.session) {
      closeAgentBrowserSession(options, session, env);
    }
  }
}

function browserLaunchFlags(options) {
  const flags = [];
  if (options.headed) flags.push('--headed');
  if (options.state) flags.push('--state', options.state);
  if (options.profile) flags.push('--profile', options.profile);
  return flags;
}

function runAgentBrowser(options, args, commandOptions = {}) {
  const result = childProcess.spawnSync(options.agentBrowserBin, args, {
    cwd: process.cwd(),
    encoding: 'utf8',
    input: commandOptions.input,
    env: commandOptions.env || process.env,
    maxBuffer: 10 * 1024 * 1024,
  });

  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    const output = [result.stderr, result.stdout].filter(Boolean).join('\n').trim();
    throw new Error(output || `${options.agentBrowserBin} ${args.join(' ')} exited ${result.status}`);
  }
  return result.stdout.trim();
}

function closeAgentBrowserSession(options, session, env) {
  try {
    childProcess.spawnSync(options.agentBrowserBin, ['--session', session, 'close'], {
      cwd: process.cwd(),
      encoding: 'utf8',
      env,
      maxBuffer: 1024 * 1024,
    });
  } catch (_) {}
}

function printAudit(audit) {
  console.log(`Blade Audit: ${audit.path}`);
  console.log(`Files Scanned: ${audit.filesScanned}`);
  console.log(`Issues: ${audit.issueCount} (${audit.counts.high || 0} high, ${audit.counts.medium || 0} medium)`);
  if (audit.issues.length === 0) return;

  console.log('\nFindings:');
  for (const issue of audit.issues.slice(0, 80)) {
    console.log(
      `- [${issue.severity.toUpperCase()}] ${issue.filePath}:${issue.line}:${issue.column} ${issue.id} - ${issue.message}`,
    );
  }
  if (audit.issues.length > 80) {
    console.log(`- ... ${audit.issues.length - 80} more findings omitted`);
  }
}

function printScore(score) {
  const result = score.result;
  console.log(`Blade Coverage: ${result.bladeCoverage}%`);
  console.log(`Blade Nodes:    ${result.bladeNodes} / ${result.totalNodes}`);
  if (result.threshold !== null) {
    console.log(`Verdict:        ${result.pass ? 'PASS' : `FAIL (threshold: ${result.threshold}%)`}`);
  }
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (err) {
    printUsage();
    console.error(`\n${err.message}`);
    process.exit(EXIT.SETUP_FAIL);
  }

  try {
    if (options.command === 'audit') {
      const audit = auditPath(options.auditPath);
      if (options.jsonOutput) {
        console.log(JSON.stringify({ command: 'audit', ...audit }));
      } else {
        printAudit(audit);
      }
      process.exit(EXIT.OK);
    }

    if (options.command === 'score') {
      const score = await runScore(options);
      if (options.jsonOutput) {
        console.log(JSON.stringify({ command: 'score', ...(score.result || {}), error: score.error }));
      } else if (score.error) {
        console.error(score.error);
      } else {
        printScore(score);
      }
      process.exit(score.exitCode);
    }

    const score = await runScore(options);
    if (score.exitCode === EXIT.SETUP_FAIL || score.exitCode === EXIT.NAVIGATION_FAIL) {
      if (options.jsonOutput) {
        console.log(JSON.stringify({ command: 'gate', score: score.result || null, error: score.error }));
      } else {
        console.error(score.error);
      }
      process.exit(score.exitCode);
    }

    const audit = auditPath(options.auditPath);
    const driftPass = (audit.counts.high || 0) === 0;
    const pass = score.exitCode === EXIT.OK && driftPass;
    const exitCode =
      score.exitCode !== EXIT.OK ? score.exitCode : driftPass ? EXIT.OK : EXIT.DRIFT_FAIL;

    if (options.jsonOutput) {
      console.log(
        JSON.stringify({
          command: 'gate',
          pass,
          score: score.result,
          audit,
        }),
      );
    } else {
      printScore(score);
      console.log('');
      printAudit(audit);
      console.log(`\nGate: ${pass ? 'PASS' : 'FAIL'}`);
    }
    process.exit(exitCode);
  } catch (err) {
    if (options && options.jsonOutput) {
      console.log(JSON.stringify({ command: options.command, error: err.message }));
    } else {
      console.error(`Error: ${err.message}`);
    }
    process.exit(EXIT.SETUP_FAIL);
  }
}

main();
