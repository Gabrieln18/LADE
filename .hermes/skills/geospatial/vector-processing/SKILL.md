---
name: vector-processing
description: Vector geospatial processing for LADE (points, lines, polygons). Use whenever an artifact reads, validates, cleans, simplifies, overlays, dissolves, joins or stores vector data, including shapefiles, GeoJSON, GeoPackage and GeoParquet, or when geometry validity, topology, spatial joins or invalid-geometry handling come up. Use it even if the task only says "clean this parcel layer" or "join points to polygons".
version: 0.1.0
owner: geospatial-engineer
---

# Vector Processing

> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Normative baseline: `references/lattinus-code.md` §8 (geometry validity, formats, provenance). Depends on `crs`.

## When to use
- Reading, writing or converting vector formats.
- Validating or repairing geometries.
- Overlay, clip, dissolve, buffer, simplify, spatial join, nearest-neighbor.
- Designing a vector schema or GeoParquet output.

## When not to use
- CRS decisions → `crs` (apply it first).
- Partitioning of very large vector data → `processing/apache-sedona`.
- Raster ↔ vector conversion details beyond the handoff → `raster-processing`.

## Inputs required
1. Source format, CRS (via `crs`), geometry type expected, approximate feature count.
2. Attribute schema and primary key (or how to create one).
3. Policy for invalid or empty geometries: **repair**, **reject** or **quarantine**.
4. Output format and consumer.

## Procedure
1. **Inspect.** Record: CRS, geometry types present, feature count, null/empty count, bounds, attribute dtypes.
2. **Apply `crs`.** Confirm CRS before any measurement or join.
3. **Validate geometries.** Check `is_valid`, `is_empty`, expected type (including mixed Multi*/single types) and coordinate sanity (no NaN/inf).
4. **Apply the invalid-geometry policy** declared in the task:
   - *Repair:* `shapely.make_valid`, then re-check type (repair can change type, e.g. polygon → collection). Log count repaired.
   - *Reject:* fail fast with counts and sample ids.
   - *Quarantine:* write invalid features to a separate output with a reason column; continue with the valid ones. Log counts.
   Silent dropping MUST NOT happen.
5. **Keep a stable key.** Preserve or create a unique feature id before transformations so outputs trace back to inputs.
6. **Process with intent:**
   - Spatial joins: state the predicate (`intersects`, `within`, `contains`, `nearest`), the CRS used and how multiple matches are resolved (first, aggregate, keep all). Use spatial indexing (`sindex`/STRtree).
   - Measurements: only in a suitable projected CRS or by geodesic method.
   - Simplification: state tolerance and units; preserve topology when polygons share borders (`preserve_topology=True`) and verify afterwards.
   - Buffers: state units and CRS; mind self-intersections.
   - Overlays: check for slivers and tiny gaps after union/intersection; define a minimum-area threshold if cleanup is needed.
7. **Re-validate** after any geometry-modifying operation.
8. **Write output.** Prefer **GeoParquet** for analytical/cloud storage. Use GeoPackage or GeoJSON for exchange when required. Shapefile only when a consumer demands it (field-name limit of 10 characters, 2 GB limit, no null-safe types). Record the CRS in the output and justify any deviation (`lattinus-code.md` §8, Formats).
9. **Record provenance.** Source dataset, version, retrieval date, steps, parameters, tolerances, row counts before and after.

## Checklist (see `lattinus-code.md` §8)
- [ ] Geometries validated (valid, non-empty, expected type).
- [ ] Invalid-geometry behavior defined and logged.
- [ ] CRS declared on input and output.
- [ ] Join predicate and multi-match rule stated.
- [ ] Row counts reconciled (in, out, quarantined, rejected).
- [ ] Output format justified if not GeoParquet.
- [ ] Source license and attribution recorded.

## Outputs
- Processed vector file(s) with CRS embedded.
- Quality summary: counts (total, valid, repaired, quarantined, rejected), geometry types, bounds.
- Quarantine file when applicable.
- Provenance record.

## Anti-patterns
- Dropping invalid geometries without logging.
- `buffer(0)` as a blanket "fix" (can erase or distort geometry); prefer `make_valid` and inspect.
- Joining or measuring before checking CRS.
- Nested-loop spatial joins instead of an index.
- Simplifying shared borders independently, creating gaps and overlaps.
- Assuming a single geometry type in a layer.
- Using shapefile as an internal storage format.
- Losing the feature id during dissolve or explode.

## References
- `references/domain/geospatial.md`
- `references/engineering/python.md`, `references/engineering/data.md`
- `references/lattinus-code.md` §8
- Related skills: `crs`, `processing/apache-sedona`

## Escalate when
- The share of invalid geometries is high enough to question the source (threshold `TBD` per dataset).
- Repair changes geometry type or area beyond the tolerance the task allows.
- The task needs a topology rule not covered here (e.g. network connectivity, cadastral consistency).
- Dataset size makes in-memory processing unsafe (hand over to `processing/apache-sedona` via the Orchestrator).