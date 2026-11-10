# open-questions.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `memory/open-questions.md`
> **Writer:** any agent, any time. **Mode:** append-only. Each entry MUST carry `task_id` and an `Owner`.
> Resolve a question by appending a `Resolution` line that cites the human decision. Humans may edit or archive entries.
> Also used to log: missing or outdated references, memory vs reference conflicts, proposed changes to governance files.

<!-- FORMAT (copy for each entry, newest last)

### Q-NNN · <title>
- **Date:** YYYY-MM-DD
- **Task:** <task_id | none (reason)>
- **Raised by:** <agent | human>
- **Owner:** <who can answer>
- **Blocking:** <no | yes: what>
- **Question:** <one or two sentences>
- **Context:** <source file and section, why it matters>
- **Status:** OPEN | RESOLVED
- **Resolution:** <date, decision, link>   # added when resolved
-->

## Entries

### Q-001 · Confirm the LADE acronym expansion
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** What is the official expansion of LADE? `SOUL.md` §1 spells "Enviroment" (typo for "Environment").
- **Context:** `README.md` Overview has a TODO on this.
- **Status:** OPEN

### Q-002 · Repository name and base branch
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** yes: delivery of any PR
- **Question:** Which repository and base branch receive LADE deliveries?
- **Context:** `references/lattinus-code.md` §4.1, §14.
- **Status:** OPEN

### Q-003 · CI system and required checks
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers, devops-sre
- **Blocking:** yes: Definition of Done cannot be verified in CI
- **Question:** Which CI runs, and which checks are required?
- **Context:** `references/lattinus-code.md` §6.1, §10, §14.
- **Status:** OPEN

### Q-004 · Commit signing policy
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** Are signed commits required?
- **Context:** `references/lattinus-code.md` §4.1, §14.
- **Status:** OPEN

### Q-005 · PR size threshold
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** Above which size must an agent propose splitting a PR?
- **Context:** `references/lattinus-code.md` §4, §14.
- **Status:** OPEN

### Q-006 · Coverage and complexity thresholds
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** What are the minimum coverage and the maximum cyclomatic complexity and function length?
- **Context:** `references/lattinus-code.md` §7, §14.
- **Status:** OPEN

### Q-007 · Secret management mechanism
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** devops-sre
- **Blocking:** no
- **Question:** Which mechanism does the platform use for secrets?
- **Context:** `references/lattinus-code.md` §10, §14.
- **Status:** OPEN

### Q-008 · SLSA target level
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** devops-sre
- **Blocking:** no
- **Question:** Which SLSA level is the target for provenance?
- **Context:** `references/lattinus-code.md` §3, §14.
- **Status:** OPEN

### Q-009 · Confirm the data contract standard
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** data-engineer, architect (proposal), human (decision)
- **Blocking:** no
- **Question:** Is ODCS the data contract standard, or another one (to be declared in an ADR)?
- **Context:** `references/lattinus-code.md` §3, §14.
- **Status:** OPEN

### Q-010 · Runtime, framework and artifact paths
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** yes: no agent can run or write artifacts consistently
- **Question:** Which runtime executes LADE, where do artifacts per class live, and how are permissions enforced (sandbox)?
- **Context:** `README.md` (Technology Stack, Getting Started), `config/permissions.md` §8.
- **Status:** OPEN

### Q-011 · Network allowlist and tools/MCPs
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** devops-sre, Maintainers
- **Blocking:** yes: `config/tools.md` does not exist, so network and tool use is denied by default
- **Question:** Which hosts and tools/MCPs are allowed, per agent?
- **Context:** `config/permissions.md` §6, §8.
- **Status:** OPEN

### Q-012 · Audit log location and retention
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** devops-sre
- **Blocking:** no
- **Question:** Where are agent actions logged, and for how long?
- **Context:** `config/permissions.md` §8.
- **Status:** OPEN

### Q-013 · Snapshot of Notion Lattinus in `references/lattinus.md`
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** yes: domain claims have no sourced reference
- **Question:** When will the Notion Lattinus snapshot be produced, and from which pages? It MUST carry its snapshot date.
- **Context:** `AGENTS.md` §12.
- **Status:** OPEN

### Q-014 · How is human approval evidenced?
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** Which evidence lets the Orchestrator write to `decisions.md` and `conventions.md`: a PR comment, a `task.md` field, or another form?
- **Context:** `AGENTS.md` §9, `memory/README.md` §3.9.
- **Status:** OPEN

### Q-015 · Memory archive location and limits
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** Where do pruned `lessons.md` and `open-questions.md` entries go, and are the soft limits in `memory/README.md` §6 right?
- **Context:** `memory/README.md` §6.
- **Status:** OPEN

### Q-016 · How are evals executed?
- **Date:** 2026-11-10
- **Task:** none (bootstrap)
- **Raised by:** bootstrap
- **Owner:** Maintainers
- **Blocking:** no
- **Question:** How and when do golden tasks run, and who records the results in `evals/reports/`?
- **Context:** `README.md` (Testing).
- **Status:** OPEN