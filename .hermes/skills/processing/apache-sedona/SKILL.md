---
name: apache-sedona
description: Design, implement or review distributed vector and spatial processing with Apache Sedona on Spark (the Mirage engine of Lattinus). Use whenever a task involves Sedona, Spark spatial SQL, ST_ functions, spatial joins, spatial partitioning, large GeoParquet/vector datasets, geometry validation at scale or parcel/field/boundary analytics, even if "Mirage" is not mentioned. Do NOT use for raster/array/data-cube work (use dask-xarray), small datasets that fit in memory (GeoPandas/DuckDB is enough), or SDK contract design (use processing-sdk).
metadata:
  version: 0.1.0
  date: 2026-11-09
  status: draft
  agents: [geospatial-engineer]
  sources: [DT-STK-001, DT-ARQ-001, DT-IF-001, references/lattinus-code.md §8]
---

# apache-sedona (Mirage)

## 1. Scope

Mirage = **Apache Sedona**, specialized in vector and distributed spatial workloads (DT-STK-001 §3).
Code written with this skill is **engine-internal**, behind an engine adapter. Spark and Sedona types MUST NOT leak into SDK public contracts (DT-IF-001 §7). For contract work, switch to `processing-sdk`.

## 2. Load on demand (declared in manifest)

`references/platform/mirage.md`, `references/domain/geospatial.md`, `references/domain/agriculture.md`, `references/engineering/data.md`, `references/lattinus-code.md` §8.
If one is missing or outdated: say so in the artifact, append to `memory/open-questions.md`, proceed only with declared assumptions.

## 3. Decide first: is Sedona justified?

| Situation | Choice |
|-----------|--------|
| Data fits comfortably in one machine's memory | GeoPandas or DuckDB spatial (state why) |
| Large vector data, spatial joins, repeated scans, cluster available | Sedona |
| Edge/monolithic deployment without Spark runtime | Do not assume Sedona; escalate |

Record the choice and rationale in the artifact. Over-engineering is a risk (SOUL §2.4).

## 4. Procedure

1. **Declare the data contract**: geometry type, CRS (EPSG) per dataset, attribute schema, validity policy, source license.
2. **Validate geometries at ingress**: valid, non-empty, expected type. Define the behavior for invalid input (repair, reject or quarantine) and log counts.
3. **CRS is explicit.** Never assume EPSG:4326 silently. Compute area and distance in a suitable projected CRS (for the São Francisco Valley, SIRGAS 2000 / UTM 24S, EPSG:31984, is a candidate: confirm in `references/domain/geospatial.md`). Check axis order (lon/lat) on every `ST_Transform`.
4. **Prefer Spark SQL / DataFrame API** with `ST_*` functions over Python UDFs and row-wise loops.
5. **Spatial joins**: filter early; broadcast the small side when it fits; choose join predicate deliberately (`ST_Intersects`, `ST_Contains`, `ST_DWithin`); handle duplicates from boundary-touching geometries.
6. **Partitioning**: state the partitioning strategy (spatial partitioning vs. attribute partitioning) and expected skew. Avoid `collect()`/`toPandas()` on unbounded data.
7. **Storage**: GeoParquet for vector output. Record CRS, geometry column, schema and partitioning in the output metadata.
8. **Lineage and reproducibility**: record source dataset, version, retrieval date, steps and parameters. Pin Spark, Sedona, Java and Scala versions.
9. **Stateless and idempotent**: re-running the job on the same input produces the same output (overwrite by partition, not append).

## 5. Minimal pattern

```python
from sedona.spark import SedonaContext

config = SedonaContext.builder().appName("mirage-job").getOrCreate()
sedona = SedonaContext.create(config)  # registers ST_* functions

parcels = sedona.read.format("geoparquet").load(PARCELS_PATH)
fields = sedona.read.format("geoparquet").load(FIELDS_PATH)

parcels.createOrReplaceTempView("parcels")
fields.createOrReplaceTempView("fields")

joined = sedona.sql("""
    SELECT p.parcel_id, f.field_id,
           ST_Area(ST_Transform(p.geometry, 'EPSG:4326', 'EPSG:31984')) AS area_m2
    FROM parcels p JOIN fields f
      ON ST_Intersects(p.geometry, f.geometry)
""")
```

Illustrative: verify API names, argument order and CRS syntax against the **pinned** Sedona version before use. Paths and CRS values come from configuration, not literals.

## 6. Anti-patterns

| Anti-pattern | Why it fails | Instead |
|--------------|--------------|---------|
| Python UDF per geometry | Serialization cost, no optimizer | Built-in `ST_*` |
| Join without early filter | Full cross-partition work | Filter or bound first |
| Area/distance in EPSG:4326 | Meaningless units | Projected CRS or geodesic method |
| `collect()` on large results | Driver OOM | Write to storage |
| Ignoring invalid geometries | Silent wrong joins | Validate and define policy |
| Unpinned Spark/Sedona/Java | Binary and API breakage | Pin and document matrix |

## 7. Testing

- Small fixture geometries with known topology (touching, overlapping, disjoint, invalid) and expected results.
- Run on a local Spark session; deterministic data, no network.
- Assert row counts, CRS, geometry validity and schema.
- Engine adapters must pass the shared contract tests (DT-IF-001 §10).

## 8. Dependencies

In the proposed baseline (DT-STK-001 §2, §9): `apache-sedona`, `geopandas`, `shapely`, `pyproj`, `pyarrow`.
Sedona has runtime compatibility constraints with Spark, Java and Scala: document the matrix in the PR. Anything outside the baseline (for example `pyspark` as an explicit pin, `sedona-db`, `geoparquet` helpers) needs the dependencies gate **and** human approval.

## 9. Done checklist (adds to `lattinus-code.md` §6.1 and §8)

- [ ] Sedona choice justified against lighter alternatives.
- [ ] CRS explicit; areas and distances in a suitable CRS.
- [ ] Geometry validity policy implemented and counted.
- [ ] Partitioning and skew assumptions stated; no unbounded `collect()`.
- [ ] Output in GeoParquet with CRS and schema metadata; lineage recorded.
- [ ] Spark/Sedona/Java/Scala versions pinned and documented.
- [ ] Job is idempotent and re-runnable; backfill procedure described.
- [ ] Source data licenses recorded.
- [ ] Dependency changes passed the gate.

## 10. Gates and traceability

Artifacts carry the header in `AGENTS.md` §10. Gates: `dependencies`, `git`, `documentation`, `safety`.

## 11. Open items (do not assume)

Interchange contract between Jaguar and Mirage, engine capability declaration, engine selection strategy and workflow runtime are open (DT-ARQ-001 §11). Declare them as assumptions or escalate.