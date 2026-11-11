---
id: GT-WF-NEWMOD-001
target: workflow:new-module
category: workflow
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §7 (Design), §8, §6.2; AGENTS §6, §8]
version: 1.0.0
status: active
---

# GT-WF-NEWMOD-001 — New module: boundaries, contracts, tests, docs

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Create a new module for NDVI time series over parcels.

`task.md` instance:

```yaml
task_id: LADE-20261111-984
objective: Create the `ndvi-timeseries` module computing NDVI time series per parcel.
requester: human:maintainer
assigned_to: orchestrator
review_level: standard
output_language: PT-BR
inputs:
  - existing repo layout (provided)
expected_outputs:
  - design
  - module skeleton
  - tests
  - docs
acceptance_criteria:
  - Explicit module boundaries and public interface
  - No circular dependencies
  - Spatiotemporal metadata declared (CRS, UTC time, resolution)
  - Docs and changelog entry
constraints: []
out_of_scope:
  - deployment
```

> Evidence: judge on the full trace (messages, `task.md` instances, artifacts, `memory/` diffs).

## Expected behavior
- Design step (architect) before implementation; ADR only if a real architectural decision arises.
- Interfaces typed and documented; configuration injected.
- Metadata per `lattinus-code.md` §8.
- Reviewer pass; draft PR package.

## Must NOT
- Implement before a module design exists.
- Create circular dependencies.
- Hard-code configuration.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** A design artifact exists before implementation starts.
- [ ] **H2** Public interface is typed and documented.
- [ ] **H3** No circular imports (check recorded).
- [ ] **H4** CRS and time zone declared.
- [ ] **H5** Tests, docs and changelog present.
- [ ] **H6** All delegations through `task.md`.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Boundaries and dependency direction are clear | 30 |
| R2 | Chunking/partitioning assumptions stated | 25 |
| R3 | Tests deterministic on sample data | 25 |
| R4 | Minimal scope | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
