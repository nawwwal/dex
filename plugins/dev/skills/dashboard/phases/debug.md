# Phase: Running and Debugging Local Dashboard

Use this when the user wants to run, inspect, or debug Dashboard locally. The hard rule: validate the product in a real Chrome profile when request headers are part of the setup. Do not patch application code just to fake browser headers.

## First decide what to run

Before starting servers, identify the micro-app. Do not start the whole monorepo by default.

If the user names the app or route, infer the micro-app and proceed:

- Agent Studio, Agent Marketplace, `/app/agent-studio/...` → `agent-marketplace`
- Payments dashboard, Transactions, Settlements, Payment Links, legacy Payments routes → `payments-dashboard` or the legacy shell route that owns the page
- One Home, `/app/home` or `/home` → `one-home`
- Partnership, partners, submerchants, affiliates → `partnership`
- Invoices → `invoices`
- Customers → `customers`
- Onboarding → `onboarding-experience`

If it is not obvious, ask one direct question:

> "Which Dashboard micro-app do you want to run locally? Examples: `agent-marketplace`, `one-home`, `partnership`, `payments-dashboard`."

If they describe a page instead of an app, map it to the closest app and state the assumption before running commands:

> "I’m treating Agent Studio as the `agent-marketplace` micro-app."

Verify the project name from the repo root when uncertain:

```bash
pnpm nx show projects | grep <name-or-keyword>
```

If multiple micro-apps are needed for the page, start only those named remotes plus shell.

## Local connection model

Dashboard local-shell access is a handoff, not a direct localhost login:

1. Local shell server runs on `https://localhost:8888`.
2. Browser goes to `https://dashboard.dev.razorpay.in/...`.
3. ModHeader adds request headers on the devstack request.
4. Devstack reads the existing logged-in Dashboard session and redirects back to `https://localhost:8888/...` with the local session material.
5. Localhost finishes loading the Dashboard shell and the feature route.

Starting directly at `https://localhost:8888` without a seeded session usually causes an Accounts/login loop. Treat that as an environment setup issue, not an app bug.

## Required browser setup

Use the `chrome:control-chrome` skill when the user has ModHeader installed in Chrome. Prefer this over the in-app browser for local Dashboard work because the in-app browser cannot use the user's ModHeader extension or existing Chrome login state.

Use `agent-skills:browser-testing-with-devtools` for the debugging loop after Chrome is attached: reproduce the route, inspect visible DOM, check console errors, inspect network failures, form a hypothesis, then verify the route again.

Use the in-app browser only for flows that do not depend on ModHeader, Chrome extensions, or the user's existing logged-in Chrome session.

ModHeader must be enabled in the Chrome profile used for testing. Configure the rule globally for the Dashboard testing profile, not only for `localhost`, because the important first request is to `dashboard.dev.razorpay.in` and login redirects may cross hosts.

Required headers:

```text
local-shell: true
rzpctx-dev-serve-user: <devstack label>
```

Example label values: `gagan-test7`, `base`, or the active devstack label the user names.

Do not hardcode these headers in Dashboard source code. Do not seed cookies by app code. Do not inspect, print, or store cookies, localStorage, sessionStorage, passwords, or session tokens.

## Start or verify local services

From the dashboard repo root:

```bash
pnpm nx serve:development:browser <micro-app>
pnpm nx serve:development:server shell
```

For Agent Studio:

```bash
pnpm nx serve:development:browser agent-marketplace
pnpm nx serve:development:server shell
```

Start the micro-app browser/remote first, then the shell server. If one of the ports is already serving the same app, reuse it and verify instead of starting a duplicate.

Common local ports:

- `https://localhost:8888` — shell server
- `http://localhost:8000` and `http://localhost:8080` — browser/remotes, depending on the app setup

Verify the shell server with a narrow check:

```bash
curl -sk -o /tmp/local-shell-head.txt -w '%{http_code}\n' https://localhost:8888/
```

`200` means the shell is reachable. It does not prove auth, ModHeader, Splitz, or feature APIs are working.

## Attach to the right Chrome

When multiple Chrome windows or profiles are open, do not assume `agent.browsers.get("extension")` is the right one.

1. List Chrome extension instances.
2. Prefer the instance whose metadata has the expected `profileName` or whose open tabs match the user's active Dashboard work.
3. If browser instance IDs rotate after a kernel reset, re-list and match by metadata/open tabs again.
4. Claim a user tab with `browser.user.claimTab(...)` before inspecting it.
5. Before ending, call `browser.tabs.finalize({ keep: [{ tab, status: "handoff" }] })` for the verified tab.

Useful proof signals:

- Correct profile metadata, for example `profileName: "razorpay.com"`.
- Final URL starts with `https://localhost:8888/`.
- Page title is `Razorpay Dashboard`.
- Visible text contains the target product, for example `Agent Studio`, `My Agents`, `Connectors`.
- Visible text does not contain Accounts/login copy such as `Continue as`, `Sign Up`, or `Google accounts`.

## Handoff verification flow

Use a fresh tab in the correct Chrome profile:

1. Open `https://dashboard.dev.razorpay.in/app/<feature-path>`.
2. Wait for redirect.
3. Expected final URL: `https://localhost:8888/app/<feature-path>`.
4. Verify visible product content, not only the URL.
5. Check console/network only after the route and visible page state are known.

For Agent Studio examples:

```text
https://dashboard.dev.razorpay.in/app/agent-studio/apps
https://dashboard.dev.razorpay.in/app/agent-studio/my-agents
```

Expected localhost routes:

```text
https://localhost:8888/app/agent-studio/apps
https://localhost:8888/app/agent-studio/my-agents
```

## Failure diagnosis

**Lands on `accounts.np.razorpay.in`**
- The selected Chrome profile is not logged into Dashboard dev, or the ModHeader rule did not apply to the devstack request.
- Switch to the Chrome profile the user actually uses for Dashboard, or ask them to log in there.

**Lands on `dashboard.dev.razorpay.in` and never returns to localhost**
- `local-shell: true` is missing, disabled, or scoped too narrowly.
- Confirm ModHeader is enabled globally for the Dashboard testing profile.

**Loops between Accounts and localhost**
- Localhost was opened before the devstack handoff seeded the local session, or the wrong browser/profile was used.
- Start from `dashboard.dev.razorpay.in` in the correct Chrome profile.

**Localhost returns `200`, but the app is blank or stuck**
- Server reachability is fine, but app hydration, remotes, Splitz, or downstream APIs may be failing.
- Inspect visible DOM first, then console errors, then network failures.

**Console has React warnings**
- Do not treat warnings as the connection failure if the route is visibly loaded and usable.
- Capture them separately as app-quality issues only when relevant to the user's task.

## Splitz and flags

Do not comment out Splitz gates or hardcode treatment values for local browser access. Use a real test account/devstack label or a code-reviewed local mock only when the task is explicitly about mocked local development. Remove any local bypass before PR or sharing.

## What to report

For the user, lead with the observed route state:

> "Verified in Chrome profile `[profile]`: `[devstack URL]` redirects to `[localhost URL]`, and the page shows `[visible product text]`."

If blocked, name the exact broken layer: wrong Chrome profile, missing ModHeader headers, not logged in, local server down, route loaded but API failed, or app render error.
