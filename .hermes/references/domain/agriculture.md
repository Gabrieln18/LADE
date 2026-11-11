# agriculture.md — Agriculture Domain Reference

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/domain/agriculture.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Sources: *O que é o Lattinus? v1.0*, *Visão 360 Técnico V1*.
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` (not from Notion; validate with agronomists) · `OPEN`.
> Bootstrap content; human-edited only. Agents are engineers, not agronomists: see §5.

## 1. Operating context `ACCEPTED`

Vale do São Francisco: one of the most productive irrigated fruit regions in the world: ~220 thousand irrigable hectares, ~100 thousand direct jobs. High-value crops (mango and grape named in technical docs) exported to European and North American markets that require traceability, ESG certification and evidence of sustainable practice.

Problem: small and medium producers rely on visual inspection, disconnected spreadsheets and experience. Three barriers: **financial** (full precision-agriculture stack costs R$ 123–280 thousand, unviable under 50 ha), **operational** (GIS learning curve, manual integration), **analytical** (raw data creates no value without interpretation).

## 2. Capability → data → method

| Capability | Inputs | Method (tier) | Lead time / note |
|------------|--------|---------------|------------------|
| Vigor monitoring | MSI time series | Indices NDVI/EVI/GNDVI/SAVI (classical) | Per-plot low-performance zones |
| Water stress | MSI + TIR + climate | NDMI, LST, CWSI (classical) | Detects before visible symptoms |
| Pest/disease anomalies | MSI/SAR embeddings | Zero-shot with Clay embeddings | 48–72 h before visible symptoms |
| Crop phenology (mango, grape) | Time series | Fine-tuning Prithvi (PyTorch + TorchGeo) | Continuous, per cycle. Needs labels (Phase 2) |
| Yield prediction per plot | NDVI series + history | Classical, XGBoost | 30–60 days before harvest |
| Plot segmentation | MSI | Fine-tuned custom U-Net | Needs labels |
| Change detection | SAR bitemporal | Zero-shot, Clay difference embeddings | 6-day detection (S1 cycle, verify constellation) |
| Variable-rate spraying | Anomaly maps | VRA maps compatible with drones/variable-rate equipment | Product |
| Irrigation optimization | ETc, climate, phenological stage | Depth recommendation per crop and stage | Product |

All rows `PROPOSED` as engineering designs; capabilities themselves `ACCEPTED` (product). Modes: zero-shot, supervised fine-tuning, classical/derived indices. Foundation models: Clay (S1+S2+Landsat, SAR-optical fusion, weaker temporal) and Prithvi (HLS temporal, no native SAR).

## 3. Operational constraints

- **24 h end-to-end alert SLA.** Pests act in 48–72 h windows: a 25 h alert is still useful, a 72 h alert is not. `ACCEPTED`
- Delivery by persona (`ACCEPTED`, Visão 360 L7): family farmer: simplified PDF + contact via Genesis agent; small/medium producer: dashboard + report; fruit company: advanced dashboard + API; Genesis analyst: processing-layer access.
- Plot identity: `talhao_id` is a mandatory field from Silver onward (`architecture.md` §6).

## 4. Learning loop and ground truth `OPEN`

Real harvest data should feed continuous calibration. The collection pipeline (who annotates, format, latency) does not exist and is a **Phase 1 engineering deliverable**, defined together with Genesis agents (`OQ-REF-005`). Fine-tuning for Vale crops depends on it. Experiment tracking tool undecided (`OQ-REF-003`).

## 5. Rules for agents

1. Keep three levels apart in every output: **observation** (sensor), **derived variable** (index/model output), **agronomic interpretation**. Never present an index value as a diagnosis.
2. Recommendations to producers (spray, irrigation, nutrients) are issued by Genesis agents/agronomists, not by LADE artifacts. Code may produce candidate maps, with `confidence_score`, `model_version` and limits declared.
3. Do not invent agronomic parameters (crop coefficients, phenological thresholds, index cut-offs). None are recorded in Notion. Use a declared assumption and flag `TBD` for domain validation.
4. State resolution limits: small plots, perennial tree rows and mixed pixels at 10–30 m can bias indices `GENERAL`.
5. Keep per-client data isolated; LGPD applies to producer data (`architecture.md` §7, L9).

## 6. Social vertical `PROPOSED`

Same technology for food- and water-vulnerable communities; pilot in the Brazilian semi-arid in Phase 2, later Africa. Validates the model under minimal resources, so designs should degrade gracefully (low bandwidth, simple reports).

## 7. Gaps

Crop-specific parameters, phenological calendars, validated thresholds, and the client-data schema are **not documented**: do not assume. `OQ-REF-005`, `OQ-REF-003`, `OQ-REF-011`.
