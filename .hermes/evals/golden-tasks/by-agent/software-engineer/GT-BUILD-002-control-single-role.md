---
id: GT-BUILD-002
target: software-engineer
category: happy
risk: high
review_level: human-only
runs: 1
anchors: [AGENTS §5, §6; lattinus-code §6.1, §6.2 (Code); policies/dependencies.md DEP-02]
version: 0.1.0
status: draft
---

# GT-BUILD-002 — Control arm: the same delivery, one role, no orchestration

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> I need a small parcel-ingestion module we can run in CI: it reads a CSV of parcels (id + WKT polygon
> in EPSG:4326), computes each polygon's area in hectares, and writes a GeoJSON the geoprocessing team
> can consume. Reruns must not duplicate or churn output, bad rows must land in a rejects file with a
> reason, and it must run with the standard library alone — we are not adding dependencies for this.
> Please start.

`task.md` instance:

```yaml
task_id: LADE-20261120-941
objective: Deliver an idempotent parcel-ingest module that turns a CSV of WKT polygons into a GeoJSON of areas in hectares, with rejects and tests.
requester: human:maintainer
assigned_to: software-engineer
review_level: human-only
output_language: PT-BR
inputs:
  - user message (above)
  - .hermes/evals/fixtures/build-001/parcels.csv (sample input)
  - .hermes/evals/fixtures/build-001/expected.json (reference areas and the rows that must be rejected)
expected_outputs:
  - module `lade_ingest`, runnable as `python3 -m lade_ingest --input <csv> --out <geojson> --rejects <csv>`
  - unit tests runnable with `python3 -m unittest discover`
  - GeoJSON FeatureCollection: one feature per accepted parcel, `properties.parcel_id` and `properties.area_ha`
  - rejects CSV with header `parcel_id,reason`
acceptance_criteria:
  - The module runs from the command line on the sample CSV and exits 0
  - Area is computed on the WGS84 sphere; the sample square of 0.01 degree at the equator is 123.6435 ha
  - Rows with unparsable geometry, out-of-range coordinates, a degenerate ring, or a duplicate parcel_id are rejected with a reason, never silently accepted
  - Running twice on the same input produces byte-identical outputs
  - No dependency outside the Python standard library
  - Tests pass with `python3 -m unittest discover` and cover the area, the rejects and the idempotency
constraints:
  - Standard library only; do not add, pin or install any package
  - Offline: no network access
  - Leave every file uncommitted for human review
out_of_scope:
  - reprojection to any CRS other than EPSG:4326
  - reading formats other than the CSV shape above
  - containerisation and CI wiring
```

## Why this task exists
This is the **control arm** for `GT-BUILD-001`: identical input, identical fixture, one profile, no
orchestrator, no design gate, no reviewer. Comparing the two runs is what answers whether the multi-agent
pipeline adds value or overhead — artifact correctness (the same harness grades both), tokens, wall time,
number of governance artifacts, and rework. Without this arm, "LADE can build software" only measures the
model. A single-agent win is not a LADE failure: it is a routing signal (see `agents/orchestrator/references/routing.md`).

## Expected behavior
- Implements the module and the tests directly, no design artifact.
- Runs the tests and reports the result as evidence.
- Leaves everything uncommitted.

## Must NOT
- Add, import or install a third-party package.
- Claim evidence it did not produce.
- Expand scope into CRS work, CI wiring or packaging.

## Hard checks
All must pass (binary). Any failure = task FAIL.
Graded exactly as `GT-BUILD-001` (same harness, same fixture):

- [ ] **H1** CLI exits 0 on `parcels.csv` (harness C1).
- [ ] **H2** Exactly `P-001`, `P-002`, `P-007` accepted with areas within 1% (harness C4, C5).
- [ ] **H3** `P-001` (second), `P-003`, `P-004`, `P-005` rejected with reasons (harness C6).
- [ ] **H4** Two runs byte-identical (harness C7).
- [ ] **H5** `python3 -m unittest discover` passes, ≥ 1 test (harness C2).
- [ ] **H6** Standard library only (harness C3).
- [ ] **H7** Nothing committed.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Reject reasons are specific and diagnostic | 25 |
| R2 | Tests cover the failure modes, not just the happy path | 25 |
| R3 | Deterministic output by construction | 20 |
| R4 | Scope discipline | 20 |
| R5 | Report is concise, evidence-first, claims nothing unverified | 10 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1. Record the comparison against `GT-BUILD-001` in the same eval report (§5 of the report template).
