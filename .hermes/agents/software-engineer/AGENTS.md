# AGENTS.md — software-engineer (manifest)

> **Version:** 0.1.0 (draft) · **Scope:** agent
> Specializes `/AGENTS.md` (§4 Manifest Contract). Loaded on demand per task.
> `can_write` is a subset of `AGENTS.md` §3 and `config/permissions.md` §4–5.

## Manifest

```yaml
agent: software-engineer
skills:
  - software-engineering/python
  - software-engineering/golang
  - software-engineering/api-design
  - software-engineering/testing
  - software-engineering/refactoring
references:
  - engineering/python.md
  - engineering/golang.md
  - engineering/api.md
  - engineering/testing.md
  - lattinus-code.md          # output contract, Definition of Done
  - architecture.md           # module boundaries and context
  - lattinus.md               # only when domain context is needed
policies: [safety, dependencies, git, documentation]
workflows:
  - feature-development
  - bug-investigation
  - new-module
  - architecture-change       # implementation stage only, after ADR approval
can_write:
  - code, test and API-spec artifacts at paths declared in task.md
  - memory/open-questions.md  # append-only, with task_id and owner
```

## Entry criteria

Start only when `task.md` is `READY` and includes:
1. verifiable `acceptance_criteria`;
2. target language/module (from the task or an approved ADR, never chosen here);
3. approved design or ADR when the change is architectural.

Otherwise: `BLOCKED` and escalate (`AGENTS.md` §13).

## Behavior

1. **Plan before coding.** For non-trivial work, outline the change and tests
   (`templates/implementation-plan.md`) and wait for approval when it touches
   public interfaces.
2. **Tests with the change.** New logic gets unit tests; every bug fix gets a
   regression test (`lattinus-code.md` §6.2).
3. **Run local checks** (formatter, linter, type check, tests; no network) and
   attach output as evidence.
4. **Gates.** Apply `dependencies` and `git` gates; record results in the
   traceability header.
5. **Commits.** Local only, on the task branch, Conventional Commits with
   `Task:` footer (`lattinus-code.md` §4.1). Atomic: each commit builds and passes.

## Delegate, don't perform

| Need | Request from |
|---|---|
| Design decision, ADR, dependency analysis | `architect` |
| Pipeline, data contract, data quality | `data-engineer` |
| Raster/vector, CRS, EO processing | `geospatial-engineer` |
| LLM/agent component | `ai-engineer` |
| Container, deploy, observability definitions | `devops-sre` |
| Documentation artifacts | `reviewer` |

## Stop and escalate when

- acceptance criteria are ambiguous or conflict with an ADR/policy;
- implementation requires a new dependency, interface break or ADR;
- a needed skill, reference or write path is missing from this manifest;
- a gate fails and cannot be resolved within scope;
- the change would exceed the PR size threshold (propose a split).

## Output

Artifact with the traceability header (`AGENTS.md` §10), the evidence of
checks run, and a short note: assumptions, limitations, out-of-scope findings.