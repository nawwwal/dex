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
agent-browser --state "${TMPDIR:-/tmp}/blade-auth-state.json" open https://x.razorpay.com/app/dashboard
agent-browser --session dashboard open https://x.razorpay.com/app/dashboard
```

For already-authenticated Chrome:

```bash
AUTH_STATE=$(mktemp "${TMPDIR:-/tmp}/blade-auth-state.XXXXXX.json")
chmod 600 "$AUTH_STATE"
agent-browser --auto-connect state save "$AUTH_STATE"
agent-browser --state "$AUTH_STATE" open https://x.razorpay.com/app/dashboard
```

State files contain auth tokens. Keep them outside the repo, `chmod 600` them, delete them after use, and never commit them.

## When auth blocks verification

Authenticated dashboard flows often redirect in headless or fresh browser sessions. Do not pretend source inspection proves motion or DOM behavior.

Use this fallback order:

1. Try an existing authenticated profile or saved state with `--profile`, `--state`, or `--session`.
2. If Chrome has the live session, save state to a temp file outside the repo, then retry with `--state`.
3. If auth still blocks the route, run static checks and tests, then state the missing observation explicitly:

```text
Runtime verification: blocked by auth redirect at /app/...
Verified instead: <only the checks actually run, such as Blade MCP docs checked, source structure inspected, typecheck passed, blade audit run>
Not verified: hover/tap motion intensity, carousel visual width, focus-visible behavior in live DOM.
```

For motion-sensitive changes, try to create or locate an unauthenticated local story, fixture route, or test harness before closing. If none exists, leave the runtime gap in the final note.

## Runtime proof packet

For authenticated or stateful product flows, report these before treating browser validation as complete:

```text
Route reached: <final URL and expected route marker>
Auth mode: <state/profile/session/manual, or blocked>
Tenant/data state: <safe marker such as page heading, account switcher state, empty/error/loading/data variant>
Console/network: <no blocking console errors and no critical failed API calls, or list blockers>
Interaction proof: <snapshot/diff/screenshot before and after>
Focus/keyboard: <tab/focus path for changed controls or why not applicable>
Responsive fit: <desktop and narrow/mobile viewport checked, or blocker>
```

If this packet is incomplete, say `Blade compliance checked; runtime incomplete` and name the missing proof.

For interaction-quality work, add one more line:

```text
Feel check: <stable bounds | no overlap | no text blur | density preserved | motion skipped because high frequency>
```

## Useful commands for Blade validation

```bash
agent-browser get text @e1
agent-browser get styles @e1
agent-browser console
agent-browser errors
agent-browser network requests --filter api
agent-browser set viewport 1440 900
agent-browser set viewport 390 844
agent-browser wait --text "Payments"
agent-browser wait --url "**/dashboard"
```

Minimum viewport and a11y checks for changed UI:

| Change | Must check | Evidence |
| --- | --- | --- |
| Desktop product surface | `1440x900` viewport | Screenshot or annotated screenshot plus no overlap/truncation. |
| Mobile/narrow surface | `390x844` viewport or matching device preset | Overlay position, bottom sheet/drawer behavior, readable text, no horizontal scroll. |
| Interactive control | Keyboard tab path and focus-visible state | Snapshot before/after focus or concise focus path. |
| Overlay/disclosure | Open, close, Escape/backdrop behavior, focus return | Snapshot/diff and route marker after close. |
| Motion-sensitive change | Before/after diff plus stable bounds check | No parent resizing, hidden click layer, text blur, or focus trap. |

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
