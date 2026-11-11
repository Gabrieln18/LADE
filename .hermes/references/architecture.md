# architecture.md — Lattinus Platform Architecture (Snapshot)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/architecture.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: *Arquitetura da Plataforma* (edited 2026-09-19), *Briefing · Visão 360 Técnico V1* (2026-06-29).
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN` (`OQ-REF-NNN`). Only `ACCEPTED` is normative. Bootstrap content; human-edited only.

## 1. Principles `ACCEPTED`

1. **Single responsibility per module.** Explicit interfaces between modules (schema + SLA).
2. External configuration and dependency injection.
3. Observability native from the start, not a Phase 2 feature.
4. Clean Architecture + Data Mesh + Medallion (Bronze → Silver → Gold).
5. Loose coupling and reversible decisions: frameworks are implementation details behind abstractions.
6. Modules are autonomous and deployable independently (cloud) or composed as a monolith (edge). `PROPOSED` (ARQ-001 V2, Observability page)

## 2. Module map (current taxonomy)

Source: *Arquitetura da Plataforma*. Tags describe the documentation state, not production state.

| Id | Module | Responsibility | State |
|----|--------|----------------|-------|
| 1.1 | Data Ingestion | Discover, authenticate, download, validate and register raw assets. **Only contact point with external providers** (credentials, rate limits, formats isolated here). Quality gate before Bronze | `PROPOSED` (V2) → `platform/ingestion.md` |
| 1.2 | Data Transformation | Raw → structured analytical products via a declarative SDK; hides distributed engines (Jaguar, Mirage) | `PROPOSED` (2.0) → `platform/transformation.md` |
| 1.3 | Metadata Catalog & Discovery | Searchable representation of datasets, collections, assets and metadata. Does **not** store primary data | `OPEN` `OQ-REF-014` |
| 1.4 | Data Management | Asset lifecycle: identity, contract, state, version, quality, lineage, publication, governance. No physical storage | `OPEN` `OQ-REF-014` |
| 1.5 | Platform Observability | Cross-cutting. Each module autonomous | `OPEN` `OQ-REF-014` |
| 1.6 | Managed Storage (S3) | Persistence and lifecycle of analytical data | `OPEN` `OQ-REF-014` |
| 1.7 | Colab Service (Collaboratory) | R&D environment (notebooks, SDK) | `HYPOTHESIS` → `platform/collaboratory.md` |
| 1.8 | Edge / Operations Layer | Field hardware lifecycle: IoT identity, firmware, calibration, state (humidity, pH, EC) | `HYPOTHESIS` |
| 1.9 | Lattinus SDK | Programmable surface: Resources, Capabilities, Operations, Composition | `OPEN` `OQ-REF-014` |
| 2 | Platform Management | Control plane: identities, users, authorization, credentials, API tokens, configuration, policies | `OPEN` `OQ-REF-014` |
| 2.1 | Serving API | Unified front door: REST, GraphQL, AI, streaming | `OPEN` `OQ-REF-014` |
| 2.2 | AI & Intelligence | Foundation models (local/third-party) behind unified governance; agents, runtimes, tools, workflows | `OPEN` `OQ-REF-014` |
| 2.3 | WebUI | Experience layer: dashboards, maps, workspaces, admin | `OPEN` `OQ-REF-014` |
| 2.4 | CLI | Terminal interface (cloud, edge, local) | `OPEN` `OQ-REF-014` |

Each module has (in Notion) five documentation sections: Foundation, Engineering, Architecture Governance, Platform Integration, Reference. Document lifecycle: `Draft → Proposed → Accepted → Deprecated/Superseded`. **Evidence rule:** no hypothesis, proposed technology or ownership boundary becomes normative without explicit evidence or approval.

## 3. Data flow and Medallion `ACCEPTED`

```
External providers → 1.1 Ingestion → [Bronze] raw, validated
  → 1.2 Transformation → [Silver] ARD (Analysis-Ready Data)
  → 1.2 Transformation/AI → [Gold] analytical products
  → 2.1 Serving API → 2.3 WebUI / CLI / external systems
