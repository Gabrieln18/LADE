# architecture-change.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/architecture-change.md`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Strongly recommended `standard`.** If the human chooses `human-only`, the choice MUST be recorded in `task.md` (SOUL §2.5 keeps the decision with the human).
> Reuses `feature-development` (implementation) and `code-review`.

## 1. When to Use

Use when a decision changes structure, boundaries, public contracts, data contracts, technology or dependencies with design impact.

Do not use when:
- behavior changes inside the current architecture → `feature-development`;
- a new, self-contained module is created → `new-module` (it escalates here if it needs a cross-cutting decision).

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Intake, migration plan, subtasks, memory |
| `architect` | Analysis, options, design, ADR proposal |
| executors | Implement subtasks via `feature-development` |
| `reviewer` | Reviews design/ADR, implementation PRs and final conformance |
| human | Approves ADR (H1, mandatory) and merges (H2) |

## 3. Preconditions

Definition of Ready (`lattinus-code.md` §5), plus in `task.md`:
- problem statement and drivers (why change now);
- constraints and non-negotiables;
- known affected components and consumers.

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate `task.md`; confirm the change is architectural; set `READY` | `task.md` → `READY` | — |
| 2 | architect | Describe current state and impact: components, consumers, data, dependencies | code, references → `templates/research.md` | — |
| 3 | architect | Dependency analysis for any added, removed or upgraded package: purpose, license, maintenance, alternatives | research → analysis in `research.md` | `dependencies` |
| 4 | architect | Define at least 2 options, including "do nothing". Trade-offs, risks, reversibility, migration cost | research → `templates/design.md` | — |
| 5 | architect | Propose ADR (`Proposed`) with a recommended option | design → `templates/adr.md` | — |
| 6 | reviewer | `CALL code-review` on design and ADR (skipped if `human-only`) | design, ADR → verdict | — |
| 7 | human | **H1** decides on the ADR. No code before approval | ADR → `Approved` / `Changes requested` / `Rejected` | — |
| 8 | orchestrator | On approval: write ADR to `memory/decisions.md`; update `conventions.md` if the ADR sets a convention (human-approved) | ADR → memory | — |
| 9 | orchestrator | Write migration plan: incremental steps, each independently revertable (§5). Create subtasks with `parent_task` and `adr: ADR-NNNN` | ADR, design → `templates/implementation-plan.md`, subtask `task.md` set | — |
| 10 | executors | Run `feature-development` per subtask. Commits reference the ADR in the footer | subtask → draft PRs | per `feature-development` |
| 11 | reviewer | Final architecture conformance review of the integrated change (skipped if `human-only`) | PRs, ADR → verdict | — |
| 12 | human | **H2** merges PRs in plan order | draft PRs → merge | — |
| 13 | orchestrator | Update memory, set `DONE` | merge → memory | — |

## 5. Migration Rules

1. Each PR is a coherent, revertable unit (`lattinus-code.md` §4).
2. Contract changes follow expand → migrate → contract: add the new form, move consumers, then remove the old one after a stated deprecation window (window `TBD`).
3. Breaking changes use `!` or `BREAKING CHANGE:` in the commit plus the ADR reference, and require a SemVer major impact note.
4. The plan states the rollback path for every step.

## 6. Human Checkpoints

| ID | When | Human decides |
|----|------|---------------|
| H1 | After ADR proposal (mandatory) | `Approved`: continue. `Changes requested`: back to step 4 (does not count as `REWORK`). `Rejected`: close; record the reason in `project-state.md`. The ADR is **not** written to `decisions.md` |
| H2 | Each PR | Merge, request changes or reject |

## 7. Exit Criteria

- ADR approved by a human before any implementation.
- Alternatives, trade-offs and dependency impact recorded.
- Implementation conforms to the ADR; deviations go back through H1.
- Definition of Done: `lattinus-code.md` §6.1 and §6.2 (Architecture, plus types of the subtasks).
- Every subtask has `PASS` or human sign-off.

## 8. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Options cannot be compared for lack of information | `ESCALATE` with the missing facts; do not recommend on guesses |
| Implementation reveals the ADR is wrong | Stop; return to step 4; new H1 |
| Subtask `REWORK` | Per `code-review`; maximum 2 cycles per subtask `task_id`, then `ESCALATE` |
| Architect would review its own ADR | Forbidden; the Reviewer or human reviews (`permissions.md` §5.3) |

## 9. Memory Updates

| File | Writer | When |
|------|--------|------|
| `memory/decisions.md` | orchestrator | Step 8, approved ADR only |
| `memory/conventions.md` | orchestrator | Step 8, only with human approval |
| `memory/project-state.md` | orchestrator | Step 13 |
| `memory/lessons.md` | reviewer | Standard review with a lesson |
| `memory/open-questions.md` | any | Unresolved questions, deprecation follow-ups |

## 10. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/design.md`, `adr.md`, `research.md`, `implementation-plan.md` | Not yet created |
| ADR numbering (`ADR-NNNN`) and statuses | Defined by `templates/adr.md` |
| Deprecation window, SemVer policy details | `TBD` (maintainers) |