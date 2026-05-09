#!/usr/bin/env python3
"""Date math utilities for devrev skill. No external deps."""

import sys
from datetime import date, timedelta


def is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # Saturday=5, Sunday=6


def add_working_days(start: date | str, n: int) -> date:
    if isinstance(start, str):
        start = date.fromisoformat(start)
    d = start
    added = 0
    while added < n:
        d += timedelta(days=1)
        if not is_weekend(d):
            added += 1
    return d


def working_days_between(start: date | str, end: date | str) -> int:
    if isinstance(start, str):
        start = date.fromisoformat(start)
    if isinstance(end, str):
        end = date.fromisoformat(end)
    count = 0
    d = start
    while d <= end:
        if not is_weekend(d):
            count += 1
        d += timedelta(days=1)
    return count


def format_iso_ist(d: date | str, kind: str = "start") -> str:
    if isinstance(d, str):
        d = date.fromisoformat(d)
    if kind == "start":
        return f"{d.isoformat()}T00:00:00+05:30"
    elif kind == "close":
        return f"{d.isoformat()}T18:29:59+05:30"
    raise ValueError(f"kind must be 'start' or 'close', got: {kind}")


def validate_iso_ist(s: str) -> bool:
    return "+05:30" in s


def schedule_task(start: date | str, effort_days: float) -> dict:
    """
    Given a start date and effort in working days, return start and close dates
    with weekends skipped. If start is a weekend, advances to Monday.
    For 1d tasks: close == start. For 1.5d: close == start + 1 working day.
    """
    if isinstance(start, str):
        start = date.fromisoformat(start[:10])
    while is_weekend(start):
        start += timedelta(days=1)
    # close = start + (effort - 1) working days, minimum 0
    extra_days = max(0, int(effort_days) - 1)
    # for fractional effort (e.g. 1.5d), add one extra day to close
    if effort_days != int(effort_days):
        extra_days += 1
    close = add_working_days(start, extra_days) if extra_days > 0 else start
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "start": start.isoformat(),
        "close": close.isoformat(),
        "start_label": f"{day_names[start.weekday()]} {start.strftime('%b %-d')}",
        "close_label": f"{day_names[close.weekday()]} {close.strftime('%b %-d')}",
        "start_ist": format_iso_ist(start, "start"),
        "close_ist": format_iso_ist(close, "close"),
    }


def next_sequential_start(close: date | str) -> date:
    """Return the first working day after close (for chaining sequential tasks)."""
    if isinstance(close, str):
        close = date.fromisoformat(close[:10])
    return add_working_days(close, 1)


if __name__ == "__main__":
    import json
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "add_working_days":
        start = sys.argv[2]
        n = int(sys.argv[3])
        result = add_working_days(start, n)
        print(json.dumps({"result": result.isoformat()}))

    elif cmd == "working_days_between":
        start = sys.argv[2]
        end = sys.argv[3]
        result = working_days_between(start, end)
        print(json.dumps({"result": result}))

    elif cmd == "format_iso_ist":
        d = sys.argv[2]
        kind = sys.argv[3] if len(sys.argv) > 3 else "start"
        print(json.dumps({"result": format_iso_ist(d, kind)}))

    elif cmd == "validate_iso_ist":
        s = sys.argv[2]
        print(json.dumps({"valid": validate_iso_ist(s)}))

    elif cmd == "schedule_task":
        # schedule_task <start_date> <effort_days>
        start = sys.argv[2]
        effort = float(sys.argv[3])
        print(json.dumps(schedule_task(start, effort)))

    elif cmd == "next_sequential_start":
        # next_sequential_start <close_date>
        close = sys.argv[2]
        result = next_sequential_start(close)
        print(json.dumps({"result": result.isoformat()}))

    else:
        print("Usage: lib_dates.py <cmd> [args]")
        print("Commands: add_working_days <start_date> <n>")
        print("          working_days_between <start> <end>")
        print("          format_iso_ist <date> [start|close]")
        print("          validate_iso_ist <datetime_string>")
        print("          schedule_task <start_date> <effort_days>")
        print("          next_sequential_start <close_date>")
        sys.exit(1)
