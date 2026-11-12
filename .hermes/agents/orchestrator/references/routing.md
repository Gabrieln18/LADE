# routing.md — task → agent

| Task type | Primary | Supporting | Workflow | Recommend review |
|-----------|---------|-----------|----------|------------------|
| New feature (code) | software-engineer | architect (if design impact), technical-writer (repo docs) | feature-development | standard |
| Bug | software-engineer | domain agent by component | bug-investigation | human-only ok |
| Architecture change / ADR | architect | affected domain agents | architecture-change | standard |
| New module/service | architect → software-engineer | devops-sre, technical-writer | new-module | standard |
| Ingestion / pipeline / contract | data-engineer | geospatial-engineer | feature-development | standard |
| Raster/vector/CRS/EO/Dask/Sedona | geospatial-engineer | data-engineer | feature-development | standard |
| Agent / LLM / eval | ai-engineer | architect | feature-development | standard |
| Container / deploy / observability / security | devops-sre | software-engineer | feature-development | standard |
| Docs only (README, CONTRIBUTING, runbook, changelog, guides) | technical-writer | author of the subject | feature-development, docs-only variant (§4.1) | human-only ok |
| Review request | reviewer | — | code-review | n/a |
| Release | orchestrator (coordination) | devops-sre, technical-writer, reviewer | release | standard |

## Rules
1. Multi-domain task → split into subtasks, one per artifact class (`permissions.md` §5.1).
2. Needs a new dependency → include dependencies gate + human approval in the plan.
3. Needs a manifest/skill/path not granted → ESCALATE, don't improvise.
4. No row matches or confidence is low → ask the requester (one grouped question), do not guess.
5. The Reviewer is never routed as author of the artifact it will review, and never authors documentation.
6. Documentation artifacts are written by `technical-writer` and reviewed by the Reviewer (standard) or a human (human-only). Docs co-located with code stay with the executor.
7. Never route documentation to the agent that will review it.
