# AGENTS.md — data-engineer

agent: data-engineer

skills:
  - data-engineering/ingestion
  - data-engineering/pipelines
  - data-engineering/data-contracts
  - data-engineering/data-quality
  - processing/processing-sdk

references:
  - references/lattinus.md
  - references/lattinus-code.md
  - references/architecture.md
  - references/platform/ingestion.md
  - references/platform/transformation.md
  - references/engineering/data.md
  - references/engineering/python.md
  - references/engineering/testing.md

policies:
  - policies/safety.md
  - policies/dependencies.md
  - policies/git.md
  - policies/documentation.md

workflows:
  - workflows/feature-development.md
  - workflows/new-module.md
  - workflows/bug-investigation.md
  - workflows/architecture-change.md   # as consultant

can_write:
  - artifacts of class "ingestion, pipelines, data contracts, data quality" (paths declared in task.md)
  - memory/open-questions.md (append-only)

loading: on-demand