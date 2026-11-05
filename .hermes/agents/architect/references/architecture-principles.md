# architecture-principles.md

> **Version:** 0.1.0 · Principles the `architect` applies. Domain facts live in `references/`, not here.

## 1. Method (in order)

1. **Frame:** problem, context, constraints, out of scope.
2. **Prioritize quality attributes:** pick at most 3 that drive the design.
3. **Generate options:** at least 2 viable, plus "do nothing" when relevant.
4. **Evaluate:** trade-offs against the prioritized attributes, with evidence or declared assumptions.
5. **Recommend:** one option, with consequences and risks.
6. **Plan:** incremental path, rollback, work split per agent.

## 2. Structural principles

- Explicit module boundaries; dependencies point inward; no cycles.
- Contracts first (API, data contract, schema) before internals.
- Configuration is injected (Twelve-Factor). No hidden state.
- Separate compute, storage and orchestration concerns in pipelines.
- Prefer cloud-native, open formats (COG, GeoParquet, Zarr) and open standards (OpenAPI, STAC, OpenTelemetry), per `references/lattinus-code.md` §3.
- Idempotent, re-runnable processing steps. Design the failure and retry path.
- Make scale explicit: data volume, chunking or partitioning strategy, memory and runtime assumptions.
- Design for operability: observability, runbook, rollback.

## 3. Decision principles

- **One-way vs two-way doors.** Reversible decisions: decide fast, record briefly. Irreversible ones: ADR plus human approval.
- **Evolutionary design.** Build the smallest increment that validates the riskiest assumption first.
- **Buy/reuse before build.** Justify custom code against existing libraries or services.
- **Avoid premature distribution.** Start as a modular monolith or single pipeline unless a requirement forces separation.
- **Cost is a quality attribute.** State compute, storage and maintenance cost impact.
- **Fitness functions.** Where possible, express an architectural rule as a check (dependency rule, latency budget, schema validation).

## 4. When an ADR is required

An ADR proposal is mandatory when the change:
1. adds, replaces or removes a core technology, framework or runtime;
2. creates or changes a module boundary, public API or data contract;
3. changes a storage format, CRS convention or data model shared across components;
4. changes deployment topology, security model or trust boundary;
5. is hard or costly to reverse;
6. deviates from `references/lattinus-code.md` or `references/architecture.md`.

Otherwise, record the decision inside the design document.

## 5. Dependency analysis (minimum content)

Purpose · license · maintenance status (activity, release cadence) · security posture · size and transitive weight · integration effort · lock-in and exit cost · alternatives considered · recommendation. Output feeds the dependencies gate. Human approval is still required.

## 6. Design document checklist

- [ ] Problem and constraints stated
- [ ] Prioritized quality attributes
- [ ] ≥ 2 options with trade-offs
- [ ] Recommendation with consequences and risks
- [ ] Boundaries, contracts and data flow shown (C4 level 1-2 is usually enough)
- [ ] Failure modes, observability and rollback
- [ ] Scale assumptions stated
- [ ] Dependency impact analyzed
- [ ] Facts, assumptions and unverified items separated
- [ ] Implementation plan split per agent

## 7. Anti-patterns to avoid

Big-design-up-front without a decision to support · diagrams without contracts · resume-driven technology choices · silent assumptions about CRS, volume or SLAs · designs that cannot be rolled back · designing around a single happy path · reviewing or approving its own design.