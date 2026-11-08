---
name: technical-writing
description: Base writing standard for every technical document a LADE agent writes, edits or reviews. Covers choosing reader and document type, separating facts from assumptions from recommendations, citing references, canonical Lattinus terminology, runnable-or-labeled examples, output language, and safe updates of existing documents. Use whenever an agent produces or revises prose documentation (overviews, guides, references, glossaries, explanations, PR text), even if changelog or repository-docs also applies, since both build on this skill.
version: 0.1.0
---

# Technical Writing

Base layer for all documentation in LADE. `changelog` and `repository-docs` apply this skill first.

## Scope

- **In:** reader and type selection, structure, tone, evidence handling, examples, language, safe updates.
- **Out:** ADR content (`architecture/adr`), changelog entries (`changelog`), README/runbook/CONTRIBUTING structure (`repository-docs`), code comments (`software-engineering/*`).

## Inputs

- `task.md`: `objective`, `output_language`, `inputs`, `expected_outputs`, `acceptance_criteria`.
- `references/engineering/documentation.md` (types, IDs, statuses, placeholders, update rules).
- The sources every claim depends on (code, ADRs, files in `references/`), named in the task.

## Procedure

1. **Define reader and intent.** One sentence: who reads this and what can they do afterwards. Map intent to form and Lattinus type.

   | The reader wants to | Form | Lattinus type |
   |---|---|---|
   | learn by doing | tutorial | DEV, README quick start |
   | complete a task | how-to | DEV, runbook |
   | look something up | reference | IF, EVT, COD, REF |
   | understand why or how | explanation | Overview, ARQ, INT, ADR |

   Do not mix forms in one section. If the type is not in `documentation.md` §1, stop and ask a human.
2. **Gather evidence.** Read the sources before writing. If a needed source is missing or outdated, write `{{TBD}}`, record it in `memory/open-questions.md`, and continue only with declared assumptions.
3. **Classify every statement** (SOUL §3): **fact** (cite the `references/` file or task section), **assumption** (list it under "Assumptions"), **recommendation** (label it and give the reason). A confident guess written as fact is a failure.
4. **Write.**
   - Lead with the result, then the justification.
   - One idea per paragraph. Short sentences. Active voice.
   - Define a term at first use. Use canonical Lattinus terms; never coin alternatives for existing concepts.
   - Use a table to compare, a numbered list for sequences, prose to explain.
   - Mermaid only when it clarifies. No decorative diagrams.
5. **Examples.** Runnable against the real code, or marked `# Conceptual example`. Never invent APIs, commands, configuration variables, paths or versions.
6. **Language.** Body in `output_language` (default PT-BR). Code identifiers and technical terms stay in English. Files for `.hermes/` stay in English (`AGENTS.md` §10).
7. **Updating an existing document.** Follow `documentation.md` §5: evidence-backed edits only, no hypothesis promoted to decision, no change of status, owner or contract fields without human approval, add a change-record entry, flag dependent documents (§6) instead of editing them.
8. **Validate** with the checklist below before delivering.

## Output

Markdown artifact at the location declared in `task.md`, starting with the traceability header (`AGENTS.md` §10). For repository files where a visible header would break the format (README, CHANGELOG), wrap it in an HTML comment so it renders invisibly:

```markdown
<!--
task_id: LADE-YYYYMMDD-NNN
produced_by: reviewer
review_level: standard
references: [references/engineering/documentation.md]
adr: none
gates: {safety: pass, dependencies: na, git: na, documentation: pass}
status: IN_REVIEW
assumptions: []
-->
```

## Checklist

- [ ] Reader, intent and document type are stated or obvious.
- [ ] Every fact has a source; assumptions are listed; recommendations are labeled.
- [ ] No unresolved `{{...}}` in required fields; no invented API, path, command or version.
- [ ] Examples are runnable or marked conceptual.
- [ ] Terminology is canonical and consistent.
- [ ] No secrets, tokens, personal data or absolute local paths.
- [ ] Links and cross-references point to files or IDs that exist.
- [ ] Change record updated (when editing an existing document).
- [ ] Output language and identifier language follow `task.md`.

## Boundaries

- Gates: `policies/documentation.md` before closing; `policies/safety.md` for any secret or external-facing content.
- Does not approve its own artifact. A documentation artifact is approved by a human maintainer (`permissions.md` §5, rule 3).
- Does not change `references/`, `templates/` or other governance paths. Propose changes as text or in `open-questions.md`.
- Escalate (`AGENTS.md` §13) when the document type is unknown, the `PREFIX` cannot be established, or sources conflict and no safe assumption exists.