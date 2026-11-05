# lattinus-code.md — Output Contract (LADE → Lattinus Code)
 
> **Version:** 0.1.0 (draft) · **Date:** 2026-11-03 · **Location:** `references/lattinus-code.md`
> Defines what LADE MUST deliver to Lattinus Code and when a delivery is considered done.
> Key words **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 2119.
> Parameters marked `TBD` depend on facts not yet confirmed (repository, CI, runtime). They are collected in §14 and MUST NOT be assumed by agents.
 
## 1. Purpose and Scope
 
Lattinus is a software and data engineering project for geoprocessing. Its code base is **Lattinus Code**. This contract makes every LADE delivery consistent, reviewable and auditable, so that maintainers integrate it with minimal rework.
 
In scope: code, tests, data pipelines, data contracts, geospatial processing, AI components, infrastructure definitions, ADRs, documentation.
Out of scope: production execution of the Lattinus platform, and merging (human-only).
 
## 2. Parties
 
| Party | Role |
|-------|------|
| LADE agents | Produce the delivery package and propose it as a PR |
| Requester | Defines the task and acceptance criteria |
| Maintainer | Reviews and decides the merge into Lattinus Code. Mandatory in every review level |
 
## 3. Standards Baseline
 
The contract adopts widely used industry standards instead of inventing local ones.
 
| Area | Standard |
|------|----------|
| Commits | Conventional Commits 1.0.0 |
| Versioning | Semantic Versioning 2.0.0 |
| Changelog | Keep a Changelog |
| Decisions | ADR, MADR-style (`templates/adr.md`) |
| HTTP APIs | OpenAPI 3.x; async interfaces: AsyncAPI |
| Data contracts | Open Data Contract Standard (ODCS) or equivalent declared in the ADR |
| Geospatial catalog | STAC (spatiotemporal assets) |
| Raster / vector formats | Cloud Optimized GeoTIFF (COG), GeoParquet, Zarr for n-dimensional arrays |
| CRS | EPSG codes, explicit always |
| Observability | OpenTelemetry (traces, metrics, logs) |
| Supply chain | SBOM in SPDX or CycloneDX; SLSA-aligned provenance (target level `TBD`) |
| Runtime config | Twelve-Factor App principles |
| Python style | PEP 8, PEP 484 type hints |
| Go style | `gofmt`, Effective Go, `go vet` |
 
## 4. Delivery Unit
 
One **task** produces one **delivery package**, proposed as **one Pull Request** (or a stacked series when the task is split).
 
Rules:
1. A PR MUST map to exactly one `task_id` (or one parent with declared subtasks).
2. A PR SHOULD be small and reviewable. Target: one coherent change. Above the size threshold in §14, the agent MUST propose a split.
3. The PR MUST be reversible: it can be reverted as a unit without leaving the system inconsistent.
4. Agents open PRs as **draft**. A human moves them to ready and merges.
### 4.1 Repository conventions
 
