# data.md — Data Engineering Reference

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-12 · **Location:** `references/engineering/data.md`
> New file: it was cited by ~10 skills and manifests but did not exist. Holds project facts only; procedures live in `skills/data-engineering/*`.
> Evidence tags as in `references/architecture.md`. Only humans edit this file.

## 1. Layers `ACCEPTED` (`architecture.md` §3)

| Tier | Content | Written by |
|------|---------|-----------|
| Bronze | Raw, validated assets with minimal metadata | Ingestion |
| Silver | Calibrated, aligned ARD (CRS, resolution, QA flags) | Transformation |
| Gold | Features, indices, fused products, predictions | Transformation / AI |

The data-engineering skills speak of `raw → curated → serving` and say layer names are `TBD`. **Proposed mapping (needs human confirmation, Q-020):** raw = Bronze, curated = Silver, serving = Gold. Until confirmed, artifacts state which naming they use.

## 2. Formats and catalog `ACCEPTED`

COG (2D raster), Zarr (n-D cubes), GeoParquet (vector), STAC (catalog). Rules: `lattinus-code.md` §3, §8; detail: `domain/geospatial.md` §2.

## 3. Contracts

Data contract standard: ODCS or equivalent, **not confirmed** (`lattinus-code.md` §14, Q-009). Skills keep the template ODCS-aligned and flag the open decision.

## 4. Pipeline expectations (from `lattinus-code.md` §6.2, §11)

Idempotent, re-runnable, atomic publish, lineage, quality checks with failure behavior, backfill and runbook. Orchestration: Prefect `ACCEPTED` (`architecture.md` §5). Operational signals: OpenTelemetry.

## 5. SLAs `PROPOSED` (`architecture.md` §6)

Ingestion → Bronze < 2 h · ARD < 4 h per IW scene · analysis < 6 h per AOI · client alert < 24 h end to end. Agents MUST NOT weaken an SLA without a human decision.

## 6. Open parameters (`TBD`)

Layer naming confirmation (Q-020) · contract standard (Q-009) · storage layout names (ADR pending) · plot-layer schema (`domain/geospatial.md` §7) · secret mechanism (Q-007).
