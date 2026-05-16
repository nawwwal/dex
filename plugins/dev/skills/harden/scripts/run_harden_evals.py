#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"
RESULTS_ROOT = ROOT / "evals" / "results"
DEFAULT_CODEX_MODEL = "gpt-5.5"
DEFAULT_REASONING_EFFORT = "medium"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_evals() -> dict[str, Any]:
    try:
        return json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{EVALS_PATH} is invalid JSON: {exc}")


def contains_any(text: str, terms: list[str]) -> tuple[bool, str]:
    lowered = text.lower()
    for term in terms:
        if term.lower() in lowered:
            return True, term
    return False, ""


def grade_output(case: dict[str, Any], output: str) -> dict[str, Any]:
    checks = case["deterministic_checks"]
    results: list[dict[str, Any]] = []

    for group in checks.get("must_include_any", []):
        passed, matched = contains_any(output, group)
        results.append({
            "text": "include one of: " + " | ".join(group),
            "passed": passed,
            "evidence": f"matched: {matched}" if passed else "no listed term found",
        })

    lowered = output.lower()
    for group in checks.get("must_not_include_any", []):
        matched = [term for term in group if term.lower() in lowered]
        passed = not matched
        results.append({
            "text": "exclude all of: " + " | ".join(group),
            "passed": passed,
            "evidence": "terms absent" if passed else "found: " + ", ".join(matched),
        })

    passed_count = sum(1 for result in results if result["passed"])
    total = len(results)
    return {
        "assertion_results": results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": passed_count / total if total else 0.0,
        },
    }


def parse_tokens(log_text: str) -> int | None:
    matches = re.findall(r"tokens used\s+([0-9,]+)", log_text, flags=re.IGNORECASE)
    if not matches:
        return None
    return int(matches[-1].replace(",", ""))


def build_prompt(case: dict[str, Any]) -> str:
    files = case.get("files") or []
    file_lines = "\n".join(f"- {ROOT / rel}" for rel in files) or "- none"
    return f"""Use the local harden skill from this exact source path:
{ROOT / "SKILL.md"}

Read the skill and any referenced harden files that are needed. Do not edit files. Produce the harden review only.

Eval case: {case["id"]}
User prompt:
{case["prompt"]}

Input files:
{file_lines}
"""


