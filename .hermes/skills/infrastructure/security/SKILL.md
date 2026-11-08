---
name: security
description: Design and check security controls for Lattinus infrastructure and delivery. Covers lightweight threat modeling, least-privilege checklists (IAM, service accounts, containers, object storage, CI tokens), secrets handling design, dependency and container scanning, SBOM and provenance, and hardening for untrusted third-party data (satellite archives, rasters, geometries, metadata). Use this skill whenever a task touches credentials, permissions, external providers, storage access, CI/CD, container or dependency changes, or user/third-party file input, even if the word "security" is never mentioned.
---

# security

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-08 · **Owner agent:** `devops-sre` · **Category:** `skills/infrastructure/`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Scope

**Covers:** threat model per change, least-privilege checklist, secrets *design*, scanning stages, SBOM/provenance, input-handling rules for untrusted data, security notes for the PR.

**Does not cover:** the final review verdict (`reviewer`), blocking gates (`policies/safety.md`, `policies/dependencies.md`, `policies/git.md`), AI-provider data policy (`ai-engineer`), application-level validation code (`software-engineer`, `data-engineer`).

This skill owns the security checklist. `containers` and `deployment` reference it and do not restate it.

## 2. When to use

A task adds or changes: credentials or permissions, a call to an external provider, storage access, CI/CD, a container or dependency, or code that parses external files.

## 3. Inputs (from `task.md`)

Components touched, data classes involved (public EO data, producer or parcel data, credentials), trust boundaries crossed, environment (cloud, edge), existing ADRs.

## 4. Procedure

1. **Map assets and trust boundaries.** Provisional baseline: Data Ingestion is the only point of contact with external providers and isolates their credentials and rate limits; Platform Management is the control plane for identities, credentials and API tokens; Managed Storage is S3-based. Confirm against the task. Cite as `unverified` until promoted to `references/`.
2. **Threat model (one page max).** Table of STRIDE categories against each crossed boundary: threat, existing control, gap, proposed control. Skip categories with no exposure and say why.
3. **Least-privilege checklist.** For each identity, answer: what is the minimum action set, on which resources, for how long?
   - Cloud/service identities scoped per module, no shared admin roles.
   - Object storage: private by default, no public access, encryption in transit and at rest, access scoped by prefix.
   - Containers: non-root, no extra capabilities, egress limited to what is needed.
   - CI tokens: minimal `permissions` per job, short-lived credentials preferred over static keys.
4. **Secrets (design only).** Define where a secret lives (mechanism is `TBD`: propose via ADR), how it reaches the workload (runtime injection, never baked), who rotates it, and how leaks are detected. If a secret appears in any file, log or output: stop, do not print it, mark the task `BLOCKED`, escalate. Humans rotate.
5. **Scanning stages in CI.** Secret detection, static analysis (SAST), dependency vulnerabilities, container image vulnerabilities, IaC misconfiguration. Language and tool names are choices to declare; the CI baseline already includes secret detection and CodeQL. High/critical findings block the PR unless a human accepts the risk in writing (`lattinus-code.md` §10.3).
6. **SBOM and provenance.** SPDX or CycloneDX for each deployable unit. Provenance level (SLSA target) is `TBD`: log it in `open-questions.md`.
7. **Untrusted data handling** (any code or job that opens external files):
   - Size limits and decompression-ratio limits for archives.
   - Allow-list of accepted formats; verify type by content, not extension.
   - Safe extraction: no path traversal, no symlink escape.
   - Geometry and metadata limits (vertex count, string length, nesting); sanitize before storage or display.
   - Run parsers (for example GDAL-based) in a least-privilege container with CPU, memory and time limits.
8. **Data protection.** Parcel geometries and producer identifiers are potentially sensitive. Do not put them in logs, metric labels or fixtures. Whether LGPD obligations apply is `unverified`: ask the maintainers.
9. **Write the security notes** into the PR section "Premissas e limitações": threats considered, controls added, residual risk, items left to humans.

## 5. Deliverable checklist (`lattinus-code.md` §6.1, §6.2, §10)

- [ ] Threat model attached or "no new boundary" justified.
- [ ] Least-privilege answers recorded for every new or changed identity.
- [ ] No secrets, tokens or personal data in any artifact.
- [ ] Scanning stages present in the CI definition; blocking thresholds stated.
- [ ] SBOM step present for deployable units.
- [ ] Untrusted-input limits defined where external files are parsed.
- [ ] Residual risk and unverified items declared.
- [ ] `safety` and `dependencies` gate results recorded in the traceability header.

## 6. Guardrails

- MUST NOT read, create, use or print secrets or credentials (`permissions.md` §6, Deny).
- MUST NOT apply IAM, network or infrastructure changes. Produce definitions; humans apply.
- MUST NOT downgrade a finding to pass a gate. Gates are blocking.
- MUST NOT approve its own artifact (`permissions.md` §5.3).
- Network access to scanners or vulnerability databases only on hosts allowlisted in `config/tools.md`.

## 7. Escalate when

- A secret or credential is exposed anywhere.
- A high/critical vulnerability has no available fix and the risk acceptance is not given.
- A boundary requires broader permissions than least privilege allows.
- Regulatory exposure (personal data, contracts) is suspected.
- The secret-management mechanism or SLSA level is needed and still `TBD`.

## 8. References

- `references/lattinus-code.md` §3, §10, §11
- `config/permissions.md` §5, §6; `policies/safety.md`, `policies/dependencies.md`
- Provisional (Notion Lattinus, "Arquitetura da Plataforma" and the `ci.yml` page): to be promoted to `references/engineering/infrastructure.md` by a human.