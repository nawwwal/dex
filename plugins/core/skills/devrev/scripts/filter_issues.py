#!/usr/bin/env python3
"""Filter and bucket issue arrays. Reads JSON from stdin."""

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone


IST = timezone(timedelta(hours=5, minutes=30))


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5


def next_workday(d: date) -> date:
    d += timedelta(days=1)
    while is_weekend(d):
        d += timedelta(days=1)
    return d


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    if "T" not in s:
        try:
            return date.fromisoformat(s[:10])
        except ValueError:
            return None
    try:
        value = s.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=IST)
        return parsed.astimezone(IST).date()
    except ValueError:
        return None


def get_stage_name(issue: dict) -> str:
    stage = issue.get("stage") or {}
    if isinstance(stage, dict):
        nested = stage.get("stage") or {}
        return str(stage.get("name") or nested.get("name") or "").lower()
    return str(stage).lower()


def morning_buckets(issues: list, today: date) -> dict:
    due_today, overdue, starts_today, rest = [], [], [], []
    for iss in issues:
        close = parse_date(iss.get("target_close_date"))
        start = parse_date(iss.get("target_start_date"))
        if close:
            if close < today:
                overdue.append(iss)
            elif close == today:
                due_today.append(iss)
            elif start and start == today:
                starts_today.append(iss)
            else:
                rest.append(iss)
        elif start and start == today:
            starts_today.append(iss)
        else:
            rest.append(iss)

    rest.sort(key=lambda i: parse_date(i.get("target_close_date")) or date(9999, 1, 1))
    return {
        "due_today": due_today,
        "overdue": overdue,
        "starts_today": starts_today,
        "rest": rest[:10],
    }


def starts_on(issues: list, target: date) -> list:
    result = []
    for iss in issues:
        start = parse_date(iss.get("target_start_date"))
        if start == target:
            result.append(iss)
    return result


def no_sprint(issues: list) -> list:
    return [i for i in issues if not i.get("sprint")]


def idle(issues: list, today: date) -> list:
    result = []
    for iss in issues:
        stage = get_stage_name(iss)
        start = parse_date(iss.get("target_start_date"))
        if "to_do" in stage or stage == "to do" or stage == "open":
            if start and start < today:
                result.append(iss)
    return result


def no_body(issues: list) -> list:
    return [i for i in issues if not (i.get("body") or "").strip()]


def groom_buckets(issues: list, active_sprint_don: str, today: date) -> dict:
    no_sprint_list, active_list, future_list = [], [], []
    no_effort_list, no_body_list, stale_list = [], [], []

    for iss in issues:
        sprint = iss.get("sprint")
        sprint_don = sprint.get("id") if isinstance(sprint, dict) else (sprint or None)

        if not sprint_don:
            no_sprint_list.append(iss)
        elif sprint_don == active_sprint_don:
            active_list.append(iss)
        else:
            future_list.append(iss)

        effort = iss.get("tnt__remaining_effort") or 0
        if not effort:
            no_effort_list.append(iss)

        if not (iss.get("body") or "").strip():
            no_body_list.append(iss)

        close = parse_date(iss.get("target_close_date"))
        stage_name = get_stage_name(iss)
        if close and close < today and "to do" in stage_name:
            stale_list.append(iss)

    return {
        "no_sprint": no_sprint_list,
        "active_sprint": active_list,
        "future_sprint": future_list,
        "no_effort": no_effort_list,
        "no_body": no_body_list,
        "stale": stale_list,
        "counts": {
            "total": len(issues),
            "no_sprint": len(no_sprint_list),
            "active_sprint": len(active_list),
            "future_sprint": len(future_list),
            "no_effort": len(no_effort_list),
            "no_body": len(no_body_list),
            "stale": len(stale_list),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    mb = sub.add_parser("morning_buckets")
    mb.add_argument("--today", required=True)

    so = sub.add_parser("starts_on")
    so.add_argument("--date", required=True, dest="target_date")

    sub.add_parser("no_sprint")

    id_ = sub.add_parser("idle")
    id_.add_argument("--today", required=True)

    sub.add_parser("no_body")

    gb = sub.add_parser("groom_buckets")
    gb.add_argument("--active-sprint", required=True)
    gb.add_argument("--today", required=True)

    args = parser.parse_args()
    issues = json.load(sys.stdin)

    if args.cmd == "morning_buckets":
        today = date.fromisoformat(args.today)
        print(json.dumps(morning_buckets(issues, today)))

    elif args.cmd == "starts_on":
        target = date.fromisoformat(args.target_date)
        if is_weekend(target):
            target = next_workday(target)
        print(json.dumps(starts_on(issues, target)))

    elif args.cmd == "no_sprint":
        print(json.dumps(no_sprint(issues)))

    elif args.cmd == "idle":
        today = date.fromisoformat(args.today)
        print(json.dumps(idle(issues, today)))

    elif args.cmd == "no_body":
        print(json.dumps(no_body(issues)))

    elif args.cmd == "groom_buckets":
        today = date.fromisoformat(args.today)
        print(json.dumps(groom_buckets(issues, args.active_sprint, today)))

    else:
        parser.print_help()
        sys.exit(1)
