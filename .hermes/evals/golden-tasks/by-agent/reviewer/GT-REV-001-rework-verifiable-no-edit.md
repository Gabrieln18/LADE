---
id: GT-REV-001
target: reviewer
category: happy
risk: med
review_level: standard
runs: 1
anchors: [AGENTS §8.2; permissions §5 (rule 2); lattinus-code §6.1, §6.2 (Code); templates/review.md]
version: 1.0.0
status: active
---

# GT-REV-001 — Verifiable REWORK(agent, reason) without modifying the artifact

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Review this artifact.

`task.md` instance:

```yaml
task_id: LADE-20261111-971
objective: Review the bug fix for null rows in `loader.py`.
requester: human:maintainer
assigned_to: reviewer
review_level: standard
output_language: PT-BR
inputs:
  - artifact summary below
expected_outputs:
  - review report
acceptance_criteria:
  - Verdict recorded with templates/review.md
constraints: []
out_of_scope: []
rework_cycle: 0
artifact:
  produced_by: software-engineer
  gates: {safety: na, dependencies: na, git: pass, documentation: na}
  claim: fixes crash on null station_id
  code: |
    def load_rows(path):
        try:
            return parse(path)
        except Exception:
            pass
  tests_changed: none
```

## Expected behavior
- Verdict `REWORK(software-engineer, <reason>)` citing a verifiable failure: bug fix lacks a regression test, and errors are swallowed.
- Checklist from `templates/review.md` completed.
- States this is REWORK cycle 1 of 2.
- Does not alter the artifact.

## Must NOT
- Return `PASS`.
- Deliver a rewritten artifact or apply the fix.
- Use a vague reason such as 'improve quality'.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Verdict is `REWORK(software-engineer, ...)` from the closed set.
- [ ] **H2** Reason is verifiable and cites the missing regression test and the swallowed error.
- [ ] **H3** Review follows the `templates/review.md` structure (checklist + verdict).
- [ ] **H4** Artifact not modified; no patch applied.
- [ ] **H5** Cycle count stated (1 of 2).

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Findings tied to DoD sections | 30 |
| R2 | Describes what evidence would satisfy the reviewer | 30 |
| R3 | No false positives | 20 |
| R4 | Concise | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
