# Agent Browser Workflow

Use `agent-browser` for browser-related Blade work. Do not use Playwright for this skill.

## Why

Agent Browser is a native Rust CLI built for AI agents. It keeps output compact, exposes refs from accessibility snapshots, persists browser sessions through a daemon, and supports screenshots, network/storage inspection, CDP connections, profile/state reuse, dashboard streaming, and diffing.

## Setup check

```bash
agent-browser --version
agent-browser doctor --offline --quick
```

If it is missing:

```bash
npm install -g agent-browser
agent-browser install
```

## Core loop

```bash
agent-browser open http://localhost:3000
agent-browser snapshot -i
agent-browser click @e2
agent-browser snapshot -i
```

Rules:
- Prefer refs from `snapshot -i` over CSS selectors.
- Re-snapshot after navigation, DOM updates, modal open/close, or route changes.
- Use `screenshot --annotate` when text snapshots are not enough for layout/icon/canvas checks.
- Use `diff snapshot` after an interaction to prove the page changed.
- Use `diff screenshot --baseline <file>` for visual regression checks.

## Auth and dashboard work

Fast paths:

```bash
agent-browser --profile Default open https://x.razorpay.com
agent-browser --state ./auth.json open https://x.razorpay.com/app/dashboard
agent-browser --session-name dashboard open https://x.razorpay.com/app/dashboard
```

For already-authenticated Chrome:

```bash
agent-browser --auto-connect state save ./auth.json
agent-browser --state ./auth.json open https://x.razorpay.com/app/dashboard
```

State files contain auth tokens. Keep them out of git.

## Useful commands for Blade validation

```bash
agent-browser get text @e1
agent-browser get styles @e1
agent-browser console
agent-browser errors
agent-browser network requests --filter api
agent-browser set viewport 1440 900
agent-browser set device "iPhone 14"
agent-browser wait --text "Payments"
agent-browser wait --url "**/dashboard"
```

Use the observability dashboard for longer debugging sessions:

```bash
agent-browser dashboard start
agent-browser open http://localhost:3000
```

Open `http://localhost:4848` to see the live viewport and command feed.

## Safety defaults

For untrusted sites or production-like agent runs, use:

```bash
agent-browser --content-boundaries --max-output 50000 --allowed-domains "your-app.com,*.your-app.com" open https://your-app.com
```

Use action policy or confirmation for risky actions such as `eval`, downloads, and uploads.