| Item | Rule |
|------|------|
| Repository | `TBD` (see §14) |
| Base branch | `TBD` (default branch of the repository) |
| Branch name | `<type>/<task_id>-<short-slug>`, e.g. `feat/LADE-20261103-001-ndvi-pipeline` |
| Branch lifetime | Short-lived. Rebase or merge from base before PR |
| Commit message | Conventional Commits. English. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert` |
| Commit footer | `Task: <task_id>` and, when applicable, `ADR: ADR-NNNN` |
| Breaking change | `!` after type or `BREAKING CHANGE:` footer, plus ADR reference |
| Commit size | Atomic: each commit builds and passes tests |
| Signing | Per repository policy (`TBD`) |
| Force-push / merge by agent | Forbidden (`AGENTS.md` §11) |
 
## 5. Definition of Ready (task accepted for delivery work)
 
A task MAY enter `IN_PROGRESS` only if `task.md` has:
- verifiable acceptance criteria;
- declared inputs and expected outputs;
- review level and output language;
- explicit out-of-scope list;
- required references available (or the gap recorded in `memory/open-questions.md`).
## 6. Definition of Done
 
### 6.1 Universal (all deliveries)
 
- [ ] Every acceptance criterion in `task.md` is met, with evidence.
- [ ] Traceability header present in every artifact (`AGENTS.md` §10).
- [ ] All policy gates passed and recorded.
- [ ] No secrets, credentials, tokens, personal data or absolute local paths.
- [ ] Linters, formatters, type checks and tests pass locally and in CI (`TBD`).
- [ ] No unapproved dependency added or changed.
- [ ] Assumptions and known limitations are declared in the PR.
- [ ] Documentation updated where behavior, interfaces or operations changed.
- [ ] Changelog entry added for user-visible or interface changes.
- [ ] Review verdict recorded: `PASS` (standard) or human sign-off (human-only).
### 6.2 By deliverable type (in addition to 6.1)
 
| Type | Additional criteria |
|------|---------------------|
| **Code** | Unit tests for new logic; regression test for every bug fix; public functions typed and documented; no dead code or commented-out blocks; errors handled explicitly, not swallowed |
| **API** | OpenAPI/AsyncAPI spec updated and valid; backward compatibility stated; error model and status codes documented; versioning impact declared |
| **Data pipeline** | Idempotent and re-runnable; data contract defined or updated; schema validation on input and output; data quality checks with failure behavior; lineage (source → output) documented; backfill procedure described |
| **Geospatial processing** | See §8 checklist |
| **AI component** | See §9 checklist |
| **Infrastructure** | Reproducible from code; least privilege; resource limits set; rollback path documented; no manual steps |
| **Architecture** | ADR approved by a human before implementation; alternatives and trade-offs recorded; dependency impact analyzed |
| **Documentation** | Accurate against the current code; examples runnable or marked illustrative; owner identified |
 
## 7. Engineering Standards
 
1. **Design.** Explicit module boundaries; dependencies point inward; no circular dependencies; configuration injected, never hard-coded (Twelve-Factor).
2. **Testing.** Pyramid: unit tests (fast, many), integration tests (boundaries, contracts), few end-to-end tests. Tests are deterministic: no network, wall-clock or unseeded randomness without isolation. Coverage thresholds `TBD`; coverage never replaces meaningful assertions.
3. **Quality gates.** Formatter, linter and type checker MUST run clean. Cyclomatic complexity and function length limits `TBD`.
4. **Error handling and logging.** Structured logs, no sensitive data, correlation by `task_id`/request id where applicable. Fail fast on invalid input.
5. **Performance.** State complexity or scaling assumptions for code on hot paths or large data. Optimize only with a measurement.
6. **Compatibility.** Public interfaces change only with SemVer discipline. Deprecation precedes removal, with a stated window.
## 8. Data and Geospatial Standards
 
Mandatory for any artifact touching spatial or spatiotemporal data.
 
| Topic | Requirement |
|-------|-------------|
| **CRS** | Every dataset states its CRS (EPSG). Reprojection is explicit, logged and justified. Never assume WGS84 silently. Area and distance computed in a suitable projected CRS or geodesic method |
| **Geometry validity** | Validate geometries (valid, non-empty, expected type). Define behavior for invalid input: repair, reject or quarantine |
| **Raster metadata** | Declare resolution, extent, nodata value, dtype, units, scale/offset, band semantics and resampling method |
| **Temporal metadata** | Declare time zone (UTC by default), acquisition vs processing time, and temporal resolution |
| **Formats** | Prefer COG, GeoParquet and Zarr for cloud-native storage. Deviations require justification in the PR |
| **Catalog** | Spatiotemporal assets described as STAC Items/Collections when cataloged |
| **Provenance and lineage** | Record source dataset, version, retrieval date, processing steps and parameters. Outputs are reproducible from this record |
| **Reproducibility** | Pinned dependency versions, seeded randomness, parameterized runs, no hidden state |
| **Scale** | Chunking strategy declared (Dask/Xarray) or partitioning strategy (Sedona). Memory and runtime assumptions stated. No full in-memory loads of unbounded data |
| **Quality checks** | Cloud/mask handling, outlier and nodata checks, spatial and temporal completeness, with thresholds declared |
| **Accuracy and uncertainty** | State known limits (resolution, sensor, interpolation). Do not present derived values with more precision than the sources support |
| **Licensing** | Source data licenses and attribution recorded |
 
Domain specifics (Earth Observation, agriculture, Jaguar, Mirage) are in `references/domain/` and `references/platform/`.
 
## 9. AI Component Standards
 
For agents, LLM integrations and evaluators delivered to Lattinus Code.
 
- [ ] Prompts, tools and model identifiers are versioned and configurable, not embedded inline.
- [ ] Inputs/outputs have schemas; outputs are validated before use.
- [ ] An evaluation exists (golden cases, metrics, pass thresholds) and its result is attached.
- [ ] Failure modes are handled: timeouts, malformed output, refusals, cost limits.
- [ ] Tool permissions follow least privilege; destructive tools require human confirmation.
- [ ] No sensitive data sent to external providers without an approved policy.
- [ ] Non-determinism is acknowledged; tests do not depend on exact free-text output.
## 10. Security and Supply Chain
 
1. **Secrets.** Never in code, history, logs, fixtures or artifacts. Use the platform's secret mechanism (`TBD`).
2. **Dependencies.** Added only after the dependencies gate and human approval. For each new package record: purpose, license, maintenance status, and alternatives considered. Versions pinned; a lockfile is committed.
3. **Vulnerabilities.** Dependency and container scans run in CI (`TBD`); high/critical findings block the PR unless a human accepts the risk in writing.
4. **SBOM.** Generated for deployable units (SPDX or CycloneDX).
5. **Input handling.** Validate and sanitize external input, including files, geometries and metadata. Treat third-party data as untrusted.
6. **Least privilege.** Credentials, service accounts and containers run with the minimum permissions needed.
7. **Containers.** Minimal base image, non-root user, pinned digests or versions.
## 11. Observability and Operability
 
For services, pipelines and jobs:
- structured logs, metrics and traces via OpenTelemetry conventions;
- health/readiness signals for services; success, failure and data-volume metrics for pipelines;
- documented runbook: how to run, monitor, retry, backfill and roll back;
- defined behavior on partial failure and on retries (idempotency).
## 12. The Delivery Package
 
Each PR MUST contain:
 
| Component | Content |
|-----------|---------|
| Code and tests | Per §6 and §7 |
| Docs and changelog | Per §6.1 |
| ADR(s) | If an architectural decision was made or changed |
| Evidence | Test results, lint/type output, evaluation or data-quality results (as applicable) |
| Review record | `templates/review.md` output (standard) or human sign-off (human-only) |
| PR description | Template below, default language `PT-BR` |
 
### 12.1 PR description template
 
```markdown
## Resumo
<what changed and why, in 2-4 sentences>
 
