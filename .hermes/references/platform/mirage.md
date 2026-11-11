# mirage.md — Mirage Processing Engine (Spatial / Vector)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/platform/mirage.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: Data Transformation architecture (2026-09-10), *Visão 360* L3/L4.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN`. Bootstrap; human-edited only.

## 1. Role

Internal engine of Data Transformation specialized in **vector and distributed spatial analysis**. Reached through the SDK and Execution Planner, never directly. Apache Sedona as vector engine at scale (over Dask GeoPandas, for massive spatial joins) is `ACCEPTED`; Mirage as a documented component is `PROPOSED`.

## 2. Technology

Apache Sedona, GeoPandas, Shapely `PROPOSED`. Visão 360 positions GeoPandas for vector processing at normal scale and Sedona when scale demands it (alternative: Wherobots managed).

## 3. Responsibilities

Spatial join · overlay · topology · nearest neighbor · buffers · intersections · polygon operations · spatial aggregation · zonal statistics.
Internal modules `PROPOSED`: `runtime`, `vector`, `topology`, `spatial_join`, `analytics`, `io`.

## 4. Route to Mirage when

Complex vector joins at scale, e.g. plot × sensor × time at large volume, and aggregation of raster results per geometry (zonal statistics). Small vector work may stay on GeoPandas inside Mirage. Threshold (geometry volume, operation type) is undefined: `OQ-REF-006`. Raster-only work stays in Jaguar.

## 5. Open concern: runtime footprint

Visão 360 rejects Spark for raster because of operational overhead, while Sedona is the vector choice. Sedona is built on distributed runtimes (Spark, Flink) `GENERAL`, which collides with the edge-monolith deployment option (`architecture.md` §1). Deployment mode (local/single-node vs cluster) and edge viability are `OPEN` (`OQ-REF-019`). Verify current Sedona runtime options before an ADR; do not assume a Spark cluster exists.

## 6. Design rules for agents

1. Validate geometries first; define repair/reject/quarantine (`references/lattinus-code.md` §8).
2. Declare CRS and use a projected CRS or geodesic method for area/distance (`domain/geospatial.md` §1).
3. Zonal statistics: record geometry source, statistic, nodata policy, all-touched rule.
4. Vector outputs: GeoParquet with declared CRS and geometry encoding. Partitioning strategy declared for Sedona jobs.
5. Cross-engine inputs arrive as persisted intermediates planned by the Execution Planner, never by calling Jaguar.

## 7. Gaps

`OQ-REF-006` routing threshold · `OQ-REF-019` Sedona runtime and edge viability · Mirage interface contract (DT-IF) unread · LiDAR/point-cloud support only mentioned as future extension `HYPOTHESIS`.
