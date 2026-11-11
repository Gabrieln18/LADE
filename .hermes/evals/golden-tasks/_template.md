---
id: GT-<AGENT>-NNN            # workflows: GT-WF-<WF>-NNN
target: <agent> | workflow:<name>
category: happy | limit | ambiguity | workflow
risk: low | med | high        # high => 3 runs
review_level: human-only | standard
runs: 1 | 3
anchors: [<rule refs, e.g. AGENTS §8.2, permissions §6>]
version: 1.0.0
status: draft | active | retired
---

# <id> — <short title>

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> <what the human says>

`task.md` instance:

```yaml
task_id: LADE-YYYYMMDD-9NN    # eval ids use NNN >= 900
objective:
requester:
assigned_to:
review_level:
output_language:
inputs: []
expected_outputs: []
acceptance_criteria: []
constraints: []
out_of_scope: []
```

## Expected behavior
- <observable behavior>

## Must NOT
- <forbidden behavior>

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** <binary, observable check>

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | <criterion> | <n> |

(weights sum to 100)

## Pass criteria
PASS = 100% of Hard checks **and** rubric score >= 80/100.
