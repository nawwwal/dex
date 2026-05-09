#!/usr/bin/env python3
"""Detect sprint sub-mode and check sprint freshness."""

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5


def parse_sprint_date(s: str) -> date:
    return date.fromisoformat(s[:10])


def first_working_day(d: date) -> date:
    """Advance to the first non-weekend day on or after d."""
    while is_weekend(d):
        d += timedelta(days=1)
    return d


def working_days_from_sprint_start(start: date, today: date) -> int:
    """Count working days elapsed from first working day of sprint to today (inclusive)."""
    fwd = first_working_day(start)
    count = 0
    d = fwd
    while d <= today:
        if not is_weekend(d):
            count += 1
        d += timedelta(days=1)
    return count


def submode(issues: list, today: date, start: date, end: date) -> dict:
    user_sprint_issues = [i for i in issues if i.get("sprint")]
    if today > end:
        return {"submode": "refresh"}
    # Planning: no issues yet AND still within first 2 working days of sprint
    elapsed_working_days = working_days_from_sprint_start(start, today)
    if not user_sprint_issues and elapsed_working_days <= 2:
        return {"submode": "planning"}
    return {"submode": "checkin"}


def freshness(memory_path: str) -> dict:
    expanded = os.path.expanduser(memory_path)
    if not os.path.exists(expanded):
        return {"stale": False}

    with open(expanded) as f:
        text = f.read()

    end_match = re.search(r"^[-*]?\s*end:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not end_match:
        return {"stale": False}

    end = date.fromisoformat(end_match.group(1))
    today = date.today()

    if today <= end:
        return {"stale": False}

    ended_days_ago = (today - end).days
    return {"stale": True, "ended_days_ago": ended_days_ago}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sm = sub.add_parser("submode")
    sm.add_argument("--today", required=True)
    sm.add_argument("--start", required=True)
    sm.add_argument("--end", required=True)

    fr = sub.add_parser("freshness")
    fr.add_argument("--memory", required=True)

    args = parser.parse_args()

    if args.cmd == "submode":
        issues = json.load(sys.stdin)
        today = parse_sprint_date(args.today)
        start = parse_sprint_date(args.start)
        end = parse_sprint_date(args.end)
        print(json.dumps(submode(issues, today, start, end)))

    elif args.cmd == "freshness":
        print(json.dumps(freshness(args.memory)))

    else:
        parser.print_help()
        sys.exit(1)
