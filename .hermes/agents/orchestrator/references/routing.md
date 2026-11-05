# routing.md — task → agent

| Task type | Primary | Supporting | Workflow | Recommend review |
|-----------|---------|-----------|----------|------------------|
| New feature (code) | software-engineer | architect (if design impact) | feature-development | standard |
| Bug | software-engineer | domain agent by component | bug-investigation | human-only ok |
| Architecture change / ADR | architect | affected domain agents | architecture-change | standard |
| New module/service | architect → software-engineer | devops-sre | new-module | standard |
| Ingestion / pipeline / contract | data-engineer | geospatial-engineer | feature-development | standard |
| Raster/vector/CRS/EO/Dask/Sedona | geospatial-engineer | data-engineer | feature-development | standard |
| Agent / LLM / eval | ai-engineer | architect | feature-development | standard |
| Container / deploy / observability / security | devops-sre | software-engineer | feature-development | standard |
| Docs only | reviewer (documentation/*) | author of subject | code-review | human-only ok |
| Review request | reviewer | — | code-review | n/a |
| Release | orchestrator (coordination) | devops-sre, reviewer | release | standard |

## Rules
1. Multi-domain task → split into subtasks, one per class (permissions §5.1).
2. Needs a new dependency → include dependencies gate + human approval in plan.
3. Needs manifest/skill/path not granted → ESCALATE, don't improvise.
4. No row matches or confidence is low → ask requester (one grouped question), do not guess.
5. Reviewer is never routed as author of the artifact it will review.