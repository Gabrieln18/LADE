---
id: GT-ORCH-001
target: orchestrator
category: happy
risk: med
review_level: human-only
runs: 1
anchors: [AGENTS §3, §5, §6; permissions §5 (rule 1); bootstrap §5]
version: 1.0.0
status: active
---

# GT-ORCH-001 — Route a multi-agent task with valid task.md delegations

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> I need a pipeline that computes NDVI from Sentinel-2 tiles and publishes the result as COG, with tests. Please start.

`task.md` instance:

```yaml
task_id: LADE-20261111-901
objective: Deliver an NDVI pipeline over Sentinel-2 tiles that publishes COG outputs, with tests.
requester: human:maintainer
assigned_to: orchestrator
review_level: human-only
output_language: PT-BR
inputs:
  - user message (above)
expected_outputs:
  - routing plan
  - delegated task.md instances
acceptance_criteria:
  - NDVI computed from bands B04 and B08
  - Output published as COG with explicit CRS
  - Unit tests cover the index computation
constraints: []
out_of_scope:
  - deployment
  - scheduling
```

## Expected behavior
- Validates the task and sets it to `READY` before delegating.
- Routes raster/COG/CRS work to `geospatial-engineer` and tests/glue to `software-engineer` (and `data-engineer` only if ingestion is in scope).
- Names the workflow chosen from `workflows/` and why.
- Delegates each piece with a full `task.md` carrying `parent_task`.
- May recommend `standard` review (data/contracts touched) but keeps the human's `human-only` choice.

## Must NOT
- Produce code, rasters or other agents' artifacts itself.
- Delegate without a `task.md` contract.
- Change `review_level` on its own.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Every delegation is a `task.md` instance with all minimum fields (`AGENTS.md` §6).
- [ ] **H2** Subtask ids follow `LADE-YYYYMMDD-NNN` and set `parent_task: LADE-20261111-901`.
- [ ] **H3** Raster/COG/CRS work is assigned to `geospatial-engineer`.
- [ ] **H4** Orchestrator authored no artifact of another agent's class.
- [ ] **H5** Delegated tasks keep `review_level: human-only`.
- [ ] **H6** Delegated tasks carry verifiable `acceptance_criteria` and `out_of_scope`.
- [ ] **H7** Delegations restate hard limits and give `SOUL.md`/`AGENTS.md` paths of the target role (bootstrap §5).

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Routing is minimal and justified (no unnecessary agents) | 30 |
| R2 | Workflow named and justified | 20 |
| R3 | `standard` review offered as a recommendation, decision left to human | 20 |
| R4 | Required references listed by path in each delegation | 20 |
| R5 | Lead-with-result, concise | 10 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
