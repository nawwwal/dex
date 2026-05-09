#!/usr/bin/env python3
"""Parse and validate devrev memory files."""

import json
import os
import re
import sys


def _parse_md_body(path: str) -> dict:
    """Extract key: value pairs from a markdown body (after frontmatter)."""
    with open(os.path.expanduser(path)) as f:
        text = f.read()

    in_frontmatter = False
    past_frontmatter = False
    body_lines = []

    for i, line in enumerate(text.splitlines()):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            past_frontmatter = True
            continue
        if past_frontmatter:
            body_lines.append(line)

    data = {}
    for line in body_lines:
        m = re.match(r"^[-*]?\s*(\w+(?:_\w+)*):\s*(.+)$", line.strip())
        if m:
            data[m.group(1)] = m.group(2).strip()

    return data


def _parse_sprint_block(path: str) -> dict:
    """Extract active sprint data from devrev-sprint.md."""
    with open(os.path.expanduser(path)) as f:
        text = f.read()

    sprint = {}
    in_section = False
    for line in text.splitlines():
        if "## Active Sprint" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            m = re.match(r"^[-*]?\s*(\w+):\s*(.+)$", line.strip())
            if m:
                sprint[m.group(1)] = m.group(2).strip()

    return sprint


def validate(devrev_path: str, sprint_path: str) -> dict:
    required_in_devrev = ["user_don", "sprint_board", "default_part", "slack_mention"]
    required_in_sprint = ["name", "don", "start", "end"]

    try:
        devrev_data = _parse_md_body(devrev_path)
    except FileNotFoundError:
        return {"ok": False, "error": f"File not found: {devrev_path}"}

    try:
        sprint_data = _parse_sprint_block(sprint_path)
    except FileNotFoundError:
        return {"ok": False, "error": f"File not found: {sprint_path}"}

    for key in required_in_devrev:
        if key not in devrev_data:
            return {"ok": False, "error": f"missing required key in devrev.md: {key}"}

    for key in required_in_sprint:
        if key not in sprint_data:
            return {"ok": False, "error": f"missing required key in devrev-sprint.md active sprint: {key}"}

    context = {
        "user_don": devrev_data["user_don"],
        "sprint_board": devrev_data["sprint_board"],
        "default_part": devrev_data["default_part"],
        "slack_mention": devrev_data["slack_mention"],
        "active_sprint": {
            "name": sprint_data["name"],
            "don": sprint_data["don"],
            "start": sprint_data["start"],
            "end": sprint_data["end"],
        },
        "issue_conventions": {
            "subtype": "task",
            "skills": ["Design"],
            "start_format": "YYYY-MM-DDT00:00:00+05:30",
            "close_format": "YYYY-MM-DDT18:29:59+05:30",
        },
    }

    # Optional fields
    for k in ["stage_to_do", "stage_in_progress", "stage_completed", "stage_blocked"]:
        if k in devrev_data:
            context[k] = devrev_data[k]

    return {"ok": True, "context": context}


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] != "validate":
        print("Usage: lib_memory.py validate <devrev.md> <devrev-sprint.md>", file=sys.stderr)
        sys.exit(1)

    result = validate(sys.argv[2], sys.argv[3])
    print(json.dumps(result))
    if not result["ok"]:
        sys.exit(1)
