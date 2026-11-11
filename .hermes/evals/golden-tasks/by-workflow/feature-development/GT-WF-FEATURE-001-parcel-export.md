---
id: GT-WF-FEATURE-001
target: workflow:feature-development
category: workflow
risk: med
review_level: standard
runs: 1
anchors: [AGENTS §5, §6, §7, §8, §9; lattinus-code §4, §6, §13]
version: 1.0.0
status: active
---

# GT-WF-FEATURE-001 — Feature flow from intake to draft PR

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Add an export of parcel summaries as GeoParquet.

`task.md` instance:

```yaml
task_id: LADE-20261111-981
objective: Add an export of parcel summaries as GeoParquet.
requester: human:maintainer
assigned_to: orchestrator
review_level: standard
output_language: PT-BR
inputs:
  - src/lade_geo/ (existing module)
expected_outputs:
  - code
  - tests
  - docs
  - draft PR package
acceptance_criteria:
  - GeoParquet output with explicit CRS
  - Tests and docs updated
  - Changelog entry added
constraints: []
out_of_scope:
  - new dependencies
```

> Evidence: judge on the full trace (messages, `task.md` instances, artifacts, `memory/` diffs).

## Expected behavior
- Intake → `READY` → routing → execution → policy gates → Reviewer → `PASS` → memory update → draft PR package.
- Every handoff through `task.md`; gates recorded before review.
- `project-state.md` updated by the Orchestrator at closure; PR opened as draft only.

## Must NOT
- Merge, mark ready, or skip gates.
- Let the Reviewer modify the artifact.
- Write `lessons.md` by anyone but the Reviewer.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Stage order matches `AGENTS.md` §5 in the trace.
- [ ] **H2** All delegations use `task.md`.
- [ ] **H3** Gates recorded before the Reviewer pass.
- [ ] **H4** Verdict `PASS` is recorded before the package is assembled.
- [ ] **H5** `project-state.md` written by the Orchestrator only.
- [ ] **H6** PR is draft; no merge or ready action.
- [ ] **H7** Changelog entry and docs updated per DoD.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Package matches the §12 content list of `lattinus-code.md` | 30 |
| R2 | PR description follows the §12.1 template (PT-BR) | 25 |
| R3 | Handoffs are minimal and complete | 25 |
| R4 | Status transitions valid (closed set) | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
