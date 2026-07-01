from pathlib import Path
import sys

skill_path = Path("plugins/core/skills/memory/SKILL.md")
text = skill_path.read_text(encoding="utf-8")

required = [
    "name: memory",
    "description: Use when",
    "PMB",
    "`prepare`",
    "`recall`",
    "`overview`",
    "`project_overview`",
    "`session_brief`",
    "`record_batch`",
    "`record_keyed_fact`",
    "`find_lessons`",
    "`mark_lesson_followed`",
    "`list_goals`",
    "`update_goal`",
]

forbidden = [
    "por" + "tent",
    "tol" + "aria",
    "q" + "md",
    "vault",
    "markdown",
    "legacy",
]

missing = [item for item in required if item not in text]
blocked = [item for item in forbidden if item in text.lower()]

if missing or blocked:
    if missing:
        print("missing required text:", missing)
    if blocked:
        print("blocked runtime vocabulary:", blocked)
    sys.exit(1)

print("memory skill ok")
