# documentation.md — documentation engineering reference

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `references/engineering/documentation.md`
> Standards for documents produced for Lattinus Code. Procedure lives in `skills/documentation/*`; templates in `templates/`. Only humans edit this file.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Document classes and identifiers

| Class | Id format | Template | Owner |
|-------|-----------|----------|-------|
| Architecture decision | `ADR-NNNN` | `templates/adr.md` | architect (proposal) |
| Design document | `DSG-NNNN` | `templates/design.md` | architect |
| Interface contract | `IF-NNN` | `templates/design.md` | architect |
| Event contract | `EVT-NNN` | `templates/design.md` | architect |
| Architecture overview | `ARQ-NNN` | `templates/design.md` | architect |
| Stack decision | `STK-NNN` | `templates/adr.md` | architect |
| Research note | `RSH-NNN` | `templates/research.md` | any agent |
| Runbook | `RB-NNN` | `templates/runbook.md` | devops-sre |
| Review report | `REV-NNN` | `templates/review.md` | reviewer |

Ids are sequential per class and never reused. The numbering authority is the repository where the document lives.

## 2. Required structure

Every document carries, in this order:

1. **Traceability header** (`AGENTS.md` §10): `task_id`, `produced_by`, `review_level`, `references`, `adr`, `gates`, `status`, `assumptions`.
2. **Status:** `draft | proposed | approved | superseded | rejected`.
3. **Context:** why the document exists, in two or three sentences.
4. **Body:** the class's own sections, from its template.
5. **Open points:** `{{TBD}}` placeholders or `Q-NNN` ids. An unresolved point MUST NOT be silently omitted.

## 3. Language and terminology

1. Internal files are written in English; `output_language` in `task.md` governs the delivered document and defaults to PT-BR.
2. Code identifiers, endpoint names, field names and dataset names stay in English.
3. Use Lattinus terminology from `references/lattinus.md` §2. Never coin a synonym for a term that already exists.
4. Spatial units and CRS are always explicit; a number without a unit is a defect.

## 4. Evidence rules

1. Every command, path, variable and endpoint is verified in the repository or labelled `unverified`.
2. Never invent an API, a flag, a version or a dataset property (`SOUL.md` §3).
3. A statement about behaviour cites the file and section that defines it.
4. Facts, assumptions and recommendations are kept in separate paragraphs or labelled inline.

## 5. Status and change rules

1. Changing the `Status`, the owner or a contract field of an existing document requires human approval (`policies/documentation.md`).
2. A superseded document stays in place with its `Status` changed and a pointer to its replacement.
3. Deleting a document requires the safety gate and a human.
4. A change to a normative document updates the changelog in the same change set.

## 6. Open parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Canonical `CHANGELOG.md` location in Lattinus Code | Maintainers |
| `docs/` layout and navigation | Maintainers |
| Documentation tooling and build | Maintainers / devops-sre |
| Deprecation window for published documents | Maintainers |
