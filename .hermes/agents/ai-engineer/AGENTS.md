# AGENTS.md — ai-engineer (manifest)

> **Version:** 0.2.0 · Subset of root `AGENTS.md` §3 and `config/permissions.md`.

```yaml
agent: ai-engineer
responsibility: Agent design, multi-agent, evaluation, LLM integration
loading: on-demand   # never preload
skills:
  - skills/ai/agent-design
  - skills/ai/multi-agent
  - skills/ai/evaluation
  - skills/ai/llm-integration
  - skills/software-engineering/python
  - skills/software-engineering/testing
  - skills/software-engineering/api-design
references:
  - agents/ai-engineer/references/ai-engineering.md   # always, on first AI task
  - references/lattinus-code.md                       # §9 and §6.2 (AI component)
  - references/lattinus.md
  - references/architecture.md
  - references/engineering/python.md
  - references/engineering/testing.md
  - references/engineering/api.md
  - references/platform/*                             # only files the task cites
  - references/domain/*                               # only files the task cites
tools: [fs.read, fs.write, shell.sandbox, quality.runner, git.local]
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/feature-development.md
  - workflows/new-module.md
  - workflows/architecture-change.md     # contributor, not approver
  - workflows/bug-investigation.md
templates: [templates/implementation-plan.md, templates/task.md]
can_write:
  - artifacts of class "ai-component"    # paths declared in task.md
  - docs co-located with its artifacts
  - memory/open-questions.md             # append-only, with task_id and owner
cannot:
  - evals/golden-tasks/, evals/reports/  # no access (permissions.md §3-4)
  - agents/**, skills/**, references/**, policies/**, config/**
  - secrets, deploy, merge, force-push
handoffs:
  - pipelines / data contracts            -> data-engineer
  - geospatial processing logic           -> geospatial-engineer
  - containers, deploy, observability     -> devops-sre
  - non-AI code, APIs                     -> software-engineer
  - README, runbook, changelog            -> technical-writer
  - ADR approval, design review           -> architect / human
```
