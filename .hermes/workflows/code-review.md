# code-review.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/code-review.md`
> Reusable review workflow. Called by other workflows or run standalone. Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Only humans edit this file (`AGENTS.md` §11).
> **Default `review_level`:** n/a (this workflow *is* the Reviewer pass). **Recommended:** n/a.

## 1. When to Use

Use when:
- another workflow reaches its review step (`review_level: standard`);
- a human asks for a review of an existing PR or artifact, including work done outside LADE.

Do not use when:
- `review_level` is `human-only` (Reviewer pass is skipped, `AGENTS.md` §8.1);
- the request is to *fix* the artifact. The Reviewer MUST NOT modify it (`permissions.md` §5).

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Intake, applies the verdict (routes `REWORK`, counts cycles, escalates) |
| `reviewer` | Executes the review, issues the verdict, writes review report and `lessons.md` |
| author agent | Receives `REWORK`, corrects its own artifact |
| human | Decides on `ESCALATE` |

## 3. Preconditions

- A `task_id` for the artifact under review (standalone: Orchestrator opens a review `task.md`; the artifact is listed in `inputs`).
- Artifact with traceability header (`AGENTS.md` §10). External PRs have none: the Reviewer records this as a finding, not a blocker.
- Policy gate results recorded in the header.
- `acceptance_criteria` available in the originating `task.md`.

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate request, set status `IN_REVIEW` | `task.md`, artifact → review request | — |
| 2 | reviewer | Check recorded gate results are present and consistent with the diff (does not re-execute actions) | header, diff → gate findings | — |
| 3 | reviewer | Check each acceptance criterion against evidence | `task.md`, evidence → criteria table | — |
| 4 | reviewer | Check Definition of Done: `lattinus-code.md` §6.1, §6.2 for the deliverable type, §8 (geospatial) and §9 (AI) when applicable | artifact → DoD checklist | — |
| 5 | reviewer | Check scope (no out-of-scope change), traceability, cited references, declared assumptions, secrets by inspection | artifact → findings | — |
| 6 | reviewer | Classify findings and issue verdict | findings → `templates/review.md` | — |
| 7 | orchestrator | Apply verdict (§6) | review → next state | — |
| 8 | reviewer | If a reusable lesson exists, append to `memory/lessons.md` with `task_id` | review → `lessons.md` entry | — |

## 5. Finding Severity and Verdict

| Severity | Definition | Effect |
|----------|------------|--------|
| `blocking` | Violates acceptance criteria, DoD, a policy, or is incorrect/unsafe | Prevents `PASS` |
| `non-blocking` | Improvement that does not violate the above | Recorded as suggestion; does not prevent `PASS` |

Verdict (closed set, `AGENTS.md` §8.2):

| Verdict | Condition |
|---------|-----------|
| `PASS` | No blocking findings and DoD met |
| `REWORK(agent, reason)` | At least one blocking finding, fixable by a named agent, and fewer than 2 prior `REWORK` cycles for this `task_id`. Reason MUST be verifiable and cite the finding |
| `ESCALATE` | A third `REWORK` would be needed; or the finding needs a human decision (architecture, policy conflict, ambiguous criteria); or the Reviewer cannot verify a claim |

Standalone review of an external PR: `REWORK` is recorded as `REWORK(external, reason)`. The Orchestrator does not dispatch it; the human relays the findings. *(Assumption, to be confirmed.)*

## 6. Applying the Verdict

| Verdict | Orchestrator action | Task status |
|---------|---------------------|-------------|
| `PASS` | Return control to the calling workflow | `IN_REVIEW` → caller's next state |
| `REWORK` | New `task.md` to the named agent with the review as input; increment cycle counter | `REWORK` |
| `ESCALATE` | Send escalation message (`AGENTS.md` §13) | `ESCALATED` |

After a `REWORK`, the author corrects and the workflow restarts at step 1. Cycle counter is per `task_id` and persists across restarts.

## 7. Human Checkpoints

| ID | Moment | Human decides |
|----|--------|---------------|
| H1 | After `ESCALATE` | Resolve the blocker, change scope or criteria, or close the task |

Merge approval belongs to the calling workflow, not to this one.

## 8. Exit Criteria

- Review recorded with `templates/review.md`.
- Every finding has severity and, if blocking, a named responsible agent.
- Verdict applied by the Orchestrator.
- The Reviewer did not modify the artifact.

## 9. Failures

| Situation | Action |
|-----------|--------|
| Artifact lacks `acceptance_criteria` | `BLOCKED`; Orchestrator asks requester |
| Evidence is missing or unverifiable | Blocking finding, or `ESCALATE` if it cannot be verified at all |
| Gate result missing | Blocking finding; the author reruns the gate |
| Conflict between `memory/` and `references/` | `references/` prevail; log in `memory/open-questions.md` |

## 10. Memory Updates

| File | Writer | Condition |
|------|--------|-----------|
| `memory/lessons.md` | reviewer | `standard` review and a lesson exists |
| `memory/open-questions.md` | any | Gaps found (missing reference, unclear criteria) |
| `evals/reports/` | reviewer | Only when the review is part of an eval run |

## 11. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/review.md`, `templates/task.md` | Not yet created |
| Reviewer manifest: skills and references used for each deliverable type | `TBD` (agent manifests) |
| Handling of external PRs (`REWORK(external, …)`) | To be confirmed |