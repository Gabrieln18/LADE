# lattinus.md — Lattinus Context (Snapshot)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/lattinus.md`
> **Snapshot:** Notion Lattinus read on **2026-11-10** (root page last edited 2026-11-05). Source: <https://app.notion.com/p/Lattinus-2f673eebda2f80d7973fc08ef9558a2e>
> Evidence tags: `ACCEPTED` recorded decision · `PROPOSED` documented, awaiting approval · `HYPOTHESIS` explicitly planning-stage · `LEGACY` archived, evidence only · `GENERAL` established domain knowledge not from Notion (verify before coding) · `OPEN` unresolved (see `OQ-REF-NNN`).
> Bootstrap content. Only humans edit this file (`AGENTS.md` §11). Re-snapshot when Notion changes in a way that affects delivery.

## 1. What Lattinus is

Geospatial intelligence platform by **Genesis Corp.** that processes Earth Observation (EO) data at scale (multispectral, SAR, time series, climate, later IoT) into actionable agricultural intelligence. Initial focus: irrigated fruit growing in the **Vale do São Francisco** (Brazil). Operated as a service (contract licence + integrated consultancy). It is a **processing system** (ingestion → transformation → analysis → delivery), not a visualization tool or an image repository. `ACCEPTED` (*O que é o Lattinus? v1.0*)

## 2. Terminology (avoid collisions)

| Term | Meaning |
|------|---------|
| Lattinus | The platform |
| Lattinus Code | The code base that receives LADE deliveries (`references/lattinus-code.md`) |
| LADE / Hermes | This agent environment (`.hermes/`). Produces artifacts, does not run the platform |
| Genesis Corp. / Genesis Systems Department | Owner company / owner of technical docs |
| **Genesis agents** | Corporate consultants/agents that turn analytics into agronomic recommendations. **Not LADE agents** |
| Module / layer | Platform component. Current taxonomy in `architecture.md` §2 |
| Bronze / Silver / Gold | Medallion data tiers (`architecture.md` §3) |
| Jaguar / Mirage | Internal processing engines: raster-cube / spatial-vector (`platform/jaguar.md`, `platform/mirage.md`) |

## 3. Purpose as tiebreaker

Purpose: make high-performance geospatial intelligence accessible to producers without scale to build it, creating measurable economic value (commercial vertical) and social impact (social vertical: access for food- and water-vulnerable communities). When a product, architecture or commercial choice conflicts with the purpose, **the purpose breaks the tie**. `ACCEPTED`

## 4. Users

| Persona | Needs | Implication for engineering |
|---------|-------|-----------------------------|
| Producer in digitalization (primary) | Quantified basis for decisions, yield predictability, practical recommendations, no technical expertise | Simple front-end, reports, alerts |
| Intelligence/analytics specialist (secondary, Genesis team) | Pipeline automation, experimentation, multi-client scale, swappable components | Robust back-end, SDK, modularity |

## 5. Core capabilities (product)

1. Vegetation vigor monitoring (NDVI, EVI, GNDVI, SAVI; per-plot failure/low-performance zones)
2. Water-stress analysis (NDMI, LST, CWSI)
3. Early disease/pest detection (spectral anomalies)
4. Localized spraying recommendation (variable-rate maps)
5. Yield forecasting (30–60 days before harvest)
6. Irrigation optimization (ETc, depth per crop and phenological stage)

Details and data needs: `domain/agriculture.md`.

## 6. Roadmap and status

Current state: **Phase 1** (proof of concept in the Vale; MVP with multispectral processing, vegetation indices, basic alerts; 10–15 partner producers). `ACCEPTED`

| Source | Phase 2 | Phase 3 |
|--------|---------|---------|
| *O que é o Lattinus?* (product) | Advanced SAR, yield modelling, irrigation/nutrient recommendation, social pilot in the semi-arid | AI anomaly detection, continuous learning, national/international expansion, adjacent markets |
| *Visão 360 Técnico V1* (technical) | Clay/Prithvi fine-tuning (mango, grape), calibrated yield model, active learning loop, external API | InSAR/PSI, geographic expansion, separate business units per vertical |

`OPEN` `OQ-REF-011`: the two sources place SAR/AI capabilities in different phases (Visão 360 has S1 SAR already native in Phase 1). Do not schedule work by phase without human confirmation.

Adjacent verticals (mining, environmental monitoring) are planned for year 3 as separate business units on the same platform. `PROPOSED`

## 7. Success metrics

North Star: **average productivity increase of active clients**. Supporting: hectares under management, active producers/organizations, contract renewal rate, NPS, reduction of chemical inputs, reduction of water consumption.

## 8. Source index

| Notion source | Topic | Last edit seen | Feeds |
|---------------|-------|----------------|-------|
| O que é o Lattinus? v1.0 | Purpose, problem, capabilities, personas | 2026-08-05 | this file, `domain/agriculture.md` |
| Arquitetura da Plataforma | Module map (1.1–2.4) | 2026-09-19 | `architecture.md` |
| Briefing · Visão 360 Técnico V1 (2026-06-29) | 10-layer pipeline, decisions, SLAs, risks | 2026-09-15 | `architecture.md`, `domain/*`, `platform/jaguar.md`, `platform/mirage.md` |
| Data Transformation (arquitetura documentada, DT 2.0) | SDK, planner, Jaguar/Mirage | 2026-09-10 | `platform/transformation.md`, `platform/jaguar.md`, `platform/mirage.md` |
| Data Ingestion V2 (ARQ-001, ADR-002, ADR-003) | Ingestion architecture and ADRs | 2026-09-02 | `platform/ingestion.md` |
| Collaboratory Layer (archived analysis) | Experience layer | 2026-09-16 | `platform/collaboratory.md` |
| Plataformas Orbitais | Sensor/provider taxonomy | 2026-10-13 | `domain/earth-observation.md` |
| Catálogo de Índices Espectrais (Spyndex) | Spectral index catalog | 2026-10-18 | `domain/earth-observation.md` |

## 9. Known gaps

- `OQ-REF-014`: Notion layer databases (Foundation/Engineering/Governance/Integration/Reference per module) could not be queried in this snapshot. Layers 1.3, 1.4, 1.5, 1.6, 1.9, 2.x are covered at headline level only.
- `OQ-REF-017`: per-provider orbital databases (SAR, MSI, HSI, TIR…) not read.
- Strategic pages (positioning, personas, Oceano Azul, commercial docs) not read; irrelevant for engineering unless a task needs them.
