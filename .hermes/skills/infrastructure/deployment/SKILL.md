---
name: deployment
description: Write reproducible deployment definitions and CI/CD pipelines as code for Lattinus modules, including per-environment configuration, rollout strategy, documented rollback, and cloud vs edge deployment profiles. Use this skill whenever a task involves infrastructure as code, GitHub Actions workflows, release or promotion steps, environment configuration, rollout or rollback planning, or running a module on cloud or edge, even if the task only says "ship it" or "set up the pipeline". Produces definitions only. Applying, deploying or touching production is always done by humans.
---

# deployment

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-08 · **Owner agent:** `devops-sre` · **Category:** `skills/infrastructure/`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Scope

**Covers:** IaC definitions, environment config, CI/CD workflow files, rollout and rollback plans, deployment profiles (cloud, edge), release evidence.

**Does not cover:** applying or running any deployment (human), fixing the runtime/orchestrator/cloud without an approved ADR (`architect`), image contents (`containers`), security checklist and scans (`security`), telemetry definitions (`observability`).

## 2. Provisional Lattinus baseline

Sources: Notion Lattinus, `ci.yml` page (2026-07-28) and "Arquitetura da Plataforma". Cite as `unverified` until promoted to `references/`.

- CI/CD baseline is GitHub Actions with the stages lint, security scan, test, build, deploy. Triggers: push and PR on `main`, `develop`, `release/*`, plus manual dispatch. It uses minimal `permissions`, `concurrency` cancel-in-progress, and a `production` environment that can require manual approval.
- The platform is modular: each module is independently deployable in cloud or composable into a monolithic edge deployment.
- Managed Storage is S3-based. Lattinus Colab and Edge services are marked hypothetical in the source: do not design deployments for them unless the task says so.
- Runtime, cloud provider, orchestrator and IaC tool are **not decided**. They are `TBD` (`lattinus-code.md` §14).

## 3. Inputs (from `task.md`)

Module(s), target environments, deployment profile (cloud or edge), approved ADR on runtime (or none), configuration variables, rollout risk tolerance, who approves production.

## 4. Procedure

1. **Check the runtime decision.** If no approved ADR names the runtime, orchestrator and IaC tool, do not pick one. Write the runtime-agnostic parts (config schema, rollout and rollback plan, CI workflow) and request an ADR from the `architect` via the Orchestrator. Kubernetes or Terraform examples are `illustrative` only.
2. **Define deployable units and profile.** One unit per module with no hidden coupling. For edge, define the composition of units into a single deployment and what differs from cloud (storage, observability profile, offline behavior).
3. **Configuration.** Twelve-Factor: config in environment, separate from the artifact. Document each variable (name, type, default, required, sensitivity). Secrets are referenced by name from the platform mechanism (`TBD`), never by value.
4. **Promotion model.** Build once, promote the same immutable artifact (pinned by digest or version) through environments. Environment names and count are declared by the task.
5. **IaC rules.** Declarative, versioned, reproducible, no manual steps, no console-only changes. Drift is a defect. State storage and locking depend on the IaC tool (`TBD`).
6. **Rollout strategy.** Default rolling. Use canary or blue/green only when the risk justifies the cost, and say why. Define health gates tied to SLOs (from `observability`) and abort criteria.
7. **Data and pipelines.** Schema or contract changes use expand-then-contract and stay backward compatible. Pipeline changes keep jobs idempotent and re-runnable; describe the backfill path.
8. **Rollback.** Document the exact path: which artifact version to return to, which config to restore, what happens to data written meanwhile, and how to verify recovery. The PR itself MUST be revertible as a unit (`lattinus-code.md` §4.3).
9. **CI/CD as code.** Start from the baseline stages. Rules:
   - Pin third-party actions to a full commit SHA. The baseline template uses a moving ref for secret detection and major tags elsewhere: flag this and propose pinning.
   - Declare `permissions` per job, minimal. Prefer short-lived federated credentials over static keys (provider `TBD`).
   - Deploy job: only from the protected branch, behind a protected environment with required human reviewers (configured by humans in the repository).
   - Deploy commands in the template are placeholders. Replace them only after the runtime ADR; the agent writes them but never executes them.
   - No secret is echoed, no `pull_request` job receives deploy credentials.
10. **Validate statically.** YAML lint, workflow syntax check, IaC format/validate and offline manifest validation, using tools the task declares. Anything needing cloud credentials (plans, diffs against live state) is left for humans and listed under Evidence as "not run".
11. **Release notes for humans.** Provide an apply checklist: pre-checks, steps, health verification, rollback trigger, owner.

## 5. Deliverable checklist (`lattinus-code.md` §6.2, Infrastructure)

- [ ] Reproducible from code, no manual steps.
- [ ] Least privilege in pipeline and runtime identities (see `security`).
- [ ] Resource limits set in the definition.
- [ ] Rollback path documented and referenced by the PR.
- [ ] Config documented, secrets referenced by name only.
- [ ] Third-party actions pinned; job permissions minimal.
- [ ] Runtime assumptions linked to an approved ADR or declared and logged in `open-questions.md`.
- [ ] Evidence lists what was validated offline and what was not run.

## 6. Guardrails

- MUST NOT apply infrastructure, deploy, or touch production (`permissions.md` §6, Deny).
- MUST NOT trigger workflows, push images, or approve deployments.
- MUST NOT embed credentials, account ids or private endpoints in definitions.
- MUST NOT fix the runtime, cloud or IaC tool without an approved ADR.
- `git` gate before any commit; `dependencies` gate for any tool or action added.

## 7. Escalate when

- The task needs the runtime or cloud provider and no ADR exists.
- Production approval path or environment protection is undefined.
- Rollback cannot restore data (irreversible migration) and no human decision is recorded.
- Edge constraints (connectivity, hardware, update channel) are required and unspecified.

## 8. References

- `references/lattinus-code.md` §4, §6.2, §10, §11
- `config/permissions.md` §6; `policies/safety.md`, `policies/git.md`, `policies/dependencies.md`
- Notion Lattinus: `ci.yml` page; "Arquitetura da Plataforma". Promote to `references/engineering/infrastructure.md` (human action).