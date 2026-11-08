---
name: repository-docs
description: Creates and updates repository-level and component-level documentation for Lattinus Code, such as README, CONTRIBUTING, developer guides, runbooks (run, monitor, retry, backfill, rollback), pipeline documentation (lineage, data contract, quality checks) and API usage docs that point to OpenAPI. Use whenever a task adds or changes a module, pipeline, service, job or public interface and documentation must follow, when a README or runbook is missing or outdated, or when the user mentions README, CONTRIBUTING, runbook, docs folder, onboarding, how to run, backfill or rollback.
version: 0.1.0
---

# Repository Docs

Applies `technical-writing` first. Contract: `references/lattinus-code.md` §6.2, §8, §11, §12. Standard: `references/engineering/documentation.md`.

## Scope

- **In:** README, CONTRIBUTING, developer guide (DEV), runbooks, pipeline and API usage documentation, `docs/` layout, updating these when behavior changes.
- **Out:** ARQ, STK, IF, EVT, INT, RFC and ADR authoring (architecture skills), changelog entries (`changelog`), the OpenAPI spec itself (`software-engineering/api-design`).

## Inputs

- `task.md` and the code, configuration and CI files the docs describe (read them, do not assume).
- Authoritative documents to link: ARQ, STK, IF, EVT, ADR, DEV, COD, RFC (`documentation.md` §7).
- `references/platform/*` and `references/domain/*` for Lattinus terminology and layers.

## Procedure

1. **Choose the target** from the trigger.

   | Trigger | Document | Template |
   |---|---|---|
   | New repository or component | README | `templates/readme.md` |
   | Contribution flow defined or changed | CONTRIBUTING | `templates/contributing.md` |
   | New or changed service, job or pipeline | Runbook | `templates/runbook.md` |
   | Pipeline added or changed | Pipeline section (see step 5) | in README or runbook |
   | Public API added or changed | API usage section (see step 6) | in README |
   | Behavior, interface or operation changed | Update every affected document | — |

2. **Collect evidence from the repository.** Structure, entrypoints, config variables, test and lint commands, CI. Anything not found becomes `{{TBD}}` or the section is omitted. Never invent APIs, commands, variables, directories or metrics.
3. **README.** Fill `templates/readme.md`. It summarizes and links to the authoritative documents. It never makes architectural decisions. Status uses the fixed vocabulary and matches reality. Keep it short; move implementation, contractual or operational detail to specialized documents.
4. **CONTRIBUTING.** Fill `templates/contributing.md`. Branch, commit and PR rules come from `lattinus-code.md` §4.1 and §12 (draft PRs, `Task:` footer, Conventional Commits), not from generic models.
5. **Runbook and pipeline docs.** Required by `lattinus-code.md` §6.2 and §11. Cover: how to run, monitor, retry, backfill and roll back; behavior on partial failure; idempotency. For pipelines add: lineage (source → output), data contract reference, quality checks with failure behavior, backfill procedure. For geospatial data state CRS (EPSG), temporal metadata, resolution and nodata (§8), source licenses and attribution.
6. **API docs.** The OpenAPI/AsyncAPI spec is the source of truth. Document purpose, authentication overview, error model, versioning impact and a verified usage example, and link to the spec. Never copy the spec.
7. **Layout.** Default: `README.md`, `CONTRIBUTING.md`, `docs/runbooks/<component>.md`, `docs/assets/`. Final paths are `TBD` until the repository layout is confirmed (`permissions.md` §8); follow `task.md` when it declares them.
8. **Verify commands.** Run documented commands locally when permitted (`permissions.md` §6). If they cannot be run, label them `unverified` in the document and in the PR.
9. **Validate** with the checklist.

## Output

Documents at the paths declared in `task.md`, each with the traceability header (HTML comment for README, CONTRIBUTING and other root-level files). Documents carrying an ID follow `documentation.md` §2–3 and keep a change record.

## Checklist

- [ ] Every command, variable, path and endpoint was verified in the repository, or is labeled `unverified`.
- [ ] README links to ARQ/STK/IF/ADR instead of restating them; status matches the implementation.
- [ ] CONTRIBUTING matches `lattinus-code.md` §4.1 (branch, commits, draft PR, footer).
- [ ] Runbook covers run, monitor, retry, backfill, rollback, partial failure and idempotency.
- [ ] Pipeline docs include lineage, data contract, quality checks and backfill.
- [ ] Geospatial docs state CRS, temporal metadata, nodata and licenses.
- [ ] API docs link to the spec; no duplicated spec content.
- [ ] No secrets, tokens, internal hostnames or absolute local paths; secrets referenced by mechanism only.
- [ ] No unresolved `{{...}}` in required sections; optional empty sections removed.

## Boundaries

- Gates: `policies/documentation.md` before closing; `policies/safety.md` for credentials, hosts and anything external-facing.
- Does not create ARQ, STK, IF, EVT, INT, RFC or ADR content. It links to them or requests them from the Orchestrator via `task.md` (cross-class work is delegated, `permissions.md` §5).
- Does not change status, owner or contract fields of existing documents without human approval.
- Escalate when the repository contradicts an authoritative document, when the run or rollback procedure cannot be determined, or when no safe assumption exists.