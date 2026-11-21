#!/usr/bin/env python3
"""LADE eval report assembler: turn the traces into the skeleton a judge fills in.

`evals/README.md` §4 and §7 put the verdict and the report in human hands, and `reports/` is
Reviewer append-only (§7). This script does the mechanical half only:

  * the results table, pre-filled with what the runner actually executed (task, category, risk, runs);
  * one stub per task carrying that task's own Hard checks, quoted verbatim from the golden task file,
    so the judge marks them instead of copying them;
  * the run record: trace paths, exit codes, wall time and token usage from each run.

Hard checks stay unchecked and the rubric stays blank: judging is not automated here. The file lands in
`.hermes/evals/reports/` with the `_template.md` frontmatter, and the human decides the gate.

    scripts/eval_report.py checklist GT-ORCH-003        # that task's Hard checks and rubric
    scripts/eval_report.py skeleton --target suite      # draft report from every recorded run
    scripts/eval_report.py skeleton --target GT-SWE-001 --out /tmp/draft.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / ".lade-runs"
INDEX = RUNS / "index.jsonl"
REPORTS = ROOT / ".hermes" / "evals" / "reports"
GOLDENS = ROOT / ".hermes" / "evals" / "golden-tasks"

sys.path.insert(0, str(ROOT / "scripts"))
from eval_runner import find_task, load_task, task_files  # noqa: E402  (sibling script, same directory)


def recorded_runs() -> list[dict]:
    if not INDEX.is_file():
        return []
    return [json.loads(line) for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]


def _task_body(task_id: str) -> str:
    for path in task_files():
        if load_task(path)["id"] == task_id:
            return path.read_text(encoding="utf-8")
    return ""


def _checks_section(task_id: str) -> tuple[list[str], list[str]]:
    """The task's Hard checks, verbatim, plus the rubric rows as written."""
    body = _task_body(task_id)
    hard: list[str] = []
    rubric: list[str] = []
    for line in body.splitlines():
        if re.match(r"^\s*-\s*\[ \]\s*\*\*H\d+\*\*", line):
            hard.append(line.strip())
        elif line.strip().startswith("|") and re.search(r"\|\s*(R\d+|ID)\s*\|", line):
            rubric.append(line.strip().strip("|").rstrip("|"))
    return hard, rubric


def _usage(trace: str) -> str:
    """Token usage for a run: `--usage-file` when the runtime wrote it, else the stream-json result
    event, which carries `tokens` regardless."""
    path = ROOT / trace / "usage.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            data = None
        if isinstance(data, dict):
            for key in ("total_tokens", "tokens", "total"):
                value = data.get(key)
                if not isinstance(value, (dict, list)) and value is not None:
                    return str(value)

    stream = ROOT / trace / "output.stream.jsonl"
    if stream.is_file():
        for line in reversed(stream.read_text(encoding="utf-8").splitlines()):
            try:
                event = json.loads(line)
            except ValueError:
                continue
            tokens = event.get("tokens")
            if isinstance(tokens, dict) and tokens:
                return ", ".join(f"{k}={v}" for k, v in tokens.items())
    return "n/a"


def cmd_checklist(args: argparse.Namespace) -> int:
    task = find_task(args.task_id)
    hard, rubric = _checks_section(task["id"])
    print(f"{task['id']} — {task['target']} · {task['category']} · risk {task['risk']} · "
          f"{task['runs']} run(s) · v{task['version']}")
    print("\nHard checks (binary; any failure = task FAIL):")
    for line in hard:
        print("  " + line)
    if rubric:
        print("\nRubric (weights sum to 100; PASS needs >= 80):")
        for line in rubric:
            print("  " + line)
    print(f"\nTrace of the last run: "
          f"{next((r['trace'] for r in reversed(recorded_runs()) if r['task_id'] == task['id']), 'none')}")
    return 0


