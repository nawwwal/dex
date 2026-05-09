#!/usr/bin/env python3
"""Smoke-test audits for devrev skill authoring quality."""

import argparse
import glob
import json
import os
import re
import sys


def scope_check(modes_dir: str) -> dict:
    """Check all list_issues() calls in modes/ include owned_by=."""
    violations = []
    pattern = os.path.join(modes_dir, "*.md")
    for path in sorted(glob.glob(pattern)):
        with open(path) as f:
            content = f.read()
        for i, line in enumerate(content.splitlines(), 1):
            if "list_issues(" in line and "owned_by=" not in line:
                violations.append({
                    "file": os.path.basename(path),
                    "line": i,
                    "text": line.strip(),
                })

    return {"ok": len(violations) == 0, "violations": violations}


def date_format_check(*files: str) -> dict:
    """Check for ISO date strings without +05:30 offset."""
    violations = []
    iso_re = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?!\+05:30)")
    for path in files:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            content = f.read()
        for i, line in enumerate(content.splitlines(), 1):
            if iso_re.search(line):
                violations.append({
                    "file": os.path.basename(path),
                    "line": i,
                    "text": line.strip(),
                })

    return {"ok": len(violations) == 0, "violations": violations}


def body_check(issues: list) -> dict:
    """Flag issues with empty bodies."""
    empty = []
    for iss in issues:
        body = (iss.get("body") or "").strip()
        if not body:
            empty.append({
                "iss_id": iss.get("display_id") or iss.get("iss_id") or "?",
                "title": iss.get("title") or "",
            })
    return {"ok": len(empty) == 0, "empty_bodies": empty}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sc = sub.add_parser("scope_check")
    sc.add_argument("modes_dir")

    dc = sub.add_parser("date_format_check")
    dc.add_argument("files", nargs="+")

    sub.add_parser("body_check")

    args = parser.parse_args()

    if args.cmd == "scope_check":
        result = scope_check(args.modes_dir)
        print(json.dumps(result))
        if not result["ok"]:
            sys.exit(1)

    elif args.cmd == "date_format_check":
        result = date_format_check(*args.files)
        print(json.dumps(result))
        if not result["ok"]:
            sys.exit(1)

    elif args.cmd == "body_check":
        issues = json.load(sys.stdin)
        result = body_check(issues)
        print(json.dumps(result))
        if not result["ok"]:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)
