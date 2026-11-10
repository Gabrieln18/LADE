<!--
TEMPLATE: adr.md · v0.1.0 (bootstrap) · Location: templates/adr.md
Purpose:   Architecture Decision Record, MADR-style. Single location for the ADR template.
Filled by: architect (proposal). Agents MUST NOT approve their own ADR.
Used when: architecture/design decision, dependency choice, data contract standard, breaking change.
Consumed by: human approver, then orchestrator (copies approved ADR to memory/decisions.md).
Rules: only `accepted` ADRs go to memory/decisions.md. ADR ids are sequential: ADR-NNNN.
Instantiate: copy, fill, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
produced_by: architect
review_level: standard   # human-only | standard
references: []
adr: ADR-NNNN
gates: {safety: na, dependencies: na, git: na, documentation: na}
status: IN_REVIEW
assumptions: []
adr_status: proposed     # proposed | accepted | rejected | superseded
supersedes: none         # ADR-NNNN or none
superseded_by: none
---

# ADR-NNNN: <decision title, imperative>

## 1. Context
<!-- Problem and forces at play. Cite references/ files. 3-8 lines. -->

## 2. Decision drivers
- <driver: e.g. scale, cost, maintainability, compliance>

## 3. Options considered
<!-- At least two, including "do nothing" when relevant. -->

### Option A: <name>
- Pros: <...>
- Cons: <...>

### Option B: <name>
- Pros: <...>
- Cons: <...>

## 4. Decision
**Chosen:** <option>.
**Why:** <reasoning tied to drivers>.

## 5. Consequences
- Positive: <...>
- Negative / trade-offs: <...>
- Risks and mitigations: <...>
- Reversibility: <easy | costly | irreversible> and how to revert.

## 6. Dependency impact
<!-- Dependencies gate applies. Write "none" if no change. -->
| Package | Purpose | License | Maintenance | Alternatives |
|---------|---------|---------|-------------|--------------|
| | | | | |

## 7. Affected components
<!-- Modules, data contracts, interfaces, workflows, references/ files to update. -->
- <item>

## 8. Follow-ups
- <action, owner>

## 9. Human approval
<!-- Filled by a human only. Without this block the ADR stays `proposed`. -->
- Approver: <name>
- Date: YYYY-MM-DD
- Decision: accepted / rejected
- Conditions: <none | text>