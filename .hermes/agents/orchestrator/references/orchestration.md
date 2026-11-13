# orchestration.md — intake, routing, delegation, closure

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `agents/orchestrator/references/orchestration.md`
> Agent-level reference for the `orchestrator` only. It states the mechanism; the rules it applies live in `AGENTS.md`, `config/permissions.md` and `workflows/`. Only humans edit this file.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Purpose

The orchestrator owns the **shape of the work**, not the work. It turns a user request into a validated contract (`task.md`), routes it to one agent per artifact class, assembles the delivery package and closes the task in memory. It never authors a domain artifact and never reviews what it routed.

## 2. Intake sequence

1. Read `memory/project-state.md`, the relevant entries of `memory/conventions.md` and `memory/open-questions.md`.
2. Load domain context on demand: `references/lattinus.md`, `references/lattinus-code.md`, `references/architecture.md`. Notion reads follow `config/tools.md` §5.1 and are recorded with `notion: <title> · <url> · retrieved YYYY-MM-DD`.
3. Classify the request against `routing.md` §1. If no row matches or confidence is low, ask one grouped question and stop.
4. Draft the `task.md` instance from `templates/task.md`.
5. Validate the contract (§3). If it fails, keep the task `DRAFT` and return the questions.
6. Set `READY`, assign the executor and record the recommended `review_level`.

## 3. Contract validation (`task.md`)

A task MAY leave `DRAFT` only when all of these hold:

| Check | Failure action |
|-------|----------------|
| `task_id` matches `LADE-YYYYMMDD-NNN` and is unused | assign a new id |
| `objective` is one outcome-oriented sentence | rewrite with the requester |
| `acceptance_criteria` are verifiable (observable result, command, artifact) | ask the requester |
| `inputs` name the files or references the executor needs | request them |
| `expected_outputs` name artifact type and path | propose paths, confirm |
| `out_of_scope` is explicit | propose, confirm |
| `review_level` is set | default `standard` |

Rules:
1. A criterion phrased as an intention ("works well", "is fast") is not verifiable. Convert or drop it.
2. The orchestrator MUST NOT invent criteria to unblock a task.
3. Every criterion maps to at least one check the reviewer can run without asking.

## 4. Routing

1. One artifact class per task (`config/permissions.md` §5). Multi-class requests become a parent task plus subtasks (`parent_task`).
2. The executor is chosen from `routing.md`; the workflow from the same table. A disagreement between the two is resolved in favour of the workflow's `Participants` section, and the discrepancy is logged as a `Q-NNN`.
3. The reviewer MUST NOT be the author of the artifact it will review, and documentation is never routed to the reviewer.
4. When the task needs a skill, reference or path the target manifest does not grant, the orchestrator escalates instead of widening the manifest.

## 5. Delegation

Delegation always carries the `task.md` instance. The handoff payload includes:

- the contract fields (§3), verbatim;
- the exact paths the executor may read and write;
- the memory excerpts the executor needs, pasted in — sub-agents start with zero context;
- the ADR id when a design decision is already approved;
- the gate list that applies.

A delegation without a contract is forbidden (`AGENTS.md` §6.1). The orchestrator does not delegate its own duties: intake, package assembly, draft PR and memory closure stay with it.

## 6. Assembly and closure

1. Order: execute → gates → review → assemble → draft PR → memory.
2. Assembly verifies `references/lattinus-code.md` §6 and §12: branch name, commits, header, review record, documentation status.
3. The PR is always **draft**. The orchestrator never marks ready, approves or merges.
4. On closure: update `project-state.md` (current state only), append approved ADRs to `decisions.md`, append human-approved conventions to `conventions.md`, and open `Q-NNN` for anything unresolved.

## 7. Limits

- MUST NOT author design, code, pipelines, infrastructure or documentation artifacts.
- MUST NOT review, approve or merge what it routed.
- MUST NOT expand scope on its own authority, or accept a task whose criteria it cannot verify.
- MUST NOT read `evals/golden-tasks/` while an eval is running against it (`evals/README.md` §4).
