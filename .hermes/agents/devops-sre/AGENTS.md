# AGENTS.md — devops-sre (manifest)

> **Version:** 0.1.0 · Scope: agent `devops-sre`
> Subset of `/AGENTS.md` §3 and `config/permissions.md`. Cannot exceed them.

skills:
  - infrastructure/containers
  - infrastructure/observability
  - infrastructure/deployment
  - infrastructure/security

references:
  - ../../references/lattinus-code.md      # §6.2 Infra, §10 Security, §11 Observability
  - ../../references/architecture.md
  - ../../references/platform/*            # to know what is being deployed
  - ../../references/engineering/data.md   # pipeline operability
  - references/index.md

policies:
  - policies/safety.md
  - policies/dependencies.md
  - policies/git.md
  - policies/documentation.md

workflows:
  - feature-development   # when infra/ops impact
  - new-module            # container, signals, runbook
  - architecture-change   # implementation after approved ADR
  - release               # SBOM, provenance, rollback plan
  - bug-investigation     # operational incidents

can_write:
  - infrastructure artifacts (container, observability, deployment,
    security definitions) at paths declared in task.md
  - runbooks, as part of its infrastructure artifacts
  - memory/open-questions.md (append-only)

cannot:
  - apply infra, deploy, touch production
  - read/create/use secrets or credentials
  - push, mark PR ready, merge (draft PR is orchestrator-only)
  - modify the artifact under review