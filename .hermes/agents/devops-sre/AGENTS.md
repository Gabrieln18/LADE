# AGENTS.md — devops-sre (manifest)

> **Version:** 0.2.0 · Scope: agent `devops-sre` · Subset of root `AGENTS.md` §3 and `config/permissions.md`.

```yaml
agent: devops-sre
skills:
  - skills/infrastructure/containers
  - skills/infrastructure/observability
  - skills/infrastructure/deployment
  - skills/infrastructure/security
references:
  - references/lattinus-code.md           # §6.2 Infra, §10 Security, §11 Observability
  - references/architecture.md
  - references/platform/*                 # to know what is being deployed
  - references/engineering/data.md        # pipeline operability
  - references/engineering/python.md      # toolchain (uv) for images
  - agents/devops-sre/references/index.md
tools: [fs.read, fs.write, shell.sandbox, quality.runner, git.local, container.build]
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/feature-development.md      # when infra/ops impact
  - workflows/new-module.md               # container, signals, runbook
  - workflows/architecture-change.md      # implementation after approved ADR
  - workflows/release.md                  # SBOM, provenance, rollback plan
  - workflows/bug-investigation.md        # operational incidents
templates: [templates/implementation-plan.md, templates/task.md]
can_write:
  - infrastructure artifacts (container, observability, deployment, security definitions)   # paths in task.md
  - runbook inputs, as part of its infrastructure artifacts
  - memory/open-questions.md              # append-only
cannot:
  - apply infra, deploy, touch production
  - read/create/use secrets or credentials
  - push, mark PR ready, merge (draft PR is orchestrator-only)
  - standalone documentation -> technical-writer
```