## Rastreabilidade
- Task: <task_id>
- ADR: <ADR-NNNN | none>
- References: <files in references/>
- Review level: <human-only | standard>
- Reviewer verdict: <PASS | n/a>
 
## Tipo de mudança
<feat | fix | refactor | perf | docs | build | ci | chore> · Breaking: <yes/no>
 
## Como testar
<commands or steps>
 
## Evidências
<test, lint, type-check, data-quality or eval results>
 
## Premissas e limitações
<declared assumptions, known gaps, unverified items>
 
## Impacto e rollback
<affected components, data, interfaces; how to revert>
 
## Dependências
<added/changed packages with justification | none>
 
## Checklist
- [ ] Definition of Done (references/lattinus-code.md §6)
- [ ] Policy gates passed
- [ ] Sem segredos ou dados sensíveis
```
 
## 13. Acceptance and Handoff
 
1. The Orchestrator assembles the package, verifies §6, and opens a **draft PR**.
2. The maintainer reviews. Possible outcomes: **approve and merge**, **request changes** (opens a new `REWORK` cycle within the limit in `AGENTS.md` §8.2), or **reject** (task closed with reason in `project-state.md`).
3. After merge, the Orchestrator updates `memory/` per `AGENTS.md` §9 and sets the task to `DONE`.
4. Post-merge defects traced to a delivery MUST be reported to the Reviewer to produce a lesson in `memory/lessons.md`.
## 14. Open Parameters (`TBD`)
 
| Parameter | Needed for | Owner |
|-----------|-----------|-------|
| Repository name and base branch | §4.1 | Maintainers |
| Commit signing policy | §4.1 | Maintainers |
| CI system and required checks | §6.1, §10 | Maintainers / devops-sre |
| PR size threshold | §4 | Maintainers |
| Coverage and complexity thresholds | §7 | Maintainers |
| Secret management mechanism | §10 | devops-sre |
| SLSA target level | §3 | devops-sre |
| Data contract standard confirmation (ODCS or other) | §3 | data-engineer / architect |
 
## 15. Maintenance
 
1. Only humans edit this file. Changes bump `Version`, `Date` and the changelog.
2. A breaking change to this contract (stricter Definition of Done, new mandatory artifact) requires an ADR.
3. This file is a snapshot-aligned reference: when the Notion Lattinus context changes in a way that affects delivery, it MUST be revisited.
