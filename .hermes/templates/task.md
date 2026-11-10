<!--
TEMPLATE: task.md · v0.1.0 (bootstrap) · Location: templates/task.md
Purpose:   Handoff contract. Mandatory for any delegation (AGENTS.md §6).
Filled by: orchestrator (or the human requester, then validated by the orchestrator).
Used when: intake of a user task, and every delegation between agents.
Consumed by: assigned agent(s). Sub-agents start with ZERO context: this file must be self-sufficient.
Instantiate: copy, fill every field, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
status: DRAFT            # DRAFT | READY | IN_PROGRESS | BLOCKED | IN_REVIEW | REWORK | ESCALATED | DONE
objective: <one sentence, outcome-oriented>
requester: <human or agent>
assigned_to: [<agent>]
review_level: standard   # human-only | standard (default: standard)
output_language: PT-BR   # default PT-BR
parent_task: none        # task_id of parent, or none
workflow: <workflows/<name>.md | auto>
---

# Task: <short title>

## 1. Context
<!-- Why this task exists. 2-5 lines. Link, do not copy, domain knowledge. -->

## 2. Inputs
<!-- Files, references, prior artifacts. Use paths. -->
- <path or link>

## 3. Expected outputs
<!-- Artifact type + location. Locations are declared here until the runtime is defined. -->
| Artifact | Type | Location |
|----------|------|----------|
| <name> | <design / adr / code / tests / pipeline / doc / ...> | <path> |

## 4. Acceptance criteria
<!-- Each criterion MUST be verifiable. A task without them MUST NOT leave DRAFT. -->
- [ ] AC1: <verifiable condition>
- [ ] AC2: <verifiable condition>

## 5. Constraints
<!-- Technical, policy or scope limits. -->
- <constraint>

## 6. Out of scope
<!-- Explicit exclusions. Findings outside scope are reported, not acted on. -->
- <exclusion>

## 7. Delegation block
<!-- Required when delegating to a sub-agent or another profile. Remove if the orchestrator executes nothing. -->
- **Target role:** <agent>
- **Role files to read first:** `agents/<agent>/SOUL.md`, `agents/<agent>/AGENTS.md`
- **References needed (by path):** <references/...>
- **Skills likely needed:** <skills/...> (load on demand, only if in the manifest)
- **Hard limits (restated):**
  - No merge, approve, mark PR ready, force-push or delete remote branches.
  - No secrets or credentials. No deploy or production access.
  - No dependency change without the dependencies gate and human approval.
  - No writes outside the manifest `can_write` and the paths in §3.
  - No self-approval. Do not fabricate APIs, paths, versions or results.
  - Maximum 2 REWORK cycles, then ESCALATE.

## 8. Definition of Ready
<!-- Reference: references/lattinus-code.md §5. The task MAY enter IN_PROGRESS only if all are checked. -->
- [ ] Acceptance criteria are verifiable
- [ ] Inputs and expected outputs declared
- [ ] Review level and output language set
- [ ] Out-of-scope list present
- [ ] Required references available (or gap logged in `memory/open-questions.md`)

## 9. Gate results
<!-- Filled by the acting agent. pass | na | fail -->
| Gate | Result | Note |
|------|--------|------|
| safety | | |
| dependencies | | |
| git | | |
| documentation | | |

## 10. Status log
<!-- Append-only. -->
| Date | Status | By | Note |
|------|--------|----|------|
| YYYY-MM-DD | DRAFT | <agent> | created |