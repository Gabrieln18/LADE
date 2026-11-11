# ingestion.md — Data Ingestion (Module 1.1)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/platform/ingestion.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources read: *ARQ-001 V2* (verified 2026-09-01), *ADR-002 V2*, *ADR-003 V2*, *Visão 360* L1, archived V1 architecture. Status of V2 documents: **"Proposta para Aprovação"**.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN`. Nothing marked `PROPOSED` is normative. Bootstrap; human-edited only.

## 1. Role and boundaries

Discovers, authenticates, acquires, validates and registers external EO assets, then persists validated assets to **Bronze** through the Storage SDK. It is the **only** platform contact with external providers: credentials, rate limits, protocols and formats stay isolated here. `PROPOSED`

| In scope | Out of scope |
|----------|--------------|
| Discovery, authentication, download/streaming, staging, checksum, quality gate, minimal metadata normalization, idempotency, quarantine, retries, telemetry, Bronze persistence | Analytical transformation, reprojection, scientific processing, defining Storage physical layout. Final STAC generation is **`OPEN`** (`OQ-REF-009`; the archived V1 excluded it) |

Transformation consumes Bronze and is not an Ingestion responsibility.

## 2. Components `PROPOSED` (ARQ-001 V2)

| Component | Responsibility |
|-----------|----------------|
| `connectors` | Provider adapters: Sentinel-2, Landsat 8/9, Planet, NASA SMAP, ICEYE |
| `runtime` | Discovery, transfer, streaming, jobs, state machine |
| `catalog` | Raw metadata, validation, identity, minimal lineage, quarantine |
| `staging` | Temporary storage and download resume |
| `storage_adapter` | Exclusive client of the Storage SDK |
| `orchestration` | Prefect flows/tasks, schedules, deployment |
| `interfaces` | CLI, API, health checks (platform-owned) |
| `observability` | Logs, metrics, traces (platform-owned) |

```
ingestion/
├── core/ (contracts, identity, config, errors, telemetry)
├── connectors/{sentinel2,landsat,planet,smap,iceye}/
├── runtime/{discovery,transfer,streaming,jobs}/
├── catalog/{metadata,validation,identity,lineage,quarantine}/
├── storage_adapter/
├── orchestration/prefect/
├── interfaces/{cli,api,health}/
└── tests/{unit,integration,contract,e2e}/
```

Connector contract `LEGACY`/`PROPOSED` (V1 exploration; V2 does not restate it): `authenticate()`, `discover()`, `download()`, `map_metadata()`, `health_check()`. A new provider implements only this interface. Treat as design intent, confirm before coding.

## 3. Identity and idempotency `PROPOSED` (ADR-002)

- Three identifiers: `provider_asset_id` (external identity), `asset_id` (deterministic), `idempotency_key` (acquisition operation).
- `asset_id = UUIDv5(namespace_lattinus, canonical(provider, provider_asset_id, product, acquired_at, spatial_extent, revision))`
- `idempotency_key = sha256(provider + provider_asset_id + acquisition_revision + requested_product + canonical_area)`
- Never create a new asset for a retry of the same acquisition. A new revision/product yields a new key, explicitly recorded. Storage treats the key as an idempotent write condition. Algorithm change = new identity version plus documented migration.
- Acceptance: per-provider fixtures, concurrent-repeat tests, behaviour for missing `provider_asset_id` defined per adapter, algorithm and namespace in the Codebook (COD-001).

## 4. Staging, quality gate, Bronze `PROPOSED` (ADR-003)

Data stays in staging until integrity and quality gate pass. Only validated assets reach Bronze (via IF-001). Staging is temporary, not an analytical layer.

Minimum gates: content checksum · format and content type · required bands/variables · minimum metadata (provider, acquisition, bbox/geometry when available, original CRS, resolution, size) · cloud cover when applicable · file size and safety limits.

Failures: retryable → `RETRYING`; permanent or invalid → `QUARANTINED` with report, reason, checksum and defined retention. **No rejected data reaches Bronze.** Streaming: incremental validation when possible; content-total gates may finish after staging; strategy per format lives in the connector. Full state machine: COD-001/ARQ (not read).

## 5. Execution model and failures

- Same code runs local (edge monolith) or cloud-agnostic: configuration, temp filesystem or mounted volume, Storage SDK endpoint (local or remote). Topology does not change data model or contracts. `PROPOSED`
- Retry with backoff and per-provider limits; circuit breaker where applicable; quarantine for permanent failure.
- Everything correlatable by `run_id`, `asset_id`, `idempotency_key`.

## 6. Technology baseline

Orchestration **Prefect** `ACCEPTED` (Airflow discarded; ADR-004 V2 exists, not read). Listed in Visão 360 L1, `PROPOSED`: STAC + pystac, Dask + rasterio/xarray (batch), Kafka/Redpanda + Flink (streaming/alerts), eodag/satpy (download), Great Expectations/Pandera (gate). Streaming stack is not in V2 scope: confirm before designing around it.

## 7. Contracts

| Contract | Direction | Status |
|----------|-----------|--------|
| IF-001 | Ingestion → Managed Storage via Storage SDK | `PROPOSED`, **not read**: consult in Notion for fields |
| EVT-001 | Event `asset.bronze.persisted` | `PROPOSED`, not read |
| ADR-001 | Ingestion accesses Storage only via the SDK | `PROPOSED`, not read (rule restated in ARQ-001) |

Do not infer IF-001/EVT-001 payloads. Request the Notion page or log a gap.

## 8. Gaps

`OQ-REF-001` SLC vs GRD retention · `OQ-REF-008` Sentinel-1 missing from V2 provider scope (ICEYE SAR present) · `OQ-REF-009` STAC ownership · `OQ-REF-014` ADR-001/004, IF-001, EVT-001, COD-001, OV-001, STK-001 unread · Owner recorded as "Time Lattinus / a confirmar".