def run_case(case: dict[str, Any], run_dir: Path, model: str, effort: str, timeout: int) -> dict[str, Any]:
    case_dir = run_dir / case["id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    output_path = case_dir / "output.md"
    log_path = case_dir / "codex.log"
    grading_path = case_dir / "grading.json"
    timing_path = case_dir / "timing.json"
    prompt_path = case_dir / "prompt.md"

    prompt = build_prompt(case)
    prompt_path.write_text(prompt, encoding="utf-8")

    command = [
        "codex",
        "exec",
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "-s",
        "read-only",
        "--ephemeral",
        "--skip-git-repo-check",
        "-o",
        str(output_path),
        "-",
    ]

    started = time.monotonic()
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    duration_seconds = time.monotonic() - started
    log_path.write_text(completed.stdout, encoding="utf-8")

    output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    grading = grade_output(case, output)
    grading["case_id"] = case["id"]
    grading["exit_code"] = completed.returncode
    if completed.returncode != 0:
        upgrade_hint = ""
        if "requires a newer version of Codex" in completed.stdout:
            upgrade_hint = " Upgrade Codex before rerunning; do not silently fall back to an older model."
        grading["assertion_results"].append({
            "text": "codex exec exits successfully",
            "passed": False,
            "evidence": f"exit code {completed.returncode}.{upgrade_hint}",
        })
        summary = grading["summary"]
        summary["failed"] += 1
        summary["total"] += 1
        summary["pass_rate"] = summary["passed"] / summary["total"]
    grading_path.write_text(json.dumps(grading, indent=2), encoding="utf-8")

    timing = {
        "duration_seconds": duration_seconds,
        "tokens": parse_tokens(completed.stdout),
        "model": model,
        "reasoning_effort": effort,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    timing_path.write_text(json.dumps(timing, indent=2), encoding="utf-8")

    return {
        "case_id": case["id"],
        "pass_rate": grading["summary"]["pass_rate"],
        "passed": grading["summary"]["failed"] == 0,
        "failed": grading["summary"]["failed"],
        "total": grading["summary"]["total"],
        "duration_seconds": duration_seconds,
        "tokens": timing["tokens"],
        "output_path": str(output_path.relative_to(ROOT)),
        "grading_path": str(grading_path.relative_to(ROOT)),
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return math.sqrt(variance)


def summarize(iteration_dir: Path, runs: list[dict[str, Any]], model: str, effort: str, runs_per_case: int) -> dict[str, Any]:
    by_case: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        by_case.setdefault(run["case_id"], []).append(run)

    case_summary: dict[str, Any] = {}
    for case_id, case_runs in by_case.items():
        pass_rates = [run["pass_rate"] for run in case_runs]
        durations = [run["duration_seconds"] for run in case_runs]
        tokens = [run["tokens"] for run in case_runs if run["tokens"] is not None]
        case_summary[case_id] = {
            "runs": len(case_runs),
            "all_passed": all(run["passed"] for run in case_runs),
            "mean_pass_rate": mean(pass_rates),
            "stddev_pass_rate": stddev(pass_rates),
            "mean_duration_seconds": mean(durations),
            "stddev_duration_seconds": stddev(durations),
            "mean_tokens": mean(tokens) if tokens else None,
            "stddev_tokens": stddev(tokens) if len(tokens) > 1 else 0.0,
            "failed_runs": [
                {
                    "output_path": run["output_path"],
                    "grading_path": run["grading_path"],
                    "failed": run["failed"],
                    "total": run["total"],
                }
                for run in case_runs
                if not run["passed"]
            ],
        }

    pass_rates = [run["pass_rate"] for run in runs]
    durations = [run["duration_seconds"] for run in runs]
    tokens = [run["tokens"] for run in runs if run["tokens"] is not None]
    summary = {
        "iteration": iteration_dir.name,
        "model": model,
        "reasoning_effort": effort,
        "runs_per_case": runs_per_case,
        "total_runs": len(runs),
        "overall": {
            "mean_pass_rate": mean(pass_rates),
            "stddev_pass_rate": stddev(pass_rates),
            "mean_duration_seconds": mean(durations),
            "stddev_duration_seconds": stddev(durations),
            "mean_tokens": mean(tokens) if tokens else None,
            "stddev_tokens": stddev(tokens) if len(tokens) > 1 else 0.0,
        },
        "cases": case_summary,
    }
    (iteration_dir / "benchmark.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run harden skill evals through codex exec.")
    parser.add_argument("--iteration", required=True, help="Result iteration name, for example iteration-1")
    parser.add_argument("--runs", type=int, default=2, help="Runs per eval case")
    parser.add_argument("--model", default=DEFAULT_CODEX_MODEL)
    parser.add_argument("--effort", default=DEFAULT_REASONING_EFFORT)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--case", action="append", help="Run only the specified case id. Repeatable.")
    args = parser.parse_args()

    if args.runs < 1:
        fail("--runs must be >= 1")

    spec = load_evals()
    cases = spec.get("evals")
    if not isinstance(cases, list) or not cases:
        fail("evals/evals.json has no eval cases")
    if args.case:
        wanted = set(args.case)
        cases = [case for case in cases if case.get("id") in wanted]
        missing = wanted - {case.get("id") for case in cases}
        if missing:
            fail("unknown case ids: " + ", ".join(sorted(missing)))

    iteration_dir = RESULTS_ROOT / args.iteration
    iteration_dir.mkdir(parents=True, exist_ok=True)

    runs: list[dict[str, Any]] = []
    for run_number in range(1, args.runs + 1):
        for case in cases:
            print(f"RUN {args.iteration} #{run_number} {case['id']}", flush=True)
            run_dir = iteration_dir / f"run-{run_number:02d}"
            runs.append(run_case(case, run_dir, args.model, args.effort, args.timeout))

    summary = summarize(iteration_dir, runs, args.model, args.effort, args.runs)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
