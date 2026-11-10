---
name: system-design
description: Produce a system design for a new or changed component, module, pipeline, integration or interface, with explicit requirements, options, trade-offs and a reversible delivery plan. Use whenever a task asks to design, architect, structure, plan the architecture of, or "figure out how to build" something non-trivial, or when a change crosses module or service boundaries, even if the word "design" is not used. Not for pure implementation, reviewing an existing design (architecture-review), recording a decision (adr) or evaluating packages (dependency-analysis).
---

# System Design

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-09 · **Location:** `skills/architecture/system-design/SKILL.md`

## Purpose

Turn a task into a design an engineer can implement, with options and trade-offs visible so a human can decide. The design proposes; it does not decide (SOUL §5).

## When to use

- New component, module, pipeline, integration or API.
- Change that crosses a boundary, alters a data flow, or touches a contract.

Do **not** use for changes contained inside an existing boundary. Say so in one line and hand back to the Orchestrator.

## Inputs

- `task.md`: objective, acceptance criteria, constraints, out of scope.
- `references/` listed in your manifest, loaded on demand: `lattinus.md`, `architecture.md`, then domain/platform files the task needs.
- `memory/decisions.md` and `memory/conventions.md`: existing ADRs and conventions.
- `references/lattinus-code.md` §7–§11: engineering, data/geospatial, AI, security and operability standards.

## Procedure

1. **Frame.** Restate objective, scope and out-of-scope in at most 5 lines. List assumptions. Ask (grouped, few questions) only if a missing answer would materially change the design.
2. **Drivers.** List functional needs and quality attributes with measurable targets (latency, throughput, data volume, freshness, availability, cost, security). A target nobody gave you is a declared assumption, not a fact.
3. **Context.** Find what already exists (components, ADRs, conventions). Prefer reuse over new build, and cite the source.
4. **Boundaries.** Identify actors, external systems, data in and out, and trust boundaries.
5. **Options.** For each significant decision, give at least 2 viable options, including "extend what exists". Compare them against the drivers, state the cost of each, recommend one and say why. Do not build a straw man.
6. **Detail the recommended option:**
   - components and responsibilities; dependencies point inward, no cycles;
   - interfaces and contracts: name the standard (OpenAPI/AsyncAPI, data contract, STAC) and specify only what the decision needs;
   - data flow, state and storage; configuration injected, not hard-coded;
   - failure modes, retries and idempotency;
   - observability and security (secrets, input trust, least privilege);
   - deployment shape stated as a requirement. `devops-sre` produces the definitions.
7. **Data and geospatial** (when applicable). Cover the checklist in `lattinus-code.md` §8: CRS, formats, chunking or partitioning, lineage, temporal metadata, quality checks, scale assumptions.
8. **AI components** (when applicable). Cover `lattinus-code.md` §9: versioned prompts, schemas, evaluation, failure modes, tool permissions.
9. **Delivery plan.** Split into increments, each reversible. Describe the test strategy as *what must be verified* and give a rollback path.
10. **Risks and open questions.** Append unresolved items to `memory/open-questions.md` with `task_id` and owner.
11. **ADR triggers.** For each decision that is hard to reverse, crosses boundaries or deviates from a standard, recommend invoking the `adr` skill. Never present such a decision as made.
12. **Self-check** against the quality bar, then hand off.

## Output

- Use `templates/design.md`. If it is missing, say so in the artifact, record it in `open-questions.md`, and use the minimum structure: Context, Drivers, Options, Proposed decision, Design, Delivery plan, Risks, Open questions.
- Start with the traceability header (`AGENTS.md` §10).
- Diagrams are text-based (Mermaid or ASCII), kept consistent with the prose and explained by it.
- Size to risk: 1–2 pages for contained changes, a full design for new components or cross-boundary work.
- Write in the task's `output_language` (default PT-BR). Keep identifiers and technical terms in English.

## Boundaries

- Do not write code or infrastructure definitions. Request them through the Orchestrator via `task.md`.
- Do not state a dependency as chosen. Name candidates and route them to `dependency-analysis`.
- Do not approve your own design or ADR.
- Never invent APIs, component names, versions or dataset properties. Label unverified items.

## Quality bar

- [ ] Every acceptance criterion maps to a design element.
- [ ] Every quality target is measurable or flagged as an assumption.
- [ ] At least 2 real options for each significant decision, with honest downsides.
- [ ] Dependency direction is stated and has no cycles.
- [ ] Each increment is reversible, and rollback is described.
- [ ] Domain claims cite a `references/` file or task section.
- [ ] Out-of-scope items are respected and out-of-scope findings are reported, not acted on.