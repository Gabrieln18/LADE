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

### ADR-0002 · Per-profile model from a single catalog, bound to specialization classes

- **Date:** 2026-11-14
- **Task:** none (v2.3.0 feature)
- **Status:** approved
- **Decision:** Each role runs one AI model, chosen by **specialization class**. `.hermes/config/models.yaml` is the single source of truth: it holds provider routing (`defaults`), the specialization classes (`classes`: `coding`, `reasoning`, `text`, `generalist`), the role→class binding (`roles`) and optional per-role `overrides`. `setup.sh` renders the `model:`, `fallback_providers:` and `agent.reasoning_effort` regions of every `profiles/<role>/config.yaml` from it — delimited by `lade:*` markers — and `setup.sh --check` reports drift. `scripts/models_render.py` backs `make models`, `models-check`, `models-apply` and `models-set`. One OpenRouter key (`OPENROUTER_API_KEY`) serves every role.
- **Context:** Before v2.3.0 the `model:` block was duplicated and hand-maintained in nine `config.yaml` files, and per-profile model choice was an open parameter (`config/profiles.md` §5). The premise: a role should run on a model suited to its task — coding for the implementation roles, reasoning for design and review, long-form text for the writer — instead of one generalist for every role.
- **Alternatives rejected:**
  - Keep the block hand-duplicated per profile: no single source, drift-prone, nine edits per change.
  - A per-profile file the runtime does not read: Hermes has no config include mechanism, so it would not take effect.
  - An interactive first-contact picker: rejected in favor of deterministic defaults plus `--model` / `LADE_MODEL_*`.
  - A different provider per role: out of scope; one OpenRouter key.
- **Consequences:**
  - Positive: one place to change a model; drift is reported; a role moves between specialists by changing its class; the catalog is versioned and human-write-only.
  - Negative: `setup.sh` now writes a marker-delimited region inside `config.yaml`; `set` needs `ruamel.yaml` to preserve catalog comments; a model change takes effect on the next profile session.
- **Affected paths:** `.hermes/config/models.yaml`, `scripts/models_render.py`, `setup.sh`, `Makefile`, `profiles/*/config.yaml`, `config/profiles.md`, `README.md`, `CHANGELOG.md`.
- **Approval evidence:** maintainer decision in the v2.3.0 session, 2026-11-14 — D1 single source + render; D2 render with markers; D3 single OpenRouter key; D4 defaults + flags/env; D5 reasoning/fallback in scope.
