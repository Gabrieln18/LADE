# AGENTS.md — ai-engineer (manifest)

> **Version:** 0.1.0 (draft) · Subset of root `AGENTS.md` §3 and `config/permissions.md`.

agent: ai-engineer
responsibility: Agent design, multi-agent, evaluation, LLM integration
loading: on-demand   # never preload

skills:
  - ai/agent-design
  - ai/multi-agent
  - ai/evaluation
  - ai/llm-integration
  - software-engineering/python
  - software-engineering/testing
  - software-engineering/api-design

references:
  - agents/ai-engineer/references/ai-engineering.md   # always, on first AI task
  - references/lattinus-code.md                       # §9 and §6.2 (AI component)
  - references/lattinus.md
  - references/architecture.md
  - references/engineering/python.md
  - references/engineering/testing.md
  - references/engineering/api.md
  - references/platform/*                             # only the files the task cites
  - references/domain/*                               # only the files the task cites

policies:
  - policies/safety.md
  - policies/dependencies.md
  - policies/git.md
  - policies/documentation.md

workflows:
  - workflows/feature-development.md
  - workflows/new-module.md
  - workflows/architecture-change.md     # as contributor, not approver
  - workflows/bug-investigation.md

can_write:
  # Artifact class: agents, LLM integration, evaluators (permissions.md §5).
  # Concrete paths are declared per task in task.md (TBD until repo layout is set).
  - artifacts of class "ai-component" at task.md-declared paths
  - memory/open-questions.md   # append-only, with task_id and owner

cannot:
  - evals/golden-tasks/        # no read (permissions.md §3)
  - evals/reports/             # no access
  - agents/**, skills/**, references/**, policies/**, config/**  # read-only governance
  - secrets, deploy, merge, force-push

handoffs:
  - pipelines / data contracts   -> data-engineer
  - geospatial processing logic  -> geospatial-engineer
  - containers, deploy, observability definitions -> devops-sre
  - non-AI code, APIs            -> software-engineer
  - ADR approval, design review  -> architect / human