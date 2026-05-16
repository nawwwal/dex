#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"
DEFAULT_CODEX_MODEL = "gpt-5.5"
DEFAULT_REASONING_EFFORT = "medium"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def term_present(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def grade_output(case: dict[str, Any], output: str) -> dict[str, Any]:
    checks = case["deterministic_checks"]
    results = []

    for group in checks.get("must_include_any", []):
        passed = term_present(output, group)
        results.append(
            {
                "text": "include " + " + ".join(group),
                "passed": passed,
                "evidence": "all terms found" if passed else "missing one or more terms",
            }
        )

    for group in checks.get("must_not_include_any", []):
        passed = not term_present(output, group)
        results.append(
            {
                "text": "exclude " + " + ".join(group),
                "passed": passed,
                "evidence": "terms absent" if passed else "forbidden terms found together",
            }
        )

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


def stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "variance": 0.0, "stddev": 0.0}
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {"mean": mean, "variance": variance, "stddev": math.sqrt(variance)}


def prompt_for(case: dict[str, Any]) -> str:
    prompt = case["prompt"].replace("evals/files/", str(ROOT / "evals" / "files") + "/")
    if not case["should_trigger"]:
        return f"""You are running a read-only routing eval for a Dex skill.

Skill contract to inspect: {ROOT / "SKILL.md"}
Expected routing mode: route away from playground.

Rules:
- Do not edit files.
- Do not create artifacts.
- Do not apply the playground artifact contract.
- Return only the route-away decision, the exact target skill, and why playground should not handle it.

User prompt:
{prompt}
"""

    return f"""You are running a read-only eval for a Dex skill.

Skill under test: {ROOT / "SKILL.md"}
Expected routing mode: use playground.

Rules:
- Do not edit files.
- Do not create artifacts.
- If a normal run would create a playground file, describe the artifact contract instead.
- Use the provided source files when present.
- Return a concise but complete response that names routing, interaction model, visual grammar, source assumptions, export shape, and any stop condition.

User prompt:
{prompt}
"""


def run_case(
    *,
    codex_bin: str,
    case: dict[str, Any],
    output_dir: Path,
    model: str,
    effort: str,
    timeout: int,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_path = output_dir / "trace.jsonl"
    final_path = output_dir / "final.txt"
    stderr_path = output_dir / "stderr.txt"

    cmd = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--json",
        "--sandbox",
        "read-only",
        "--cd",
        str(ROOT.parents[3]),
        "--output-last-message",
        str(final_path),
    ]
    cmd.extend([
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
    ])
    cmd.append(prompt_for(case))

    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=ROOT.parents[3],
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    duration = time.perf_counter() - start

    trace_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    output = final_path.read_text(encoding="utf-8") if final_path.exists() else ""
    if proc.returncode != 0 or not output.strip():
        grading = {
            "assertion_results": [
                {
                    "text": "agent run completed and produced final output",
                    "passed": False,
                    "evidence": f"exit_code={proc.returncode}, output_chars={len(output)}",
                }
            ],
            "summary": {"passed": 0, "failed": 1, "total": 1, "pass_rate": 0.0},
            "error": proc.stderr[-4000:],
        }
    else:
        grading = grade_output(case, output)
    grading.update(
        {
            "case_id": case["id"],
            "exit_code": proc.returncode,
            "duration_seconds": duration,
            "output_chars": len(output),
            "model": model,
            "reasoning_effort": effort,
        }
    )
    (output_dir / "grading.json").write_text(json.dumps(grading, indent=2), encoding="utf-8")
    return grading


def main() -> int:
    parser = argparse.ArgumentParser(description="Run playground eval benchmark with Codex.")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument("--category", action="append", dest="categories")
    parser.add_argument("--out-dir", default=f"/tmp/playground-eval-benchmark-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--model", default=DEFAULT_CODEX_MODEL)
    parser.add_argument("--effort", default=DEFAULT_REASONING_EFFORT)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    spec = load_json(EVALS_PATH)
    cases = spec["evals"]
    if args.case_ids:
        selected = set(args.case_ids)
        cases = [case for case in cases if case["id"] in selected]
    if args.categories:
        selected_categories = set(args.categories)
        cases = [case for case in cases if case["category"] in selected_categories]
    if not cases:
        raise SystemExit("No eval cases selected")

    out_dir = Path(args.out_dir)
    all_results = []
    for round_index in range(1, args.rounds + 1):
        for case in cases:
            case_dir = out_dir / f"round-{round_index}" / case["id"]
            print(f"RUN round={round_index} case={case['id']}", flush=True)
            try:
                result = run_case(
                    codex_bin=args.codex_bin,
                    case=case,
                    output_dir=case_dir,
                    model=args.model,
                    effort=args.effort,
                    timeout=args.timeout,
                )
            except subprocess.TimeoutExpired:
                result = {
                    "case_id": case["id"],
                    "exit_code": 124,
                    "duration_seconds": args.timeout,
                    "output_chars": 0,
                    "assertion_results": [],
                    "summary": {"passed": 0, "failed": 1, "total": 1, "pass_rate": 0.0},
                }
                case_dir.mkdir(parents=True, exist_ok=True)
                (case_dir / "grading.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            result["round"] = round_index
            all_results.append(result)
            print(
                f"RESULT round={round_index} case={case['id']} pass_rate={result['summary']['pass_rate']:.3f} duration={result['duration_seconds']:.1f}s",
                flush=True,
            )

    by_case: dict[str, list[dict[str, Any]]] = {}
    for result in all_results:
        by_case.setdefault(result["case_id"], []).append(result)

    case_summary = {}
    for case_id, results in by_case.items():
        pass_rates = [result["summary"]["pass_rate"] for result in results]
        durations = [result["duration_seconds"] for result in results]
        case_summary[case_id] = {
            "pass_rate": stats(pass_rates),
            "duration_seconds": stats(durations),
            "runs": len(results),
        }

    benchmark = {
        "skill_name": "playground",
        "model": args.model,
        "reasoning_effort": args.effort,
        "rounds": args.rounds,
        "case_count": len(cases),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "out_dir": str(out_dir),
        "overall": {
            "pass_rate": stats([result["summary"]["pass_rate"] for result in all_results]),
            "duration_seconds": stats([result["duration_seconds"] for result in all_results]),
        },
        "cases": case_summary,
    }
    (out_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    print(json.dumps(benchmark, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
