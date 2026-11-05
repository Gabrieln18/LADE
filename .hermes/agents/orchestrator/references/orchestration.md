# orchestration.md

## 1. Lifecycle
Intake → Validate → Route → Delegate → Monitor → Gate check → Review → Close

## 2. State transitions (owner: orchestrator)
| From | To | Condition |
|------|----|-----------|
| DRAFT | READY | Definition of Ready met (lattinus-code §5) |
| READY | IN_PROGRESS | Agent(s) assigned via task.md |
| IN_PROGRESS | IN_REVIEW | Artifact has traceability header + gates recorded |
| IN_PROGRESS | BLOCKED | Gate failed or permission missing |
| IN_REVIEW | DONE | PASS (or human sign-off) + draft PR + memory updated |
| IN_REVIEW | REWORK | Verdict REWORK(agent, reason), cycle ≤ 2 |
| REWORK | IN_PROGRESS | Re-delegated to named agent |
| any | ESCALATED | Escalation trigger (AGENTS §13) |

## 3. Intake checklist
1. Objective in one sentence, outcome-oriented.
2. Verifiable acceptance_criteria (else ask requester, grouped).
3. inputs, expected_outputs, out_of_scope, constraints.
4. review_level: recommend `standard` if touching architecture,
   data contracts, security or public APIs; human decides.
5. Required references exist; else log gap in open-questions.md.

## 4. Delegation rules
- Always via templates/task.md. task_id: LADE-YYYYMMDD-NNN.
- One accountable agent per task; subtasks use parent_task.
- Sequence when output of A is input of B (e.g. ADR → implementation).
- Parallel only if inputs and write scopes are disjoint.
- Architectural decision → ADR approved by human BEFORE implementation.

## 5. Rework control
- Count cycles per task_id. Third failure → ESCALATE.
- REWORK goes back to the agent named by the Reviewer, never to a different one.

## 6. Closure
1. Verify Definition of Done (lattinus-code §6) against evidence.
2. Assemble package + PR description (lattinus-code §12.1).
3. Gate: git → push branch, open DRAFT PR. Never mark ready or merge.
4. Update memory per AGENTS §9. Status DONE only after human merge.
5. Post-merge defect reported → forward to Reviewer for lessons.md.

## 7. Escalation
Use the message format in AGENTS §13. Include state, blocker, options, recommendation.