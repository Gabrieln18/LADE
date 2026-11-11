# geospatial.md — Geospatial Domain Reference

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/domain/geospatial.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: *Visão 360 Técnico V1*, Data Transformation architecture.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` (established practice; verify codes and versions) · `OPEN`.
> **Scope split:** mandatory delivery rules (CRS, geometry, raster/temporal metadata, scale, provenance, accuracy) live in `references/lattinus-code.md` §8. This file adds Lattinus-specific context and does not repeat them. Bootstrap; human-edited only.

## 1. Reference CRS for the Vale AOI `GENERAL`

The Vale do São Francisco (Petrolina/Juazeiro area) falls in **UTM zone 24 South**. Verify codes against the EPSG registry when used.

| EPSG | Name | Use |
|------|------|-----|
| 4674 | SIRGAS 2000 (geographic) | Official Brazilian geodetic reference; storage of Brazilian vector data |
| 31984 | SIRGAS 2000 / UTM 24S | Metric analysis (areas, distances, buffers) over the Vale |
| 32724 | WGS 84 / UTM 24S | Native CRS of Sentinel-2 tiles over the area |
| 4326 | WGS 84 (geographic) | Interchange (GeoJSON, STAC bbox) |
| 5880 | SIRGAS 2000 / Brazil Polyconic | Multi-region/national work |

SIRGAS 2000 and WGS 84 agree at roughly metre level but are distinct datums: declare which one, never treat them as interchangeable silently (`lattinus-code.md` §8). Reprojection is a logged, justified operation; resampling method is a parameter (nearest for categorical, bilinear/cubic for continuous) `GENERAL`.

## 2. Data models and formats `ACCEPTED`

| Model | Format | Notes |
|-------|--------|-------|
| 2D raster | **COG** | HTTP-range access; internal tiling and overviews |
| N-D cube (x, y, time, band) | **Zarr** | Cloud-native chunking, parallel access |
| Vector | **GeoParquet** | Lattinus-code baseline; GeoJSON for interchange |
| Catalog | **STAC** (pystac, stac-fastapi) | Items/Collections for spatiotemporal assets |
| Lakehouse / versioning | Iceberg, DVC | `PROPOSED` (`OQ-REF-012`) |

## 3. Tool baseline

| Need | Tool | State |
|------|------|-------|
| Raster IO | rasterio, rioxarray | `ACCEPTED` (Jaguar) |
| N-D arrays, lazy compute | Xarray + Dask (+ xarray-spatial) | `ACCEPTED` |
| SAR preprocessing | PyroSAR (GPT/SNAP) | `ACCEPTED` |
| Vector small/medium | GeoPandas, Shapely | `PROPOSED` (Mirage) |
| Vector at scale | Apache Sedona | `ACCEPTED` as engine, deployment `OPEN` (`platform/mirage.md` §5) |
| Catalog | pystac, stac-fastapi | `ACCEPTED` |
| Raster tiles / serving | TiTiler, FastAPI, OGC (WMTS, WCS, Features) | `PROPOSED` (Serving) |
| Visualization | Deck.gl, Kepler.gl, PyDeck, QGIS Server | `PROPOSED` |
| Quality validation | Great Expectations / Pandera | `PROPOSED` |

## 4. Engine routing (summary)

Continuous raster workloads (indices, time series, cubes) → **Jaguar** (Dask + Xarray). Complex vector joins at scale (plot × sensor × time) → **Mirage** (Sedona). The criterion must be explicit in code, not in a developer's head (`OQ-REF-006`). See `platform/jaguar.md` and `platform/mirage.md`. Cross-engine flows (e.g. NDVI raster → zonal statistics per plot → GeoParquet) go through the Execution Planner.

## 5. Spatiotemporal conventions for Lattinus

- Plot identity is `talhao_id`; spatial joins to plots use the project's plot layer, whose schema is not yet documented (`TBD`).
- Time: UTC by default; keep acquisition time separate from processing time (`lattinus-code.md` §8). STAC `datetime` carries acquisition.
- Chunking: declare spatial × time chunks for cubes; align chunks with the COG/Zarr layout to avoid rechunking `GENERAL`.
- Zonal statistics: define the geometry (valid, in the raster's CRS or reprojected explicitly), the statistic, the nodata policy and the all-touched rule, and record them in lineage.

## 6. Common pitfalls `GENERAL`

| Pitfall | Guard |
|---------|-------|
| Area/distance in a geographic CRS | Use a projected CRS or geodesic method |
| Silent reprojection or resampling | Explicit, logged step |
| Nodata treated as a value | Declare nodata, mask before aggregation |
| Invalid geometries in joins | Validate/repair/quarantine before join |
| Loading unbounded rasters in memory | Lazy, chunked access |
| Axis-order confusion (lat/lon vs lon/lat) | Fix order at IO boundaries |
| Mixed time zones | UTC at the platform edge |

## 7. Gaps

Plot-layer schema, official boundaries source, and chunking defaults are not documented (`TBD`, collect when Transformation/Catalog docs are read: `OQ-REF-014`).
