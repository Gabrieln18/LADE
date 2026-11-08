---
name: crs
description: Coordinate reference systems for LADE geospatial work. Use whenever an artifact reads, writes, compares, reprojects or measures spatial data, or whenever a dataset's CRS, EPSG code, datum, axis order, units, area, distance, buffer or projection is mentioned or unclear. Use it even when the task does not mention CRS explicitly but combines two spatial datasets.
version: 0.1.0
owner: geospatial-engineer
---

# CRS

> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Normative baseline: `references/lattinus-code.md` §8 (CRS row). This skill adds the procedure, not new rules.

## When to use
- Any dataset enters or leaves a pipeline.
- Two or more spatial datasets are joined, overlaid or compared.
- Area, length, distance, buffer or density is computed.
- A CRS is missing, ambiguous or mismatched.

## When not to use
- File format, validity or topology questions → `vector-processing`, `raster-processing`.
- Timestamps and time zones → `spatiotemporal`.

## Inputs required
Verify, or ask (grouped, few questions, SOUL §5):
1. Declared CRS of each input (EPSG code, not a name or a WKT guess).
2. Region of interest (drives projected CRS choice).
3. Purpose: measurement (area/distance), display, storage or exchange.
4. Expected accuracy and whether datum transformation matters.

## Procedure
1. **Read the CRS from the data.** Never assume. If absent, stop: record the gap in `memory/open-questions.md` and proceed only with a declared assumption, or escalate.
2. **Normalize to an EPSG code** (`pyproj.CRS.from_user_input(...).to_epsg()`). If no EPSG match exists, keep the full WKT2 and state why.
3. **Check axis order.** Authority order for EPSG:4326 is lat/lon. Use `always_xy=True` in `pyproj.Transformer` so code uses lon/lat consistently.
4. **Choose the CRS by purpose:**

| Purpose | CRS choice |
|---------|-----------|
| Storage / exchange | Keep the source CRS, or a geographic CRS declared in the ADR. GeoParquet and COG record it. |
| Area, density | Equal-area projected CRS suited to the region. |
| Distance, buffer | Local projected CRS (e.g. UTM zone) or geodesic method (`pyproj.Geod`). |
| Web display only | EPSG:3857. MUST NOT be used for measurement. |

5. **Select the UTM zone by computation, not memory.** Derive it with `pyproj.database.query_utm_crs_info` for the area of interest and the datum in use. For regions spanning several zones, use an equal-area CRS or geodesic method instead of one zone.
6. **Reproject explicitly and once.** One named step, with source CRS, target CRS and justification logged. MUST NOT reproject repeatedly back and forth (accumulated error, wasted compute).
7. **Mind the datum.** If a transformation involves a datum shift (e.g. SAD69 → SIRGAS 2000), identify the pipeline used (`Transformer.from_crs(...).description`) and record it. Do not accept a silent default.
8. **Handle special geometry cases:** antimeridian crossing, polar areas, and datasets larger than one projected zone. Prefer geodesic computation.
9. **Validate after reprojection:** bounds are plausible for the region, no `inf`/`NaN` coordinates, row counts unchanged.

## Brazil context (default for national data)
- Reference geographic CRS: **SIRGAS 2000, EPSG:4674**. It is the official geodetic datum in Brazil; EPSG:4326 is acceptable only when the source or consumer requires it, and the choice is stated.
- SIRGAS 2000 UTM zone codes: derive with step 5 and confirm by `CRS.from_epsg(code).name`. Do not hardcode from memory.
- Brazilian equal-area options (e.g. an Albers variant for national statistics): `TBD`, confirm in `references/domain/geospatial.md`.

## Checklist (see `lattinus-code.md` §8)
- [ ] Every dataset states its EPSG.
- [ ] Reprojection is explicit, logged and justified.
- [ ] No silent WGS84 assumption.
- [ ] Area and distance use a projected CRS or geodesic method.
- [ ] Axis order handled (`always_xy=True`).
- [ ] Datum transformation recorded where applicable.

## Outputs
- CRS table in the artifact or PR: dataset, source EPSG, target EPSG, reason.
- Transformation pipeline description when a datum shift occurred.
- Declared assumptions in the traceability header.

## Anti-patterns
- Computing area or buffers in degrees (EPSG:4326/4674).
- Computing area in EPSG:3857.
- Overwriting a CRS with `set_crs(..., allow_override=True)` to "make it work" instead of reprojecting.
- Swapped lat/lon from axis-order confusion.
- Joining datasets without comparing CRS first.
- Using one UTM zone for data spanning several zones.
- Hardcoding EPSG codes recalled from memory.

## References
- `references/domain/geospatial.md`
- `references/engineering/python.md`
- `references/lattinus-code.md` §8

## Escalate when
- The CRS of a source is missing and cannot be inferred from metadata or provenance.
- Reprojection changes values materially for the task's accuracy needs.
- The datum transformation has several candidate pipelines with different results.
- The target CRS choice affects a data contract or public API (ADR required).