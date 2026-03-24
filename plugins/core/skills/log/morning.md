# Morning Briefing

Start-of-day synthesis. Generates both text briefing and HTML dashboard.

## Step 1: Check Yesterday's Sessions
```bash
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d 2>/dev/null)
ls ~/.claude/log/${YESTERDAY}-*.md 2>/dev/null | grep -v compact | head -3
```
Read the most recent session file. Know what was in progress.

## Step 2: Read TASKS.md
Read ~/.claude/TASKS.md. Identify: overdue, due today, quick wins.

## Step 3: Check Calendar (if Google Workspace MCP available)
Get today's events. Flag: back-to-back meetings, hard constraints, TCDs within 3 days.

## Step 4: Drift Check
Quick scan: what project hasn't appeared in sessions for 5+ days?

## Step 5: Generate Text Briefing
5-bullet crisp summary:
1. Yesterday's carry-forward
2. Today's calendar constraints
3. Top 3 tasks (with priority)
4. Any TCDs due this week
5. Any drift warning

## Step 6: Generate HTML Dashboard
Write to `~/.claude/log/YYYY-MM-DD-dashboard.html`:
A self-contained HTML file with:
- Live clock (JavaScript)
- Priority ring showing task completion
- Clickable task checklist (localStorage persistence)
- Today's calendar events
- Color-coded TCDs

```html
<!DOCTYPE html>
<html>
<head>
<title>Dashboard — {DATE}</title>
<style>
/* Minimal, dark theme */
body { font-family: system-ui; background: #0d1117; color: #e6edf3; padding: 2rem; max-width: 800px; margin: 0 auto; }
.clock { font-size: 3rem; font-weight: bold; color: #58a6ff; }
.task { padding: 0.5rem; margin: 0.25rem 0; border-left: 3px solid #30363d; cursor: pointer; }
.task.done { opacity: 0.4; text-decoration: line-through; }
.tcd { color: #f85149; font-weight: bold; }
</style>
</head>
<body>
<div class="clock" id="clock"></div>
<h2>Today: {DATE}</h2>
<!-- Tasks populated dynamically from TASKS.md content -->
<div id="tasks"></div>
<script>
function updateClock() { document.getElementById('clock').textContent = new Date().toLocaleTimeString(); }
setInterval(updateClock, 1000); updateClock();
// Task persistence via localStorage
// (populate from Python parsing of TASKS.md)
</script>
</body>
</html>
```
