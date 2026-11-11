# dependencies.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-11 · **Location:** `policies/dependencies.md`
> Blocking gate. Prevails over agent instructions (`AGENTS.md` §2). Aligned with `lattinus-code.md` §10.
> Key words **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 2119. Only humans edit this file.

## 1. Purpose and Trigger

Gate **Dependencies** (`AGENTS.md` §7). Applies **before** adding, removing or upgrading any dependency, at every review level. Adding or changing a dependency also requires **human approval** (`AGENTS.md` §7.2, `SOUL.md` §5).

## 2. Scope

A dependency is anything the artifact needs from outside its own code:

- language packages (Python/PyPI, Go modules), runtime and dev/test dependencies;
- system and native libraries (e.g. GDAL, PROJ, GEOS);
- container base images and GitHub Actions or other CI components;
- models, datasets and external services the code relies on.

Dev-only dependencies are covered, with the same gate.

## 3. Rules

| ID | Rule |
|----|------|
| DEP-01 | **Justify the need.** Prefer the standard library or an already-approved dependency. A new dependency MUST have a stated purpose that these cannot meet. |
| DEP-02 | **Proposal first.** No installation, import or lockfile change before the proposal (§4) is approved. |
| DEP-03 | **Human approval** is required for every add, remove or upgrade that changes the resolved dependency set. Patch-level upgrades made only by a lockfile refresh still need approval if requested by an agent. |
| DEP-04 | **License check.** See §5. Unknown or missing license blocks the proposal. |
| DEP-05 | **Maintenance check.** Record last release date and repository status. Flag a package with no release in 12 months, an archived repository, or a single inactive maintainer. A flag does not block by itself. It MUST appear in the proposal with a risk note. |
| DEP-06 | **Vulnerability check.** Known **high** or **critical** vulnerabilities block the proposal, unless a human accepts the risk in writing. If scanning is not possible in the environment, label the status `unverified` and let the human decide. |
| DEP-07 | **Pin versions.** Exact versions, never `latest` or open ranges. Commit the lockfile. Container images use pinned versions or digests. |
| DEP-08 | **Trusted sources only.** Official registries (PyPI, Go module proxy, official image registries). No install from arbitrary URLs, unreviewed forks or raw git refs. Verify the exact package name against typosquatting. |
| DEP-09 | **Install safely.** Install only in an isolated environment, over allowlisted hosts (`config/tools.md`, Safety gate SAF-23). Review install or build scripts for packages that run code at install time. |
| DEP-10 | **Minimal footprint.** Report transitive dependencies added. Reject a proposal whose transitive weight is out of proportion to its benefit. |
| DEP-11 | **Upgrades.** Read the changelog and breaking changes. A major-version upgrade or a change that alters public behavior requires an ADR. |
| DEP-12 | **Removals.** Confirm the dependency is unused (imports, config, build files, docs) before removal. |
| DEP-13 | **Scope.** One purpose per dependency change. Keep dependency changes in their own commit, and list them in the PR section "Dependências" (`lattinus-code.md` §12.1). |
| DEP-14 | **SBOM.** Regenerate it for deployable units after any change (SPDX or CycloneDX). |
| DEP-15 | **Architectural weight.** Frameworks, runtimes, databases and engines (e.g. a processing engine such as Apache Sedona) require an ADR in addition to this gate. |

## 4. Dependency Proposal Format

```
DEPENDENCY PROPOSAL · <task_id>
Change:        add | upgrade | remove
Package:       <name> <exact version> (<ecosystem>)
Scope:         runtime | dev | build | system | image | ci
Purpose:       <need it meets, link to acceptance criterion>
Alternatives:  <stdlib / existing deps / other packages, and why not>
License:       <SPDX id> · Class: allowed | needs-human-decision | blocked
Maintenance:   <last release date> · <repo status> · Flag: none | <reason>
Vulnerabilities: none known | <ids, severity> | unverified
Transitive:    <count and notable additions>
Source:        <registry URL>
Impact:        <affected modules, build size, SBOM, ADR needed yes/no>
Rollback:      <how to revert>
Needed from human: approve | reject | modify
```

## 5. License Classes (baseline, to be confirmed by maintainers)

| Class | Licenses | Treatment |
|-------|----------|-----------|
| `allowed` | MIT, BSD-2/3-Clause, Apache-2.0, ISC, PSF-2.0, Unlicense | Proceed to approval |
| `needs-human-decision` | MPL-2.0, LGPL, EPL, CC-BY (data) | Proposal MUST state the obligations. The human decides |
| `blocked` | GPL, AGPL, SSPL, BUSL, proprietary or commercial, **unknown or no license** | Not proposed unless a human decides otherwise via ADR |

Data and model licenses (datasets, weights) follow the same logic. Source data licenses and attribution are recorded as required by `lattinus-code.md` §8.

## 6. Gate Checklist

The acting agent records `dependencies: pass | na` in the traceability header.

- [ ] A proposal (§4) exists and was approved by a human, and is referenced in the PR.
- [ ] Purpose justified, alternatives recorded (DEP-01).
- [ ] License class checked, and not `blocked` (DEP-04).
- [ ] Maintenance flags recorded (DEP-05).
- [ ] No unaccepted high/critical vulnerability, or status marked `unverified` and accepted (DEP-06).
- [ ] Versions pinned, lockfile committed (DEP-07).
- [ ] Source is an official registry, and the name was verified (DEP-08).
- [ ] ADR attached when DEP-11 or DEP-15 applies.
- [ ] SBOM regenerated when applicable (DEP-14).

`na` only when the task changes no dependency. Any unchecked item sets the task to `BLOCKED`.

## 7. Open Parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| License baseline confirmation (§5) | Maintainers |
| Vulnerability scanner and CI integration | devops-sre |
| Private registry or mirror, if any | devops-sre |
| SBOM format and generation step | devops-sre |
| Lockfile and tool conventions per ecosystem | Maintainers |