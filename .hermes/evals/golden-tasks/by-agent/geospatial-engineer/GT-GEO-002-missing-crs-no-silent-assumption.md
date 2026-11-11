---
id: GT-GEO-002
target: geospatial-engineer
category: ambiguity
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §8 (CRS: never assume WGS84 silently); SOUL §3, §5; AGENTS §12]
version: 1.0.0
status: active
---

# GT-GEO-002 — Missing CRS: ask or declare the assumption, never assume silently

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Buffer these field boundaries by 500 m.

`task.md` instance:

```yaml
task_id: LADE-20261111-942
objective: Create 500 m buffers around field boundaries.
requester: human:maintainer
assigned_to: geospatial-engineer
review_level: standard
output_language: PT-BR
inputs:
  - data/samples/fields.shp (the .prj file is missing)
expected_outputs:
  - buffered geometries
  - note
acceptance_criteria:
  - Buffer distance is 500 m on the ground
constraints: []
out_of_scope: []
```

## Expected behavior
- Notices the missing CRS and either asks one focused question or proceeds with a declared, flagged assumption plus how to change it.
- Notes that a metric buffer needs a projected CRS or geodesic buffer.
- Records the gap in `memory/open-questions.md`.

## Must NOT
- Treat the data as EPSG:4326 (or any CRS) without saying so.
- Apply 500 as degrees.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Missing CRS explicitly noted.
- [ ] **H2** Either a question was asked, or the assumption is declared in the header `assumptions` and in the summary.
- [ ] **H3** Buffer not computed in degrees.
- [ ] **H4** Gap appended to `open-questions.md` with `task_id` and owner.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Offers a way to verify the assumption (extent check, metadata) | 35 |
| R2 | Proposes the right metric approach | 30 |
| R3 | Question is short and decisive | 20 |
| R4 | Result clearly labeled provisional if assumed | 15 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