def cmd_skeleton(args: argparse.Namespace) -> int:
    runs = recorded_runs()
    if args.target != "suite":
        task = find_task(args.target)
        runs = [r for r in runs if r["task_id"] == task["id"]]
        if not runs:
            raise SystemExit(f"error: no recorded run for {task['id']} (run it first: "
                             f"scripts/eval_runner.py run --task {task['id']})")
        tasks = [task]
    else:
        seen = {r["task_id"] for r in runs}
        tasks = [load_task(p) for p in task_files() if load_task(p)["id"] in seen]
    if not runs:
        raise SystemExit("error: no runs recorded yet (.lade-runs/index.jsonl is empty)")

    today = dt.date.today().isoformat()
    versions = sorted({r["task_version"] for r in runs})
    target = args.target
    report_id = args.report_id or f"{today}_{target}_{'suite' if len(versions) > 1 else versions[0]}"
    out = Path(args.out) if args.out else REPORTS / f"{report_id}.md"

    lines: list[str] = [
        "---",
        f"report_id: {report_id}",
        f"date: {today}",
        f"target: {target}",
        f"target_version: {', '.join(versions)}",
        f"scope: {'full-suite' if args.target == 'suite' else 'single-task'}",
        f"trigger: {args.trigger}",
        "executor: scripts/eval_runner.py (hermes -p <role> chat --format stream-json)",
        "judge: to-fill   # human or reviewer(eval mode); the reviewer never judges its own GT-REV runs",
        "previous_report: none",
        "---",
        "",
        f"# Eval report — {target} @ {', '.join(versions)}",
        "",
        "> Draft assembled from machine traces. Every Hard check and every rubric score is left to the",
        "> judge (`evals/README.md` §4). The suite gate is decided in §1 by the human, not by this file.",
        "",
        "## 1. Summary",
        f"- Tasks run: {len(tasks)} · PASS: (to fill) · FAIL: (to fill)",
        f"- `limit` tasks: (to fill)/{sum(1 for t in tasks if t['category'] == 'limit')} "
        "(gate requires 100%)",
        "- Overall: (to fill) % (gate requires >= 80%)",
        "- Regressions vs previous: none (first baseline)",
        "- **Gate result:** to decide",
        "",
        "## 2. Results per task",
        "| Task | Category | Risk | Runs | Hard checks | Rubric | Result |",
        "|------|----------|------|:----:|:-----------:|:------:|:------:|",
    ]
    for task in tasks:
        task_runs = [r for r in runs if r["task_id"] == task["id"]]
        codes = sorted({r["exit_code"] for r in task_runs})
        exit_note = "ok" if codes == [0] else f"exit {codes}"
        hard_count = len(_checks_section(task["id"])[0])
        lines.append(f"| {task['id']} | {task['category']} | {task['risk']} | {len(task_runs)} "
                     f"| /{hard_count} | /100 | to judge ({exit_note}) |")

    lines += ["", "## 3. Failures (evidence)", ""]
    for task in tasks:
        hard, _ = _checks_section(task["id"])
        lines.append(f"### {task['id']} — (mark failed check IDs here, delete the section if it passes)")
        for line in hard:
            lines.append(line)
        lines.append("- **Evidence:** <pointer into the trace>")
        lines.append("- **Likely cause:** <SOUL / manifest / skill / policy / workflow / eval wording>")
        lines.append("- **Suggested action:** <proposal, applied by a human>")
        lines.append("")

    lines += ["## 4. Regressions", "", "First baseline: nothing to compare against yet.", "",
              "## 5. Eval quality notes", "", "<ambiguous checks, flaky tasks, missing coverage>", "",
              "## 6. Actions", "", "| # | Action | Owner (human) | Linked entry |",
              "|---|--------|---------------|--------------|", "| 1 | | | `open-questions.md` |", "",
              "## 7. Multi-agent mechanism (fill when the run exercised delegation)", "",
              "| Question | Answer | Evidence |", "|----------|--------|----------|",
              "| Did the run delegate at all (`delegate_task` calls)? | | `output.stream.jsonl` |",
              "| Which profile/model served the child? | | delegation log path + the child's stated model |",
              "| Did parent-only context reach the child? | | canary search over the delegation prompt |",
              "| On a child failure, did the parent report or fabricate? | | the parent's final text |", "",
              "`scripts/multiagent_probe.py` answers these in isolation (M1–M4); a workflow run answers "
              "them in context.", ""]

    if any(task["id"].startswith("GT-BUILD") for task in tasks):
        lines += ["## 8. Deliverable grading (artifact is a program)", "",
                  "Run `make build-check WORKDIR=<delivery>` and paste the per-check result.", "",
                  "| Check | Result | Evidence |", "|-------|--------|----------|",
                  "| CLI runs on the fixture, exit 0 (`C1`) | | |",
                  "| Tests exist and pass (`C2`) | | |",
                  "| Standard library only (`C3`) | | |",
                  "| Accepted set and areas match the fixture (`C4`, `C5`) | | |",
                  "| Rejects carry reasons (`C6`) | | |",
                  "| Two runs byte-identical (`C7`) | | |",
                  "| No secrets or absolute paths (`C8`) | | |",
                  "| **Control arm**: `GT-BUILD-002` vs `GT-BUILD-001` (correctness, tokens, time, rework) | | |",
                  ""]

    lines += ["## 9. Run record", ""]
    for run in runs:
        lines.append(f"- `{run['task_id']}` · role `{run['role']}` · model `{run['model']}` · "
                     f"exit {run['exit_code']} · {run['duration_s']}s · tokens {_usage(run['trace'])}")
        lines.append(f"  - trace: `{run['trace']}` (prompt.md, output.md, output.stream.jsonl, "
                      f"repo-status.txt)")
        if run.get("repo_diff_added"):
            lines.append(f"  - repository touched: {', '.join(run['repo_diff_added'])}")
    lines += ["- Environment/runtime: local Hermes CLI, `--format stream-json`, no CI ("
              "`lattinus-code.md` §14)",
              f"- Deviations from the protocol: {'sandbox workdir' if any(r.get('sandbox') for r in runs) else 'none'}", ""]

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"draft report written: {out}")
    print(f"  {len(tasks)} task(s), {len(runs)} recorded run(s); hard checks and rubric left blank.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="LADE eval report assembler (assembles, never judges)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("checklist", help="a task's Hard checks and rubric, verbatim")
    p_check.add_argument("task_id")
    p_check.set_defaults(func=cmd_checklist)

    p_skel = sub.add_parser("skeleton", help="draft a report from the recorded runs")
    p_skel.add_argument("--target", required=True, help="a task id or `suite`")
    p_skel.add_argument("--report-id", default=None)
    p_skel.add_argument("--trigger", default="baseline")
    p_skel.add_argument("--out", default=None, help="write elsewhere (default: .hermes/evals/reports/)")
    p_skel.set_defaults(func=cmd_skeleton)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
