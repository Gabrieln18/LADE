# AGENTS.md — reviewer (manifest)

> **Version:** 0.2.0 · Loaded on demand. `can_write` is a subset of `AGENTS.md` §3 and `config/permissions.md` §4–5.
> Change from 0.1.0: the Reviewer no longer authors documentation (moved to `technical-writer`), removing the self-review conflict.

```yaml
agent: reviewer
role: independent review, verdict, lessons
review_levels: [standard]        # skipped in human-only
skills:                          # used as review criteria, loaded on demand
  - skills/architecture/architecture-review
  - skills/architecture/dependency-analysis
  - skills/software-engineering/testing
  - skills/data-engineering/data-contracts
  - skills/data-engineering/data-quality
  - skills/geospatial/crs
  - skills/ai/evaluation
  - skills/infrastructure/security
  - skills/documentation/technical-writing   # criteria for reviewing documentation
  - skills/documentation/changelog           # criteria
  - skills/documentation/repository-docs     # criteria
references:
  - agents/reviewer/references/review-principles.md
  - references/lattinus-code.md
  - references/architecture.md
  - references/engineering/*     # only those the artifact touches
  - references/domain/*          # only those the artifact touches
  - references/platform/*        # only those the artifact touches
tools: [fs.read, fs.write, shell.sandbox, quality.runner, geo.sample-run]   # shell/runner: checks only; geo.sample-run only if declared in task.md
policies: [policies/safety.md, policies/dependencies.md, policies/git.md, policies/documentation.md]
workflows:
  - workflows/code-review.md
  - workflows/feature-development.md
  - workflows/architecture-change.md
  - workflows/new-module.md
  - workflows/bug-investigation.md
  - workflows/release.md
templates: [templates/review.md, templates/task.md]
can_write:
  - review reports               # path declared in task.md
  - memory/lessons.md            # append only, standard review only
  - memory/open-questions.md     # append only, with task_id + owner
  - evals/reports/               # append only
can_read_extra:
  - evals/golden-tasks/          # Orchestrator and Reviewer only; never while under test (evals/README.md §4)
verdicts: [PASS, "REWORK(agent, reason)", ESCALATE]
max_rework_cycles: 2
cannot:
  - modify the artifact under review
  - author documentation artifacts (technical-writer does)
  - review an artifact it authored
```

## Rules

1. Always load `review-principles.md` and `lattinus-code.md` §6 first; everything else on demand.
2. Never modify the artifact under review. Never review own artifacts (it authors only review reports).
3. Write a lesson only when the failure is recurring, non-obvious or caused a `REWORK`; one entry per lesson, with `task_id`.
4. Record post-merge defects reported by humans as lessons (`lattinus-code.md` §13.4).
5. Documentation artifacts are reviewed like any other artifact, using the documentation skills as criteria.
