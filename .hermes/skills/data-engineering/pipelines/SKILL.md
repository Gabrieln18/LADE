---
name: pipelines
description: Design, implement or review data pipelines: layered flow from raw to curated to serving, idempotent and re-runnable stages, backfill and reprocessing, lineage, partial-failure handling, observability and runbooks. Use whenever a task builds or changes a transformation flow, ETL/ELT job, scheduled job, batch or incremental processing, backfill, or asks how data should move between stages, even if it does not say "pipeline".
owner: data-engineer
version: 0.1.0
---

# pipelines

## 1. When to use / When NOT to use
Use: stage design, orchestration logic, reprocessing, backfill, lineage, failure behavior, runbooks.
Do NOT use: for source access (`ingestion`), schema (`data-contracts`), check definitions (`data-quality`), or engine-specific tuning (`processing/*`).
Raster/vector transformations are delegated to `geospatial-engineer` via `task.md`; this skill owns the flow around them.

## 2. Required inputs (task.md)
- Input and output datasets with contract ids and versions.
- Trigger and cadence (event, schedule, manual) and expected volume.
- Latency/freshness needs and acceptable failure behavior.
- Chosen engine/orchestrator, if any (otherwise propose via ADR; do not assume).

## 3. Procedure
1. Define stages and layers: `raw` (immutable, from ingestion) → `curated` (validated, conformed) → `serving` (consumer-ready). Layer names are `TBD` until an ADR exists.
2. For each stage declare: inputs, outputs, contract versions, parameters, owner, and quality checkpoints (from `data-quality`).
3. Make every stage **idempotent**: same input + parameters + code version gives the same output. Write by partition overwrite or merge on key; never blind append.
4. Publish atomically: write to a staging location, validate, then swap/commit. Consumers never see partial output.
5. Parameterize runs (time range, partition, version). No hidden state, no wall-clock or unseeded randomness inside logic; pass them in.
6. Define partial-failure behavior: what is retried, what is resumable (checkpoints), what blocks, what is quarantined.
7. Record lineage per run: source datasets and versions, code version, parameters, run id, output location, timestamps.
8. Declare scaling strategy: partitioning/chunking, memory and runtime assumptions. No full in-memory loads of unbounded data.
9. Write the backfill procedure: how to choose the range, run in order, verify, and roll back; confirm it does not duplicate or overwrite unrelated partitions.
10. Add observability (OpenTelemetry conventions): rows/bytes in and out, duration, failures, retries, freshness; structured logs correlated by `task_id` or run id.
11. Write the runbook: run, monitor, retry, backfill, roll back, who to contact.

## 4. Standards
`lattinus-code.md` §6.2 (data pipeline), §7 (engineering), §8 (geospatial/scale/reproducibility), §11 (operability).
- Pinned dependencies and lockfile; seeded randomness; configuration injected (Twelve-Factor).
- Stage boundaries use contracts; schema validation on input and output.

## 5. Outputs
Pipeline code and tests (idempotency and failure-path tests included), lineage description, backfill procedure, runbook, traceability header (`AGENTS.md` §10).

## 6. Gates triggered
Dependencies (engines, orchestrators, libraries), Safety (anything that overwrites or deletes data, or touches external systems), Git, Documentation.
Deployment or scheduling in production is produced as definitions only; humans apply (`config/permissions.md` §6).

## 7. Done checklist
- [ ] Stages, layers and contracts declared.
- [ ] Re-run on the same input yields the same output (tested).
- [ ] Atomic publish; no partial output visible.
- [ ] Lineage recorded per run.
- [ ] Failure and retry behavior defined and tested.
- [ ] Backfill procedure written and safe.
- [ ] Scaling assumptions stated.
- [ ] Metrics, logs and runbook present.
- [ ] Quality checkpoints wired to `data-quality` rules.

## 8. Escalate when
- Engine/orchestrator choice is needed and no ADR exists.
- Requirements conflict (e.g. exactly-once vs available infrastructure).
- A backfill would overwrite data outside the declared scope.
- Spatial transformation is required (delegate through the Orchestrator).

## 9. Anti-patterns
Append-only writes that duplicate on retry; mutating raw data; hidden global state; transform logic mixed with I/O and orchestration; backfill by editing production tables; no lineage; swallowing errors to keep the run green.

## 10. References (pointers only)
`references/platform/transformation.md`, `references/engineering/data.md`, `references/domain/geospatial.md`, `references/lattinus-code.md`.
Record missing files in `memory/open-questions.md`; do not invent platform details.