# feature-development.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/feature-development.md`
> Base workflow for new capability or behavior change. Reused as a subworkflow by `bug-investigation`, `new-module` and `architecture-change`.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Recommended `standard`** when the change touches architecture, data contracts, security or public APIs (`AGENTS.md` §8.1).

## 1. When to Use

Use when a task adds or changes behavior inside an existing architecture.

Do not use when:
- the change alters structure, contracts, boundaries or dependencies → `architecture-change`;
- the task creates a new module, pipeline or component → `new-module`;
- the task fixes a defect → `bug-investigation`;
- the task only reviews → `code-review`.

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Intake, routing, package assembly, draft PR, memory |
| executor | Chosen by `routing.md`: `software-engineer`, `data-engineer`, `geospatial-engineer`, `ai-engineer` or `devops-sre` |
| `reviewer` | Review (`code-review`) and documentation step |
| human | Approves plan when required (H1) and merge (H2) |

## 3. Preconditions

Definition of Ready (`lattinus-code.md` §5), plus:
- the behavior change is described in terms of observable outcomes;
- consumers or affected interfaces are listed in `inputs`;
- required references exist, or the gap is in `memory/open-questions.md`.

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate `task.md`; confirm DoR; set `READY`; recommend `review_level` | `task.md` → `READY` | — |
| 2 | orchestrator | Route to executor. Check architecture triggers (§5); if any fires, stop and open `architecture-change` | `routing.md` → `assigned_to` | — |
| 3 | executor | Write plan: files touched, tests, risks, proposed dependencies, assumptions | `task.md`, references → `templates/implementation-plan.md` | — |
| 4 | human | **H1** when required (§6). Otherwise orchestrator proceeds and reports | plan → approval | — |
| 5 | executor | Implement on task branch with tests. Atomic commits (Conventional Commits, `Task:` footer) | approved plan → code, tests | `dependencies` before any package change; `git` before each commit |
| 6 | executor | Update docs that live with the code (docstrings, module docs, OpenAPI, runbook) | code → updated docs | `documentation` if impact |
| 7 | executor | Run formatter, linter, type check and tests locally. Attach output | code → evidence | `safety` if any action is external or destructive |
| 8 | orchestrator | Assemble delivery package and verify `lattinus-code.md` §6 and §12 | artifacts → package | — |
| 9 | reviewer | `CALL code-review` (skipped if `human-only`) | package → verdict | — |
| 10 | reviewer | If standard and PASS: write repo-level documentation and changelog entry when required (§7) | package → docs, changelog | `documentation` |
| 11 | orchestrator | Push branch and open **draft** PR with the description template | package → draft PR | `git` |
| 12 | human | **H2** reviews and merges | draft PR → merge | — |
| 13 | orchestrator | Update memory, set `DONE` | merge → memory | — |

## 5. Architecture Triggers (step 2)

Stop and open `architecture-change` if the task:
- adds, removes or upgrades a dependency with design impact;
- changes a public API, data contract or module boundary;
- introduces a new technology or pattern;
- alters security, deployment or data-retention behavior.

A routine dependency patch with no design impact stays here, behind the `dependencies` gate and human approval.

## 6. Human Checkpoints

| ID | When | Human decides |
|----|------|---------------|
| H1 | Required if the plan: adds/changes a dependency, touches a public interface or data contract, expands scope, or includes an irreversible step. Also whenever `task.md` requests it | Approve, change or reject the plan |
| H2 | Always | Merge, request changes (opens `REWORK` within the limit) or reject |

## 7. Documentation Ownership (open point)

`permissions.md` §5 gives `documentation/*` artifacts to the Reviewer, and the Reviewer MUST NOT review what it wrote. Therefore:
- docs co-located with code are written by the executor and reviewed normally (step 6);
- repo-level docs and changelog are written by the Reviewer after `PASS` (step 10) and verified by the human at H2;
- in `human-only`, the human writes them or opens a documentation task for the Reviewer.

*To be confirmed by maintainers (see §11).*

## 8. Exit Criteria

- Definition of Done: `lattinus-code.md` §6.1 and the §6.2 row for the deliverable type.
- Verdict `PASS` (standard) or human sign-off (human-only).
- Draft PR opened with traceability, evidence, assumptions and rollback.
- Merge decided by a human.

## 9. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Gate fails | Status `BLOCKED`; fix within scope or escalate |
| Verdict `REWORK` | Back to step 5 for the named agent. Maximum 2 cycles, then `ESCALATE` |
| Plan cannot meet criteria | Stop at step 3 and escalate with options |
| Scope grows during execution | Stop; report; wait for approval (SOUL §5) |
| Missing skill, reference or path in manifest | Escalate or request manifest change |

Escalation uses the format in `AGENTS.md` §13.

## 10. Memory Updates

| File | Writer | When |
|------|--------|------|
| `memory/project-state.md` | orchestrator | Step 13 |
| `memory/decisions.md` | orchestrator | Only if an ADR was approved in this task |
| `memory/conventions.md` | orchestrator | Only after human approval |
| `memory/lessons.md` | reviewer | Standard review with a lesson |
| `memory/open-questions.md` | any | Gaps, out-of-scope findings |

## 11. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/task.md`, `implementation-plan.md`, `review.md` | Not yet created |
| `agents/orchestrator/references/routing.md` | Not yet created |
| CI required checks, PR size threshold, branch and signing rules | `TBD` (`lattinus-code.md` §14) |
| Documentation ownership (§7) | To be confirmed |