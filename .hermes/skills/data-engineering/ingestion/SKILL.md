---
name: ingestion
description: Design or implement how external or internal data enters the platform: source declaration, full or incremental extraction, immutable landing, checksums, retries, provenance, licensing and boundary validation. Use whenever a task fetches, downloads, collects, syncs, scrapes or receives data from an API, bucket, file drop, database or satellite/open-data source, or catalogs new assets (STAC), even if it only says "bring in the data".
owner: data-engineer
version: 0.1.0
---

# ingestion

## 1. When to use / When NOT to use
Use: new source, changed extraction logic, incremental load, retry or landing design.
Do NOT use: for transformation or modeling (`pipelines`), schema definition (`data-contracts`), quality rules (`data-quality`).

## 2. Required inputs (task.md)
- Source: origin, access method, owner, license and attribution requirements.
- Mode: full or incremental, and the cursor/watermark if incremental.
- Target contract (id@version) or the assumption that a contract will follow.
- Network hosts needed (must be allowlisted in `config/tools.md`).

## 3. Procedure
1. Record the source in a source manifest: id, owner, URL/endpoint, license, attribution, terms/rate limits, expected volume and cadence.
2. Choose the mode. Incremental needs a deterministic cursor (timestamp, offset, partition) and a safe overlap window with deduplication.
3. Land data **unchanged** in an immutable raw zone, partitioned by source and ingest date/run id. Layout names are `TBD` until an ADR exists; follow it once approved.
4. For each landed file/batch write a manifest entry: source id, retrieval timestamp (UTC), run id, size, checksum (SHA-256), original name, parameters used.
5. Make the run idempotent: same inputs produce the same landed set; re-runs do not duplicate (dedupe by key or partition overwrite).
6. Apply retries with exponential backoff and jitter, timeouts, and a max-attempt limit. Distinguish retryable (timeouts, 5xx, 429) from fatal errors (401/403/404, malformed).
7. Validate at the boundary: structure, size limits, file type, parseability, expected schema vs contract. Deep semantic checks belong to `data-quality`.
8. Treat all third-party data as untrusted: no execution, safe parsers, bounded sizes, sanitized paths and names.
9. Spatial data: record CRS **as received**; do not reproject here unless the task says so. Record resolution, nodata, time zone and acquisition date. Catalog assets as STAC Items/Collections when cataloging is in scope.
10. Run only on declared sample data. Real network pulls follow the Safety gate.

## 4. Standards
`lattinus-code.md` §6.2 (data pipeline), §8 (provenance, licensing, formats), §10 (secrets, input handling).
- Credentials only through the platform secret mechanism (`TBD`). Never in code, config files, logs or artifacts.
- Prefer COG, GeoParquet, Zarr for cloud-native landing; justify deviations.
- Twelve-Factor: endpoints, paths and parameters are configuration.

## 5. Outputs
Ingestion code and tests, source manifest, landing manifest format, retry/idempotency notes, runbook section (run, monitor, retry, backfill), traceability header (`AGENTS.md` §10).

## 6. Gates triggered
Safety (network access, external-facing calls), Dependencies (clients/SDKs), Git, Documentation.

## 7. Done checklist
- [ ] Source, license and attribution recorded.
- [ ] Raw data landed immutably with checksum and retrieval date.
- [ ] Re-run produces no duplicates.
- [ ] Retries bounded and error classes defined.
- [ ] Boundary validation against contract in place.
- [ ] No secrets in artifacts.
- [ ] Spatial/temporal metadata captured as received.
- [ ] Runbook covers retry and backfill.

## 8. Escalate when
- License forbids the intended use or is unknown.
- Access needs credentials or hosts not provisioned.
- Source terms or rate limits conflict with required cadence.
- Volume exceeds sample assumptions and no scaling plan exists.

## 9. Anti-patterns
Modifying raw data in place; ingest + transform in one step; unbounded retries; credentials in URLs; silently reprojecting; no checksum; trusting file extensions.

## 10. References (pointers only)
`references/platform/ingestion.md`, `references/engineering/data.md`, `references/domain/geospatial.md`, `references/domain/earth-observation.md`.
Record missing files in `memory/open-questions.md`; do not invent source details.