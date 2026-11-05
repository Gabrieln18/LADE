# AGENTS.md — orchestrator (manifest)

skills:
  - ai/multi-agent            # on demand, only for non-trivial parallel plans
references:
  - agents/orchestrator/references/orchestration.md
  - agents/orchestrator/references/routing.md
  - references/lattinus.md
  - references/lattinus-code.md
  - references/architecture.md
policies: [safety, dependencies, git, documentation]
workflows: [feature-development, bug-investigation, architecture-change,
            new-module, code-review, release]
can_write:
  - task.md instances
  - memory/project-state.md
  - memory/decisions.md       # approved ADR only
  - memory/conventions.md     # human-approved only
  - memory/open-questions.md  # append-only
actions:
  - push task branch and open DRAFT PR (gate: git)
read_extra:
  - agents/*                  # routing
  - evals/golden-tasks/       # read-only