# git.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-11 · **Location:** `policies/git.md`
> Blocking gate. Prevails over agent instructions (`AGENTS.md` §2). Implements `lattinus-code.md` §4 and `permissions.md` §6.
> Key words **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 2119. Only humans edit this file.

## 1. Purpose and Trigger

Gate **Git** (`AGENTS.md` §7). Applies **before** any commit, push or PR, at every review level.

| Step | Who may do it | Gate |
|------|---------------|------|
| Local commit on task branch | Authoring agents | Git (§4) |
| Push task branch, open **draft** PR | `orchestrator` | Git (§4 and §5) |
| Mark PR ready, approve, merge | **Humans only** | n/a |
| Force-push, rewrite shared history, delete remote branches | **Nobody** | Denied |

## 2. Repository Parameters

Repository, base branch, commit signing and PR size threshold are `TBD` (`lattinus-code.md` §14). Agents MUST NOT assume them. If a needed parameter is missing, the agent stops and escalates.

## 3. Rules

### 3.1 Branches

| ID | Rule |
|----|------|
| GIT-01 | Work only on a task branch named `<type>/<task_id>-<short-slug>`, e.g. `feat/LADE-20261111-001-ndvi-pipeline`. |
| GIT-02 | Never commit or push directly to the base branch. |
| GIT-03 | One branch maps to one `task_id` (or one parent task with declared subtasks). |
| GIT-04 | Keep branches short-lived. Sync with base (rebase or merge) before opening the PR. |

### 3.2 Commits

| ID | Rule |
|----|------|
| GIT-10 | Messages follow **Conventional Commits 1.0.0**, in English. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`. |
| GIT-11 | Footer MUST include `Task: <task_id>`, and `ADR: ADR-NNNN` when applicable. |
| GIT-12 | Breaking change: `!` after the type or a `BREAKING CHANGE:` footer, plus the ADR reference. |
| GIT-13 | Commits are **atomic**: each one builds and passes tests. |
| GIT-14 | Dependency changes go in their own commit (Dependencies gate DEP-13). |
| GIT-15 | Commit signing follows repository policy (`TBD`). |
| GIT-16 | No hook bypass (`--no-verify`) and no changes to git config, hooks or ignore rules unless the task requires it. |

### 3.3 Content

| ID | Rule |
|----|------|
| GIT-20 | **Scope check.** The staged diff contains only files within the manifest's `can_write` and the paths declared in `task.md`. Unrelated changes are removed or reported. |
| GIT-21 | **Quality check.** Formatter, linter, type check and tests pass locally (no network). Results are kept as evidence. |
| GIT-22 | **No secrets or sensitive data** in the diff: credentials, tokens, keys, `.env` files, personal data, absolute local paths. Review the staged diff before committing. |
| GIT-23 | **No unplanned artifacts:** build output, caches, large binaries or datasets, unless declared in `task.md` and justified. |
| GIT-24 | **Traceability.** Every artifact in the diff starts with the traceability header (`AGENTS.md` §10). |

### 3.4 History

| ID | Rule |
|----|------|
| GIT-30 | Amend or rebase is allowed **only** on local commits not yet pushed. |
| GIT-31 | After a push, corrections go forward as new commits. No force-push (`--force`, `--force-with-lease`). |
| GIT-32 | Never rewrite, amend or delete commits made by others. |
| GIT-33 | Never delete remote branches or tags. |

### 3.5 Push and Pull Request

| ID | Rule |
|----|------|
| GIT-40 | Push is allowed to the task branch only, by the `orchestrator`, after the Safety gate (SAF-23, network allowlist). |
| GIT-41 | Open PRs as **draft**. A human marks ready and merges. |
| GIT-42 | One PR maps to one `task_id`. Above the size threshold (`TBD`), propose a split. |
| GIT-43 | The PR is reversible as a unit (`lattinus-code.md` §4). |
| GIT-44 | The PR description follows the template in `lattinus-code.md` §12.1 (default `PT-BR`), including assumptions, limitations, impact, rollback and dependencies. |
| GIT-45 | Before opening: Definition of Done (`lattinus-code.md` §6) verified, all other gates recorded as `pass` or `na`, ADR approved if architectural, review verdict recorded (`PASS`, or human sign-off for `human-only`). |

## 4. Gate Checklist: Commit

- [ ] On a task branch with a valid name (GIT-01, GIT-02).
- [ ] Commit message is valid, with `Task:` footer (GIT-10, GIT-11).
- [ ] Commit is atomic and passes checks (GIT-13, GIT-21).
- [ ] Staged diff is within scope (GIT-20).
- [ ] No secrets, personal data, absolute paths or unplanned artifacts (GIT-22, GIT-23).
- [ ] Traceability headers present (GIT-24).
- [ ] No history rewrite after push (GIT-30, GIT-31).

## 5. Gate Checklist: Push and Draft PR

- [ ] All items in §4 hold for every commit in the branch.
- [ ] Other gates recorded in the traceability header (safety, dependencies, documentation).
- [ ] PR is **draft**, maps to one `task_id`, and uses the §12.1 template (GIT-41 to GIT-44).
- [ ] Pre-open conditions in GIT-45 are met.

The acting agent records `git: pass | na`. `na` only when the task involves no commit, push or PR. Any unchecked item sets the task to `BLOCKED`.

## 6. Open Parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Repository name and base branch | Maintainers |
| Commit signing policy | Maintainers |
| CI system and required checks | Maintainers / devops-sre |
| PR size threshold | Maintainers |
| Pre-commit hook set | Maintainers |
| Remote and push credentials mechanism (without agent access to secrets) | devops-sre |