---
name: architecture-review
description: Review a design document, ADR, module structure or dependency layout and produce evidence-based findings with severity and a recommendation. Use whenever someone asks to review, assess, audit, critique or sanity-check an architecture or design ("is this design sound?", "check boundaries and coupling", "what are the risks here?"), for pre-implementation design checks, and when the Reviewer must judge the architectural impact of an artifact. Not for producing a new design (system-design) or line-level code review (workflows/code-review.md).
---

# Architecture Review

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-09 · **Location:** `skills/architecture/architecture-review/SKILL.md`

## Purpose

Find architectural problems early, with evidence, and say what to do about them. A finding without evidence or without a violated criterion is an opinion, not a finding.

## When to use

- A design, ADR or architecture-relevant change needs an independent assessment.
- The Reviewer needs the architectural dimension of a `standard` review.
- A maintainer asks for a health check of module structure or boundaries.

## Inputs

- The artifact under review and its `task.md` (acceptance criteria, constraints).
- Related ADRs (`memory/decisions.md`) and conventions (`memory/conventions.md`).
- `references/lattinus-code.md` §7–§11 and the `references/` files the manifest allows.

## Procedure

1. **Scope.** State what is reviewed, against which criteria (acceptance criteria, ADRs, references, standards) and the depth: *quick* (key risks only) or *full* (all dimensions). Default to *quick* for contained changes and *full* for new components, data contracts, security or public APIs.
2. **Gather evidence.** Read the artifact, trace it to the task and ADRs. For code structure, use `dependency-analysis` (Mode B) to get the real graph instead of guessing. Anything you cannot verify is labeled `unverified`.
3. **Evaluate by dimension.** Apply only the dimensions relevant to the scope.

| Dimension | Key question |
|-----------|--------------|
| Fit to requirements | Does every acceptance criterion have a design element? |
| Boundaries and coupling | Are responsibilities clear and interfaces explicit? |
| Dependency direction | Do dependencies point inward, with no cycles? |
| Data and contracts | Are schemas, versioning and ownership defined? |
| Geospatial / data standards | CRS, formats, lineage, scale and quality checks per `lattinus-code.md` §8? |
| AI components | Versioned prompts, schemas, evaluation, failure handling per §9? |
| Reliability and operability | Failure modes, idempotency, observability, runbook per §11? |
| Security and supply chain | Secrets, input trust, least privilege, dependency gate per §10? |
| Evolvability and reversibility | Can it change and be rolled back as a unit? |
| Simplicity | Is any part more complex than the problem requires? |
| Consistency and decisions | Does it follow existing ADRs and conventions, and are new decisions recorded? |

4. **Record findings.** Each finding has:
   - `id` (`AR-01`, `AR-02`, ...), `dimension`, `severity`;
   - `evidence`: file and section, or the concrete failure scenario;
   - `criterion`: the requirement, ADR, reference or standard it violates;
   - `impact` and `recommendation`;
   - `owner`: the agent that should fix it.
5. **Calibrate severity.**
   - **Blocker:** violates a policy, a Lattinus standard or an acceptance criterion, or carries an irreversible risk.
   - **Major:** significant risk or likely rework.
   - **Minor:** worthwhile improvement.
   - **Note:** observation, including "I would do it differently" with no violated criterion.
6. **Name strengths.** List what is sound and should be preserved, in a few lines.
7. **Conclude.** Give an overall assessment and the top 3 issues.

## Output

- When invoked by the **Reviewer** in a `standard` review: record findings in `templates/review.md` and map to a verdict:
  - any Blocker → `REWORK(agent, reason)` with a verifiable reason;
  - no Blocker → `PASS` (for the architectural dimension);
  - unresolved ambiguity, policy conflict, or a third `REWORK` → `ESCALATE`.
- When invoked by **any other agent or a human**: deliver findings only. No verdict.
- Start with the traceability header (`AGENTS.md` §10).
- If `templates/review.md` is missing, say so, log it in `open-questions.md` and use the finding fields above.

## Boundaries

- Never modify the artifact under review. Corrections return through `REWORK` (`permissions.md` §5).
- Never review your own artifact or ADR. Ask the Orchestrator to reassign.
- Stay in the architectural scope. Report out-of-scope issues in one line instead of expanding the review.
- Do not fabricate evidence. If you could not check something, say so.

## Quality bar

- [ ] Every finding has evidence and a violated criterion or concrete failure scenario.
- [ ] Severity follows the definitions above, with no inflation.
- [ ] Recommendations are actionable and name an owner.
- [ ] Strengths are listed.
- [ ] Scope and depth are stated at the top.