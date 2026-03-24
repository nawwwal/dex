---
name: agent-browser
description: "Use when automating browser interactions — login flows, form submission, screenshots, data extraction, or testing. Use auth vault for username/password forms, --headed for Google/OAuth (headless triggers CAPTCHA), --profile for persistent sessions, login-machine agent for complex SSO flows."
allowed-tools: Bash(agent-browser:*)
---

# Browser Automation with agent-browser

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Decision Guide

| Need | Use |
|------|-----|
| Simple form login (username+password) | `auth save` + `auth login` |
| Google/OAuth/SSO login | `--headed` + manual sign-in + `state save` |
| Complex SSO (magic links, popups) | `login-machine` agent |
| Import existing Chrome session | `--auto-connect state save` |
| Persist auth across runs (same app) | `--profile ~/.agent-browser/myapp` |
| One-off auth export / cross-machine | `state save` / `state load` |
| Watch AI browse live | `AGENT_BROWSER_STREAM_PORT=9223` |
| Untrusted page content | `--content-boundaries` |
| Restrict navigation domains | `--allowed-domains` |
| Parallel tasks | `--session name1` / `--session name2` |

## Auth Patterns

### Google / OAuth (headless triggers CAPTCHA — always use `--headed`)

```bash
# Option 1: Import from a running Chrome session (zero re-login)
agent-browser --auto-connect state save ~/.agent-browser/google-auth.json
# ⚠️ Only use --auto-connect when you know Chrome is running with the right session
# Load saved state in future headless runs:
agent-browser state load ~/.agent-browser/google-auth.json
agent-browser open https://target.com

# Option 2: Fresh headed login
agent-browser --headed open https://accounts.google.com
# Sign in manually in the window, then save:
agent-browser state save ~/.agent-browser/google-auth.json
agent-browser close
```

### Simple username/password (auth vault — LLM never sees password)

```bash
# Save once (AES-256-GCM encrypted, stored in ~/.agent-browser/auth/)
agent-browser auth save myapp \
  --url https://app.example.com/login \
  --username user@example.com --password mypass

# Reuse any time (no re-entering credentials):
agent-browser auth login myapp
```

### Persistent profile (simplest for repeated access)

```bash
# Cookies + localStorage survive across runs automatically
agent-browser --profile ~/.agent-browser/myapp-profile open https://app.example.com
# Next run with same --profile: already logged in, no save/load needed
```

Use `--profile` when you access the same app repeatedly. Use `state save/load` for one-off exports or cross-machine sharing.

### Complex SSO / magic links / popup flows

Delegate to the `login-machine` agent — it handles credential forms, OAuth redirects, loading screens, and popup blockers automatically. Use `auth save` + `auth login` only for simple static forms.

## Streaming (pair browsing)

```bash
# Human watches + can interact alongside AI
AGENT_BROWSER_STREAM_PORT=9223 agent-browser open <url>
# Open ws://localhost:9223 in a browser viewer
```

## Security Defaults

For tasks involving untrusted page content:

```bash
agent-browser --content-boundaries snapshot        # Nonce-wrapped output (prompt injection guard)
agent-browser --allowed-domains "example.com" open ...  # Block off-domain navigation
agent-browser --max-output 50000 get text body     # Cap context flood from large pages
```

## Commands

