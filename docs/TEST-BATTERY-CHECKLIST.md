# Test battery — execution checklist

> **Version:** 1.0.0 · **Date:** 2026-11-20 · **Location:** `docs/TEST-BATTERY-CHECKLIST.md`
> **Owner:** maintainer · **Protocol:** `.hermes/evals/README.md` (isolation, judging, scoring, governance)
> Runbook, not a report. Tick the boxes; record results in `.hermes/evals/reports/`. Nothing here judges:
> the runner records evidence, a human fills the verdicts.
> Cost estimate: 42 turns for the 24 active tasks, plus 2 for the new build tasks.

All commands run from the repository root (`~/Área de trabalho/LADE`).

---

## 0. Preconditions

- [ ] Deterministic battery is clean. Everything below is meaningless if this fails.

```bash
make test-all          # exit 0: setup --check, lint, links, models-check, tools-check, verify
```

- [ ] Tool surface matches the declaration (9/9 roles).

```bash
make tools-check       # "9 role(s) resolve to exactly the declared surface"
```

- [ ] Gateway serves every profile.

```bash
make roster            # 9 served, parked_profiles: none
```

## 1. Clean the working tree

- [ ] Decide the fate of the pilot artifact `src/` + `tests/` (uncommitted, produced by `GT-SWE-001`).
      Keep it in a delivery directory outside the repository root, or delete it. Leaving it in place
      pollutes every future trace's `repo-status.txt` and the harness's `unittest discover`.

```bash
git status --porcelain          # what is uncommitted
rm -rf src tests                # option A: discard the pilot artifact
```

## 2. Baseline — the 8 `limit` tasks (22 turns)

Gate-critical: 100% of these must pass, and a FAIL here is a rule defect, not a quality score.

- [ ] Run them.

```bash
make eval-suite CATEGORY=limit
```

- [ ] All 22 turns happened.

```bash
make eval-status                        # recorded runs, newest last
make eval-plan CATEGORY=limit           # 8 task(s) · 22 turn(s)
```

- [ ] Draft the report.

```bash
make eval-report TARGET=suite
```

## 3. `happy` + `ambiguity` (10 turns)

- [ ] Run both sets.

```bash
make eval-suite CATEGORY=happy          # 8 task(s) · 8 turn(s)
make eval-suite CATEGORY=ambiguity      # 2 task(s) · 2 turn(s)
```

- [ ] Re-draft the report so it includes them.

```bash
make eval-report TARGET=suite
```

## 4. Multi-agent mechanism (1 turn)

- [ ] Run the missing scenario (M1, M3, M4 already ran; results in `docs/reports/LADE-20261120-test-battery-pilot.md` §5).

```bash
make probe SCENARIO=M2_routing_without_delegation
```

- [ ] What to look for: did intake write a real `task.md` (the `file` toolset exists now), and did it
      delegate or route? Reference behaviour: `make probe-static`.

## 5. Build capability (2 turns + objective grading)

- [ ] Activate the two drafted tasks (governance: `golden-tasks/` is human-write-only). Without this,
      `eval-run`/`eval-suite` ignore them on purpose (`status: draft`).

```bash
sed -i 's/^status: draft$/status: active/' \
  .hermes/evals/golden-tasks/by-workflow/new-module/GT-BUILD-001-idempotent-parcel-ingest.md \
  .hermes/evals/golden-tasks/by-agent/software-engineer/GT-BUILD-002-control-single-role.md
```

- [ ] Run the **control arm first** (`GT-BUILD-002`): direct to `software-engineer`, no design gate, so it
      actually delivers code the harness can grade.

```bash
make eval-run TASK=GT-BUILD-002
```

- [ ] Grade the delivered artifact objectively (C1–C8).

```bash
make eval-status                                  # find the trace directory
cat .lade-runs/GT-BUILD-002/<stamp>/repo-status.txt   # see what was created
make build-check WORKDIR=<delivery dir>
```

- [ ] Then `GT-BUILD-001` (full `new-module` workflow). Expected: it stops at the human design gate (H1)
      and does **not** implement — that is correct behaviour with no human in the loop, and it is a valid
      eval of the gate. Do not read it as a failure.

```bash
make eval-run TASK=GT-BUILD-001
make eval-checklist TASK=GT-BUILD-001
```

- [ ] Compare the two arms and record it in the report (§8 of the report template): correctness, tokens,
      wall time, rework.

## 6. Workflows (10 turns, trace-judged)

- [ ] Run last, they are the most expensive.

```bash
make eval-suite CATEGORY=workflow       # 6 task(s) · 10 turn(s)
```

- [ ] Judge on the trace (sequence, gates, approvals), not on the final text.

## 7. Verdicts (human)

- [ ] Print each task's own checks and rubric.

```bash
make eval-checklist TASK=GT-ORCH-003
```

- [ ] Fill every Hard check and rubric score in `.hermes/evals/reports/<report>.md`.
- [ ] Apply the gate: **100% of `limit`** and **≥ 80% overall**, no regression vs the previous report.
- [ ] Never let the Reviewer judge its own `GT-REV-*` runs — human or separate session.
- [ ] Fixes go to the rule, skill, manifest or policy. **Editing the eval so it passes is not a fix**
      (`evals/README.md` §7).

## 8. When to re-run (regression triggers)

- [ ] A `SOUL.md`, agent manifest, skill, policy, workflow or template changed → that agent's tasks, **all**
      `limit` tasks, and the workflows that include it (`evals/README.md` §6).
- [ ] Root `SOUL.md`, root `AGENTS.md`, `permissions.md` or `lattinus-code.md` changed → full suite.

---

## Reading the results

| Observation | Meaning | Action |
|---|---|---|
| exit code ≠ 0 with 0 tokens and duration < 1 s | infrastructure failure (CLI flag, missing model), no signal about the agent | exclude from the gate, say so in report §3 |
| `tools_missing` from `make tools-check` | a `disabled_toolsets` entry carries tools the role keeps | remove the bundle name, re-run (`ADR-0003`) |
| `--` in a results table cell | the run happened but nothing was judged yet | fill it from the task's checks |
| harness `C1`/`C2` FAIL on a delivery | the artifact does not run or has no tests | check `repo-status.txt` first: the delivery may not be where you pointed `--workdir` |
| probe shows the child on the parent's model | expected: delegation does not confer the role's model (`ADR-0001`) | not a defect; record it |

## Battery at a glance

| Layer | Command | Turns | Gate |
|---|---|:--:|---|
| Deterministic | `make test-all` | 0 | exit 0 |
| Smoke (optional) | `make smoke ROLE=<role>` | 9 | 9/9 exit 0 |
| Mechanism | `make probe` | 4 | evidence, judged by eye |
| `limit` | `make eval-suite CATEGORY=limit` | 22 | 100% |
| `happy` + `ambiguity` | `make eval-suite CATEGORY="happy ambiguity"` | 10 | ≥ 80% overall |
| Build | `make eval-run TASK=GT-BUILD-00{1,2}` + `make build-check` | 2 | C1–C8 + control comparison |
| Workflows | `make eval-suite CATEGORY=workflow` | 10 | ≥ 80% overall |

## Do not

- Do not run the whole battery in one go: the `limit` sweep decides whether the rest is meaningful as is.
- Do not trust an attached test log from an agent: `make build-check` re-executes the artifact.
- Do not hand-edit inside a `lade:*` region, and do not commit — everything stays uncommitted for review.
- Do not treat a `status: draft` golden task as runnable; activation is a human decision.
