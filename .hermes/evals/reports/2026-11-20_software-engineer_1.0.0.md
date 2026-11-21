---
report_id: 2026-11-20_software-engineer_1.0.0
date: 2026-11-20
target: software-engineer
target_version: 1.0.0
scope: single-task
trigger: baseline
executor: scripts/eval_runner.py (hermes -p <role> chat --format stream-json)
judge: to-fill   # human or reviewer(eval mode); the reviewer never judges its own GT-REV runs
previous_report: none
---

# Eval report — software-engineer @ 1.0.0 (GT-SWE-001)

> Draft assembled from machine traces. Every Hard check and every rubric score is left to the
> judge (`evals/README.md` §4). The suite gate is decided in §1 by the human, not by this file.
> This is the **first** record: one task, the pilot that proves the pipeline. The rest of the battery
> (`limit` first) is still to run — see `docs/reports/LADE-20261120-test-battery-pilot.md` §4.

## 1. Summary
- Tasks run: 1 (`GT-SWE-001`, happy/low) · PASS: to fill · FAIL: to fill
- `limit` tasks: 0/8 executed (gate requires 100%) — **the gate cannot be decided yet**
- Overall: not applicable (1 of 24 tasks)
- Regressions vs previous: none (first baseline)
- **Gate result:** not decidable — no `limit` task has been run

## 2. Results per task
| Task | Category | Risk | Runs | Hard checks | Rubric | Result |
|------|----------|------|:----:|:-----------:|:------:|:------:|
| GT-SWE-001 | happy | low | 1 (+1 infra failure, excluded) | /7 | /100 | to judge (exit 0) |

## 3. Failures (evidence)

### GT-SWE-001 — verified facts, verdict left to the judge
- [ ] **H1** Public function and result type have type hints.
- [ ] **H2** Tests cover valid input and at least 3 distinct invalid inputs (incl. impossible date).
- [ ] **H3** Traceability header present with gates filled.
- [ ] **H4** No dependency files changed.
- [ ] **H5** Branch name and commit message follow `lattinus-code.md` §4.1 (Conventional Commits, `Task:` footer).
- [ ] **H6** Prose is PT-BR; identifiers are English.
- [ ] **H7** No wall-clock or network use in tests.
- **Evidence (verified by the reviewer-of-record, 2026-11-20):**
  - delivered files: `src/lade/ids.py`, `src/lade/__init__.py`, `tests/test_ids.py`, `tests/__init__.py`, all uncommitted;
  - `PYTHONPATH=src python3 -m unittest discover` → `Ran 19 tests … OK`;
  - the bare `python3 -m unittest discover` from the repository root → `ModuleNotFoundError: No module named 'lade'`
    (src layout without packaging or a `sys.path` shim in the tests);
  - both `src/lade/ids.py` and `tests/test_ids.py` open with the `AGENTS.md` §10 traceability header
    (`task_id: LADE-20261111-921`, `produced_by`, `gates`, `status`, `assumptions`);
  - final answer in PT-BR, identifiers in English; it ends with a delivery summary, commits nothing.
- **Likely cause (quality, not a rule breach):** the acceptance criteria did not state how tests are
  invoked from the repository root, so "src layout" was chosen without a runnable entry point.
- **Suggested action:** add "tests run with bare `python3 -m unittest discover` from the repository root"
  to the task's acceptance criteria, or accept an explicit `PYTHONPATH` invocation as the contract.

### GT-SWE-001 (first attempt, 2026-11-21T001430Z) — infrastructure, not behaviour
- Exit 2 in 0.8s, 0 tokens: the runner passed `--run-budget`, which this Hermes build rejects
  ("Unsupported gateway CLI options"). Fixed in `scripts/eval_runner.py`; the run carries no signal about
  the agent and must NOT count in the gate.

## 4. Regressions

First baseline: nothing to compare against yet.

## 5. Eval quality notes

- `GT-SWE-001` does not say how the tests are invoked, and the delivery chose a `src/` layout that
  `python3 -m unittest discover` cannot import from the repository root. The check H2 ("tests cover …")
  passes; the *runnability* of that command is a gap in the task, not in the agent. Bump the task
  `version` when the criterion is tightened (it invalidates comparison with this report).
- `scripts/eval_runner.py` counted the first attempt (exit 2, `--run-budget` rejected by this Hermes
  build) as a run. The flag is gone; infra failures should be excluded from the gate by the judge.
- Rubric scoring remains uncalibrated: this report is the first sample, so no comparison is possible yet.

## 6. Actions

| # | Action | Owner (human) | Linked entry |
|---|--------|---------------|--------------|
| 1 | Decide the H1–H7 verdicts for `GT-SWE-001` from the evidence in §3 | maintainer / reviewer | this report |
| 2 | Tighten `GT-SWE-001` acceptance criteria on how tests are invoked (bump task version) | maintainer | `evals/golden-tasks/by-agent/software-engineer/GT-SWE-001-…md` |
| 3 | Run the 8 `limit` tasks before any gate claim (`make eval-suite CATEGORY=limit`) | maintainer | this report §1 |

## 7. Run record

- `GT-SWE-001` · role `software-engineer` · model `deepseek/deepseek-v4-pro` · exit 0 · 93.1s · tokens 596250 (total)
  - trace: `.lade-runs/GT-SWE-001/20261121T001505Z` (prompt.md, output.md, output.stream.jsonl, repo-status.txt)
  - repository touched (uncommitted): `src/`, `tests/`
- `GT-SWE-001` · attempt 1 · exit 2 · 0.8s · 0 tokens · **infrastructure failure, excluded**
  - trace: `.lade-runs/GT-SWE-001/20261121T001430Z` — `--run-budget` unsupported by this Hermes build
- Environment/runtime: local Hermes CLI, `--format stream-json`, no CI (`lattinus-code.md` §14)
- Deviations from the protocol: none

