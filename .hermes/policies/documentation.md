# documentation.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-11 · **Location:** `policies/documentation.md`
> Blocking gate. Prevails over agent instructions (`AGENTS.md` §2). Implements `lattinus-code.md` §6.1 and §6.2.
> Key words **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 2119. Only humans edit this file.

## 1. Purpose and Trigger

Gate **Documentation** (`AGENTS.md` §7). Applies **before closing an artifact with documentation impact**, at every review level.

An artifact has documentation impact when it changes any of:

- behavior or public interfaces (API, CLI, function signatures);
- configuration or environment requirements;
- data contracts, schemas or pipeline lineage;
- architecture, boundaries or dependencies;
- operations (run, monitor, retry, backfill, rollback);
- agent definitions, prompts, tools or evaluation criteria.

## 2. Rules

| ID | Rule |
|----|------|
| DOC-01 | **Assess impact.** Every artifact states `documentation impact: yes | no`, with a one-line reason. `no` is a valid answer, and it makes the gate `na`. |
| DOC-02 | **Same delivery.** Documentation for a change ships in the same PR as the change. No "docs later". |
| DOC-03 | **Cover the right documents.** Update every affected item in §3. |
| DOC-04 | **Accuracy.** Documentation is verified against the current code or artifact. Unverified statements are labeled `unverified`. Never document planned or assumed behavior as fact (`SOUL.md` §3). |
| DOC-05 | **Examples.** Runnable and tested, or marked **illustrative**. |
| DOC-06 | **Single source.** Link to `references/`, `templates/` and ADRs instead of copying their content (`SOUL.md` §2.2). |
| DOC-07 | **Citations.** Domain claims cite the supporting `references/` file or task section (`AGENTS.md` §10.3). |
| DOC-08 | **Language.** Internal files (agents, skills, policies, templates) in **English**. Output documents in the task's `output_language` (default `PT-BR`). Code identifiers and technical terms stay in English (`AGENTS.md` §10.1). |
| DOC-09 | **No sensitive content.** No secrets, personal data or absolute local paths. |
| DOC-10 | **Ownership.** Each document names an owner (maintainer or team) and, for snapshots, the snapshot date. `references/lattinus.md` MUST carry its Notion snapshot date. |
| DOC-11 | **Naming.** Lowercase `kebab-case` for files and folders. ADR ids are sequential: `ADR-NNNN` (`AGENTS.md` §10.4). |
| DOC-12 | **Concise, task-oriented.** State what was done and why. Avoid restating code or other documents. |
| DOC-13 | **Reference gaps.** If a needed reference is missing or outdated, say so in the artifact and record it in `memory/open-questions.md` (`AGENTS.md` §12.3). |

## 3. Documentation by Change Type

| Change | Required documentation |
|--------|------------------------|
| New or changed public function or module | Typed signatures and docstrings; module-level purpose |
| HTTP or async API | OpenAPI or AsyncAPI spec updated and valid; compatibility, error model and versioning impact stated |
| Data pipeline or contract | Data contract; lineage (source to output); quality checks and failure behavior; backfill procedure |
| Geospatial processing | CRS, resolution, nodata, temporal metadata, chunking or partitioning, accuracy limits, licensing (`lattinus-code.md` §8) |
| AI component | Prompt, tool and model versions; evaluation result and thresholds; failure modes (`lattinus-code.md` §9) |
| Infrastructure | Reproduction steps from code, rollback path, resource limits, runbook |
| Architectural decision | ADR (`templates/adr.md`), approved by a human before implementation |
| User-visible or interface change | `CHANGELOG.md` entry in Keep a Changelog format (`TBD`, file to be created) |
| Dependency change | PR section "Dependências" and updated SBOM when applicable |
| Operational change | Runbook: run, monitor, retry, backfill, roll back |

## 4. Responsibility

| Documentation type | Written by |
|--------------------|------------|
| Docstrings, code comments, API specs, data contracts, runbook inputs, changelog entry | The authoring agent, as part of its artifact |
| ADR proposals | `architect` |
| Standalone documentation artifacts | `reviewer` (`permissions.md` §5) |

Rules:
1. The authoring agent MUST NOT leave documentation impact to the Reviewer. If a standalone document is needed, the Orchestrator creates a `task.md` for it.
2. The Reviewer verifies this gate but MUST NOT modify the artifact under review (`permissions.md` §5.2). Missing documentation returns as `REWORK(agent, reason)`.
3. In `human-only` review, the Reviewer pass is skipped, but the gate still applies. Standalone documentation in that mode is `TBD` (§6).

## 5. Gate Checklist

The acting agent records `documentation: pass | na` in the traceability header.

- [ ] Documentation impact assessed and stated (DOC-01).
- [ ] If impact is `yes`: every affected item in §3 is updated in the same PR (DOC-02, DOC-03).
- [ ] Content verified against the current artifact; unverified items labeled (DOC-04).
- [ ] Examples runnable or marked illustrative (DOC-05).
- [ ] Citations and links used instead of copies (DOC-06, DOC-07).
- [ ] Language, naming and owner follow DOC-08, DOC-10 and DOC-11.
- [ ] No secrets, personal data or absolute local paths (DOC-09).
- [ ] Reference gaps recorded (DOC-13).

`na` only when impact is `no`. Any unchecked item with impact `yes` sets the task to `BLOCKED`.

## 6. Open Parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| `CHANGELOG.md` location and creation | Maintainers |
| Documentation location in Lattinus Code (`docs/` layout) | Maintainers |
| Who writes standalone documentation in `human-only` reviews | Maintainers |
| Documentation tooling (linting, link checks, API spec validation) | Maintainers / devops-sre |