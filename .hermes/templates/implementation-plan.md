<!--
TEMPLATE: implementation-plan.md · v0.1.0 (bootstrap) · Location: templates/implementation-plan.md
Purpose:   Step-by-step plan that maps acceptance criteria to steps and tests.
Filled by: architect or software-engineer (or the engineer of the relevant class).
Used when: before executing a task with more than one step, or whenever the task may split into several PRs.
Consumed by: executing agents, orchestrator (delegation), reviewer.
Instantiate: copy, fill, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
produced_by: <agent>
review_level: standard   # human-only | standard
references: []
adr: none
gates: {safety: na, dependencies: na, git: na, documentation: na}
status: IN_PROGRESS
assumptions: []
design: <path to design.md | none>
---

# Implementation plan: <title>

## 1. Scope
- In scope: <...>
- Out of scope: <...>

## 2. Traceability: criteria → steps → tests
<!-- Every acceptance criterion from task.md MUST map to at least one step and one verification. -->
| AC | Step(s) | Verification (test / check / evidence) |
|----|---------|----------------------------------------|
| AC1 | S1, S2 | <test name or command> |

## 3. Steps
<!-- Ordered. Each step: one responsible agent, one deliverable, reversible when possible. -->
| # | Step | Agent | Deliverable | Depends on | Gate |
|---|------|-------|-------------|------------|------|
| S1 | | | | none | |
| S2 | | | | S1 | |

## 4. PR split
<!-- Reference: references/lattinus-code.md §4. One PR per task, or a stacked series if above the size threshold (TBD). Each PR is revertible as a unit. -->
| PR | Content | Branch | Type (Conventional Commits) |
|----|---------|--------|------------------------------|
| 1 | | `<type>/<task_id>-<slug>` | feat / fix / refactor / ... |

## 5. Dependencies to propose
<!-- Dependencies gate + human approval before use. Write "none" if no change. -->
| Package | Purpose | License | Maintenance | Alternatives |
|---------|---------|---------|-------------|--------------|
| | | | | |

## 6. Test strategy
- Unit: <...>
- Integration: <...>
- End-to-end (few): <...>
- Data quality / evaluation (if applicable): <...>
- Determinism: <no network, fixed seeds, isolated clock>

## 7. Definition of Done by deliverable type
<!-- Reference: references/lattinus-code.md §6.2. List the types in this plan and point to the section; do not copy items. -->
- Types: <code | api | data-pipeline | geospatial | ai | infrastructure | documentation>
- Extra criteria specific to this task: <...>

## 8. Documentation and changelog
- Docs to update: <...>
- Changelog entry: <yes / no>

## 9. Rollback
<how to revert the delivery as a unit; data and interface considerations>

## 10. Risks and assumptions
| Risk / assumption | Impact | Mitigation / how to verify |
|-------------------|--------|----------------------------|
| | | |

## 11. Approval
<!-- The plan proceeds without human approval only if it is routine, in scope, reversible and has no ADR or dependency change (SOUL §5). -->
- [ ] Needs human approval (ADR, dependency, scope expansion, irreversible step)
- Approved by / date: <name, YYYY-MM-DD | n/a>