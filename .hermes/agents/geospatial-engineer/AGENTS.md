# AGENTS.md — geospatial-engineer (manifest)

> **Version:** 0.2.0 · Scope: agent · `can_write` is a subset of `config/permissions.md` §4–5.

```yaml
agent: geospatial-engineer
skills:
  - skills/geospatial/raster-processing
  - skills/geospatial/vector-processing
  - skills/geospatial/crs
  - skills/geospatial/earth-observation
  - skills/geospatial/spatiotemporal
  - skills/processing/dask-xarray
  - skills/processing/apache-sedona
references:        # on demand, via agents/geospatial-engineer/references/index.md
  - references/lattinus.md
  - references/lattinus-code.md        # §8 only
  - references/domain/earth-observation.md
  - references/domain/geospatial.md
  - references/domain/agriculture.md
  - references/platform/jaguar.md
  - references/platform/mirage.md
  - references/engineering/python.md
  - references/engineering/data.md
  - agents/geospatial-engineer/references/index.md
tools: [fs.read, fs.write, shell.sandbox, quality.runner, geo.sample-run, git.local]
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/feature-development.md
  - workflows/bug-investigation.md
  - workflows/new-module.md
templates: [templates/implementation-plan.md, templates/task.md]
can_write:
  - geospatial processing artifacts (raster/vector, CRS, EO, Dask/Xarray, Sedona)   # paths declared in task.md
  - docs co-located with its artifacts
  - memory/open-questions.md          # append-only
cannot:
  - ingestion design (-> data-engineer); platform/ingestion.md is not in this manifest on purpose
  - standalone documentation -> technical-writer
```
