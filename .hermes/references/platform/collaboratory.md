# collaboratory.md — Collaboratory / Colab Service (Module 1.7)

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `references/platform/collaboratory.md`
> **Snapshot:** Notion Lattinus, read 2026-11-10. Source: *Arquitetura Documentada — Collaboratory Layer* (archived analysis, 2026-09-16). The platform page states this layer is **planning/hypothesis only, with no definitive use**. A newer *Lattinus Colab Service 2.0* page exists and was **not read** (`OQ-REF-013`).
> Evidence tags: `ACCEPTED` · `PROPOSED` · `HYPOTHESIS` · `LEGACY` · `GENERAL` · `OPEN`. Everything here is `HYPOTHESIS` unless stated. Bootstrap; human-edited only.

## 1. Role

R&D environment for analysts, data scientists and engineers: explore datasets, develop algorithms, run experiments, prototype pipelines, collaborate, using platform services **without** accessing their internals. Recommended framing: an **Experience Layer**, not infrastructure. It orchestrates and consumes platform capabilities; it does not implement data capabilities.

## 2. Boundaries

| Responsible for | Not responsible for |
|-----------------|--------------------|
| Development environment, notebooks, authenticated access to platform services, experimentation, consuming APIs, scientific tooling | Running production pipelines, permanent dataset storage, distributed processing, replacing the processing layer |

**Rule:** every resource consumed by the Collaboratory has a public interface (API or SDK). No direct buckets, internal databases, private tables or engine internals. Business logic never lives in notebooks. The layer stays stateless: notebooks are recreatable; relevant artifacts persist in the proper layers.

```
Notebook → Lattinus SDK → Transformation API / Storage API / Ingestion API / Metadata API / AI services
```

## 3. Initial stack (deliberately lean)

JupyterLab, JupyterHub (multi-user), Python, Lattinus SDK, OAuth2 or Keycloak when needed, Docker, SSH, Git, uv or Poetry. **Excluded at start:** Kubeflow, Airflow, MLflow, Spark, Ray, VS Code Server, web IDEs, feature store, workflow engines. Can be added later without architecture change.

## 4. Evolution

| Phase | Capabilities |
|-------|--------------|
| 1 Foundation | JupyterHub, JupyterLab, SDK, Git, SSH, APIs of core layers |
| 2 Collaboration | Notebook templates, shared environments, experiment catalog, richer metadata integration |
| 3 Advanced research | Ephemeral environments, GPU, AI integrations, transparent distributed execution, advanced observability |

## 5. Rules for agents

1. Do not design features that make notebooks a second processing engine.
2. Do not depend on this layer for production flows.
3. Exclusions in §3 are an architectural position, not an oversight. Adding one needs a human decision.
4. The ML experiment tracking choice (`OQ-REF-003`) is open; do not embed MLflow here by default.

## 6. Gaps

`OQ-REF-010` the archived example imports engine names through the SDK (conflicts with `platform/transformation.md` §3) · `OQ-REF-013` Colab Service 2.0 unread · whether the Collaboratory is a platform module or an experience layer is not settled in the module map.
