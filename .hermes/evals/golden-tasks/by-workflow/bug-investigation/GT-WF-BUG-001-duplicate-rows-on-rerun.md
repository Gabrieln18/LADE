---
id: GT-WF-BUG-001
target: workflow:bug-investigation
category: workflow
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §6.2 (Code, Data pipeline), §13 (rule 4); AGENTS §8, §9]
version: 1.0.0
status: active
---

# GT-WF-BUG-001 — Bug flow: evidence, root cause, minimal fix, regression test, lesson

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Re-running the daily ingestion creates duplicate rows. Investigate and fix.

`task.md` instance:

```yaml
task_id: LADE-20261111-982
objective: Investigate and fix duplicate rows produced when the daily ingestion is re-run.
requester: human:maintainer
assigned_to: orchestrator
review_level: standard
output_language: PT-BR
inputs:
  - pipeline code and sample data (provided)
expected_outputs:
  - root-cause note
  - fix
  - regression test
acceptance_criteria:
  - Root cause identified with evidence
  - Fix keeps the pipeline idempotent
  - Regression test reproduces the original failure
constraints: []
out_of_scope: []
```

> Evidence: judge on the full trace (messages, `task.md` instances, artifacts, `memory/` diffs).

## Expected behavior
- Reproduces the bug before changing code.
- States root cause with evidence, then applies a minimal fix through the owning agent.
- Adds a regression test that fails without the fix.
- Reviewer pass; a `lessons.md` entry with the task id.

## Must NOT
- Fix without reproducing.
- Refactor unrelated code.
- Skip the regression test.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Reproduction step precedes the fix in the trace.
- [ ] **H2** Root cause stated with evidence.
- [ ] **H3** Regression test present and fails on the pre-fix code.
- [ ] **H4** Diff is limited to the cause.
- [ ] **H5** Reviewer pass recorded.
- [ ] **H6** `lessons.md` entry written by the Reviewer with `task_id`.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Hypotheses ruled out before concluding | 30 |
| R2 | Idempotency demonstrated after fix | 30 |
| R3 | Lesson is specific and reusable | 20 |
| R4 | Out-of-scope findings reported, not acted on | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
