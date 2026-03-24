---
name: today
description: "Use when generating an interactive HTML daily dashboard — 'daily dashboard', 'today's command center', 'make me a dashboard'."
allowed-tools: Read, Write, Bash, Glob
---

# /today — Interactive HTML Daily Dashboard

Generate a self-contained HTML daily command center and save it to `~/.claude/log/YYYY-MM-DD-dashboard.html`.

## Step 1: Gather Data

```bash
TODAY=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%A)
echo "Date: $TODAY ($DAY_OF_WEEK)"
```

Read sources:
1. **TASKS.md** — `head -80 ~/.claude/TASKS.md 2>/dev/null` — extract open tasks, due dates, any TCDs
2. **Recent session** — `ls -t ~/.claude/log/${TODAY}-*.md 2>/dev/null | grep -v "compact\|commits\|changes\|dashboard" | head -1` — what was in progress
3. **Calendar** — if Google Workspace MCP is available, get today's events
4. **DevRev** — if DevRev MCP is available, check sprint board for open items

## Step 2: Parse Tasks

From TASKS.md, extract:
- **Overdue**: anything with a date that has passed
- **Due today**: any TCD or explicit date for today
- **Quick wins**: items marked small/easy or under 30 min
- **Blocked**: items marked blocked or waiting
- **Top 3 focus**: your best judgment of what to work on today

## Step 3: Generate HTML Dashboard

Write a complete self-contained HTML file to `~/.claude/log/$TODAY-dashboard.html`:

