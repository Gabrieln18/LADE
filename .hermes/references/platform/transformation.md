# transformation.md — Data Transformation (Module 1.2)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/platform/transformation.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: *Arquitetura Documentada — Data Transformation Layer* (2026-09-10), *Data Transformation 2.0* documentation system (status **Proposed**), *Visão 360* L3/L4.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN`. Bootstrap; human-edited only.

## 1. Role

Turns raw data from Ingestion (Bronze) into structured analytical products (Silver ARD, Gold). Abstracts distributed processing behind a **declarative SDK**: pipelines are defined by high-level operations, not engine code. Described as a *declarative processing platform* inspired by Palantir Foundry, geospatial-oriented. `PROPOSED`

## 2. Three abstraction levels `PROPOSED`

| Level | Question it answers | Component |
|-------|---------------------|-----------|
| API/SDK | How does the developer work? | Lattinus SDK (Python API + declarative DSL), Transformation API |
| Execution layer | Who plans execution? | Execution Planner |
| Processing engines | Who actually executes? | **Jaguar** (raster/cube), **Mirage** (spatial/vector) |

Business rules stay independent of processing technology, so engines can evolve without changing developer experience.

```
Lattinus SDK (DSL) → Transformation API
   → Dataset Catalog · Transformation Catalog · Output Catalog
   → Execution Planner (parser → dependency graph/DAG → optimization → execution plan)
   → Jaguar | Mirage → Output Writers → Storage (S3/MinIO) → Catalog
```

## 3. Components

| Component | Responsibility |
|-----------|----------------|
| SDK | Python API, DSL, pipeline construction, dataset typing, transformation composition. The developer **never chooses Jaguar or Mirage directly** `PROPOSED` (see conflict below) |
| Dataset Catalog | All inputs: Sentinel, Landsat, SAR, GeoJSON, GeoParquet, CSV, Parquet, Arrow, Zarr, STAC, streaming sources |
| Transformation Catalog | Official operations: Clip, Merge, Union, Join, Filter, Overlay, Mask, Normalize, Resample, Reproject, Aggregate, Buffer, Rasterize, Vectorize, NDVI, NDMI, EVI, Cloud Mask, SAR Calibration, Terrain Correction. Declarative; the executor is decided later |
| Output Catalog | GeoTIFF, COG, GeoParquet, Parquet, Arrow, Zarr, NetCDF, Feature Store, Data Lake, STAC |
| Execution Planner | Builds the DAG and decides engine, order, parallelism, intermediate persistence, cache, optimization. Knows engine capabilities; engines do not know each other |
| Quality | Validates CRS, resolution, bands, metadata, NoData, cloud cover, integrity, schemas, spatial consistency |
| Metadata & lineage | Origin, datasets, transformations, parameters, versions, outputs: reproducibility and audit |
| Workflow | Reusable pipelines (e.g. Download → Clip → Mask → NDVI → Quality → Persist). Prefect discussion must be validated before normative use |

Illustrative SDK shape (not an API contract): `Dataset("sentinel").clip(area).compute_ndvi().join(climate).save("gold/ndvi")`.

`OPEN` `OQ-REF-010`: the archived Collaboratory analysis shows a notebook importing `Jaguar` through the SDK, which contradicts "the developer never chooses an engine". Until resolved, design public SDK surfaces **without** engine names.

## 4. Proposed internal layout

```
data-transformation/
├── sdk/{datasets,transformations,outputs,decorators,pipeline,api}/
├── planner/{execution_planner,optimizer,dependency_graph,scheduler,routing}/
├── engines/{jaguar,mirage}/
├── catalog/{inputs,transformations,outputs,metadata}/
├── quality/{validation,schema,integrity,lineage}/
├── workflow/  monitoring/  config/
```

## 5. Hybrid flow

A pipeline may use both engines. Example: Sentinel → Jaguar (NDVI raster) → Mirage (zonal statistics per plot) → GeoParquet → Storage. Engine change is transparent to the user; handoff between engines is planned (intermediate persistence), not direct engine-to-engine calls.

## 6. Documentation system (DT 2.0) `PROPOSED`

Canonical order: Technical Overview (DT-OVW-001), Architecture (DT-ARQ-001), Stack (DT-STK-001), Interface Contract (DT-IF-001), Event Contract (DT-EVT-001), Codebook (DT-COD-001), Developer Guide (DT-DEV-001), ADR (DT-ADR-NNN), RFC (DT-RFC-NNN), Platform Integration (DT-INT-001), Reference (DT-REF-001), README. Separation rule: ARQ explains structure, STK records technology, IF/EVT define contracts, COD/REF normalize terms, ADR records decisions, RFC discusses proposals. RFCs are not normative until accepted. Legacy content is evidence until classified accepted/proposed/deprecated/superseded. Current priority: Foundation, Interface Contract, Platform Integration, Developer Guide, Codebook.

IF-001-type contracts for Dataset, Transformation, Pipeline, Output, ExecutionPlan, Engine are named but **not read** (`OQ-REF-014`).

## 7. Principles applied `PROPOSED`

Reuse mature engines behind an own API · plan for failure (declarative pipelines + intermediate persistence enable reprocessing) · scale engines independently · SDK standardizes team practice · new engines (LiDAR, GPU, hyperspectral) must not change the public API · loose coupling · reversible decisions · centralized validation, governance and lineage before persistence · FinOps via engine choice per workload.

## 8. Gaps

`OQ-REF-006` routing criterion owner (Planner vs `AnalyticsRouter`) · `OQ-REF-010` SDK engine exposure · `OQ-REF-012` storage format choices · `OQ-REF-014` unread DT 2.0 documents · SAR preprocessing placement: catalog lists SAR Calibration/Terrain Correction, but PyroSAR (GPT/SNAP, Java) is not clearly assigned to Jaguar or a separate runtime (`OQ-REF-018`).
