# earth-observation.md — Earth Observation Domain Reference

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/domain/earth-observation.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: *Plataformas Orbitais*, *Visão 360 Técnico V1*, *Catálogo de Índices Espectrais (Spyndex)*, Data Ingestion V2.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` (established EO knowledge, not from Notion: **verify against provider docs before using in code**) · `OPEN`.
> Bootstrap content; human-edited only.

## 1. Sensor taxonomy used by Lattinus `ACCEPTED` (*Plataformas Orbitais*)

Orbital platforms are catalogued by sensing technology and by program:

| Group | Meaning |
|-------|---------|
| SAR | Synthetic Aperture Radar |
| MSI | Multispectral |
| HSI | Hyperspectral |
| LiDAR | Light Detection and Ranging |
| MWR | Microwave Radiometer |
| TIR | Thermal Infrared |
| GEO | Geostationary (meteorological) |
| ALT | Altimetry |
| Programs | Copernicus (ESA), JAXA, ISRO, NOAA, multi-platform |

Per-provider records live in Notion databases (`OQ-REF-017`, not read).

## 2. Sensors in scope

| Sensor / provider | Modality | In scope per | Notes |
|-------------------|----------|--------------|-------|
| Sentinel-2 | MSI optical | Ingestion V2 `PROPOSED`; Visão 360 | Phase 1 core |
| Sentinel-1 | C-band SAR | Visão 360 `ACCEPTED` | **Absent from Ingestion V2 provider list** (`OQ-REF-008`) |
| Landsat 8/9 | MSI + TIR | Ingestion V2 `PROPOSED`; Visão 360 | Thermal feeds LST |
| Planet | Commercial MSI | Ingestion V2; Visão 360 | Licence terms: record in PR |
| NASA SMAP | Soil moisture (radiometer) | Ingestion V2 `PROPOSED` | Coarse (km-scale) resolution `GENERAL` |
| ICEYE | Commercial SAR microsatellites | Ingestion V2 `PROPOSED` | |
| CBERS (INPE), Sentinel Hub, AWS Earth | Source/provider | Visão 360 L1 | Not in Ingestion V2 (`OQ-REF-008`) |
| Climate: NASA, INMET, local stations | Non-EO inputs | *O que é o Lattinus?* | ET, phytosanitary risk, water balance |
| IoT (humidity, pH, EC) | In-situ | Edge layer `HYPOTHESIS` | Future complement |

Reference facts `GENERAL` (verify mission status and product baselines before use):

- Sentinel-2: 13 bands at 10/20/60 m; revisit ≈ 5 days (constellation). L1C = top-of-atmosphere, L2A = surface reflectance with scene classification layer. Check the reflectance scale/offset in product metadata, which changed with processing baseline.
- Sentinel-1: C-band SAR, IW mode over land; products SLC (complex, phase preserved) and GRD (detected, ~10 m). Revisit depends on constellation status.
- Landsat 8/9: 30 m multispectral, 100 m thermal (distributed resampled), ≈ 8 days combined.

## 3. Processing levels and Medallion mapping

| Level (`GENERAL`) | Meaning | Lattinus tier `ACCEPTED` |
|-------------------|---------|--------------------------|
| L0/L1 | Raw / radiometrically-geometrically basic | Bronze |
| L2 | Surface-level (reflectance, backscatter calibrated) | Silver (ARD) |
| L3+ | Derived/composited/fused products | Gold |

Silver is **Analysis-Ready Data (ARD)**: calibrated, corrected, geometrically aligned, with QA flags. Modules: calibration/correction, geometric alignment, formatting, quality validation (*Visão 360* L3).

## 4. SAR

- **SLC vs GRD (critical).** SLC preserves signal phase, required for interferometry (InSAR/PSI, Phase 3). Phase **cannot be reconstructed from GRD**. Retention policy undecided: `OPEN` `OQ-REF-001` (ADR for storage layer). Agents must not drop SLC from an ingestion design silently.
- Wrapper: **PyroSAR** over GPT/SNAP, not Snappy. `ACCEPTED`
- Typical chain `GENERAL`: orbit file → thermal noise removal → radiometric calibration → speckle filtering → terrain correction → conversion to dB. Declare each step and parameter in lineage.
- Pitfalls `GENERAL`: layover/shadow in relief, incidence-angle dependence, dB averaging (average in linear, convert after), mixing orbit directions in time series without declaring it.
- SAR operates regardless of cloud cover; it complements optical in wet-season cloud. `ACCEPTED` (product rationale)

## 5. Optical

- Always apply a cloud/shadow mask and declare its source and thresholds (quality check required by `lattinus-code.md` §8).
- Never mix TOA and surface reflectance in one series. Record product level, processing baseline, scale and offset.
- Compositing and gap-filling method is a declared parameter, not a default.
- Cloud cover percentage is part of the ingestion gate (ADR-003) and of the Silver contract (`cloud_cover_pct`).

## 6. Spectral indices

- Catalog candidate: **Spyndex / Awesome Spectral Indices** (formulas, required bands, parameters, references; works on NumPy, Pandas, Xarray, Dask). `PROPOSED` ("potential internal use").
- Core set named by Lattinus docs: NDVI, EVI, GNDVI, SAVI (vigor); NDMI, LST, CWSI (water stress). Transformation catalog also lists NDWI-type, cloud mask, SAR calibration, terrain correction (`platform/transformation.md`).
- NDVI = (NIR − Red) / (NIR + Red). `GENERAL`
- Names are ambiguous across literature (e.g. NDMI vs NDWI variants). Use the **catalog short name and its band mapping**, and record which one in lineage.
- **Observation → index → interpretation.** The satellite gives observations; the index is a derived variable; agronomic or environmental interpretation depends on context and other evidence. Outputs must keep these three apart (see `domain/agriculture.md` §5).

## 7. Formats and catalog `ACCEPTED`

COG (2D raster), Zarr (n-D cubes), STAC (catalog), GeoParquet (vector). Details and CRS rules: `domain/geospatial.md` and `references/lattinus-code.md` §8. STAC extensions commonly used for EO/SAR/projection/raster metadata `GENERAL`.

## 8. Gaps

`OQ-REF-001` SLC retention · `OQ-REF-008` provider scope mismatch · `OQ-REF-017` provider databases unread · scaling factors, band maps and baselines per provider are **not recorded** in Notion: take from provider docs and register in the PR.