The HTML must include:
- Live clock (updates every second via JavaScript)
- Priority ring showing task completion percentage (uses localStorage to track checked tasks)
- Clickable task checklist with localStorage persistence (checks survive page reload)
- Color-coded sections: Overdue (red), Today (orange), Focus (blue), Blocked (gray)
- Calendar events if available
- TCDs (tight commitments with dates) highlighted if within 3 days
- Responsive design (works from 320px to 1440px)
- Zero external dependencies (no CDN, fully self-contained)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard — {DATE}</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: #0d1117;
  color: #e6edf3;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  min-height: 100vh;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #21262d;
}
.clock {
  font-size: 2.5rem;
  font-weight: 700;
  color: #58a6ff;
  font-variant-numeric: tabular-nums;
  letter-spacing: -1px;
}
.date-info { text-align: right; }
.date-info .date { font-size: 1rem; color: #8b949e; }
.date-info .day { font-size: 1.25rem; font-weight: 600; }
.progress-ring {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #161b22;
  border-radius: 12px;
  border: 1px solid #21262d;
  margin-bottom: 1.5rem;
}
.ring-svg { transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: #21262d; stroke-width: 4; }
.ring-fill { fill: none; stroke: #238636; stroke-width: 4; stroke-linecap: round; transition: stroke-dashoffset 0.5s ease; }
.progress-text { font-size: 0.875rem; color: #8b949e; }
.progress-count { font-size: 1.5rem; font-weight: 700; color: #3fb950; }
.section { margin-bottom: 1.5rem; }
.section-title {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #8b949e;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #21262d;
}
.task-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.625rem 0.875rem;
  border-radius: 8px;
  margin-bottom: 0.375rem;
  cursor: pointer;
  transition: background 0.15s;
  border: 1px solid transparent;
}
.task-item:hover { background: #161b22; border-color: #21262d; }
.task-item.done { opacity: 0.4; }
.task-item.done .task-text { text-decoration: line-through; }
.task-check {
  width: 16px;
  height: 16px;
  min-width: 16px;
  border-radius: 4px;
  border: 2px solid #30363d;
  margin-top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.task-item.done .task-check { background: #238636; border-color: #238636; }
.task-check::after { content: '✓'; font-size: 10px; color: white; opacity: 0; }
.task-item.done .task-check::after { opacity: 1; }
.task-text { font-size: 0.9rem; line-height: 1.4; flex: 1; }
.badge {
  font-size: 0.65rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.badge-overdue { background: #3d1f1f; color: #f85149; }
.badge-today { background: #2a1f0a; color: #e3b341; }
.badge-tcd { background: #3d1f1f; color: #f85149; font-weight: 700; }
.badge-blocked { background: #1f2428; color: #8b949e; }
.event-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.5rem 0;
  font-size: 0.875rem;
  border-bottom: 1px solid #21262d;
}
.event-time { color: #58a6ff; min-width: 80px; font-variant-numeric: tabular-nums; }
.event-title { flex: 1; }
.footer {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #21262d;
  font-size: 0.75rem;
  color: #484f58;
  display: flex;
  justify-content: space-between;
}
</style>
</head>
<body>

<header>
  <div class="clock" id="clock">00:00:00</div>
  <div class="date-info">
    <div class="day">{DAY_OF_WEEK}</div>
    <div class="date">{FULL_DATE}</div>
  </div>
</header>

<div class="progress-ring">
  <svg class="ring-svg" width="48" height="48" viewBox="0 0 48 48">
    <circle class="ring-bg" cx="24" cy="24" r="20"/>
    <circle class="ring-fill" id="ring" cx="24" cy="24" r="20"
      stroke-dasharray="125.6"
      stroke-dashoffset="125.6"/>
  </svg>
  <div>
    <div class="progress-count"><span id="done-count">0</span> / <span id="total-count">0</span></div>
    <div class="progress-text">tasks completed today</div>
  </div>
</div>

{TASK_SECTIONS_HTML}

{EVENTS_HTML}

<div class="footer">
  <span>Generated {DATETIME}</span>
  <span>Click tasks to check off · Persists across reloads</span>
</div>

<script>
// Clock
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    String(now.getHours()).padStart(2,'0') + ':' +
    String(now.getMinutes()).padStart(2,'0') + ':' +
    String(now.getSeconds()).padStart(2,'0');
}
setInterval(updateClock, 1000);
updateClock();

// Task persistence
const STORAGE_KEY = 'dashboard-{DATE}-tasks';
let saved = {};
try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch(e) {}

function updateRing() {
  const items = document.querySelectorAll('.task-item');
  const done = document.querySelectorAll('.task-item.done').length;
  const total = items.length;
  document.getElementById('done-count').textContent = done;
  document.getElementById('total-count').textContent = total;
  const circumference = 125.6;
  const offset = total > 0 ? circumference * (1 - done/total) : circumference;
  document.getElementById('ring').style.strokeDashoffset = offset;
}

document.querySelectorAll('.task-item').forEach(item => {
  const id = item.dataset.id;
  if (saved[id]) item.classList.add('done');
  item.addEventListener('click', () => {
    item.classList.toggle('done');
    saved[id] = item.classList.contains('done');
    localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
    updateRing();
  });
});
updateRing();
</script>
</body>
</html>
```

## Step 4: Populate the HTML

Replace the placeholders with actual data from Step 1:
- `{DATE}` → YYYY-MM-DD
- `{DAY_OF_WEEK}` → Monday, Tuesday, etc.
- `{FULL_DATE}` → e.g., "March 10, 2026"
- `{DATETIME}` → full timestamp
- `{TASK_SECTIONS_HTML}` → Generated HTML sections for tasks:

```html
<!-- Overdue section (if any overdue tasks) -->
<div class="section">
  <div class="section-title">🔴 Overdue</div>
  <div class="task-item" data-id="task-001">
    <div class="task-check"></div>
    <div class="task-text">Task name</div>
    <span class="badge badge-overdue">Overdue</span>
  </div>
</div>

<!-- Focus section -->
<div class="section">
  <div class="section-title">🎯 Today's Focus</div>
  <div class="task-item" data-id="task-002">
    <div class="task-check"></div>
    <div class="task-text">Task name</div>
  </div>
</div>
```

- `{EVENTS_HTML}` → Calendar events if available:
```html
<div class="section">
  <div class="section-title">📅 Calendar</div>
  <div class="event-item">
    <span class="event-time">10:00 AM</span>
    <span class="event-title">Meeting name</span>
  </div>
</div>
```

## Step 5: Save and Report

```bash
OUTPUT="$HOME/.claude/log/${TODAY}-dashboard.html"
# [write the complete HTML to this path]
echo "Dashboard saved to: $OUTPUT"
echo "Open with: open $OUTPUT"
```

After writing, offer to open it:
`open ~/.claude/log/${TODAY}-dashboard.html`

Report the 5-line text summary too:
```
📅 Today: {DAY}, {DATE}
🎯 Focus: {top 3 tasks}
⚠️ Overdue: {count} items
📋 Calendar: {next event}
🔴 TCDs: {any within 3 days}
```
