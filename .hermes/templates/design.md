<!--
TEMPLATE: design.md · v0.1.0 (bootstrap) · Location: templates/design.md
Purpose:   Technical design for a change or new module.
Filled by: architect.
Used when: before implementing non-trivial changes (new module, interface change, pipeline, architecture change).
Consumed by: implementing agents, reviewer, human approver.
Sections marked (if applicable) may be removed when they do not apply. Keep it as short as the change allows.
Instantiate: copy, fill, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
produced_by: architect
review_level: standard   # human-only | standard
references: []
adr: none                # ADR-NNNN or none
gates: {safety: na, dependencies: na, git: na, documentation: na}
status: IN_PROGRESS
assumptions: []
---

# Design: <title>

## 1. Problem and context
<!-- What needs to change and why. Cite references/. -->

## 2. Goals and non-goals
- Goals: <...>
- Non-goals: <...>

## 3. Requirements and constraints
- Functional: <...>
- Non-functional (performance, scale, security, cost): <...>
- Constraints (policies, existing contracts): <...>

## 4. Proposed design
- **Overview:** <3-6 lines>
- **Components and responsibilities:** <...>
- **Interfaces and contracts:** <API / event / data contract, with spec link or sketch>
- **Data flow:** <source → processing → output>
- **Error handling and idempotency:** <...>

## 5. Data and geospatial considerations (if applicable)
<!-- Reference: references/lattinus-code.md §8. -->
- CRS (EPSG): <...>
- Formats (COG / GeoParquet / Zarr / STAC): <...>
- Temporal metadata (time zone, resolution): <...>
- Scale strategy (chunking / partitioning), memory and runtime assumptions: <...>
- Quality checks and uncertainty: <...>
- Provenance and licensing: <...>

## 6. AI components (if applicable)
<!-- Reference: references/lattinus-code.md §9. Prompts/models versioned, output schemas, evaluation plan, failure modes. -->

## 7. Alternatives considered
| Alternative | Why not |
|-------------|---------|
| | |

## 8. Dependency impact
<!-- Dependencies gate + human approval. Write "none" if no change. -->
- <package: purpose, license, alternatives>

## 9. Security and observability
- Security: <input validation, secrets, least privilege>
- Observability: <logs, metrics, traces, health signals>

## 10. Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | | | |

## 11. Rollout and rollback
- Rollout: <steps>
- Rollback: <how to revert as a unit>

## 12. Open questions
<!-- Also append to memory/open-questions.md with task_id and owner. -->
- <question, owner>

## 13. ADR required?
- [ ] Yes (architecture decision, dependency choice, breaking change): ADR-NNNN proposed
- [ ] No