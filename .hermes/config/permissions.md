# permissions.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-04 · **Location:** `config/permissions.md`
> Authoritative permission matrix for LADE (Hermes). Key words MUST, MUST NOT, MAY follow RFC 2119.
> Only humans edit this file (`AGENTS.md` §11).

## 1. Purpose and Precedence

Defines what each agent may read, write and execute, and which approval each action requires.

1. **Default deny.** Anything not granted here is forbidden.
2. **Deny wins** over any grant, from any layer.
3. This file MAY restrict `AGENTS.md` §3 and agent manifests. It MUST NOT exceed them.
   A manifest `can_write` MUST be a subset of §4 and §5.
4. `policies/` prevail over this file (`AGENTS.md` §2).
5. Permissions are per task: an agent acts only on paths and inputs declared in its `task.md`.

## 2. Legend

| Symbol | Meaning |
|--------|---------|
| `R` | Read |
| `W` | Create / modify |
| `A` | Append only (no edit or delete of existing entries) |
| `—` | No access |

Approval levels: **None** · **Gate** (policy gate, `AGENTS.md` §7) · **Human** (explicit approval before the action).

## 3. Governance Paths (human-only write)

`SOUL.md`, `AGENTS.md`, `README.md`, `config/`, `policies/`, `references/`,
`templates/`, `workflows/`, `skills/`, `agents/*` and `evals/golden-tasks/`
are **read-only for all agents**. Agents propose changes as text in the artifact
or in `memory/open-questions.md`.

Read scope:
- All agents: `R` on `SOUL.md`, `AGENTS.md`, `config/`, `policies/`, `templates/`, `workflows/`.
- `skills/`, `references/`: `R` only if listed in the agent's manifest (`AGENTS.md` §4).
- `agents/<agent>/`: `R` on its own folder. The Orchestrator has `R` on all (routing).
- `evals/golden-tasks/`: `R` for Orchestrator and Reviewer only (prevents tuning to the test).

## 4. Memory, Tasks and Evals

| Path | orch | arch | swe | data | geo | ai | devops | reviewer |
|------|:----:|:----:|:---:|:----:|:---:|:--:|:------:|:--------:|
| `task.md` instances | W | R* | R* | R* | R* | R* | R* | R* |
| `memory/project-state.md` | W | R | R | R | R | R | R | R |
| `memory/decisions.md` (approved ADR only) | W | R | R | R | R | R | R | R |
| `memory/conventions.md` (human-approved only) | W | R | R | R | R | R | R | R |
| `memory/lessons.md` | R | R | R | R | R | R | R | A |
| `memory/open-questions.md` | A | A | A | A | A | A | A | A |
| `evals/reports/` | R | — | — | — | — | — | — | A |

\* Only the task(s) assigned to the agent.
Every `open-questions.md` entry MUST carry `task_id` and owner.
`lessons.md` is written only in `standard` review.

## 5. Artifact Write Scope

Each agent writes only artifacts of its own class, at locations declared in `task.md`.

| Artifact class | Writer | Others |
|----------------|--------|--------|
| Design, ADR proposals, dependency analysis | architect | R |
| Code, tests, APIs, refactoring | software-engineer | R |
| Ingestion, pipelines, data contracts, data quality | data-engineer | R |
| Raster/vector, CRS, EO, Dask/Xarray, Sedona | geospatial-engineer | R |
| Agents, LLM integration, evaluators | ai-engineer | R |
| Containers, observability, deployment, security definitions | devops-sre | R |
| Documentation artifacts, review reports | reviewer | R |

Rules:
1. **Cross-class work is delegated, not performed.** An agent needing an artifact
   outside its class requests it from the Orchestrator via `task.md`.
2. **Separation of duties.** The Reviewer MUST NOT modify the artifact under review.
   Corrections return through `REWORK(agent, reason)`.
3. An agent MUST NOT approve its own artifact or its own ADR.
4. Deleting or overwriting files outside the agent's own task artifacts requires Safety gate + Human.

## 6. Execution Permissions

| Action | Allowed to | Approval |
|--------|------------|----------|
| Read files declared in `task.md` inputs | All | None |
| Run formatter, linter, type check, tests (local, no network) | swe, data, geo, ai, devops, reviewer | None |
| Run data or geospatial jobs on declared sample data | data, geo | None |
| Add, remove or upgrade a dependency | Proposing agent, after approval | Gate (`dependencies`) + Human |
| Network access | Only hosts allowlisted in `config/tools.md` | Gate (`safety`) |
| Use tools / MCPs | Only those listed in `config/tools.md` for that agent | None |
| Local commit on task branch | Authoring agents | Gate (`git`) |
| Push task branch, open **draft** PR | orchestrator | Gate (`git`) |
| Mark PR ready, approve, merge | **Nobody (human only)** | Human |
| Force-push, rewrite shared history, delete remote branches | **Nobody** | Deny |
| Read, create or use secrets / credentials | **Nobody** | Deny |
| Apply infrastructure, deploy, touch production | **Nobody** (devops produces definitions; humans apply) | Deny |
| Any irreversible or external-facing action | Proposing agent | Gate (`safety`) + Human |

## 7. Violations and Changes

1. An action outside this matrix MUST NOT be executed. The agent stops, sets the task
   `BLOCKED` and escalates (`AGENTS.md` §13).
2. Permission changes are made by humans only, and bump `Version`, `Date` and the changelog.
3. Widening an agent's permissions requires an ADR when it removes a separation of duties
   (e.g. letting an author also review).
4. A conflict between this file and a manifest is resolved in favor of the more restrictive
   one and logged in `memory/open-questions.md`.

## 8. Open Parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Concrete artifact paths per class (depends on repository layout) | Maintainers |
| Network allowlist | devops-sre / Maintainers |
| Sandbox / runtime enforcement mechanism | Maintainers |
| Audit log location and retention | devops-sre |