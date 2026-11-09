---
name: processing-sdk
description: Design, implement or review code that uses or extends the Lattinus Transformation SDK and its engine adapters (Dataset, Transformation, Operation, Pipeline, ExecutionPlan, Engine, Output). Use whenever a task involves declaring transformations or pipelines, composing operations into DAGs, writing an engine adapter for Jaguar or Mirage, defining SDK contracts, capability ports, providers, execution context, outputs or contract tests, even if the user only says "SDK", "pipeline" or "transformation". Do NOT use for engine-internal computation (use dask-xarray or apache-sedona) or for ingestion pipelines (use data-engineering skills).
metadata:
  version: 0.1.0
  date: 2026-11-09
  status: draft
  agents: [data-engineer]
  sources: [DT-IF-001, DT-ARQ-001, DT-STK-001, SDK-ARQ-001, references/lattinus-code.md]
---

# processing-sdk

## 1. Scope

The Transformation SDK is the **public programming abstraction** over processing: it expresses transformation **intent** and hides the execution engines (DT-ARQ-001 §4). Engines are Jaguar (Dask + Xarray) and Mirage (Apache Sedona).
This skill covers contracts, composition, adapters and contract tests. It does not implement the Planner, the workflow runtime or any engine internals.

## 2. Load on demand (declared in manifest)

`references/platform/transformation.md`, `references/platform/jaguar.md`, `references/platform/mirage.md`, `references/architecture.md`, `references/engineering/api.md`, `references/engineering/python.md`, `references/engineering/testing.md`, `references/lattinus-code.md`.
If one is missing or outdated: say so in the artifact, append to `memory/open-questions.md`, proceed only with declared assumptions.

## 3. Principles (non-negotiable)

1. **Contract before engine.** Consumers depend on stable contracts, never on Dask, Xarray, Sedona or Spark.
2. **Planner before execution.** Composing a pipeline does not execute it. Execution starts only on submit.
3. **Engine specialization.** Raster, array and data-cube workloads target Jaguar; vector and spatial workloads target Mirage. The engine selection *strategy* is open: do not hard-code it in the SDK.
4. **Portable execution.** Deployment (cloud or edge) MUST NOT change the logical transformation model.
5. **Explicit boundaries.** Storage, Catalog, Ingestion and Observability are separate domains; the SDK calls them through contracts.

## 4. Canonical objects (DT-IF-001 §3)

`Dataset` (logical data) · `Asset` (materialized unit) · `Transformation` (declarative description) · `Operation` (atomic unit) · `Pipeline` (ordered composition) · `DAG` (dependencies) · `ExecutionPlan` (derived executable plan) · `Engine` (specialized runtime) · `Execution` (instance of a plan) · `Output` (logical result) · `Artifact` (materialized output).

Do not invent new top-level objects. If one is needed, propose it through an ADR (architect).

## 5. Procedure

### 5.1 Declaring a Transformation

A transformation MUST declare: identifier, inputs, parameters, operations, expected outputs, execution requirements when needed (DT-IF-001 §5). Parameters are typed and serializable.

### 5.2 Composing a Pipeline

1. Reference inputs as `Dataset` identifiers (catalog URIs), not file paths.
2. Express dependencies explicitly; the result MUST be an acyclic graph.
3. Keep Operations atomic and engine-agnostic. Engine-specific logic belongs in adapters.

### 5.3 Writing or changing an Engine adapter

1. The adapter implements the Lattinus execution model and is the **only** place that imports engine libraries.
2. Translate `ExecutionPlan` to engine calls; translate engine results to `Output`.
3. Map engine errors to the platform error taxonomy (open: declare assumption).
4. Pass the shared contract tests. Add new cases to the shared suite, not to a private one.

### 5.4 Outputs

Every `Output` has logical identity and enough context for persistence, cataloging, lineage, validation and downstream consumption (DT-IF-001 §8): identity, schema/metadata (CRS, nodata, units, time), lineage record, quality results.

### 5.5 Context and security

Carry `correlation_id`, `causation_id`, `deadline`, runtime, identity reference, scope and tracing metadata through the SDK `Context` (SDK-ARQ-001 §8). **Secrets MUST NOT appear in Resources, logs, pipeline definitions or outputs.**

## 6. Dependency direction

```
Public API → Contracts → Capability Ports → Provider Ports → Adapters/Transports → Platform APIs
```

Dependencies point inward. Core stays minimal and free of infrastructure. Heavy dependencies (engines, service libs) live behind extras or adapter packages (DT-STK-001 §10).

## 7. Conceptual shape (not an implemented API)

```python
from lattinus import Dataset, Transformation, Pipeline

source = Dataset("catalog://sentinel-2/collection")
pipeline = Pipeline(
    Transformation("cloud_mask", inputs=[source]),
    Transformation("ndvi", inputs=["cloud_mask"]),
)
execution = pipeline.submit()
```

Source: DT-IF-001 §4, explicitly **conceptual**. Never present it as an existing API; verify the real package before writing code against it.

## 8. Open contracts (do not assume)

Dataset schema, serialization format, execution status model, error taxonomy, plugin protocol and engine capability declaration are undefined (DT-IF-001 §11). Interchange contract between engines, persistence of the Transformation Catalog and the Planner/Workflow boundary are also open (DT-ARQ-001 §11). For each one you touch: declare an assumption, record it in `memory/open-questions.md`, and propose an ADR via the architect instead of deciding.

## 9. Versioning

A breaking change to a public object requires a new contract version and an architectural evaluation (ADR). Internal engine changes MUST NOT require SDK changes while the contract is stable. Apply SemVer and deprecate before removing.

## 10. Testing

- Contract tests shared across engines and adapters.
- Unit tests for composition: DAG validity, cycle rejection, parameter validation, serialization round-trip.
- Fake engine adapter for SDK tests, so SDK tests never import Dask, Xarray, Sedona or Spark.
- Deterministic; no network.

## 11. Done checklist (adds to `lattinus-code.md` §6.1 and §6.2)

- [ ] No engine library imported outside adapters.
- [ ] Composition is lazy; execution only on submit.
- [ ] Transformations declare inputs, parameters, operations, outputs.
- [ ] Outputs carry identity, metadata and lineage.
- [ ] No secrets in definitions, logs or outputs.
- [ ] Contract tests pass; new behavior covered in the shared suite.
- [ ] Breaking changes have an ADR and a contract version bump.
- [ ] Open contracts touched are declared as assumptions and logged.
- [ ] Dependency changes passed the gate.

## 12. Gates and traceability

Artifacts carry the header in `AGENTS.md` §10. Gates: `dependencies`, `git`, `documentation`, `safety`. Architecture-affecting changes need a human-approved ADR before implementation (`lattinus-code.md` §6.2).