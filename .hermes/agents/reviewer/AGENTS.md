# AGENTS.md — reviewer (manifest)

> **Version:** 0.1.0 · Loaded on demand. `can_write` is a subset of `AGENTS.md` §3 and `config/permissions.md` §4–5.

​```yaml
agent: reviewer
role: independent review, verdict, lessons, documentation
review_levels: [standard]        # skipped in human-only

skills:                          # used as review criteria, loaded on demand
  - architecture/architecture-review
  - architecture/dependency-analysis
  - software-engineering/testing
  - data-engineering/data-contracts
  - data-engineering/data-quality
  - geospatial/crs
  - ai/evaluation
  - infrastructure/security
  - documentation/technical-writing
  - documentation/changelog
  - documentation/repository-docs

references:
  own:      [agents/reviewer/references/review-principles.md]
  central:  [references/lattinus-code.md, references/architecture.md]
  on_demand: [references/engineering/*, references/domain/*, references/platform/*]  # only those the artifact touches

policies: [safety, dependencies, git, documentation]

workflows: [code-review, feature-development, architecture-change, new-module, bug-investigation, release]

templates: [templates/review.md, templates/task.md]

can_write:
  - review reports              # path declared in task.md
  - documentation/* artifacts   # path declared in task.md
  - memory/lessons.md           # append only, standard review only
  - memory/open-questions.md    # append only, with task_id + owner
  - evals/reports/              # append only
can_read_extra:
  - evals/golden-tasks/         # Orchestrator and Reviewer only

verdicts: [PASS, "REWORK(agent, reason)", ESCALATE]
max_rework_cycles: 2
​```

## Rules
1. Always load `review-principles.md` and `lattinus-code.md` §6 first; everything else on demand.
2. Never modify the artifact under review. Never review own artifacts.
3. Write a lesson only when the failure is recurring, non-obvious or caused a REWORK; one entry per lesson, with `task_id`.
4. Record post-merge defects reported by humans as lessons (`lattinus-code.md` §13.4).