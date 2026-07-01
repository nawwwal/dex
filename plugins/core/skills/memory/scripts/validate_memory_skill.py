from pathlib import Path
import sys

skill_path = Path("plugins/core/skills/memory/SKILL.md")
reference_path = Path("plugins/core/skills/memory/references/pmb-cli.md")
text = skill_path.read_text(encoding="utf-8")
reference_text = reference_path.read_text(encoding="utf-8")

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
    "references/pmb-cli.md",
]

reference_required = [
    "pmb note",
    "pmb learn",
    "pmb fact",
    "pmb remember",
    "pmb import",
    "pmb watch",
    "pmb index project",
    "pmb track changes",
    "pmb track modules",
    "pmb track install",
    "pmb resume",
    "pmb distill",
    "pmb consolidate",
    "pmb recall",
    "pmb why",
    "pmb overview",
    "pmb timeline",
    "pmb insights",
    "pmb digest",
    "pmb audit",
    "pmb lessons",
    "pmb reminders",
    "pmb list",
    "pmb graph",
    "pmb doctor",
    "pmb stats",
    "pmb warmup",
    "pmb daemon",
    "pmb export",
    "pmb snapshot",
    "pmb workspaces",
    "pmb workspace",
    "pmb forget",
    "pmb delete",
    "pmb restore",
    "pmb forget-topic",
    "pmb pin",
    "pmb tag",
    "pmb untag",
    "pmb ttl",
    "pmb prune-expired",
    "pmb reindex",
    "pmb regraph",
    "pmb repair-keyed",
]

runtime_forbidden = [
    "por" + "tent",
    "tol" + "aria",
    "q" + "md",
    "vault",
    "markdown",
    "legacy",
]

shared_forbidden = [
    "por" + "tent",
    "tol" + "aria",
    "q" + "md",
    "vault",
    "legacy",
]

missing = [item for item in required if item not in text]
reference_missing = [item for item in reference_required if item not in reference_text]
blocked = [item for item in runtime_forbidden if item in text.lower()]
reference_blocked = [item for item in shared_forbidden if item in reference_text.lower()]

if missing or reference_missing or blocked or reference_blocked:
    if missing:
        print("missing required text:", missing)
    if reference_missing:
        print("missing reference text:", reference_missing)
    if blocked:
        print("blocked runtime vocabulary:", blocked)
    if reference_blocked:
        print("blocked reference vocabulary:", reference_blocked)
    sys.exit(1)

print("memory skill ok")