Storage (1.6) and Catalog (1.3) support every stage. Observability (1.5) and security span all.
```

| Tier | Content | Written by |
|------|---------|-----------|
| Bronze | Raw assets as acquired, validated, with minimal metadata | Ingestion (via Storage SDK) |
| Silver | Calibrated, corrected, aligned ARD (CRS, resolution, QA flags) | Transformation |
| Gold | Features, indices, fused products, predictions | Transformation / AI |

## 4. Boundary rules

1. Ingestion reaches Storage **only** through the Storage SDK (IF-001). Storage notifies consumers by events (EVT-001). `PROPOSED`
2. Transformation consumes Bronze. It is not an Ingestion responsibility. `PROPOSED`
3. Developers program against SDK abstractions (Dataset, Transformation, Output), never against Dask/Sedona. `PROPOSED`
4. Experience layers (Collaboratory, WebUI) consume public APIs/SDK only: no direct buckets, databases or engines. `PROPOSED` / `HYPOTHESIS`
5. Engines do not know each other; the Execution Planner knows engine capabilities. `PROPOSED`

## 5. Recorded decisions `ACCEPTED` (Visão 360, §5, closed; reopening needs explicit technical justification)

| Decision | Choice | Discarded | Reason |
|----------|--------|-----------|--------|
| SAR wrapper | PyroSAR | Snappy | Java bridge slow and unstable |
| 2D raster format | COG | Classic GeoTIFF | HTTP-range without full download |
| N-D cube format | Zarr | NetCDF | Cloud-native chunking |
| Orchestration | Prefect | Airflow | Lower overhead, Python-first |
| Raster engine | Dask + Xarray | RasterFrames | RasterFrames poorly maintained |
| Vector engine at scale | Apache Sedona | Dask GeoPandas | Massive spatial joins |
| ML framework | PyTorch + TorchGeo | TensorFlow | Mature EO ecosystem |

Listed as choices in Visão 360 §2.2 but **not** in the closed register: Apache Iceberg (over Delta Lake), STAC catalog, DVC (over Git LFS). Treat as `PROPOSED` until the Managed Storage/Catalog docs confirm (`OQ-REF-012`).

## 6. Interface contracts and SLAs `PROPOSED` (not yet materialized in Notion)

| Transition | Output | Minimum schema |
|------------|--------|----------------|
| Ingestion → Bronze | COG + Zarr + STAC Item | `bbox`, `datetime`, `sensor`, `processing_level`, checksum |
| Bronze → Silver | Calibrated SLC/GRD | `crs`, `resolution`, `cloud_cover_pct`, `qa_flags` |
| Silver → Gold | Validated ARD (COG/Zarr) | `ard_validated`, `indices_available[]`, `talhao_id` |
| Gold/AI → Serving | Analytical products | `product_type`, `confidence_score`, `generated_at`, `model_version` |

| Stage | Target SLA | Rationale |
|-------|-----------|-----------|
| Ingestion → Bronze | < 2 h after acquisition | Copernicus publishes in < 1 h |
| ARD | < 4 h per IW scene | SAR processing is the bottleneck |
| Analysis | < 6 h per AOI | Depends on plot volume |
| Client alert | **< 24 h end to end** | Pests act in 48–72 h windows |

The 24 h product SLA drives pipeline SLAs, not the reverse. Agents must not weaken an SLA without a human decision.

## 7. Legacy mapping (Visão 360 L1–L10 → current modules)

`LEGACY` taxonomy, kept because older docs use it. Mapping is an **inference** (`OQ-REF-007`), confirm before citing.

| Legacy | Current |
|--------|---------|
| L1 Ingestion | 1.1 |
| L2 Storage & Catalog (Bronze) | 1.6 + 1.3 |
| L3 Pre-processing (Silver/ARD), L4 Processing (Gold) | 1.2 |
| L5 AI/ML | 2.2 |
| L6 Serving & API | 2.1 |
| L7 Visualization | 2.3 |
| L8 Orchestration (Prefect) | inside modules (e.g. Ingestion `orchestration/`, Transformation `workflow/`) |
| L9 Security & Governance (Keycloak, OPA) | 2 Platform Management + governance |
| L10 Monitoring (Prometheus, Grafana, OpenTelemetry, Loki) | 1.5 |

## 8. Open items

| Id | Item | Urgency |
|----|------|---------|
| `OQ-REF-001` | SLC retention: ingest SLC together with GRD? Phase cannot be rebuilt from GRD; deciding late closes InSAR/PSI | High, before first ingestion pipeline |
| `OQ-REF-002` | Genesis agents access Gold via Serving API or directly? Defines permissions, SLA and whether WebUI is product or back-office | High, before 2.1 spec |
| `OQ-REF-003` | ML experiment tracking (MLflow, W&B, other); DVC covers data/artifacts only | Medium, before first fine-tuning |
| `OQ-REF-004` | `InferenceEngine` contract separating inference from training | Medium |
| `OQ-REF-005` | Ground-truth pipeline (who labels, format, latency) is a Phase 1 deliverable | High |
| `OQ-REF-006` | Dask/Sedona routing: `AnalyticsRouter` (Jun) vs Execution Planner (Sep). Which is normative? Criterion must live in code | Medium, before L4/Transformation implementation |
| `OQ-REF-007` | Confirm L1–L10 → module mapping | Low |
| `OQ-REF-009` | Ownership of final STAC generation: Ingestion catalog vs Metadata Catalog (1.3) | Medium |
| `OQ-REF-010` | SDK public surface: does it expose engines? (see `platform/transformation.md` §3) | Medium |
| `OQ-REF-012` | Iceberg/DVC/STAC confirmation | Medium |
| `OQ-REF-014` | Unread module docs (1.3–1.6, 1.9, 2.x) | Medium |

Compliance, security and governance tools (Keycloak, OPA, Unity Catalog or open equivalent, LGPD) appear in Visão 360 §L9 as `PROPOSED`; observability stack (Prometheus, Grafana, OpenTelemetry, Loki) in §L10 as `PROPOSED`. OpenTelemetry also appears in `references/lattinus-code.md` §3 as the delivery standard.
