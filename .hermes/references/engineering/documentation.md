# documentation.md — Documentation Standard (Lattinus)

> **Version:** 0.1.0 (draft) · **Snapshot date:** 2026-11-08 · **Location:** `references/engineering/documentation.md`
> Derived from Notion Lattinus › Arquitetura da Plataforma › "Templates Markdown | Padrão Documental Lattinus" (last edited 2026-09-04) and "Technical Docs Skill" (last edited 2026-09-01).
> Single source for documentation types, IDs, statuses, placeholders and README rules. Skills point here instead of repeating it.
> Where Notion differs from `AGENTS.md` or `lattinus-code.md`, the LADE files prevail. Differences are marked **[Δ]**.

## 1. Document types

| Type | Code | Use it to | Covered by |
|------|------|-----------|------------|
| Technical Overview | `OVERVIEW` | Describe a module (entry point, one per module) | `technical-writing` |
| Architecture | `ARQ` | Structure: boundaries, ownership | `architecture/*` |
| Stack | `STK` | Select technologies, runtime, dependencies | `architecture/*` |
| Interface Contract | `IF` | Specify contracts | `architecture/*` |
| Event Contract | `EVT` | Specify asynchronous events | `architecture/*` |
| Codebook | `COD` | Normalize operational vocabulary and naming | `technical-writing` (class `TBD`) |
| Developer Guide | `DEV` | Guide implementation and local development | `repository-docs` |
| Architecture Decision Record | `ADR` | Record a decision | `architecture/adr` |
| Request for Comments | `RFC` | Discuss a proposal | `architecture/*` |
| Platform Integration | `INT` | Explain cross-module integration | `architecture/*` |
| Reference / Glossary | `REF` | Fix canonical terminology | `technical-writing` |
| README | — | Operational entry point of a repo or component | `repository-docs` |

Canonical order: Overview, ARQ, STK, IF, EVT, COD, DEV, ADR, RFC, INT, REF, README.
Creating a document type not listed here requires human approval.

## 2. Identifiers

Pattern: `{PREFIX}-{TYPE}-{NNN}` (example: `INGEST-IF-001`).

1. `PREFIX`: 2–6 uppercase letters, unique per module. If it is not established, ask before generating (once, grouped with other questions).
2. `NNN`: three digits, sequential per module and type. Find the highest existing number and increment.
3. Never reuse an ID across modules. A replacement document gets a new ID; the old ID stays in the deprecation record.
4. The Overview has no number: `{PREFIX}-OVERVIEW`. The glossary is `{PREFIX}-REF`.
5. **[Δ]** LADE's own ADRs use `ADR-NNNN` (`AGENTS.md` §10). Platform-module ADRs use `{PREFIX}-ADR-NNN`. Do not mix the two.

## 3. Status

`Draft → Proposed → Accepted → Deprecated | Superseded`

**[Δ]** The older PT-BR statuses (Rascunho, Vigente, Aprovado) are superseded by this set.
Agents MAY set `Draft` or `Proposed`. `Accepted`, `Deprecated` and `Superseded` require human approval.

## 4. Placeholders and evidence

1. Placeholders use `{{UPPER_SNAKE_CASE}}`. Common ones: `{{DOCUMENT_ID}}`, `{{TITLE}}`, `{{OWNER}}`, `{{DATE}}` (ISO `YYYY-MM-DD`), `{{VERSION}}`, `{{SOURCE}}`, `{{RELATED_DOCS}}`.
2. Fill a placeholder only with evidence or an explicit decision. Otherwise write `{{TBD}}` or omit an optional section.
3. A delivered document MUST NOT contain unresolved placeholders in required fields.
4. Never invent: APIs, CLI commands, configuration variables, dependencies, directories, metrics, events, interfaces, providers, execution modes, architectural relationships.
5. Never record secret values. Reference the secret mechanism instead.

## 5. Updating an existing document

1. Change only fields backed by confirmed evidence.
2. Never promote a hypothesis to a decision.
3. Never change status, owner or contract fields without human approval.
4. Add an entry to the document's change record (date, version, change, approval reference).
5. If the change affects other documents (§6), flag them for review. Do not edit them automatically.

## 6. Dependency map

| When this changes | Review |
|-------------------|--------|
| ARQ | Overview, INT, all IF |
| STK | ARQ, all IF |
| ADR (accepted) | IF, STK, ARQ |
| IF | INT, STK, ARQ, COD |
| COD | All IF that use its values |
| REF | All documents in the module |

**[Δ]** The Notion skill calls the integration document `OV`. The current template library calls it `INT`. Use `INT`.

## 7. README rules

1. The README is the operational entry point. It answers: what is it, why it exists, what it does and does not do, how it is structured, how it integrates, how to run it, how to develop it, where the authoritative documents are.
2. The README is **not** the source of truth. Authority: ARQ (architecture), STK (stack), IF/EVT (interfaces), ADR (decisions), DEV (development), COD (conventions), RFC (proposals). The README summarizes and links to them. It never creates decisions.
3. Use canonical Lattinus terminology. Do not introduce alternative names for existing concepts.
4. Status vocabulary: `Experimental`, `Alpha`, `Beta`, `Stable`, `Production`, `Deprecated`. It MUST reflect the real implementation status.
5. Diagrams: Mermaid only when it clarifies (`flowchart` architecture, `sequenceDiagram` interactions, `stateDiagram-v2` lifecycle). Never decorative.
6. Code examples are real, or marked `# Conceptual example`. Pseudocode is never presented as a production API.
7. Move content to specialized documents when it becomes implementation-specific, architectural, contractual, governance-related or operationally extensive.

## 8. File naming **[Δ]**

Notion pattern: `{NN}_{PREFIX}-{TYPE}-{NNN}_{slug}.md` with `00_` for the Overview.
`AGENTS.md` §10 requires lowercase `kebab-case`. Until a human decides, LADE-produced files use lowercase: `03_auth-adr-001_token-storage-decision.md`. The document ID inside the file keeps its uppercase form.