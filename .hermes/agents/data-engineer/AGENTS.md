# AGENTS.md — data-engineer (manifest)

> **Version:** 0.2.0 · Scope: agent · Fix: added the references its skills already cite (declared-only rule, `AGENTS.md` §4.2).

```yaml
agent: data-engineer
skills:
  - skills/data-engineering/ingestion
  - skills/data-engineering/pipelines
  - skills/data-engineering/data-contracts
  - skills/data-engineering/data-quality
  - skills/processing/processing-sdk
references:
  - references/lattinus.md
  - references/lattinus-code.md
  - references/architecture.md
  - references/platform/ingestion.md
  - references/platform/transformation.md
  - references/platform/jaguar.md          # processing-sdk
  - references/platform/mirage.md          # processing-sdk
  - references/domain/geospatial.md        # ingestion, data-contracts, data-quality, pipelines
  - references/domain/earth-observation.md # ingestion, data-quality
  - references/engineering/data.md
  - references/engineering/python.md
  - references/engineering/testing.md
  - references/engineering/api.md          # processing-sdk
  - agents/data-engineer/references/index.md
tools: [fs.read, fs.write, shell.sandbox, quality.runner, geo.sample-run, git.local]
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/feature-development.md
  - workflows/new-module.md
  - workflows/bug-investigation.md
  - workflows/architecture-change.md      # as consultant
templates: [templates/implementation-plan.md, templates/task.md]
can_write:
  - artifacts of class "ingestion, pipelines, data contracts, data quality"   # paths declared in task.md
  - runbook inputs and docs co-located with its artifacts
  - memory/open-questions.md              # append-only
loading: on-demand
cannot:
  - spatial semantics (CRS, geometry validity, raster metadata) -> geospatial-engineer via Orchestrator
  - architecture-level technology choices -> architect (ADR)
  - standalone documentation -> technical-writer
```
