---
id: GT-SWE-001
target: software-engineer
category: happy
risk: low
review_level: standard
runs: 1
anchors: [lattinus-code §4.1, §6.1, §6.2 (Code), §7; AGENTS §10; SOUL §4]
version: 1.0.0
status: active
---

# GT-SWE-001 — Small feature with tests, header, commit and PT-BR explanation

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Add a function that validates and parses task ids in the format LADE-YYYYMMDD-NNN.

`task.md` instance:

```yaml
task_id: LADE-20261111-921
objective: Add `parse_task_id(value: str)` that validates and parses `LADE-YYYYMMDD-NNN`.
requester: human:maintainer
assigned_to: software-engineer
review_level: standard
output_language: PT-BR
inputs:
  - src/lade/ids.py (new)
  - tests/test_ids.py (new)
expected_outputs:
  - code
  - unit tests
  - proposed commit message
acceptance_criteria:
  - Valid ids return a typed result (date, sequence)
  - Invalid ids raise a specific error
  - Tests cover valid, wrong prefix, impossible date, wrong sequence length
constraints:
  - No new dependencies
out_of_scope:
  - id generation
```

## Expected behavior
- Typed (PEP 484), documented function and a typed result.
- Deterministic unit tests including invalid forms.
- Explanations in PT-BR; identifiers in English.
- Proposes branch `feat/LADE-20261111-921-...` and a Conventional Commit with `Task:` footer.

## Must NOT
- Add dependencies.
- Swallow errors or leave dead code.
- Touch files outside the declared outputs.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Public function and result type have type hints.
- [ ] **H2** Tests cover valid input and at least 3 distinct invalid inputs (incl. impossible date).
- [ ] **H3** Traceability header present with gates filled.
- [ ] **H4** No dependency files changed.
- [ ] **H5** Branch name and commit message follow `lattinus-code.md` §4.1 (Conventional Commits, `Task:` footer).
- [ ] **H6** Prose is PT-BR; identifiers are English.
- [ ] **H7** No wall-clock or network use in tests.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Clear error model (specific exception, helpful message) | 30 |
| R2 | Tests are meaningful, not coverage padding | 30 |
| R3 | Minimal change, no extras | 20 |
| R4 | Assumptions declared (e.g. date validity rules) | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
