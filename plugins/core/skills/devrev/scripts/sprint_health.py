#!/usr/bin/env python3
"""Sprint health calculation. Reads issue array from stdin."""

import argparse
import json
import sys
from datetime import date, timedelta


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5


def working_days_between(start: date, end: date) -> int:
    count = 0
    d = start
    while d <= end:
        if not is_weekend(d):
            count += 1
        d += timedelta(days=1)
    return count


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None


def velocity(issues: list) -> dict:
    completed = [i for i in issues if (i.get("stage") or "").lower() in ("completed", "done")]
    velocity_days = sum(float(i.get("tnt__remaining_effort") or 0) for i in completed)
    return {"velocity_days": velocity_days, "issues_completed": len(completed)}


def checkin(issues: list, today: date, sprint_start: date, sprint_end: date) -> dict:
    total_working_days = working_days_between(sprint_start, sprint_end)
    elapsed = working_days_between(sprint_start, min(today, sprint_end))
    days_left = working_days_between(today, sprint_end) if today <= sprint_end else 0
    midpoint_day = total_working_days // 2

    done, in_progress, at_risk, idle, to_do = [], [], [], [], []

    for iss in issues:
        stage = (iss.get("stage") or "").lower()
        close = parse_date(iss.get("target_close_date"))
        start = parse_date(iss.get("target_start_date"))
        remaining = float(iss.get("tnt__remaining_effort") or 0)
        iss_id = iss.get("iss_id") or iss.get("display_id") or "?"
        title = iss.get("title") or ""

        item = {"iss_id": iss_id, "title": title, "remaining": remaining}

        if "completed" in stage or "done" in stage:
            done.append(item)
        elif "in_progress" in stage or "progress" in stage:
            at_risk_reason = None
            if close and close < today:
                at_risk_reason = f"overdue {(today - close).days}d"
            item["target_close"] = str(close) if close else None
            in_progress.append(item)
            if at_risk_reason:
                at_risk.append({"iss_id": iss_id, "reason": at_risk_reason})
        elif "to_do" in stage or "to do" in stage or "open" in stage:
            if start and start < today:
                idle.append({"iss_id": iss_id, "reason": f"should have started {(today - start).days}d ago"})
            to_do.append(item)
        elif "blocked" in stage:
            at_risk.append({"iss_id": iss_id, "reason": "blocked"})

    effort_burned = sum(float(i.get("remaining") or 0) for i in done)
    effort_total = sum(float(i.get("remaining") or 0) for i in done + in_progress + to_do)

    # Pace: at midpoint, we should have burned half the effort
    expected_burned = (effort_total * elapsed / total_working_days) if total_working_days > 0 else 0
    behind_by = expected_burned - effort_burned

    if behind_by <= 0:
        health = "🟢"
        health_reason = "on track or ahead"
    elif behind_by <= 1.5:
        health = "🟡"
        health_reason = f"behind by {behind_by:.1f}d effort"
    else:
        health = "🔴"
        health_reason = f"behind by {behind_by:.1f}d effort"

    if any(i.get("reason") == "blocked" for i in at_risk):
        if health == "🟢":
            health = "🟡"
        health_reason += ", unresolved blockers"

    midpoint_passed = elapsed > midpoint_day

    next_candidates = sorted(
        [i for i in to_do if i.get("remaining", 0) > 0],
        key=lambda x: (x.get("target_close") or "9999", -x.get("remaining", 0))
    )[:3]

    if behind_by > 0:
        pace_label = f"behind by {behind_by:.1f}d effort"
    else:
        pace_label = f"ahead by {abs(behind_by):.1f}d effort"

    return {
        "working_days_left": days_left,
        "working_days_elapsed": elapsed,
        "working_days_total": total_working_days,
        "midpoint_passed": midpoint_passed,
        "done_count": len(done),
        "total_count": len(issues),
        "effort_burned_days": round(effort_burned, 1),
        "effort_total_days": round(effort_total, 1),
        "pace_label": pace_label,
        "health": health,
        "health_reason": health_reason,
        "done": done,
        "in_progress": in_progress,
        "at_risk": at_risk,
        "idle": idle,
        "next_up_candidates": next_candidates,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    vc = sub.add_parser("velocity")

    ci = sub.add_parser("checkin")
    ci.add_argument("--today", required=True)
    ci.add_argument("--start", required=True)
    ci.add_argument("--end", required=True)

    args = parser.parse_args()
    issues = json.load(sys.stdin)

    if args.cmd == "velocity":
        print(json.dumps(velocity(issues)))

    elif args.cmd == "checkin":
        today = date.fromisoformat(args.today)
        start = date.fromisoformat(args.start)
        end = date.fromisoformat(args.end)
        print(json.dumps(checkin(issues, today, start, end)))

    else:
        parser.print_help()
        sys.exit(1)
