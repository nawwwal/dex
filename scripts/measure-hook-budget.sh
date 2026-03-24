#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SETTINGS_FILE="${CLAUDE_DIR}/settings.json"
CACHE_DIR="${CLAUDE_DIR}/plugins/cache"
PROJECT_CWD="${1:-${HOME}/projects/agent-studio-demo}"

measure_bytes() {
  local payload="$1"
  local script="$2"
  if [ ! -x "$script" ] && [ ! -f "$script" ]; then
    echo "missing"
    return
  fi
  printf '%s' "$payload" | "$script" 2>/dev/null | wc -c | tr -d ' '
}

latest_plugin_dir() {
  local marketplace="$1"
  local plugin="$2"
  find "${CACHE_DIR}/${marketplace}/${plugin}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort -V | tail -1
}

measure_prompt_case() {
  local prompt="$1"
  local total=0
  local script bytes

  for script in \
    "${ROOT_DIR}/plugins/core/hooks/enrich-short-messages.sh" \
    "${ROOT_DIR}/plugins/core/hooks/continuation-enricher.sh" \
    "${ROOT_DIR}/plugins/core/hooks/frustration-structure.sh" \
    "${ROOT_DIR}/plugins/core/hooks/resume-injector.sh" \
    "${ROOT_DIR}/plugins/core/hooks/fill-compact.sh" \
    "${ROOT_DIR}/plugins/core/hooks/reflect-others-detector.sh"; do
    bytes=$(jq -cn --arg prompt "$prompt" --arg cwd "$PROJECT_CWD" '{prompt:$prompt, cwd:$cwd}' | "$script" 2>/dev/null | wc -c | tr -d ' ')
    total=$((total + bytes))
  done

  echo "$total"
}

echo "Hook Budget Report"
echo "Project CWD: ${PROJECT_CWD}"
echo ""

DEX_STARTUP=$(measure_bytes "$(jq -cn --arg cwd "$PROJECT_CWD" --arg source "startup" '{cwd:$cwd, source:$source}')" "${ROOT_DIR}/plugins/core/hooks/session-context.sh")
DEX_SUBAGENT=$(measure_bytes '{}' "${ROOT_DIR}/plugins/core/hooks/subagent-context.sh")

echo "Dex SessionStart bytes: ${DEX_STARTUP}"
echo "Dex SubagentStart bytes: ${DEX_SUBAGENT}"

SUPERPOWERS_DIR=$(latest_plugin_dir "superpowers-marketplace" "superpowers")
if [ -n "${SUPERPOWERS_DIR:-}" ] && [ -f "${SUPERPOWERS_DIR}/hooks/session-start" ]; then
  SUPERPOWERS_STARTUP=$(measure_bytes "$(jq -cn --arg cwd "$PROJECT_CWD" --arg source "startup" '{cwd:$cwd, source:$source}')" "${SUPERPOWERS_DIR}/hooks/session-start")
  echo "Superpowers SessionStart bytes: ${SUPERPOWERS_STARTUP}"
else
  echo "Superpowers SessionStart bytes: missing"
fi

echo ""
echo "Representative UserPromptSubmit totals"
echo "  'How do I log an error?': $(measure_prompt_case "How do I log an error?")"
echo "  'continue': $(measure_prompt_case "continue")"
echo "  '/resume': $(measure_prompt_case "/resume")"
echo "  'this is wrong': $(measure_prompt_case "this is wrong")"

echo ""
echo "Enabled plugin Stop hook counts"
python3 - "$SETTINGS_FILE" "$CACHE_DIR" <<'PYEOF'
import json
import os
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])
cache_dir = Path(sys.argv[2])

settings = json.load(open(settings_path))
enabled = settings.get("enabledPlugins", {})

for key, is_enabled in sorted(enabled.items()):
    if not is_enabled:
        continue
    if "@" not in key:
        continue
    plugin, marketplace = key.split("@", 1)
    plugin_root = cache_dir / marketplace / plugin
    versions = sorted([p for p in plugin_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not versions:
        print(f"  {key}: missing")
        continue
    latest = versions[-1]
    hooks_file = latest / "hooks" / "hooks.json"
    if not hooks_file.exists():
        print(f"  {key}: 0")
        continue
    try:
        data = json.load(open(hooks_file))
        stop_hooks = len(data.get("hooks", {}).get("Stop", []))
    except Exception:
        stop_hooks = "error"
    print(f"  {key}: {stop_hooks}")
PYEOF

echo ""
echo "CLAUDE.md footprint"
GLOBAL_CLAUDE="${CLAUDE_DIR}/CLAUDE.md"
PROJECT_CLAUDE="${PROJECT_CWD}/CLAUDE.md"
if [ -f "${GLOBAL_CLAUDE}" ]; then
  echo "  Global CLAUDE.md: $(wc -c < "${GLOBAL_CLAUDE}" | tr -d ' ') bytes / $(wc -l < "${GLOBAL_CLAUDE}" | tr -d ' ') lines"
fi
if [ -f "${PROJECT_CLAUDE}" ]; then
  echo "  Project CLAUDE.md: $(wc -c < "${PROJECT_CLAUDE}" | tr -d ' ') bytes / $(wc -l < "${PROJECT_CLAUDE}" | tr -d ' ') lines"
fi
