---
name: raster-processing
description: Raster geospatial processing for LADE (GeoTIFF, COG, NetCDF, Zarr-backed rasters). Use whenever an artifact reads, writes, resamples, reprojects, masks, clips, mosaics, windows or computes on raster data, or whenever nodata, dtype, resolution, extent, scale/offset, band semantics or COG come up. Use it even if the task only says "calculate X from this image" or "clip this raster to the polygon".
version: 0.1.0
owner: geospatial-engineer
---

# Raster Processing

> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Normative baseline: `references/lattinus-code.md` §8 (Raster metadata, Formats, Scale, Accuracy). Depends on `crs`.

## When to use
- Reading, writing or converting raster files.
- Resampling, reprojecting, aligning, clipping, mosaicking, masking.
- Band math on a single or co-registered rasters.
- Producing Cloud Optimized GeoTIFFs.

## When not to use
- CRS selection → `crs` (apply first).
- Chunked, lazy or multi-scene computation → `processing/dask-xarray`.
- Sensor-specific logic, cloud masks, spectral indices → `earth-observation`.
- Time dimension handling → `spatiotemporal`.

## Inputs required
1. CRS, resolution, extent, dtype, nodata, band count and meaning (read from the file, not assumed).
2. Units and scale/offset (e.g. stored integers vs physical values).
3. Data nature: **continuous** (reflectance, elevation) or **categorical** (land cover, masks). This drives resampling.
4. File size and whether it fits in memory.
5. Output format and consumer.

## Procedure
1. **Inspect metadata** (`rasterio.open(...).profile` and tags): CRS, transform, resolution, extent, dtype, nodata, band descriptions, scale/offset, compression, tiling, overviews. Record it.
2. **Apply `crs`** for any reprojection or mixed-CRS operation.
3. **Resolve nodata explicitly.** Identify the nodata value; use masked arrays or `NaN` (float) consistently. MUST NOT let nodata values enter statistics or band math. Check that the output declares nodata.
4. **Apply scale/offset before computing** with physical values; declare units after.
5. **Choose resampling by data nature:**

| Data | Methods | Avoid |
|------|---------|-------|
| Categorical | `nearest`, `mode` | `bilinear`, `cubic`, `average` (creates invalid classes) |
| Continuous, downsample | `average`, `bilinear`, `cubic` (state which) | `nearest` unless justified |
| Continuous, upsample | `bilinear`, `cubic` | claiming added information |

6. **Align before combining.** Rasters used together MUST share CRS, resolution, extent/grid and alignment. Define the reference grid and reproject/resample the others to it, explicitly.
7. **Control dtype.** Choose a dtype that holds the value range and nodata (e.g. avoid uint8 with a nodata of 0 that collides with valid values). Watch integer overflow in band math; cast first.
8. **Clip and mask:** state whether the clip uses the geometry bounds or the exact shape, how edge pixels are treated (`all_touched`), and the CRS of the geometry (must match the raster, via `crs`).
9. **Read by window** for large files. MUST NOT load unbounded data fully into memory. Declare memory assumptions. If the data exceeds a single worker, hand over to `processing/dask-xarray`.
10. **Write output as COG** unless justified otherwise: internal tiling, compression (state codec and predictor), overviews with resampling suited to data nature, nodata, CRS, and band descriptions. Validate the COG (e.g. `rio cogeo validate`).
11. **Record provenance.** Source file and version, steps, resampling method, parameters, software versions.

## Checklist (see `lattinus-code.md` §8)
- [ ] Resolution, extent, nodata, dtype, units, scale/offset, band semantics and resampling declared.
- [ ] Nodata excluded from computations and declared on output.
- [ ] Resampling matches data nature.
- [ ] Inputs aligned to a defined reference grid.
- [ ] No unbounded in-memory load.
- [ ] Output is a valid COG (or deviation justified).
- [ ] Precision of derived values does not exceed what the sources support.

## Outputs
- Raster output(s) with full metadata.
- Metadata table: input vs output (CRS, resolution, extent, dtype, nodata, units).
- COG validation result.
- Provenance record.

## Anti-patterns
- Bilinear or cubic resampling on categorical rasters.
- Treating nodata (e.g. `-9999`, `0`, `65535`) as data.
- Band math on integers without applying scale/offset or without casting (overflow, truncation).
- Combining rasters that differ slightly in grid or alignment.
- Reprojecting repeatedly, or resampling twice in sequence.
- Writing uncompressed, untiled GeoTIFF for cloud use.
- Storing float64 when float32 or scaled int suffices, without reason.
- Reporting derived values with false precision.

## References
- `references/domain/geospatial.md`, `references/domain/earth-observation.md`
- `references/engineering/python.md`, `references/engineering/data.md`
- `references/lattinus-code.md` §8
- Related skills: `crs`, `earth-observation`, `processing/dask-xarray`

## Escalate when
- Nodata, scale/offset or units are missing or contradictory in the source metadata.
- Source grids cannot be aligned without material information loss.
- Output size or memory needs exceed the declared assumption.
- The required output format deviates from COG without an agreed reason.