# bug-investigation.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/bug-investigation.md`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Recommended `standard`** for any fix touching a contract, data or security.
> Reuses `feature-development` (fix stage) and `code-review`.

## 1. When to Use

Use when a defect is reported: observed behavior differs from expected behavior.

Do not use when:
- the "bug" is really a missing capability → `feature-development`;
- the fix requires a structural or contract change → open `architecture-change` after step 5;
- the task is only a code review → `code-review`.

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Intake, routing, package, draft PR, memory |
| executor | Domain agent chosen by `routing.md`. Investigates and fixes |
| `reviewer` | `code-review`; lesson on root cause |
| human | Approves risky fixes (H1) and merge (H2) |

## 3. Preconditions

`task.md` MUST include:
- `scope`: `investigate-only` or `investigate-and-fix` (default `investigate-and-fix`);
- observed vs expected behavior;
- reproduction steps or evidence (logs, input sample, version, environment);
- severity (impact and affected data or users).

Without a reproduction or evidence the task stays `DRAFT` and the Orchestrator asks the requester (grouped, few questions).

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate bug report; set `READY`; route | `task.md` → `assigned_to` | — |
| 2 | executor | Reproduce: failing automated test, or documented manual repro. Read-only on production data | report → reproduction in `templates/research.md` | `safety` if data is real |
| 3 | executor | Root cause analysis. Label facts, assumptions and hypotheses. State blast radius and fix options | repro, code, logs → `research.md` (root cause) | — |
| 4 | orchestrator | If `investigate-only`: deliver `research.md`, go to step 12 | `research.md` → closure | — |
| 5 | orchestrator | Classify the fix (§5). If it needs H1, wait; if structural, open `architecture-change` | `research.md` → classification | — |
| 6 | executor | Write a regression test that fails for the reported reason | root cause → failing test | — |
| 7 | executor | Apply the minimal fix. No refactoring or unrelated cleanup | failing test → passing test | `dependencies`, `git` |
| 8 | executor | Run formatter, linter, type check and full affected tests. Attach evidence | code → evidence | — |
| 9 | orchestrator | Assemble package per `lattinus-code.md` §12 (commit type `fix`) | artifacts → package | — |
| 10 | reviewer | `CALL code-review` (skipped if `human-only`) | package → verdict | — |
| 11 | orchestrator | Push branch, open **draft** PR | package → draft PR | `git` |
| 12 | human | **H2** merge (or acceptance of `research.md` for investigate-only) | draft PR → decision | — |
| 13 | orchestrator | Update memory, set `DONE` | decision → memory | — |

## 5. Fix Classification (step 5)

| Class | Condition | Path |
|-------|-----------|------|
| Routine | Local change, no interface, data or dependency impact | Proceed and report |
| Needs H1 | Touches a public interface or data contract, changes persisted data, needs a backfill or reprocessing, affects security, or adds a dependency | Wait for human approval |
| Structural | Root cause is a design flaw that needs boundary, contract or technology change | Stop. Open `architecture-change`; this task keeps the investigation |

## 6. Human Checkpoints

| ID | When | Human decides |
|----|------|---------------|
| H1 | Fix class "Needs H1" | Approve fix, backfill plan or reclassify |
| H2 | Always | Merge, request changes or reject |

## 7. Exit Criteria

- Root cause documented with evidence, separated from assumptions.
- Regression test fails before the fix and passes after (code path).
- Definition of Done: `lattinus-code.md` §6.1 and §6.2 (Code, plus Data pipeline or Geospatial if applicable).
- Verdict `PASS` or human sign-off.
- Out-of-scope findings reported, not fixed.

## 8. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Cannot reproduce | `BLOCKED`; ask requester for more evidence. Do not "fix" blindly |
| Root cause uncertain | State hypotheses with confidence; escalate with options rather than guessing |
| Several plausible fixes | Present options with trade-offs; human chooses at H1 |
| Verdict `REWORK` | Back to step 7. Maximum 2 cycles, then `ESCALATE` |
| Fix would change behavior other consumers rely on | Needs H1 |

## 9. Memory Updates

| File | Writer | When |
|------|--------|------|
| `memory/project-state.md` | orchestrator | Step 13 |
| `memory/lessons.md` | reviewer | Root cause class and how to prevent it (standard review) |
| `memory/open-questions.md` | any | Out-of-scope findings, missing references, unreproduced symptoms |

## 10. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/research.md`, `task.md`, `review.md` | Not yet created |
| Severity scale and hotfix path (SLA, expedited review) | `TBD` (maintainers) |
| Bug intake source (issue tracker) | `TBD` |