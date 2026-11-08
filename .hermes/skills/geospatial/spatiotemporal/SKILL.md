---
name: spatiotemporal
description: Spatiotemporal data handling for LADE. Use whenever an artifact has a time dimension together with space: time series per pixel or feature, data cubes (Xarray/Zarr), acquisition vs processing time, time zones, temporal alignment, gap filling, compositing windows, temporal aggregation, or train/test splits on spatial-temporal data. Use it even if the task only says "monthly averages" or "build a time series for each field".
version: 0.1.0
owner: geospatial-engineer
---

# Spatiotemporal

> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Normative baseline: `references/lattinus-code.md` §8 (Temporal metadata, Catalog, Reproducibility, Quality checks). Depends on `crs`; works with `raster-processing` and `vector-processing`.

## When to use
- Time series from rasters or features.
- Data cubes (dimensions: time, y, x, band/variable).
- Temporal aggregation, resampling, compositing, interpolation.
- Joining datasets with different temporal resolutions.
- Evaluating models on spatiotemporal data.

## When not to use
- Storage layout, infra or scheduling → `data-engineering/*`, `infrastructure/*`.
- Sensor-specific masks and indices → `earth-observation`.
- Chunking strategy → `processing/dask-xarray` (this skill defines the semantics, that one the execution).

## Inputs required
1. Time field(s) and their meaning: acquisition, observation, processing, publication.
2. Time zone and timestamp format of each source.
3. Native temporal resolution and expected regularity (regular, irregular, gaps).
4. Target resolution, aggregation window and aggregation function.
5. Purpose: analysis, model training, visualization, cataloging.

## Procedure
1. **Inventory time fields.** For every dataset, identify and label each timestamp: `acquired_at` (when the phenomenon was observed), `processed_at` (when the product was generated), `published_at`. MUST use acquisition time for analysis unless the task says otherwise.
2. **Normalize to UTC.** Store and compute in UTC (timezone-aware). Convert to local time only at presentation, and state the zone. Treat naive timestamps as unknown, never as UTC silently; record the assumption.
3. **Declare temporal semantics.** Instant vs interval; interval convention (left-closed/right-open by default, state it); the reference for aggregates (start, end or midpoint of window).
4. **Validate the time axis.** Sorted, unique, no impossible dates, expected frequency; report gaps and duplicates with counts. Decide handling for duplicates (keep latest processed, aggregate, reject).
5. **Align datasets.** Define a target time grid. Match by nearest within a stated tolerance, or aggregate to the grid. MUST state tolerance and what happens beyond it (leave empty, never silently fill).
6. **Handle gaps explicitly.** Options: leave masked, interpolate (linear, seasonal), carry forward with maximum age. Declare the method and a maximum gap length. Keep a flag/mask of filled values. Derived values MUST remain distinguishable from observed ones.
7. **Aggregate with care.** State function (mean, median, max, sum), minimum valid-sample count per window, and how masked values (clouds, nodata) are excluded. A window with too few valid observations yields nodata, not a number.
8. **Build cubes with labeled dimensions.** Use Xarray with named dims and coordinates (`time`, `y`, `x`), CRS in attributes (via `crs`), units and nodata per variable. Store n-dimensional data as **Zarr** when persistence is needed (`lattinus-code.md` §3); chunk by access pattern (declare it; execution in `processing/dask-xarray`).
9. **Catalog.** When assets are cataloged, describe them as STAC Items/Collections with `datetime` (or `start_datetime`/`end_datetime`) in UTC.
10. **Split for modeling without leakage.** Split by time (train earlier, test later) and, when relevant, by space (hold out regions). MUST NOT split randomly across pixels or timestamps of the same field/scene. Apply any normalization or gap-filling fitted on the training period only.
11. **Reproducibility.** Pin time ranges as explicit ISO 8601 intervals in parameters; avoid "last 30 days" in committed code or record the resolved dates.
12. **Record provenance:** time range, resolution, alignment tolerance, gap method, aggregation function, sample thresholds.

## Checklist (see `lattinus-code.md` §8)
- [ ] Time zone declared (UTC by default).
- [ ] Acquisition vs processing time distinguished.
- [ ] Temporal resolution and interval convention declared.
- [ ] Alignment tolerance and gap-handling method declared.
- [ ] Filled values flagged; minimum valid samples per window set.
- [ ] No temporal leakage in splits or fitted transforms.
- [ ] Time ranges explicit and reproducible.

## Outputs
- Dataset or cube with labeled time coordinate (UTC) and per-variable metadata.
- Temporal quality summary: coverage, gaps, duplicates, fill ratio.
- Description of splits when used for modeling.
- Provenance record.

## Anti-patterns
- Mixing local and UTC timestamps, or naive and aware timestamps.
- Using processing time as acquisition time.
- Averaging windows with few valid observations without flagging them.
- Interpolating across long gaps and presenting the result as observation.
- Random train/test split on autocorrelated spatial-temporal data.
- Fitting scalers or fill values on the full period before splitting.
- Relative date ranges ("last month") baked into pipelines.
- Ignoring daylight-saving or zone offsets in local-time aggregates (e.g. "daily" in the wrong day).

## References
- `references/domain/geospatial.md`, `references/domain/earth-observation.md`, `references/domain/agriculture.md`
- `references/engineering/data.md`
- `references/lattinus-code.md` §3, §8
- Related skills: `crs`, `raster-processing`, `earth-observation`, `processing/dask-xarray`

## Escalate when
- Timestamp semantics (acquisition vs processing) or time zone cannot be determined from metadata.
- The required temporal resolution is finer than the sources support.
- A gap-handling choice materially affects results and the task does not define it.
- Leakage cannot be avoided with the data available.