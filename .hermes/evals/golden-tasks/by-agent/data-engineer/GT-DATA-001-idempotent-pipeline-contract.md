---
id: GT-DATA-001
target: data-engineer
category: happy
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §6.2 (Data pipeline), §3, §11, §14; AGENTS §6]
version: 1.0.0
status: active
---

# GT-DATA-001 — Idempotent ingestion pipeline with data contract and checks

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Ingest daily weather-station CSV files into Parquet.

`task.md` instance:

```yaml
task_id: LADE-20261111-931
objective: Ingest daily station-reading CSV files into partitioned Parquet.
requester: human:maintainer
assigned_to: data-engineer
review_level: standard
output_language: PT-BR
inputs:
  - sample: data/samples/stations_2026-11-10.csv (columns: station_id, ts_utc, temp_c, rain_mm)
expected_outputs:
  - pipeline code
  - data contract
  - quality checks
  - runbook
acceptance_criteria:
  - Re-running the same day yields identical output
  - Contract defined for input and output
  - Schema validation on input and output
  - Quality checks with failure behavior
  - Lineage and backfill documented
constraints: []
out_of_scope:
  - scheduling
  - orchestration infrastructure
```

## Expected behavior
- Idempotent writes (partition overwrite or deterministic keys).
- Data contract for input and output; contract standard (ODCS) stated as assumption since confirmation is `TBD`.
- Quality checks (nulls, ranges, duplicates) with defined failure behavior (reject, quarantine, fail).
- Lineage and backfill procedure described.

## Must NOT
- Assume CI, repository or secret mechanism (`TBD` parameters).
- Load unbounded data fully in memory without justification.
- Hard-code paths or credentials.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Re-run safety is demonstrated (test or explicit mechanism).
- [ ] **H2** Data contract present for input and output.
- [ ] **H3** Schema validation on both sides.
- [ ] **H4** Each quality check states failure behavior.
- [ ] **H5** Lineage (source → output) documented.
- [ ] **H6** Backfill procedure described.
- [ ] **H7** TBD parameters are not assumed as facts; assumptions declared in the header.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Time handling explicit (UTC, event vs processing time) | 25 |
| R2 | Checks fit the data (ranges, duplicates, late arrivals) | 25 |
| R3 | Tests are deterministic with sample data | 25 |
| R4 | Runbook is actionable | 25 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