### Navigation
```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (page analysis)
```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
agent-browser snapshot -C         # Include cursor-interactive elements (onclick, cursor:pointer)
```

### Interactions (use @refs from snapshot)
```bash
agent-browser click @e1                    # Click
agent-browser click @e1 --new-tab          # Open link in new tab
agent-browser dblclick @e1                 # Double-click
agent-browser focus @e1                    # Focus element
agent-browser fill @e2 "text"              # Clear and type
agent-browser type @e2 "text"              # Type without clearing
agent-browser press Enter                  # Press key
agent-browser press Control+a              # Key combination
agent-browser keydown Shift                # Hold key down
agent-browser keyup Shift                  # Release key
agent-browser hover @e1                    # Hover
agent-browser check @e1                    # Check checkbox
agent-browser uncheck @e1                  # Uncheck checkbox
agent-browser select @e1 "value"           # Select dropdown
agent-browser scroll down 500              # Scroll page
agent-browser scroll down 500 --selector "#feed"  # Scroll within container
agent-browser scrollintoview @e1           # Scroll element into view
agent-browser drag @e1 @e2                 # Drag and drop
agent-browser upload @e1 file.pdf          # Upload files
agent-browser keyboard type "text"         # Type globally (no selector needed)
agent-browser keyboard inserttext "text"   # Insert text globally (no selector needed)
```

### Get information
```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get styles @e1      # Get computed CSS styles
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get cdp-url         # Get CDP WebSocket URL for active page
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
```

### Check state
```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### Screenshots & PDF
```bash
agent-browser screenshot                            # Screenshot to stdout
agent-browser screenshot path.png                   # Save to file
agent-browser screenshot --full                     # Full page
agent-browser screenshot --annotate                 # Overlay numbered labels → @eN refs
agent-browser screenshot --screenshot-dir ./shots   # Output directory
agent-browser screenshot --screenshot-quality 80    # 0–100 quality
agent-browser screenshot --screenshot-format webp   # png / jpeg / webp
agent-browser pdf output.pdf                        # Save as PDF
```

### Clipboard
```bash
agent-browser clipboard read           # Read clipboard contents
agent-browser clipboard write "text"   # Write to clipboard
agent-browser clipboard copy           # Ctrl+C (copy selection)
agent-browser clipboard paste          # Ctrl+V (paste)
```

### Diff
```bash
agent-browser diff snapshot                          # Compare current vs baseline accessibility tree
agent-browser diff screenshot --baseline base.png    # Visual diff between screenshots
agent-browser diff url https://example.com           # Compare current page vs URL
```

### Video recording
```bash
agent-browser record start ./demo.webm    # Start recording
agent-browser record stop                 # Stop and save video
agent-browser record restart ./take2.webm # Stop current + start new recording
```

### Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "**/dashboard"    # Wait for URL pattern
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --fn "window.ready"     # Wait for JS condition
```

### Mouse control
```bash
agent-browser mouse move 100 200      # Move mouse
agent-browser mouse down left         # Press button
agent-browser mouse up left           # Release button
agent-browser mouse wheel 100         # Scroll wheel
```

### Semantic locators (alternative to refs)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

### Browser settings
```bash
agent-browser set viewport 1920 1080           # Set viewport size
agent-browser set viewport 1920 1080 --scale 2 # Retina / HiDPI scale factor
agent-browser set device "iPhone 14"           # Emulate device
agent-browser set geo 37.7749 -122.4194        # Set geolocation
agent-browser set offline on                   # Toggle offline mode
agent-browser set headers '{"X-Key":"v"}'      # Extra HTTP headers
agent-browser set credentials user pass        # HTTP basic auth
agent-browser set media dark                   # Emulate color scheme
agent-browser --color-scheme dark open <url>   # Persistent dark/light preference
agent-browser --ignore-https-errors open <url> # Self-signed certificate support
agent-browser --allow-file-access open file:// # Enable file:// URLs (PDFs, local HTML)
agent-browser --engine lightpanda open <url>   # Lightpanda fast headless engine
```

### Cookies & Storage
```bash
agent-browser cookies                                                              # Get all cookies
agent-browser cookies set name value                                               # Set cookie
agent-browser cookies set name value --httpOnly --secure --domain .ex.com --expires 3600
agent-browser cookies clear                                                        # Clear cookies
agent-browser storage local                # Get all localStorage
agent-browser storage local key            # Get specific key
agent-browser storage local set k v        # Set value
agent-browser storage local clear          # Clear all
```

### Network
```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests (method, URL, type)
agent-browser network requests --filter api    # Filter requests
```

### Tabs & Windows
```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab
agent-browser tab close           # Close tab
agent-browser window new          # New window
```

### Frames
```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

