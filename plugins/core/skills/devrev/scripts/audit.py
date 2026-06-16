#!/usr/bin/env python3
"""Smoke-test audits for devrev skill authoring quality."""

import argparse
import glob
import json
import os
import re
import sys


REQUIRED_EVAL_IDS = {
    "explicit-devrev-morning-sync",
    "implicit-plate-query",
    "fresh-sync-cache",
    "stale-sync-refresh",
    "eod-sync-state-closeout",
    "external-github-codex-evidence",
    "source-failure-honesty",
    "proposed-writebacks-not-auto-write",
    "no-portent-ledger-regression",
    "no-session-policy-regression",
}


def read(path: str) -> str:
    with open(path) as f:
        return f.read()


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


def _require_text(content: str, needle: str, label: str, violations: list) -> None:
    if needle not in content:
        violations.append({"check": label, "missing": needle})


def _require_any(content: str, needles: list, label: str, violations: list) -> None:
    if not any(needle in content for needle in needles):
        violations.append({"check": label, "missing_any": needles})


def sync_contract_check(skill_dir: str) -> dict:
    """Check the DevRev Sync State contract and eval coverage."""
    violations = []
    skill_path = os.path.join(skill_dir, "SKILL.md")
    morning_path = os.path.join(skill_dir, "modes", "morning.md")
    eod_path = os.path.join(skill_dir, "modes", "eod.md")
    eval_path = os.path.join(skill_dir, "evals", "evals.json")
    sync_ref_path = os.path.join(skill_dir, "references", "sync-state.md")

    for path in [skill_path, morning_path, eod_path, sync_ref_path]:
        if not os.path.exists(path):
            violations.append({"check": "required_file", "missing": path})

    if violations:
        return {"ok": False, "violations": violations}

    skill = read(skill_path)
    morning = read(morning_path)
    eod = read(eod_path)
    sync_ref = read(sync_ref_path)

    _require_text(skill, "[[DevRev local knowledge]]", "skill_mentions_local_note", violations)
    _require_text(skill, "## Sync State", "skill_mentions_sync_state", violations)
    _require_text(skill, "External evidence", "skill_mentions_external_evidence", violations)
    _require_text(skill, "source_coverage", "skill_mentions_source_coverage", violations)
    _require_text(skill, "references/sync-state.md", "skill_links_sync_reference", violations)
    _require_text(skill.lower(), "closeout", "skill_routes_eod_closeout_phrase", violations)
    _require_text(skill.lower(), "reconcile", "skill_routes_reconcile_intent", violations)
    _require_text(skill.lower(), "ledger", "skill_routes_ledger_negative_control", violations)
    _require_text(skill.lower(), "devrev aware", "skill_routes_working_session_negative_control", violations)

    for needle in ["## Section Shape", "## Authority", "## Source Coverage", "## Write Rules"]:
        _require_text(sync_ref, needle, "sync_reference_complete", violations)
    _require_text(sync_ref, "Do not fetch directly in v1", "sync_reference_external_evidence_limit", violations)
    _require_text(sync_ref, "Require explicit confirmation", "sync_reference_write_confirmation", violations)

    for forbidden in ["[[active-work-ledger]]", "UserPromptSubmit", "PostToolUse", "PreToolUse"]:
        if forbidden in skill + morning + eod:
            violations.append({"check": "forbidden_session_or_hook_language", "found": forbidden})

    forbidden_active_policy = [
        r"mandatory\s+ticket",
        r"must\s+open\s+a\s+ticket\s+before",
        r"must\s+create\s+a\s+ticket\s+before",
        r"session\s+gate",
    ]
    combined = "\n".join([skill, morning, eod]).lower()
    for pattern in forbidden_active_policy:
        if re.search(pattern, combined):
            violations.append({"check": "forbidden_session_or_ticket_policy", "found": pattern})

    _require_text(morning, "## Sync State", "morning_reads_sync_state", violations)
    _require_text(morning, "last_synced", "morning_checks_last_synced", violations)
    _require_text(morning, "4 hours", "morning_cache_window", violations)
    _require_text(morning, "source_coverage", "morning_reports_source_coverage", violations)
    _require_text(morning, "External evidence", "morning_accepts_external_evidence", violations)
    _require_text(morning, "references/sync-state.md", "morning_reads_sync_reference", violations)
    _require_any(morning.lower(), ["overwrite only `## sync state`", "overwrite `## sync state`"], "morning_updates_sync_state", violations)

    _require_text(eod, "## Sync State", "eod_reads_sync_state", violations)
    _require_text(eod, "source_coverage", "eod_reports_source_coverage", violations)
    _require_text(eod, "External evidence", "eod_accepts_external_evidence", violations)
    _require_text(eod, "references/sync-state.md", "eod_reads_sync_reference", violations)
    _require_any(eod.lower(), ["overwrite only `## sync state`", "overwrite `## sync state`"], "eod_updates_sync_state", violations)

    runtime_files = [skill_path, os.path.join(skill_dir, "gotchas.md")]
    runtime_files.extend(sorted(glob.glob(os.path.join(skill_dir, "modes", "*.md"))))
    runtime_id_re = re.compile(r"don:core:[^\s`|)]+|don:identity:[^\s`|)]+")
    for path in runtime_files:
        if not os.path.exists(path):
            continue
        for i, line in enumerate(read(path).splitlines(), 1):
            if runtime_id_re.search(line):
                violations.append({
                    "check": "no_hardcoded_runtime_don",
                    "file": os.path.relpath(path, skill_dir),
                    "line": i,
                    "text": line.strip(),
                })

    if not os.path.exists(eval_path):
        violations.append({"check": "eval_json_exists", "missing": eval_path})
    else:
        try:
            evals = json.loads(read(eval_path))
            found_ids = {case.get("id") for case in evals.get("evals", [])}
            missing_ids = sorted(REQUIRED_EVAL_IDS - found_ids)
            extra_ids = sorted(found_ids - REQUIRED_EVAL_IDS)
            if missing_ids:
                violations.append({"check": "required_eval_ids", "missing": missing_ids})
            if extra_ids:
                violations.append({"check": "unexpected_eval_ids", "extra": extra_ids})
            for case in evals.get("evals", []):
                for key in ["id", "category", "prompt", "expected_output", "assertions", "deterministic_checks"]:
                    if key not in case:
                        violations.append({
                            "check": "eval_case_shape",
                            "id": case.get("id", "?"),
                            "missing": key,
                        })
        except json.JSONDecodeError as exc:
            violations.append({"check": "eval_json_parse", "error": str(exc)})

    return {"ok": len(violations) == 0, "violations": violations}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sc = sub.add_parser("scope_check")
    sc.add_argument("modes_dir")

    dc = sub.add_parser("date_format_check")
    dc.add_argument("files", nargs="+")

    sub.add_parser("body_check")

    scc = sub.add_parser("sync_contract_check")
    scc.add_argument("skill_dir")

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

    elif args.cmd == "sync_contract_check":
        result = sync_contract_check(args.skill_dir)
        print(json.dumps(result))
        if not result["ok"]:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)
