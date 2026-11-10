---
name: adr
description: Propose, write, revise or supersede an Architecture Decision Record (ADR) using templates/adr.md. Use whenever a hard-to-reverse or cross-boundary technical decision is made or needs to be made: choosing technologies, patterns, formats or contracts, deviating from a Lattinus standard, breaking a public interface, adopting a significant dependency, or when someone says "document this decision", "why did we choose X", or is unsure whether something deserves an ADR. Produces an ADR in status Proposed. It never accepts its own ADR.
---

# ADR

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-09 · **Location:** `skills/architecture/adr/SKILL.md`

## Purpose

Capture a decision, its alternatives and its consequences so future maintainers understand *why*. This skill guides how to fill the ADR well. It does not redefine the template.

## Ground rules

1. **Template:** `templates/adr.md` is the only source of structure. If it is missing, say so, log it in `memory/open-questions.md` and use a MADR-style minimum: Context, Drivers, Options, Decision, Consequences.
2. **Lifecycle:** `Proposed` → `Accepted` | `Rejected`; later `Superseded by ADR-NNNN` or `Deprecated`.
3. **Agents produce only `Proposed`.** A human approves. After approval the Orchestrator records it in `memory/decisions.md` (`AGENTS.md` §9). No agent approves its own ADR.
4. **Accepted ADRs are immutable** except status and links. A changed decision is a new ADR that supersedes the old one.

## When an ADR is warranted

Write one if any of these holds:

1. The decision is hard or costly to reverse (storage format, data contract standard, core framework, public API shape).
2. It crosses component or team boundaries.
3. It deviates from a standard in `lattinus-code.md` §3 or from `memory/conventions.md`.
4. It adds or replaces a significant dependency or external service.
5. It is a breaking change to a public interface or data contract.
6. It sets a convention that will be repeated.
7. The trade-off is non-obvious and a future maintainer will ask "why?".

**Not warranted:** routine implementation choices, reversible local choices, or anything already covered by an existing ADR (reference it instead). If a borderline case touches trigger 1, 2 or 5, prefer a short ADR over lost rationale. Otherwise state in one line why none is needed.

## Procedure

1. **Check existing decisions.** Read `memory/decisions.md`. If the topic is covered or conflicts, reference or supersede instead of duplicating.
2. **Assign the id.** Next sequential `ADR-NNNN` after the highest in `decisions.md` and any pending proposals named in the task. If you cannot verify it, write `ADR-NNNN (unverified id)` and let the Orchestrator confirm.
3. **Title.** Short and decision-shaped, e.g. "Use GeoParquet for vector intermediates".
4. **Context.** Forces, constraints and why now. Cite `references/` for facts and declare assumptions. Stay neutral and do not foreshadow the answer.
5. **Drivers.** Ranked, and measurable where possible.
6. **Options.** At least 2 genuinely viable ones, including "keep the status quo" when applicable. For each: what it is, pros, cons and cost to reverse. If an option is a package, run `dependency-analysis` (Mode A) first and cite the result.
7. **Decision.** One sentence: "We will ... because ...", naming the deciding drivers. While `Proposed`, phrase it as the recommendation awaiting approval.
8. **Consequences.** Positive, negative and neutral. List follow-ups: new tasks, migrations, convention updates, and `references/` that need changes (propose these as text, since agents do not edit `references/`).
9. **Confirmation.** How compliance and success will be checked (test, review check, metric), and a revisit trigger (condition or date).
10. **Links.** `task_id`, related ADRs, references, and `supersedes` when relevant.
11. **Self-check** against the quality bar and hand to the Orchestrator for human approval.

## Output

- One ADR per decision, from `templates/adr.md`, preceded by the traceability header (`AGENTS.md` §10) with `adr: <id>`.
- Location is declared in `task.md`.
- Write in the task's `output_language` (default PT-BR). Keep identifiers and technical terms in English.

## Quality bar

- [ ] A reader gets the decision in 30 seconds.
- [ ] Alternatives are real: a reasonable engineer could have picked them.
- [ ] Negative consequences are stated honestly.
- [ ] One decision per ADR, about 1–2 pages.
- [ ] Supersession is explicit.
- [ ] No implementation detail beyond what the decision needs.

## Anti-patterns

- Retroactive justification: the decision is made and the options are decoration.
- One real option plus straw men.
- Bundling several decisions in one ADR.
- Using the ADR as a design document (that belongs in `design.md`).
- Editing an accepted ADR instead of superseding it.