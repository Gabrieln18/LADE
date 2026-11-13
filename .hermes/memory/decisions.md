# decisions.md

> **Writer:** orchestrator, after human approval of an ADR. **Mode:** append; only `Status` may change (supersede).
> Index of approved decisions. The full text of each ADR lives in the artifact that proposed it; this file holds the decision and its pointer.

## Entries

### ADR-0001 · Hermes Agent is the runtime and one role equals one profile

- **Date:** 2026-11-13
- **Task:** none (v2.2 structure change)
- **Status:** approved
- **Decision:** The Hermes Agent is the execution runtime for LADE. Each of the nine roles is materialized as one Hermes profile under `profiles/<role>/`, symlinked into `~/.hermes/profiles/<role>`. Role isolation is achieved by profile separation, not by `delegate_task`.
- **Context:** The previous structure was content-only; nothing bound a role to a tool surface. `delegate_task` children inherit the parent's tools, so per-role tool isolation could not be expressed through delegation.
- **Alternatives rejected:**
  - Content-only repository with no profile layer: no real capability separation.
  - Two profiles (orchestrator and reviewer) with six delegated executors: executors would inherit the orchestrator's tool surface, including Notion and draft-PR capability.
  - A single Profile Distribution shipping nine profiles: `distribution.yaml` is read at the repository root and installs exactly one profile.
- **Consequences:**
  - Positive: tool surfaces are enforced per role; skills are scoped per role; the structure stays content-first with no build step.
  - Negative: nine profile homes to provision and keep in sync; profile runtime state (`state.db`, `memories/`, `sessions/`) must stay out of git.
- **Affected paths:** `profiles/`, `setup.sh`, `config/profiles.md`, `.hermes.md`, `README.md`, `CODEOWNERS`.
- **Approval evidence:** maintainer decision in the v2.2 structure session, 2026-11-13.
