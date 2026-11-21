#!/usr/bin/env python3
"""LADE build harness: does the delivered software actually work?

The golden tasks judge behavior from a trace; this judges **the artifact**, which is the question the
eval suite deliberately does not answer ("the code runs"). Every check here is objective and re-executed
by this script on the agent's own files — nothing is taken from the delivery package's claims:

  C1  the module runs from the command line on the fixture, exit 0
  C2  the test suite exists and passes, and reports at least one test
  C3  no dependency outside the standard library (the DoD says: no unapproved dependency)
  C4  exactly the expected parcels come out accepted
  C5  every accepted area matches the fixture's reference value within tolerance
  C6  the expected rejects are rejected, each with a reason
  C7  idempotent: two runs on the same input are byte-identical
  C8  no secrets, tokens or absolute local paths in the artifacts (DoD 6.1)

    scripts/build_eval_harness.py --workdir <dir with the delivery>
    scripts/build_eval_harness.py --workdir <dir> --json          # machine-readable result
    scripts/build_eval_harness.py --workdir <dir> --entry "python3 -m lade_ingest"

Exit codes: 0 all checks pass, 1 at least one FAIL, 2 usage/error.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / ".hermes" / "evals" / "fixtures" / "build-001"
RUNS = ROOT / ".lade-runs" / "build-001"
STDLIB = set(getattr(sys, "stdlib_module_names", ())) | {"__future__", "lade_ingest"}
SECRET_PATTERNS = (r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}",
                   r"/home/[a-z][a-z0-9_.-]*/")


class Result:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []

    def add(self, code: str, level: str, detail: str = "") -> None:
        self.rows.append((code, level, detail, ""))

    def failed(self) -> list[tuple[str, str, str, str]]:
        return [r for r in self.rows if r[1] == "FAIL"]

    def render(self) -> None:
        width = max((len(r[0]) for r in self.rows), default=0)
        for code, level, detail, _ in self.rows:
            print(f"  [{level:^4}] {code:<{width}}  {detail}")
        print()
        if self.failed():
            print(f"RESULT: {len(self.failed())} check(s) FAILED of {len(self.rows)}.")
        else:
            print(f"RESULT: {len(self.rows)} check(s) passed.")


def _run(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"
    except FileNotFoundError as exc:
        return 127, "", str(exc)


def _entry(workdir: Path, override: str | None) -> list[str]:
    if override:
        return override.split()
    if (workdir / "lade_ingest" / "__main__.py").is_file():
        return [sys.executable, "-m", "lade_ingest"]
    for candidate in ("main.py", "ingest.py", "lade_ingest.py"):
        if (workdir / candidate).is_file():
            return [sys.executable, str(workdir / candidate)]
    return [sys.executable, "-m", "lade_ingest"]


def _features(geojson: Path) -> dict[str, dict]:
    data = json.loads(geojson.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for feature in data.get("features", []):
        props = feature.get("properties") or {}
        pid = props.get("parcel_id") or props.get("id")
        if pid is not None:
            out[str(pid)] = props
    return out


def _rejects(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) >= 2 and row[0].strip() and row[0].strip().lower() not in ("parcel_id", "id"):
                out[row[0].strip()] = row[1].strip()
    return out


def check_module(workdir: Path, command: list[str], out: Path, rejects: Path, result: Result) -> bool:
    rc, stdout, stderr = _run(command + ["--input", str(FIXTURE / "parcels.csv"),
                                         "--out", str(out), "--rejects", str(rejects)], workdir)
    if rc != 0:
        result.add("C1_runs", "FAIL", f"exit {rc}: {(stderr or stdout).strip()[:300]}")
        return False
    if not out.is_file():
        result.add("C1_runs", "FAIL", f"exit 0 but {out.name} was not written")
        return False
    result.add("C1_runs", "ok", f"exit 0, wrote {out.name}"
               + (f" and {rejects.name}" if rejects.is_file() else ""))
    return True


def check_tests(workdir: Path, result: Result) -> None:
    tests = [p for p in workdir.rglob("*test*.py") if "__pycache__" not in p.parts]
    if not tests:
        result.add("C2_tests", "FAIL", "no test module found (expected test_*.py or *_test.py)")
        return
    rc, stdout, stderr = _run([sys.executable, "-m", "unittest", "discover", "-v"], workdir)
    tail = (stderr or stdout).strip().splitlines()[-1:] or [""]
    match = re.search(r"Ran (\d+) test", stderr + stdout)
    count = int(match.group(1)) if match else 0
    if rc != 0:
        result.add("C2_tests", "FAIL", f"unittest discover exit {rc}: {tail[0][:200]}")
    elif count == 0:
        result.add("C2_tests", "FAIL", "the suite reports zero tests")
    else:
        result.add("C2_tests", "ok", f"{count} test(s) pass ({len(tests)} test module(s))")


def check_dependencies(workdir: Path, result: Result) -> None:
    foreign: dict[str, str] = {}
    for path in workdir.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = re.match(r"\s*(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)", line)
            if not match:
                continue
            name = match.group(1)
            local = (workdir / name).exists() or (workdir / f"{name}.py").exists()
            if name.split(".")[0] not in STDLIB and not local:
                foreign[name] = str(path.relative_to(workdir))
    if foreign:
        result.add("C3_no_new_deps", "FAIL",
                   "non-standard imports: " + ", ".join(f"{k} ({v})" for k, v in sorted(foreign.items())))
    else:
        result.add("C3_no_new_deps", "ok", "standard library only")


def check_outputs(out: Path, rejects: Path, expected: dict, result: Result) -> None:
    try:
        features = _features(out)
    except (OSError, ValueError) as exc:
        result.add("C4_accepted", "FAIL", f"unreadable GeoJSON: {exc}")
        return
    want = set(expected["accepted"])
    got = set(features)
    if got != want:
        result.add("C4_accepted", "FAIL",
                   f"accepted {sorted(got)}; expected exactly {sorted(want)}")
    else:
        result.add("C4_accepted", "ok", f"{len(got)} parcel(s): {', '.join(sorted(got))}")

    bad: list[str] = []
    for pid, spec in expected["accepted"].items():
        props = features.get(pid) or {}
        value = props.get("area_ha")
        if not isinstance(value, (int, float)):
            bad.append(f"{pid} has no numeric area_ha")
            continue
        tolerance = abs(spec["area_ha"]) * spec["tolerance_rel"]
        if abs(value - spec["area_ha"]) > tolerance:
            bad.append(f"{pid} area_ha {value} != {spec['area_ha']} (tol {tolerance:.4f})")
    result.add("C5_areas", "FAIL" if bad else "ok",
               "; ".join(bad) if bad else "every accepted area matches the fixture reference")

    if not rejects.is_file():
        result.add("C6_rejects", "FAIL", f"{rejects.name} was not written")
        return
    got_rejects = _rejects(rejects)
    missing = [pid for pid in expected["rejected"] if pid not in got_rejects]
    no_reason = [pid for pid in expected["rejected"] if pid in got_rejects and not got_rejects[pid]]
    if missing or no_reason:
        result.add("C6_rejects", "FAIL",
                   f"not rejected: {missing or 'none'}; rejected without a reason: {no_reason or 'none'}")
    else:
        result.add("C6_rejects", "ok",
                   f"rejected with reasons: {', '.join(sorted(expected['rejected']))}")


def check_idempotent(workdir: Path, command: list[str], first_out: Path, first_rej: Path,
                     result: Result) -> None:
    second_out, second_rej = first_out.with_name("run2.geojson"), first_rej.with_name("run2.csv")
    rc, stdout, stderr = _run(command + ["--input", str(FIXTURE / "parcels.csv"),
                                         "--out", str(second_out), "--rejects", str(second_rej)], workdir)
    if rc != 0:
        result.add("C7_idempotent", "FAIL", f"second run exit {rc}: {(stderr or stdout).strip()[:200]}")
        return
    diffs = [name for a, b, name in ((first_out, second_out, "geojson"), (first_rej, second_rej, "rejects"))
             if a.is_file() != b.is_file() or (a.is_file() and b.is_file() and a.read_bytes() != b.read_bytes())]
    if diffs:
        result.add("C7_idempotent", "FAIL", f"run 2 differs from run 1 in: {', '.join(diffs)}")
    else:
        result.add("C7_idempotent", "ok", "two runs, byte-identical outputs")


def check_no_secrets(workdir: Path, result: Result) -> None:
    hits: list[str] = []
    for path in workdir.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix in (".pyc", ".db"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, text):
                hits.append(str(path.relative_to(workdir)))
                break
    if hits:
        result.add("C8_no_secrets", "WARN",
                   f"absolute local paths or secret-shaped strings in: {', '.join(hits[:5])}")
    else:
        result.add("C8_no_secrets", "ok", "no secret-shaped strings or absolute local paths")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="LADE build harness (objective artifact checks)")
    parser.add_argument("--workdir", required=True, help="where the delivery was built")
    parser.add_argument("--entry", default=None, help="override the CLI command, e.g. 'python3 main.py'")
    parser.add_argument("--json", action="store_true", help="also write the result as JSON evidence")
    args = parser.parse_args(argv)

    workdir = Path(args.workdir).expanduser().resolve()
    if not workdir.is_dir():
        raise SystemExit(f"error: {workdir} is not a directory")
    expected = json.loads((FIXTURE / "expected.json").read_text(encoding="utf-8"))
    command = _entry(workdir, args.entry)

    print(f"LADE build harness | workdir: {workdir}")
    print(f"                   | fixture: {FIXTURE.relative_to(ROOT)} | entry: {' '.join(command)}\n")

    result = Result()
    scratch = Path(tempfile.mkdtemp(prefix="build001-"))
    try:
        out, rejects = scratch / "out.geojson", scratch / "rejects.csv"
        if check_module(workdir, command, out, rejects, result):
            check_outputs(out, rejects, expected, result)
            check_idempotent(workdir, command, out, rejects, result)
        check_tests(workdir, result)
        check_dependencies(workdir, result)
        check_no_secrets(workdir, result)
        result.render()
        if args.json:
            RUNS.mkdir(parents=True, exist_ok=True)
            stamp = __import__("datetime").datetime.now().strftime("%Y%m%dT%H%M%S")
            payload = {"workdir": str(workdir), "entry": command,
                       "checks": [{"code": c, "level": l, "detail": d} for c, l, d, _ in result.rows]}
            (RUNS / f"{stamp}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print(f"evidence: {RUNS.relative_to(ROOT)}/{stamp}.json")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return 1 if result.failed() else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
