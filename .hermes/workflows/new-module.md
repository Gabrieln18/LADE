# new-module.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/new-module.md`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Recommended `standard`.**
> Reuses `feature-development` (per subtask) and `code-review`.

## 1. When to Use

Use to create a new module, pipeline, service or component.

Do not use when:
- the work extends an existing module → `feature-development`;
- the work changes the system's structure or existing contracts → `architecture-change`;
  (a new module that needs a new technology or dependency with design impact also needs an ADR, produced in step 3).

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Intake, subtask split, integration check, draft PRs, memory |
| `architect` | Design and ADR proposals |
| executors | Domain agents by subtask: `software-engineer`, `data-engineer`, `geospatial-engineer`, `ai-engineer`, `devops-sre` |
| `reviewer` | Reviews design and each PR; architecture conformance at the end |
| human | Approves design (H1) and merges (H2) |

## 3. Preconditions

Definition of Ready (`lattinus-code.md` §5), plus in `task.md`:
- purpose and consumers of the module;
- inputs and outputs, with formats and expected volumes;
- domain constraints (CRS, temporal resolution, scale) when spatial data is involved;
- known dependencies and integration points.

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate `task.md`; set `READY`; route | `task.md` → `assigned_to` | — |
| 2 | architect | Write design: boundaries, public interface, contracts, dependencies, data and CRS assumptions, scale, observability, failure modes, test strategy, alternatives | `task.md`, references → `templates/design.md` | — |
| 3 | architect | Propose ADR if there is a decision with trade-offs (technology, dependency, contract standard) | design → `templates/adr.md` (`Proposed`) | `dependencies` if packages are proposed |
| 4 | reviewer | `CALL code-review` on design and ADR (skipped if `human-only`) | design → verdict | — |
| 5 | human | **H1** approves the design and any ADR. Nothing is implemented before this | design, ADR → decision | — |
| 6 | orchestrator | Record approved ADR in `memory/decisions.md`. Split work into subtasks, ordered by dependency (§5) | design → subtask `task.md` set (`parent_task`) | — |
| 7 | executors | Run `feature-development` per subtask, starting with the scaffold. One PR per subtask (stacked) | subtask → draft PRs | per `feature-development` |
| 8 | orchestrator | Integration check: module matches `design.md`; DoD by type; runbook and observability present | PRs, design → conformance report | — |
| 9 | reviewer | Final architecture conformance pass over the integrated result (skipped if `human-only`) | PRs, design → verdict | — |
| 10 | human | **H2** merges PRs in order | draft PRs → merge | — |
| 11 | orchestrator | Update memory, set `DONE` | merge → memory | — |

## 5. Subtask Order (step 6)

Default order, adjusted by the design:
1. Scaffold: structure, configuration injection, empty test harness, CI hooks (`TBD`).
2. Contracts and interfaces (data contracts, OpenAPI/AsyncAPI).
3. Core logic with unit tests.
4. Integration tests and data-quality or evaluation checks.
5. Observability, container and deployment *definitions* (`devops-sre`; humans apply).
6. Documentation and runbook.

Each PR MUST build and pass tests on its own and be revertable as a unit.

## 6. Human Checkpoints

| ID | When | Human decides |
|----|------|---------------|
| H1 | After design and ADR | Approve, request changes (step 2, does not count as `REWORK`) or reject |
| H2 | Each PR | Merge, request changes or reject |

## 7. Exit Criteria

- Approved design; module conforms to it.
- Definition of Done: `lattinus-code.md` §6.1 plus §6.2 rows for each deliverable type (Code, API, Data pipeline, Geospatial, AI, Infrastructure).
- Runbook (run, monitor, retry, backfill, roll back) documented (`lattinus-code.md` §11).
- Every subtask has `PASS` or human sign-off.

## 8. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Design rejected at H1 | Close with reason in `project-state.md`, or return to step 2 with feedback |
| Implementation diverges from design | Stop; change the design through H1 again, then continue |
| Subtask `REWORK` | Per `code-review`; maximum 2 cycles per subtask `task_id`, then `ESCALATE` |
| Design needs a manifest-excluded skill or reference | Escalate |

## 9. Memory Updates

| File | Writer | When |
|------|--------|------|
| `memory/decisions.md` | orchestrator | After H1 approves an ADR |
| `memory/conventions.md` | orchestrator | Only if the design sets a convention and a human approves it |
| `memory/project-state.md` | orchestrator | Step 11 |
| `memory/lessons.md` | reviewer | Standard review with a lesson |
| `memory/open-questions.md` | any | Gaps, unresolved design questions |

## 10. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/design.md`, `adr.md`, `task.md`, `review.md` | Not yet created |
| Module layout and naming in Lattinus Code | `TBD` (repository) |
| CI hooks, coverage and complexity thresholds, PR size threshold | `TBD` (`lattinus-code.md` §14) |