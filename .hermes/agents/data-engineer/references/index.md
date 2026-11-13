# index.md — data-engineer references

Pointers only. Never copy content from central `references/`.

| Need | Load |
|------|------|
| Ingestion design, sources and cadence | `references/platform/ingestion.md` |
| Transformation and processing model | `references/platform/transformation.md` |
| Processing SDK, job contract | `references/platform/jaguar.md`, `references/platform/mirage.md` |
| Data engineering standards (formats, partitioning, idempotency) | `references/engineering/data.md` |
| Python toolchain and style | `references/engineering/python.md` |
| Test strategy for pipelines | `references/engineering/testing.md` |
| API and contract surfaces of a pipeline | `references/engineering/api.md` |
| Geospatial semantics of ingested data | `references/domain/geospatial.md` |
| Earth Observation products and bands | `references/domain/earth-observation.md` |
| Output contract, Definition of Done | `references/lattinus-code.md` §6, §7 |
| Module boundaries | `references/architecture.md` |
| Templates | `templates/implementation-plan.md`, `templates/task.md` |

Known gaps (record in `memory/open-questions.md` when hit): canonical storage layout per dataset, retention policy, and the exact contract documents for ingestion ↔ storage.
