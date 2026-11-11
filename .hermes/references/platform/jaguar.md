# jaguar.md — Jaguar Processing Engine (Raster / Data Cubes)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/platform/jaguar.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: Data Transformation architecture (2026-09-10), *Visão 360* L3/L4.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN`. Bootstrap; human-edited only.

## 1. Role

Internal engine of Data Transformation specialized in **matrix processing**: rasters, data cubes, temporal analysis, spectral indices. Not a public API: reached through the SDK and the Execution Planner. Engine choice for raster workloads (Dask + Xarray over RasterFrames) is `ACCEPTED`; the engine's formal documentation (Jaguar as component) is `PROPOSED`.

## 2. Technology

Dask, Xarray, Rasterio, Rioxarray, NumPy, Zarr `PROPOSED`. Also in Visão 360: xarray-spatial for analytics, PyroSAR (GPT/SNAP) for SAR preprocessing `ACCEPTED`. Why Dask over Spark for raster: lazy evaluation, smaller memory footprint, better raster integration. Spark/RasterFrames carry operational overhead not justified by Lattinus raster workloads. `ACCEPTED`

## 3. Responsibilities

Raster processing · data cubes · chunking · temporal analysis · spectral indices · band operations · distributed arrays · parallel computing.
Examples: NDVI, NDMI, SAVI, EVI, mosaics, resampling, reprojection, masks, time series.
Internal modules `PROPOSED`: `runtime`, `raster`, `datacube`, `temporal`, `dataframe`, `io`.

## 4. Route to Jaguar when

Continuous raster workloads: spectral indices, time series, n-D cubes. Vector joins at scale go to Mirage (`platform/mirage.md`). The criterion must be implemented in code, not tacit (`OQ-REF-006`).

## 5. Design rules for agents

1. Lazy by default. No full in-memory loads of unbounded data; declare chunking (`references/lattinus-code.md` §8).
2. Raster metadata declared on every output: CRS, resolution, extent, nodata, dtype, units, scale/offset, band semantics, resampling.
3. Outputs follow the Output Catalog: COG for 2D, Zarr for cubes.
4. Indices come from a catalog with declared formula and band mapping (Spyndex candidate, `domain/earth-observation.md` §6).
5. Deterministic: pinned versions, no hidden state, parameterized runs.
6. No engine-specific types in public interfaces (Dask arrays, Xarray objects) unless the interface contract explicitly allows it `PROPOSED`.

## 6. Gaps

`OQ-REF-018` SAR preprocessing placement · Jaguar interface contract (DT-IF) unread · performance targets per scene/AOI exist only as SLAs (`architecture.md` §6) · GPU acceleration `HYPOTHESIS`.
