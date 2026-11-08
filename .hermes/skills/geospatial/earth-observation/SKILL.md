---
name: earth-observation
description: Earth Observation (EO) satellite data handling for LADE. Use whenever an artifact uses optical or radar satellite imagery or derived products: sensor and product-level selection, cloud/shadow masking, surface reflectance, spectral indices (NDVI, EVI, NDWI etc.), composites, STAC search and cataloging, or uncertainty of derived values. Use it even if the task only says "get NDVI for these fields" or "find Sentinel images for this area".
version: 0.1.0
owner: geospatial-engineer
---

# Earth Observation

> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Normative baseline: `references/lattinus-code.md` §8 (Raster metadata, Catalog, Provenance, Quality checks, Accuracy, Licensing). Depends on `crs`, `raster-processing`, `spatiotemporal`.
> Sensor and platform facts specific to Lattinus (data sources, Jaguar, Mirage) are `TBD` until `references/platform/` confirms them. Agents MUST NOT assume them.

## When to use
- Selecting EO products for an area and period.
- Masking clouds, shadows, snow, water or invalid pixels.
- Computing spectral indices or other derived variables.
- Building composites or per-field/pixel time series from imagery.
- Searching or publishing assets via STAC.

## When not to use
- Generic raster operations → `raster-processing`.
- Time alignment, gap filling, splits → `spatiotemporal`.
- Lattinus platform behavior → `references/platform/*` (read, do not infer).

## Inputs required
1. Area of interest (geometry + CRS) and period (explicit ISO 8601 interval).
2. Target variable or index and the intended use (monitoring, classification, reporting).
3. Required spatial and temporal resolution, and tolerance for cloud contamination.
4. Preferred sensor/collection, or authority to choose and justify.
5. Data source (catalog, bucket, API) and its access/licensing terms. If unconfirmed, `TBD`.

## Procedure
1. **Select product and processing level.** Prefer **surface reflectance** (atmospherically corrected, e.g. L2A-type products) for indices and time series. Use top-of-atmosphere only with justification. State sensor, collection, product level and version/processing baseline.
2. **Search via STAC** when available: filter by area, interval, collection and cloud metadata; record query parameters and the number of items returned. Treat search metadata (e.g. cloud %) as a coarse filter, not as a per-pixel mask.
3. **Check product metadata, never assume.** Read scale factor, offset, nodata, band names, resolution per band and units from the product's metadata. Values differ across collections and processing baselines. Apply scale/offset before computing (via `raster-processing`).
4. **Mask invalid pixels.** Use the product's quality layer (scene classification, QA band or equivalent) to exclude cloud, cloud shadow, cirrus, snow/ice and saturated or no-data pixels as the task requires. Declare which classes are excluded and any buffer/dilation applied. Report the valid-pixel fraction.
5. **Harmonize inputs.** Co-register bands of different native resolutions to a declared reference grid with a resampling method (via `raster-processing`). Mixing sensors requires stating band correspondence and known radiometric differences.
6. **Compute indices from physical values.** Write the formula in the artifact (e.g. NDVI = (NIR − Red) / (NIR + Red)); name the exact bands per sensor; guard against division by zero; restrict to the valid range; mask results from invalid inputs. Do not carry a formula between sensors without mapping bands.
7. **Composite and aggregate** through `spatiotemporal`: state the window, selection rule (median, max-value, best-pixel) and minimum valid observations. A composite pixel with insufficient valid data is nodata.
8. **Quality checks with declared thresholds:** valid-pixel fraction per scene/period, outliers and implausible index values, spatial and temporal completeness. Define the behavior on failure (skip scene, flag, fail the job).
9. **Catalog outputs** as STAC Items/Collections: datetime (UTC), geometry, `proj` metadata, band/asset descriptions, processing parameters; prefer COG (rasters) and Zarr (cubes).
10. **State uncertainty.** Note sensor resolution vs field/feature size (mixed pixels), residual cloud/shadow, atmospheric-correction limits and the interpolation used. Do not present derived values with more precision than the sources support, and do not describe results as validated without ground reference.
11. **Record provenance and licensing:** collection, item ids, versions, retrieval date, processing steps, parameters; data license and required attribution.

## Checklist (see `lattinus-code.md` §8)
- [ ] Sensor, collection, level and version stated.
- [ ] Scale/offset/nodata read from metadata and applied.
- [ ] Mask classes, buffers and valid-pixel fraction declared.
- [ ] Index formula and band mapping written out per sensor.
- [ ] Composite rule and minimum-observation threshold declared.
- [ ] Quality thresholds and failure behavior defined.
- [ ] STAC metadata complete when cataloged.
- [ ] Uncertainty, license and attribution recorded.

## Outputs
- Derived raster, cube or table with full metadata.
- Product selection record (query, items, versions).
- Quality report: valid fraction, coverage, outliers.
- Uncertainty statement and provenance record.

## Anti-patterns
- Computing indices on raw digital numbers or on top-of-atmosphere values without saying so.
- Hardcoding scale/offset or band names from memory across collections.
- Relying only on scene-level cloud percentage instead of a pixel mask.
- Applying the same formula to different sensors without band mapping.
- Averaging masked and unmasked values, or compositing without a minimum-sample rule.
- Mixing processing baselines in one time series without checking for step changes.
- Treating index values as ground truth (e.g. "NDVI = crop health") without validation.
- Using pixels much coarser than the target feature without stating mixed-pixel risk.

## References
- `references/domain/earth-observation.md`, `references/domain/agriculture.md`, `references/domain/geospatial.md`
- `references/platform/ingestion.md`, `references/platform/jaguar.md`, `references/platform/mirage.md` (`TBD` content)
- `references/lattinus-code.md` §3, §8
- Related skills: `crs`, `raster-processing`, `spatiotemporal`, `processing/dask-xarray`

## Escalate when
- The required sensor/product or data source is not confirmed in `references/` and no safe assumption exists.
- Valid-pixel coverage is below the declared threshold for the period or area.
- Product metadata is missing or contradicts the documentation.
- The task asks for accuracy claims (yield, health, area) that need ground-truth validation not available.
- Data license or attribution terms are unknown.