---
name: containers
description: Write and validate container definitions (Dockerfile, Compose, .dockerignore, healthchecks, resource limits) for Lattinus services, pipelines and jobs. Use this skill whenever a task involves containerizing code, changing a base image, packaging Python/Go workloads, or bundling native geospatial libraries (GDAL, PROJ, GEOS), even if the task only says "package", "dockerize" or "make it runnable anywhere". Produces definitions only; never builds-and-pushes or runs containers on shared infrastructure.
---

# containers

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-08 · **Owner agent:** `devops-sre` · **Category:** `skills/infrastructure/`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Scope

**Covers:** Dockerfile / OCI image definitions, Compose files for local development, `.dockerignore`, multi-stage builds, base-image selection, non-root runtime, health signals, resource limits (declared), OCI labels, SBOM generation step, pinned native geospatial libraries.

**Does not cover:** building and pushing images to a registry (CI, human-approved), choosing the orchestrator (`deployment` + ADR), scanning policy and threat modeling (`security`), instrumentation inside application code (`observability`, `software-engineer`).

## 2. When to use

- A task adds, changes or reviews anything that is packaged as an image.
- A dependency change affects image contents (new native library, new Python/Go version).
- A base image is added or upgraded.

## 3. Inputs (from `task.md`)

Workload type (service, pipeline job, CLI), language and version, entrypoint, runtime profile (cloud or edge), target architecture (`amd64`/`arm64`; if absent, declare an assumption), native dependencies, ports, config variables, expected resource envelope.

## 4. Procedure

1. **Confirm inputs.** If workload type or target architecture is missing and cannot be inferred, state the assumption in the artifact header.
2. **Select the base image.** Official, minimal, maintained. Pin by version tag **and** digest. Record purpose, license, maintenance status and the alternative considered. A new base image family is a dependency: run the `dependencies` gate.
3. **Use a multi-stage build.** Builder stage holds compilers and build tools; runtime stage holds only what execution needs.
4. **Install from the lockfile only.** Python: `uv.lock` with a frozen sync. Go: `go.sum` with module mode. No dependency resolution at build time without a lockfile and none at runtime.
5. **Native geospatial libraries.** Pin GDAL/PROJ/GEOS versions. State whether Python wheels bundle them or the system provides them, and do not mix both silently. Record resulting versions as image labels. If linkage is not verified, label it `unverified`.
6. **Run as non-root.** Fixed numeric UID, no `privileged`, no added capabilities, read-only root filesystem where the workload allows, writable paths declared explicitly (temp, cache).
7. **Config via environment** (Twelve-Factor). No secrets in `ARG`, `ENV`, layers, Compose files or defaults. OpenTelemetry settings stay injectable through environment variables.
8. **Write `.dockerignore`.** At minimum: VCS data, `.env*`, credentials, local datasets, notebooks with outputs, build caches.
9. **Health signal.** Services: `HEALTHCHECK` or an HTTP readiness endpoint reference. Jobs: documented exit-code contract (0 success, non-zero failure).
10. **Declare resource limits** (CPU, memory, ephemeral storage) in the deployment definition. For raster/array workloads state the memory model (chunking or streaming) so limits are justified.
11. **Labels.** OCI standard labels: source, revision, version, created; plus `lattinus.task-id`.
12. **SBOM.** Add the generation step (SPDX or CycloneDX) to the CI definition. Do not run it against registries.
13. **Validate statically.** Dockerfile lint, Compose config validation, secret-pattern check on the changed files. Building an image requires network (base-image pull): run it only if the host is allowlisted in `config/tools.md` and the `safety` gate passes. Otherwise leave the build to CI and say so under Evidence.

## 5. Illustrative skeleton (adapt, do not copy blindly)

```dockerfile
# ILLUSTRATIVE. Pin versions and digests before use.
FROM python:3.12-slim@sha256:<digest> AS builder
COPY --from=ghcr.io/astral-sh/uv:<pinned-version> /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:3.12-slim@sha256:<digest> AS runtime
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=builder --chown=10001:10001 /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER 10001
HEALTHCHECK --interval=30s --timeout=3s CMD ["python", "-m", "<module>.healthcheck"]
ENTRYPOINT ["python", "-m", "<module>"]
```

## 6. Deliverable checklist (`lattinus-code.md` §6.2, Infrastructure)

- [ ] Reproducible from code: pinned base image, pinned dependencies, lockfile used, no manual build step.
- [ ] Least privilege: non-root, no extra capabilities, no secrets baked in.
- [ ] Resource limits declared.
- [ ] Rollback path documented (previous image tag/digest is retained and referenced).
- [ ] No manual steps in build or run instructions.
- [ ] Native library versions recorded; linkage stated or marked `unverified`.
- [ ] SBOM step present in the CI definition.
- [ ] Traceability header present; gates recorded.

## 7. Guardrails

- MUST NOT push images, authenticate to registries, or run containers against shared or production systems (`permissions.md` §6).
- MUST NOT read, create or embed secrets. A secret found in a file is reported, never printed.
- MUST NOT add or upgrade a package or base image without the `dependencies` gate and human approval.
- MUST NOT use `latest` or unpinned tags.

## 8. Escalate when

- The workload requires root, `privileged`, host mounts or extra capabilities.
- The base image license or maintenance status is unclear.
- GDAL/PROJ versions conflict between the system, the wheel and a required dependency.
- Target architecture or runtime profile affects the design and was not declared.
- Edge constraints (size, memory, offline operation) are stated but not quantified.

## 9. References

- `references/lattinus-code.md` §3 (SBOM, Twelve-Factor), §6.2, §10.7, §10.2
- `config/permissions.md` §6
- Provisional baseline (Notion Lattinus, OBS-STK-001, Draft 2026-09-14): Python `>=3.12`, `uv`, `ruff`. Promote to `references/engineering/infrastructure.md` (human action). Until then cite as `unverified`.
- Gap: `references/engineering/infrastructure.md` does not exist yet. Record in `memory/open-questions.md` when relevant to the task.