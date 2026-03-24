# Agentation — Visual Annotation for AI Agents

Browser-based annotation toolbar that lets you drop visual notes on a running UI, then syncs those notes to Claude Code via MCP. Like DialKit for parameters, but for design feedback.

**MCP status:** Agentation MCP is installed in this vault. Verify with `agentation_get_all_pending` (no args required — use this, not `agentation_get_pending` which requires a sessionId). If it returns an error, Agentation is not installed — request screenshots manually instead.

**MCP tool prefix:** Claude Code exposes these as `mcp__agentation__agentation_*` in tool lists. In prose and skill instructions, use the short names (e.g. `agentation_watch_annotations`) — Claude Code resolves them.

## Setup

```bash
# Install the React component
npm install agentation -D

# Add to your app (development only)
{process.env.NODE_ENV === "development" && <Agentation />}
```

```bash
# Set up the MCP server (enables Claude Code to read annotations)
npx agentation-mcp init
# Then restart Claude Code — MCP starts automatically on launch
```

Default port: 4747.

## Annotation Modes

| Mode | Use when |
|---|---|
| **Text** | Flagging specific copy, labels, error messages |
| **Element** | Annotating a specific UI component |
| **Area** | Drawing a bounding box over a region |
| **Multi-Select** | Selecting multiple elements simultaneously (markers turn green) |
| **Animation** | Press Pause first to freeze the animation state, then annotate |

## Annotation Anatomy

Each annotation exposes:

```json
{
  "id": "ann_123",
  "comment": "Button is cut off on mobile",
  "element": "button",
  "elementPath": "body > main > .hero > button.cta",
  "reactComponents": "App > LandingPage > HeroSection > Button",
  "intent": "fix",
  "severity": "blocking"
}
```

- **intent**: `fix` | `change` | `question` | `approve`
- **severity**: `blocking` | `important` | `suggestion`

## All 9 MCP Tools

| Tool | Purpose |
|---|---|
| `agentation_list_sessions` | List all active annotation sessions |
| `agentation_get_session(sessionId)` | Get a session with all its annotations |
| `agentation_get_pending(sessionId)` | Get unresolved annotations for a session |
| `agentation_get_all_pending()` | Get unresolved annotations across all sessions |
| `agentation_acknowledge(annotationId)` | Mark as seen (before fixing) |
| `agentation_resolve(annotationId, summary?)` | Mark as fixed — annotation disappears from toolbar |
| `agentation_dismiss(annotationId, reason)` | Reject with a reason |
| `agentation_reply(annotationId, message)` | Add a reply to the annotation thread |
| `agentation_watch_annotations(sessionId?, batchWindowSeconds?, timeoutSeconds?)` | Block until annotations arrive, then return a batch |

## Watch Mode (Annotation Loop)

Set up a continuous feedback loop: you annotate, Claude fixes:

```
1. Call agentation_watch_annotations (blocks for up to 120s waiting for annotations)
2. Receive batch of new annotations
3. For each annotation:
   a. agentation_acknowledge(id) — mark as seen
   b. Find element via elementPath or reactComponents
   c. Edit the code
   d. agentation_resolve(id, "Fixed: changed color to surface.action.background.primary.intense")
4. Loop back to step 1
```

Trigger watch mode with: "Start watch mode" or "Watch for my annotations"

## Critique Mode

Agent opens a headed browser, scrolls top-to-bottom, and autonomously annotates what it sees — hierarchy, spacing, typography, navigation, CTAs. Requires the agent-browser skill.

## Self-Driving Mode

Agent annotates issues AND fixes them in a single pass:
1. Opens browser → scrolls to element
2. Drops annotation (visible in your toolbar)
3. Reads source → edits code
4. Calls agentation_resolve (annotation disappears)
5. Verifies fix in browser → continues

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Cmd/Ctrl+Shift+F` | Toggle feedback mode |
| `Esc` | Close toolbar / cancel |
| `P` | Pause/resume animations |
| `H` | Hide/show markers |
| `C` | Copy feedback |
| `X` | Clear all annotations |