### Dialogs
```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

### JavaScript
```bash
agent-browser eval "document.title"       # Run JavaScript
agent-browser eval --stdin                 # Read JS from stdin (heredoc support)
agent-browser eval -b "base64script"       # Base64-encoded script (avoids shell escaping)
```

### State management
```bash
agent-browser state save auth.json    # Save browser state (cookies + localStorage)
agent-browser state load auth.json    # Restore saved state
agent-browser state list              # List all saved states
agent-browser state show auth.json    # Show state metadata
agent-browser state rename old new    # Rename saved state
agent-browser state clear             # Delete all saved states
```

### Auth vault (encrypted credentials)
```bash
agent-browser auth save <name>    # Save login credentials (AES-256-GCM encrypted)
agent-browser auth login <name>   # Login using saved credentials
agent-browser auth list           # List saved credential sets
agent-browser auth show <name>    # Show credential details
agent-browser auth delete <name>  # Delete credentials
```

### Action policy & safety
```bash
agent-browser --allowed-domains "example.com,api.example.com" open <url>  # Restrict navigation
agent-browser --action-policy allow open <url>             # Restrict action categories
agent-browser --confirm-actions open <url>                 # Require confirmation per action
agent-browser --confirm-interactive open <url>             # Human-in-the-loop (60s auto-deny)
agent-browser confirm                                      # Approve pending action
agent-browser deny                                         # Deny pending action
agent-browser --max-output 10000 snapshot                  # Truncate large outputs
agent-browser --content-boundaries snapshot                # Wrap output with nonce delimiters
```

### Download
```bash
agent-browser download <url>                          # Trigger and await download
agent-browser --download-path ./downloads open <url>  # Set default download directory
```

### Inspect / DevTools
```bash
agent-browser inspect    # Open Chrome DevTools via local proxy (agent commands still work)
```

### Profiler
```bash
agent-browser profiler start    # Start CPU/memory profiler
agent-browser profiler stop     # Stop and print report
```

### iOS / Mobile (requires Appium)
```bash
agent-browser device list
agent-browser -p ios --device "iPhone 15" open <url>
agent-browser tap @e1
agent-browser swipe up 500
```

### Cloud providers
```bash
agent-browser -p browserbase open <url>    # Browserbase (env: BROWSERBASE_API_KEY)
agent-browser -p kernel open <url>         # Kernel stealth mode (env: KERNEL_API_KEY)
agent-browser -p browserless open <url>    # Browserless.io (env: BROWSERLESS_TOKEN)
```

### Persistent profiles & sessions
```bash
agent-browser --profile myprofile open <url>     # Persist cookies/localStorage across runs
agent-browser --session-name myapp open <url>    # Auto save/restore session state by name
```

### Browser launch flags
```bash
agent-browser --args "--disable-web-security" open <url>
agent-browser --user-agent "Custom/1.0" open <url>
agent-browser --proxy socks5://host:1080 open <url>
agent-browser --proxy-bypass "localhost,127.0.0.1" open <url>
agent-browser --extension ./my-extension open <url>
```

### Connect (CDP WebSocket)
```bash
agent-browser connect wss://cdp.browserbase.io/...   # Persist CDP connection for subsequent commands
```

## Example: Form submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

## Example: Authentication with saved state

```bash
# Login once, save state
agent-browser open https://app.example.com/login
agent-browser fill @e1 "username" && agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later: restore and continue
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Example: Annotated screenshot for element targeting

```bash
agent-browser screenshot --annotate   # Labels interactive elements with @e1, @e2...
agent-browser click @e3               # Use label from screenshot
```

## Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## JSON output (for parsing)

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Debugging

```bash
agent-browser open example.com --headed    # Show browser window
agent-browser inspect                      # Open Chrome DevTools proxy
agent-browser console                      # View console messages
agent-browser console --clear              # Clear console
agent-browser errors                       # View page errors
agent-browser errors --clear               # Clear errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                  # Start recording trace
agent-browser trace stop trace.zip         # Stop and save trace
agent-browser --cdp 9222 snapshot          # Connect via CDP port
```

## Config file

Auto-loaded (lower → higher priority): `~/.agent-browser/config.json` → `./agent-browser.json` → CLI flags.

```json
{ "headed": false, "annotate": true, "color-scheme": "dark" }
```

## Key env vars

```
AGENT_BROWSER_PROVIDER=browserbase|kernel|browserless
AGENT_BROWSER_ANNOTATE=1
AGENT_BROWSER_COLOR_SCHEME=dark|light
AGENT_BROWSER_ENGINE=lightpanda
AGENT_BROWSER_ALLOWED_DOMAINS=example.com
AGENT_BROWSER_MAX_OUTPUT=10000
AGENT_BROWSER_DEFAULT_TIMEOUT=25000
```
