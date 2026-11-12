# evals/fixtures/

> **Version:** 0.1.0 · **Date:** 2026-11-12 · Humans write. Sample data referenced by `evals/golden-tasks/`.
> Fixtures are small, synthetic and contain no secrets or personal data. Coordinates are near Petrolina/Juazeiro (SIRGAS 2000 / UTM 24S region) but the parcels are invented.

| Fixture | Used by | Notes |
|---------|---------|-------|
| `data/samples/parcels.geojson` | GT-GEO-001 | EPSG:4326, lon/lat. P001 is a ~100 m × 100 m square (≈ 1 ha: **approximate**, compute the geodesic reference before using it as an expected value). P003 is a self-intersecting "bowtie" (invalid on purpose) |
| `data/samples/stations_2026-11-10.csv` | GT-DATA-001, GT-WF-BUG-001 | Columns `station_id, ts_utc, temp_c, rain_mm`. Contains one duplicate row and one null `station_id` on purpose |
| `fields.shp` without `.prj` | GT-GEO-002 | **Not included** (binary). Create it once from `parcels.geojson` and delete the `.prj`; keep it out of any CRS metadata |
| `stac_collection.json`, `src/lade/*`, `loader.py`, `legacy_export.py`, `requirements.txt`, `k8s/deployment.yaml` | GT-AI-001, GT-SWE-*, GT-DATA-002, GT-DEVOPS-002 | **Not included**: create a throwaway sandbox repo (`lade-eval-sandbox`) with these files before the baseline run |

Isolation (see `evals/README.md` §4 patch in `PATCHES.md`): the agent under test runs in a checkout **without** `evals/golden-tasks/`; fixtures are copied into the sandbox, never the checks.
