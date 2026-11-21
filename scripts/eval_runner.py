#!/usr/bin/env python3
"""LADE eval runner: execute a golden task and capture the trace the report needs.

The evals in `.hermes/evals/` are markdown by design — a human or an LLM judge decides the verdict
(`evals/README.md` §4). What was missing is everything around the decision: giving the agent ONLY the
`## Input` section, choosing the profile from `target`, keeping the checks away from it, and keeping the
evidence. This script does exactly that and nothing more: **it never judges and never scores**. It writes
machine evidence to `.lade-runs/` (gitignored) and leaves the verdict and the report to a human.

    scripts/eval_runner.py list                      # the catalog: id, target, category, risk, runs
    scripts/eval_runner.py show GT-ORCH-001          # metadata + the exact input the agent would receive
    scripts/eval_runner.py plan --category limit     # what a suite would run, and how many turns
    scripts/eval_runner.py run GT-SWE-001 --dry-run  # print the command and the prompt, execute nothing
    scripts/eval_runner.py run GT-SWE-001            # one run, one trace directory
    scripts/eval_runner.py suite --category limit    # every limit task, honors `runs:` per task
    scripts/eval_runner.py status                    # last runs, from the index

Isolation, per `evals/README.md` §4:
  * Only the `## Input` section reaches the agent; the guidance line is stripped and the checks
    (`## Expected behavior`, `## Hard checks`, `## Rubric`) are never read into the prompt.
  * The prompt travels through `--query-file`, so quotes, `$(...)` and backticks are preserved verbatim.
  * The role comes from `target`: `workflow:<name>` runs as `orchestrator` (workflow tasks are judged on
    the trace, and the orchestrator drives them).
  * Known limitation: the workload runs with the repository as its working directory (so rules, skills and
    references resolve), which means the agent *could* read `evals/golden-tasks/` itself. The trace records
    the repository diff before/after, so a write is visible as evidence; reading is not detectable. Run the
    eval for a role that must not see the checks in a separate session if that matters.

Exit codes: 0 ok, 1 a run failed, 2 usage error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDENS = ROOT / ".hermes" / "evals" / "golden-tasks"
RUNS = ROOT / ".lade-runs"
INDEX = RUNS / "index.jsonl"
HERMES = os.environ.get("HERMES", "hermes")
GUIDANCE_MARK = "only this section"

CATEGORY_ORDER = ("limit", "ambiguity", "happy", "workflow")


# ── task loading ──────────────────────────────────────────────────────────────────────────────────

def task_files() -> list[Path]:
    return sorted(p for p in GOLDENS.rglob("GT-*.md") if p.name != "_template.md")


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the YAML frontmatter as flat `key: value` scalars.

    Deliberately not a YAML parser: `anchors` holds free text with commas, semicolons and parentheses
    that flow-sequence parsing mangles, and every field this script needs is a scalar.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if line.strip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.split("#", 1)[0].strip().strip('"').strip("'")
        meta[key.strip()] = value
    return meta, text[end + 4:]


def load_task(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = _frontmatter(text)

    section: list[str] = []
    inside = False
    for line in body.splitlines():
        if line.startswith("## "):
            inside = line.strip().lower() == "## input"
            continue
        if inside and GUIDANCE_MARK not in line:
            section.append(line)

    target = meta.get("target", "")
    role = target.split(":", 1)[1] if target.startswith("workflow:") else target
    return {
        "id": meta.get("id", path.stem),
        "target": target,
        "role": role,
        "category": meta.get("category", "unknown"),
        "risk": meta.get("risk", "med"),
        "review_level": meta.get("review_level", "standard"),
        "runs": int(meta.get("runs", "1") or 1),
        "version": meta.get("version", "0.0.0"),
        "status": meta.get("status", "draft"),
        "path": str(path.relative_to(ROOT)),
        "input": "\n".join(section).strip() + "\n",
    }


def catalog() -> list[dict]:
    return [load_task(p) for p in task_files()]


def find_task(task_id: str) -> dict:
    matches = [t for t in catalog() if t["id"] == task_id or t["id"].startswith(task_id)]
    if not matches:
        raise SystemExit(f"error: no golden task matches {task_id!r} (see: eval_runner.py list)")
    if len(matches) > 1:
        raise SystemExit(f"error: {task_id!r} is ambiguous: {', '.join(t['id'] for t in matches)}")
    return matches[0]


# ── trace plumbing ────────────────────────────────────────────────────────────────────────────────

def _repo_status() -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip()


def _profile_model(role: str) -> str:
    config = ROOT / "profiles" / role / "config.yaml"
    if not config.is_file():
        return ""
    in_model = False
    for line in config.read_text(encoding="utf-8").splitlines():
        if line.strip() == "model:":
            in_model = True
        elif in_model and line.strip().startswith("default:"):
            return line.split("default:", 1)[1].strip()
        elif in_model and line and not line[0].isspace():
            break
    return ""


def _stream_text(raw: str) -> str:
    """Assistant text out of a stream-json transcript, for reading and judging by eye."""
    parts: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            parts.append(line)
            continue
        try:
            event = json.loads(line)
        except ValueError:
            parts.append(line)
            continue
        for key in ("text", "content", "delta", "message", "output"):
            value = event.get(key)
            if isinstance(value, str) and value.strip():
                parts.append(value)
                break
    return "\n".join(parts).strip() + "\n"


def execute(task: dict, *, timeout: float, max_turns: int | None,
            sandbox: bool, yolo: bool, dry_run: bool) -> dict:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    trace = RUNS / task["id"] / f"{stamp}"
    prompt_path = RUNS / task["id"] / f"{stamp}.prompt.md"

    command = [HERMES, "--usage-file", str(trace / "usage.json"), "-p", task["role"],
               "chat", "--query-file", str(prompt_path), "--oneshot", "--format", "stream-json"]
    if max_turns:
        command += ["--max-turns", str(max_turns)]
    if yolo:
        command += ["--yolo"]

    workdir = ROOT
    if sandbox:
        workdir = trace / "workdir"
        command += ["--in", str(workdir)]

    record = {
        "task_id": task["id"], "target": task["target"], "role": task["role"],
        "category": task["category"], "risk": task["risk"], "runs_declared": task["runs"],
        "task_version": task["version"], "started_utc": stamp, "model": _profile_model(task["role"]),
        "command": command, "cwd": str(workdir), "sandbox": sandbox,
        "prompt_sha256": hashlib.sha256(task["input"].encode()).hexdigest(),
        "trace": str(trace.relative_to(ROOT)),
    }

    if dry_run:
        print(f"# dry-run {task['id']} (role {task['role']}, {task['category']}, risk {task['risk']})")
        print(f"# cwd: {workdir}")
        print("# command:")
        print("  " + " ".join(shlex.quote(part) for part in command) + f"   # prompt from {prompt_path}")
        print("# prompt the agent would receive (only the ## Input section):\n")
        print(task["input"])
        return record

    trace.mkdir(parents=True, exist_ok=True)
    if sandbox:
        (trace / "workdir").mkdir(parents=True, exist_ok=True)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(task["input"], encoding="utf-8")

    before = _repo_status()
    started = time.monotonic()
    try:
        proc = subprocess.run(command, cwd=workdir, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, rc = (exc.stdout or "") if isinstance(exc.stdout, str) else "", \
                             f"TIMEOUT after {timeout}s", 124
    duration = time.monotonic() - started
    after = _repo_status()

    (trace / "output.stream.jsonl").write_text(stdout, encoding="utf-8")
    (trace / "output.md").write_text(_stream_text(stdout), encoding="utf-8")
    (trace / "stderr.txt").write_text(stderr, encoding="utf-8")
    (trace / "repo-status.txt").write_text(
        f"=== before ===\n{before}\n\n=== after ===\n{after}\n", encoding="utf-8")

    record |= {
        "finished_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "duration_s": round(duration, 1), "exit_code": rc,
        "repo_diff_added": sorted(set(after.splitlines()) - set(before.splitlines())),
        "reported": "to-judge",
    }
    (trace / "meta.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    RUNS.mkdir(parents=True, exist_ok=True)
    with INDEX.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    return record


# ── subcommands ───────────────────────────────────────────────────────────────────────────────────

def cmd_list(args: argparse.Namespace) -> int:
    tasks = catalog()
    if args.category:
        tasks = [t for t in tasks if t["category"] in args.category]
    print(f"{'id':<22} {'role':<20} {'category':<10} {'risk':<5} {'runs':<5} version")
    for task in tasks:
        print(f"{task['id']:<22} {task['role']:<20} {task['category']:<10} {task['risk']:<5} "
              f"{task['runs']:<5} {task['version']}")
    turns = sum(t["runs"] * (3 if t["risk"] == "high" else 1) for t in tasks)
    print(f"\n{len(tasks)} task(s) · {turns} turn(s) if every run is executed "
          f"(high risk = 3 runs, per evals/README.md §5)")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    task = find_task(args.task_id)
    for key in ("id", "target", "role", "category", "risk", "review_level", "runs", "version", "status", "path"):
        print(f"{key:<14} {task[key]}")
    print("\n--- input sent to the agent (nothing else is) ---\n")
    print(task["input"], end="")
    return 0


def _select(args: argparse.Namespace) -> list[dict]:
    tasks = [t for t in catalog() if t["status"] == "active"]
    if args.task:
        wanted: list[dict] = []
        for needle in args.task:
            matches = [t for t in tasks if t["id"].startswith(needle)]
            if not matches:
                raise SystemExit(f"error: no active golden task matches {needle!r}")
            wanted.extend(matches)
        tasks = sorted({t["id"]: t for t in wanted}.values(), key=lambda t: t["id"])
    if args.category:
        tasks = [t for t in tasks if t["category"] in args.category]
    if args.role:
        tasks = [t for t in tasks if t["role"] in args.role]
    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    tasks.sort(key=lambda t: (order.get(t["category"], 99), t["id"]))
    return tasks


def cmd_plan(args: argparse.Namespace) -> int:
    tasks = _select(args)
    turns = 0
    print(f"{'id':<22} {'role':<20} {'category':<10} {'risk':<5} runs")
    for task in tasks:
        runs = args.runs or task["runs"]
        turns += runs
        print(f"{task['id']:<22} {task['role']:<20} {task['category']:<10} {task['risk']:<5} {runs}")
    print(f"\n{len(tasks)} task(s) · {turns} turn(s) · roles touched: "
          f"{', '.join(sorted({t['role'] for t in tasks}))}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    tasks = _select(args) if args.task else []
    if not tasks and not args.task:
        raise SystemExit("error: name at least one task (or use `suite`)")
    failed = 0
    for task in tasks:
        runs = args.runs or task["runs"]
        for attempt in range(1, runs + 1):
            record = execute(task, timeout=args.timeout, max_turns=args.max_turns,
                             sandbox=args.sandbox, yolo=args.yolo, dry_run=args.dry_run)
            if args.dry_run:
                continue
            status = "ok" if record["exit_code"] == 0 else f"rc={record['exit_code']}"
            failed += 0 if record["exit_code"] == 0 else 1
            extra = f" files changed: {', '.join(record['repo_diff_added'])}" if record["repo_diff_added"] else ""
            print(f"{task['id']} run {attempt}/{runs}: {status} in {record['duration_s']}s "
                  f"-> {record['trace']}{extra}")
    return 1 if failed else 0


def cmd_status(args: argparse.Namespace) -> int:
    if not INDEX.is_file():
        print("no runs yet (.lade-runs/index.jsonl absent)")
        return 0
    rows = [json.loads(line) for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.task:
        rows = [r for r in rows if r["task_id"].startswith(args.task)]
    for row in rows[-args.limit:]:
        print(f"{row['started_utc']}  {row['task_id']:<22} {row['role']:<20} rc={row['exit_code']} "
              f"{row['duration_s']}s  {row['trace']}")
    print(f"\n{len(rows)} recorded run(s) in {INDEX.relative_to(ROOT)}")
    return 0


def cmd_suite(args: argparse.Namespace) -> int:
    return cmd_run(args)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="LADE eval runner (executes and records, never judges)")
    parser.add_argument("--timeout", type=float, default=900.0, help="per-run wall-clock timeout (s)")
    parser.add_argument("--max-turns", type=int, default=None, help="agent turns per run")
    parser.add_argument("--sandbox", action="store_true",
                        help="run in an isolated workdir instead of the repository")
    parser.add_argument("--yolo", action="store_true", help="skip approval prompts (pass --yolo to Hermes)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="catalog of golden tasks")
    p_list.add_argument("--category", nargs="*", help="filter: limit ambiguity happy workflow")

    p_show = sub.add_parser("show", help="metadata plus the exact input the agent receives")
    p_show.add_argument("task_id")

    for name, help_text, runner in (("plan", "what a suite would run, and how many turns", cmd_plan),
                                    ("run", "execute the named task(s) and capture the trace", cmd_run),
                                    ("suite", "execute every matching task, honoring `runs:`", cmd_suite)):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--task", nargs="*", help="task id or unique prefix")
        p.add_argument("--category", nargs="*", help="filter: limit ambiguity happy workflow")
        p.add_argument("--role", nargs="*", help="filter by role (the profile that runs it)")
        p.add_argument("--runs", type=int, default=None, help="override `runs:` from the task")
        p.add_argument("--dry-run", action="store_true", help="print the command and prompt, run nothing")
        p.set_defaults(func=runner)

    p_status = sub.add_parser("status", help="last runs, from the index")
    p_status.add_argument("--task", default=None)
    p_status.add_argument("--limit", type=int, default=20)

    args = parser.parse_args(argv)
    if args.command == "list":
        return cmd_list(args)
    if args.command == "show":
        return cmd_show(args)
    if args.command == "status":
        return cmd_status(args)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
