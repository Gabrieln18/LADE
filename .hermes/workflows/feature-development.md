# feature-development.md

> **Version:** 0.2.0 (draft) · **Date:** 2026-11-12 · **Location:** `workflows/feature-development.md`
> Base workflow for new capability or behavior change. Reused as a subworkflow by `bug-investigation`, `new-module` and `architecture-change`.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Recommended `standard`** when the change touches architecture, data contracts, security or public APIs (`AGENTS.md` §8.1).
> Changes vs 0.1.0: one canonical order (review before package assembly, matching `orchestration.md` §6); `technical-writer` owns repo-level docs; docs-only variant; documentation ownership is no longer open.

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
| `technical-writer` | Repo-level documentation and changelog (step 8) |
| `reviewer` | Review of code **and** documentation (`code-review`) |
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
| 6 | executor | Update docs that live with the code (docstrings, module docs, OpenAPI, runbook inputs) | code → updated docs | `documentation` if impact |
| 7 | executor | Run formatter, linter, type check and tests locally. Attach output | code → evidence | `safety` if any action is external or destructive |
| 8 | technical-writer | When required (§7): write repo-level docs (README, CONTRIBUTING, runbook) and the changelog entry, from the executor's artifacts. Skipped when not required | code, docs, evidence → docs, changelog | `documentation`; `git` for the local commit |
| 9 | reviewer | `CALL code-review` over code, tests **and** documentation (skipped if `human-only`) | artifacts → verdict | — |
| 10 | orchestrator | Assemble delivery package and verify `lattinus-code.md` §6 and §12, including the review record (or human sign-off) | artifacts, verdict → package | — |
| 11 | orchestrator | Push branch and open **draft** PR with the description template | package → draft PR | `git` |
| 12 | human | **H2** reviews and merges (in `human-only`, this is also the review) | draft PR → merge | — |
| 13 | orchestrator | Update memory, set `DONE` | merge → memory | — |

### 4.1 Docs-only variant

For tasks routed to `technical-writer` (`routing.md`): run steps 1–2; step 3 is a short outline inside the task (H1 not required unless the document changes status, owner or contract fields); the `technical-writer` takes the executor role for steps 5–7 (author, verify commands, record gates); step 8 is skipped; steps 9–13 as above. In `human-only`, the human reviews at step 12.

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

## 7. Documentation Ownership (resolved)

| Documentation | Author | Reviewed by |
|---------------|--------|-------------|
| Docstrings, module docs, OpenAPI/AsyncAPI, data contracts, runbook inputs | executor (step 6) | Reviewer (standard) / human (human-only) |
| README, CONTRIBUTING, runbook, changelog, guides, `documentation/*` | `technical-writer` (step 8) | Reviewer (standard) / human (human-only) |

Step 8 is **required** when the change alters user-visible behavior, public interfaces, configuration, operations, or when a new component needs a README or runbook (`policies/documentation.md` §3). Otherwise record `documentation impact: no` and skip.
The Reviewer never authors documentation, so the Reviewer can review all of it. In `human-only` the `technical-writer` still authors and the human reviews.

## 8. Exit Criteria

- Definition of Done: `lattinus-code.md` §6.1 and the §6.2 row for the deliverable type.
- Verdict `PASS` (standard) or human sign-off (human-only), recorded **before** the package is assembled.
- Draft PR opened with traceability, evidence, assumptions and rollback.
- Merge decided by a human.

## 9. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Gate fails | Status `BLOCKED`; fix within scope or escalate |
| Verdict `REWORK` | Back to the named agent (executor → step 5; documentation finding → `technical-writer`, step 8). Maximum 2 cycles, then `ESCALATE` |
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
| `templates/*`, `agents/orchestrator/references/routing.md` | Exist (stale "not yet created" notes removed) |
| CI required checks, PR size threshold, branch and signing rules | `TBD` (`lattinus-code.md` §14) |
| `CHANGELOG.md` and `docs/` location in Lattinus Code | `TBD` (`policies/documentation.md` §6) |
