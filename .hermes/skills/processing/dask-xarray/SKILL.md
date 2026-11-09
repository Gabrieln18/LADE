---
name: dask-xarray
description: Design, implement or review raster, n-dimensional array, time-series and data-cube computation with Dask + Xarray (the Jaguar engine of Lattinus). Use whenever a task involves xarray, dask, raster stacks, spectral indices (NDVI etc.), cloud/nodata masking, temporal composites, chunking, rechunking, Zarr/COG output or out-of-core computation, even if "Jaguar" is not mentioned. Do NOT use for vector or spatial-join workloads (use apache-sedona) or for designing SDK contracts (use processing-sdk).
metadata:
  version: 0.1.0
  date: 2026-11-09
  status: draft
  agents: [geospatial-engineer]
  sources: [DT-STK-001, DT-ARQ-001, DT-IF-001, references/lattinus-code.md §8]
---

# dask-xarray (Jaguar)

## 1. Scope

Jaguar = **Dask + Xarray**, specialized in raster, arrays, time series and data cubes (DT-STK-001 §3).
Code written with this skill is **engine-internal**: it lives behind an engine adapter. Dask and Xarray types MUST NOT leak into SDK public contracts (DT-IF-001 §7). For contract work, switch to `processing-sdk`.

## 2. Load on demand (declared in manifest)

`references/platform/jaguar.md`, `references/domain/earth-observation.md`, `references/domain/geospatial.md`, `references/engineering/python.md`, `references/engineering/data.md`, `references/lattinus-code.md` §8.
If one is missing or outdated: say so in the artifact, append to `memory/open-questions.md`, proceed only with declared assumptions.

## 3. Procedure

1. **Declare the data contract before coding**: CRS (EPSG), resolution, extent, nodata, dtype, units, scale/offset, band semantics, time zone (UTC default), temporal resolution.
2. **Declare chunking**: chunk shape, rationale, estimated memory per chunk and per worker. Align spatial chunks with storage tiling (COG tiles / Zarr chunks). Chunk time contiguously when access is per-pixel time series. Start near ~128 MiB per chunk as a heuristic and adjust by measurement.
3. **Stay lazy.** No `.compute()`, `.values` or `.load()` inside functions or loops. One compute at the boundary. Use `.persist()` only for reused intermediates that fit in memory.
4. **Prefer labeled operations** (`sel`, `where`, `resample`, `groupby`, `rolling`). For custom logic use `xr.apply_ufunc(..., dask="parallelized", output_dtypes=[...])` or `map_blocks` with an explicit `template`. For neighborhood ops use `map_overlap` with an explicit `depth`.
5. **Masks and nodata are explicit**: apply with `where`, keep a valid-pixel count, state the composite method (median, max-NDVI, etc.) and its thresholds.
6. **Reprojection and resampling are explicit and logged.** Resampling by semantics: categorical/QA bands → nearest; continuous → bilinear or as justified.
7. **Spectral indices**: use the project catalog (Notion: *Catálogo de Índices Espectrais (Spyndex)*) instead of hand-written formulas. Cite the index and formula source.
8. **Write chunk-aligned output** (Zarr or COG) with metadata attrs (CRS, nodata, units, scale/offset) and emit a lineage record: source dataset, version, retrieval date, steps, parameters.
9. **Scheduler is injected configuration**, never hard-coded. Local `distributed.Client` for development only.

## 4. Minimal pattern

```python
import xarray as xr

def ndvi(nir: xr.DataArray, red: xr.DataArray) -> xr.DataArray:
    """Lazy NDVI. Zero-denominator pixels become NaN. Inputs must share CRS/grid."""
    denom = nir + red
    out = ((nir - red) / denom).where(denom != 0)
    return out.astype("float32").rename("ndvi")
```

Illustrative: verify band scaling and nodata against the source collection before use.

## 5. Anti-patterns

| Anti-pattern | Why it fails | Instead |
|--------------|--------------|---------|
| `.compute()` in a loop | Re-executes graph, loses parallelism | Build the graph, compute once |
| Tiny chunks (graph explosion) | Scheduler overhead dominates | Merge chunks; measure |
| Chunks misaligned with storage | Redundant reads | Align to tiles/Zarr chunks |
| Rechunk/groupby on misaligned dims without need | Shuffle, memory spikes | Plan dims and chunks up front |
| Silent CRS assumption | Wrong area/distance | Declare and check EPSG |
| Full in-memory load of unbounded data | OOM | Stay chunked |
| Dask/Xarray types in public signatures | Couples SDK to engine | Adapter + contract types |

## 6. Testing

- Small synthetic `DataArray` with known expected results; assert values, dtype, shape, dims, CRS/nodata attrs.
- Run with `dask.config.set(scheduler="synchronous")` for determinism; assert laziness (`isinstance(result.data, dask.array.Array)`) where relevant.
- Float comparisons with explicit tolerance. No network, no wall-clock dependence.
- Engine adapters must pass the shared contract tests (DT-IF-001 §10).

## 7. Dependencies

In the proposed baseline (DT-STK-001 §2, §9): `dask`, `distributed`, `xarray`, `rasterio`, `pyproj`, `pyarrow`.
**Not in baseline**, so they need the dependencies gate **and** human approval before use: `zarr`, `rioxarray`, `stackstac`/`odc-stac`, `dask-geopandas`, `numba`, `spyndex`. Note: Zarr is the preferred n-dimensional format in `lattinus-code.md` §3, but its package is not yet in the baseline: raise it as a proposal.
Pin GDAL/PROJ-sensitive packages when binary compatibility requires it.

## 8. Done checklist (adds to `lattinus-code.md` §6.1 and §8)

- [ ] Data contract declared (CRS, resolution, nodata, dtype, units, time).
- [ ] Chunking declared with memory estimate.
- [ ] No eager compute in library code; laziness tested.
- [ ] Resampling and reprojection logged and justified.
- [ ] Output carries metadata and lineage; reproducible (pinned versions, seeded randomness).
- [ ] Accuracy limits stated (resolution, sensor, interpolation).
- [ ] Source data licenses and attribution recorded.
- [ ] Dependency changes passed the gate.

## 9. Gates and traceability

Artifacts carry the header in `AGENTS.md` §10. Gates: `dependencies` (any package change), `git` (commit/PR), `documentation` (behavior change), `safety` (any destructive or external action).

## 10. Open items (do not assume)

Interchange contract between engines, engine capability declaration, engine selection strategy and workflow runtime are open (DT-ARQ-001 §11). Declare them as assumptions or escalate.