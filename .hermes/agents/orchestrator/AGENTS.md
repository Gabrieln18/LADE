# AGENTS.md — orchestrator (manifest)

> **Version:** 0.2.0 · Scope: agent `orchestrator` · Format: root `AGENTS.md` §4 (all paths repo-root relative).

```yaml
agent: orchestrator
skills:
  - skills/ai/multi-agent            # on demand, only for non-trivial parallel plans
references:
  - agents/orchestrator/references/orchestration.md
  - agents/orchestrator/references/routing.md
  - references/lattinus.md
  - references/lattinus-code.md
  - references/architecture.md
tools: [fs.read, fs.write, git.draft-pr, mcp.notion.search, mcp.notion.fetch]
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/feature-development.md
  - workflows/bug-investigation.md
  - workflows/architecture-change.md
  - workflows/new-module.md
  - workflows/code-review.md
  - workflows/release.md
templates: [templates/task.md]
can_write:
  - task.md instances
  - memory/project-state.md
  - memory/decisions.md        # approved ADR only
  - memory/conventions.md      # human-approved only
  - memory/open-questions.md   # append-only
actions:
  - push task branch and open DRAFT PR (gate: git)
read_extra:
  - agents/*                   # routing
  - evals/golden-tasks/        # read-only; see evals/README.md §4 (isolation) before running evals
cannot:
  - domain artifacts of any other class
  - approve or review what it routed
  - mark PR ready, approve, merge
```
