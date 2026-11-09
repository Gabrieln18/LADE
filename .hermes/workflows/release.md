# release.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-09 · **Location:** `workflows/release.md`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119. Only humans edit this file.
> **Default `review_level`:** `standard`. **Recommended `standard`.**
> Agents **prepare** a release. Tagging, publishing and deploying are human-only (`permissions.md` §6).

## 1. When to Use

Use to close a version of Lattinus Code or one of its deployable units.

Do not use for:
- hotfix scope that skips normal flow (hotfix path is `TBD`);
- applying infrastructure or deploying. No agent does it.

## 2. Participants

| Agent | Role |
|-------|------|
| `orchestrator` | Scope, readiness check, draft release PR, memory |
| `software-engineer` | Version bump and lockfile consistency |
| `devops-sre` | SBOM, scan evidence, build/deploy definitions, rollback runbook |
| `reviewer` | Changelog, release notes, `code-review` |
| human | Confirms version (H1); merges, tags, publishes, deploys (H2) |

## 3. Preconditions

Definition of Ready (`lattinus-code.md` §5), plus:
- target repository, base branch and last release tag known (`TBD` until confirmed);
- changes to release identified (merged PRs since the last tag);
- every included task is `DONE` with a recorded verdict or human sign-off.

## 4. Steps

| # | Agent | Action | Input → Output | Gate |
|---|-------|--------|----------------|------|
| 1 | orchestrator | Validate `task.md`; set `READY` | `task.md` → `READY` | — |
| 2 | orchestrator | Collect scope: merged PRs, `task_id`s, commit types, ADRs. List open `BLOCKED` or `ESCALATED` tasks | repository history → release scope list | — |
| 3 | orchestrator | Propose version by SemVer: breaking change → major, `feat` → minor, `fix` and others → patch | scope → proposed version | — |
| 4 | human | **H1** confirms or changes the version and the scope | proposal → decision | — |
| 5 | software-engineer | Bump version in the files declared in `task.md`; keep the lockfile consistent | decision → version commit | `git`; `dependencies` if the lockfile changes |
| 6 | reviewer | Write changelog (Keep a Changelog) and release notes (default PT-BR). Cover breaking changes with migration notes | scope → changelog, release notes | `documentation` |
| 7 | devops-sre | Produce SBOM (SPDX or CycloneDX), attach scan evidence, update build/deploy definitions and rollback runbook. Definitions only | repository → SBOM, definitions | `safety` |
| 8 | orchestrator | Readiness checklist (§5). Any failed item sets `BLOCKED` | artifacts → checklist | — |
| 9 | reviewer | `CALL code-review` on the release PR (skipped if `human-only`). Excludes the changelog and notes the Reviewer wrote, which the human verifies at H2 | release PR → verdict | — |
| 10 | orchestrator | Push branch, open **draft** release PR with notes and checklist | package → draft PR | `git` |
| 11 | human | **H2** merges, tags, publishes and deploys, outside LADE | draft PR → release | — |
| 12 | orchestrator | After the human confirms the tag, update memory, set `DONE` | confirmation → memory | — |

## 5. Readiness Checklist (step 8)

- [ ] All included tasks `DONE`; no included task is `BLOCKED` or `ESCALATED`.
- [ ] Definition of Done met for the included changes (`lattinus-code.md` §6).
- [ ] Version matches SemVer impact; breaking changes have an ADR and migration notes.
- [ ] Changelog and release notes complete.
- [ ] CI green on the release branch (`TBD`).
- [ ] No high or critical vulnerability unless a human accepted the risk in writing (`lattinus-code.md` §10.3).
- [ ] SBOM generated for each deployable unit.
- [ ] Rollback path documented.
- [ ] No secrets, credentials or absolute local paths.
- [ ] Provenance per target SLSA level (`TBD`).

## 6. Human Checkpoints

| ID | When | Human decides |
|----|------|---------------|
| H1 | After the version proposal | Confirm version and scope, exclude changes, or postpone |
| H2 | After the draft release PR | Merge, tag, publish, deploy, or request changes. Verifies the changelog and release notes written by the Reviewer |

## 7. Exit Criteria

- Readiness checklist fully passed.
- Verdict `PASS` or human sign-off on the release PR.
- Release PR opened as draft.
- Release, tag and deploy performed by a human.

## 8. Failures and Escalation

| Situation | Action |
|-----------|--------|
| Included task not `DONE` | `BLOCKED`; human decides: wait or exclude from the release |
| Vulnerability scan fails | `BLOCKED`; human accepts risk in writing or fixes via `bug-investigation` |
| CI red | `BLOCKED`; investigate via `bug-investigation` |
| Verdict `REWORK` | Back to the named agent. Maximum 2 cycles, then `ESCALATE` |
| Post-release defect | Open `bug-investigation`; the Reviewer records a lesson |

## 9. Memory Updates

| File | Writer | When |
|------|--------|------|
| `memory/project-state.md` | orchestrator | Step 12: released version and scope |
| `memory/lessons.md` | reviewer | Standard review with a lesson |
| `memory/open-questions.md` | any | Deferred items, follow-ups |

## 10. Dependencies and `TBD`

| Item | Status |
|------|--------|
| `templates/task.md`, `review.md` | Not yet created |
| `references/lattinus-code.md` §14: repository, CI, signing, SLSA level | `TBD` |
| Hotfix path and expedited review | `TBD` |
| Release publishing target (registry, environment) | `TBD` (humans) |
| Reviewer authoring the changelog, verified by a human instead of reviewed | To be confirmed (same open point as `feature-development` §7) |