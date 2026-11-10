---
name: dependency-analysis
description: Analyze dependencies in two modes. Mode A evaluates an external package, library, service or base image before adding, removing or upgrading it, producing the evidence for the dependencies gate (purpose, license, maintenance, security, alternatives, exit cost). Mode B analyzes the internal structure (module and package graph, cycles, layering violations, coupling, blast radius of a change). Use whenever a task mentions adding, upgrading or replacing a dependency, "should we use X", alternatives to a library, license or maintenance checks, circular imports, dependency graphs or change-impact analysis, even if not phrased as "analysis".
---

# Dependency Analysis

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-09 · **Location:** `skills/architecture/dependency-analysis/SKILL.md`

## Purpose

Make dependency decisions evidence-based and make internal coupling visible. This skill produces analysis and recommendations. It never edits manifests or lockfiles, and it does not grant approval.

## Mode selection

| Question | Mode |
|----------|------|
| "Can we add / upgrade / replace package X?" | **A** External |
| "What depends on what? Any cycles? What breaks if I change Y?" | **B** Internal |
| Both (e.g. new package plus structural impact) | A, then B |

## Mode A: External dependency evaluation

**Inputs:** the need, candidate(s), ecosystem, and current manifests and lockfiles from the task inputs.

1. **Confirm the need.** State the problem. Check whether the standard library or an existing dependency already solves it. "Do nothing / stdlib / existing" is always an option.
2. **List candidates.** At least 2 where realistic, including existing dependencies.
3. **Evaluate each candidate** on these fields:

| Field | What to record |
|-------|----------------|
| Purpose | What it does for this task |
| License | SPDX id and compatibility with the project |
| Maintenance | Last release, cadence, maintainers, archived or not |
| Maturity | Adoption, stability, SemVer discipline |
| Footprint | Size and transitive dependencies |
| Security | Known advisories, supply-chain risk |
| Fit | Python/Go versions, formats, platform fit |
| Operational cost | Native libraries (e.g. GDAL, PROJ), image size, build time |
| Exit cost | How hard it is to replace later |

4. **Verify facts.** Take facts only from sources you can access (lockfile, package metadata, repo files, allowlisted network in `config/tools.md`). Mark each field `verified` or `unverified — needs human check`. Never state a version, license or date from memory as fact.
5. **Recommend.** State the choice, the version to pin (verified, or "to be pinned"), the lockfile requirement and an exit plan.
6. **Hand to the gate.** Fill the record for `policies/dependencies.md` and state exactly what human approval is requested. The change itself is made by the authorized agent after approval.

## Mode B: Internal dependency analysis

**Inputs:** the scope (modules, packages, services) and the code or design to analyze.

1. **Scope and granularity.** State what is analyzed (package, module, service).
2. **Build the graph.** Use imports, manifests and declared interfaces. Use local static-analysis tooling when available (no network), and state the method and its limits (dynamic imports, reflection, runtime wiring).
3. **Check the rules** from `lattinus-code.md` §7: dependencies point inward, no cycles, explicit boundaries, injected configuration, no hidden shared state.
4. **Report:**
   - cycles, listed as paths;
   - layering violations;
   - hubs with high fan-in or fan-out;
   - unstable dependencies (stable code depending on volatile code);
   - hidden coupling through shared schemas or state.
5. **Impact analysis** (when a change is proposed). List direct and transitive dependents, affected interfaces and contracts, tests to run, blast radius and the rollback unit.
6. **Recommend the minimal fix** (invert a dependency, extract an interface, move a module). If the fix amounts to a redesign, hand over to `system-design`.

## Output

Start with the traceability header (`AGENTS.md` §10), then:

```markdown
## Scope and method
<mode, scope, sources used, limits>

## Findings
<Mode A: candidate table + recommendation | Mode B: cycles, violations, hubs, impact>

## Dependency record (Mode A only, for the gate)
| Package | Version | License | Purpose | Alternatives considered | Verified? |

## Recommendation
<what to do and why>

## Approval needed
<exact human decision requested | none>

## Unverified items
<list>
```

Write in the task's `output_language` (default PT-BR). Keep identifiers and technical terms in English.

## Boundaries

- Do not edit manifests, lockfiles or code. Request changes through the Orchestrator.
- Do not approve a dependency. The gate plus human approval does (`AGENTS.md` §7).
- Do not widen scope. Report unrelated findings in one line.

## Quality bar

- [ ] Alternatives include "none / stdlib / existing".
- [ ] Every fact is labeled `verified` or `unverified`.
- [ ] License, maintenance, pinning and exit cost are covered for each recommended package.
- [ ] Cycles and violations are listed as concrete paths, not generalities.
- [ ] The method and its limits are stated.