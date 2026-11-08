<!--
templates/contributing.md · v0.1.0 · Used by: skills/documentation/repository-docs
Derived from Notion "CONTRIBUTING.MD". Where it differs, references/lattinus-code.md §4.1 and §12 prevail
(branch naming, commits, draft PR, footer). Do not copy generic fork or branch conventions.
- Replace {{PLACEHOLDER}} with evidence or {{TBD}}. Commands must be verified in the repository or labeled `unverified`.
- Remove this comment and add the traceability header (AGENTS.md §10) as an HTML comment.
-->

# Contributing

Thank you for contributing to {{PROJECT_NAME}}. Follow the guidelines below.

---

## 🛠️ Getting started

1. Clone the repository: `{{CLONE_COMMAND}}`
2. Install dependencies: `{{INSTALL_COMMAND}}`
3. Create a branch from `{{BASE_BRANCH}}` using the pattern `<type>/<task_id>-<short-slug>`.
   Example: `feat/LADE-20261103-001-ndvi-pipeline`

## 📏 Code and commit standards

- **Style:** run the project formatter, linter and type checker before committing: `{{LINT_COMMAND}}`, `{{TYPECHECK_COMMAND}}`.
- **Commits:** [Conventional Commits 1.0.0](https://www.conventionalcommits.org/), in English. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`.
- **Footer:** `Task: <task_id>` and, when applicable, `ADR: ADR-NNNN`.
- **Breaking change:** `!` after the type or a `BREAKING CHANGE:` footer, plus the ADR reference.
- **Atomic commits:** each commit builds and passes tests.

Example:

```text
feat(ingestion): add Sentinel-2 asset validation

Task: LADE-20261103-001
```

## 🧪 Tests and quality

1. All tests pass: `{{TEST_COMMAND}}`
2. New logic has unit tests; every bug fix has a regression test.
3. Documentation and `CHANGELOG.md` are updated when behavior or interfaces change.
4. No secrets, credentials or personal data in code, history, logs or fixtures.

## 🔀 Pull requests

1. Open a **draft** PR. A maintainer moves it to ready and merges.
2. One PR maps to one task. Keep it small, reversible and reviewable.
3. Fill the PR description: summary, traceability, change type, how to test, evidence, assumptions and limitations, impact and rollback, dependencies.
4. Adding or changing a dependency needs justification (purpose, license, maintenance, alternatives) and human approval.

## 🧭 Decisions

Architectural changes need an approved ADR before implementation. Proposals go through {{RFC_OR_ADR_PROCESS}}.

## 🤝 Conduct

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).