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

### ADR-0002 · Per-profile AI model from a single catalog (per-role, with optional presets)

- **Date:** 2026-11-14 · **Refined:** 2026-11-15
- **Task:** none (v2.3.0 feature)
- **Status:** approved
- **Decision:** Each role runs **its own** AI model. `.hermes/config/models.yaml` is the single source of truth: provider routing (`defaults`); the **per-profile model** under `roles` (each role names its own `model`, plus optional `reasoning_effort` / `fallback`); and an **optional** preset library `classes` (`coding`, `reasoning`, `text`, `generalist`) that a role MAY reference with `class:` — a role's own `model` always wins over its class. Precedence: `roles.<role>` > `classes.<class>` > `defaults`. `setup.sh` renders the `model:`, `fallback_providers:` and `agent.reasoning_effort` regions of every `profiles/<role>/config.yaml` from it — delimited by `lade:*` markers — and `setup.sh --check` reports drift. `scripts/models_render.py` backs `make models`, `models-check`, `models-apply` and `models-set` (which writes `roles.<role>.model`). One OpenRouter key (`OPENROUTER_API_KEY`) serves every role.
- **Context:** Before v2.3.0 the `model:` block was duplicated and hand-maintained in nine `config.yaml` files, and per-profile model choice was an open parameter (`config/profiles.md` §5). The premise: a role should run on a model suited to its task — coding for the implementation roles, reasoning for design and review, long-form text for the writer — instead of one generalist for every role; and the maintainer needs **full per-profile control** of which specialist is scaled to each role, so the model is named per role and shared presets are only a convenience.
- **Alternatives rejected:**
  - Keep the block hand-duplicated per profile: no single source, drift-prone, nine edits per change.
  - A per-profile file the runtime does not read: Hermes has no config include mechanism, so it would not take effect.
  - An interactive first-contact picker: rejected in favor of deterministic defaults plus `--model` / `LADE_MODEL_*`.
  - **Class-only binding** (every role forced into a shared preset): removes per-profile control; kept `classes` only as an opt-in shorthand instead.
  - A separate `overrides:` layer on top of `roles`: redundant once each role names its own model; dropped, so there is one per-role place.
  - A different provider per role: out of scope; one OpenRouter key.
- **Consequences:**
  - Positive: one place to change a model; each profile is individually controlled; drift is reported; presets shorten the common case; the catalog is versioned and human-write-only.
  - Negative: `setup.sh` writes a marker-delimited region inside `config.yaml`; `set` needs `ruamel.yaml` to preserve catalog comments; a model change takes effect on the next profile session.
- **Affected paths:** `.hermes/config/models.yaml`, `scripts/models_render.py`, `setup.sh`, `Makefile`, `profiles/*/config.yaml`, `config/profiles.md`, `README.md`, `CHANGELOG.md`.
- **Approval evidence:** maintainer decision in the v2.3.0 session, 2026-11-14 — D1 single source + render; D2 render with markers; D3 single OpenRouter key; D4 defaults + flags/env; D5 reasoning/fallback in scope. Refined 2026-11-15: per-profile model as the primary layer with `classes` as optional presets, `overrides` dropped.

### ADR-0003 · The tool surface is verified by resolving it, never by reading the config

- **Date:** 2026-11-20
- **Task:** none (defect found while planning the test battery)
- **Status:** draft — pending human approval
- **Decision:** The declared tool surface (`config/profiles.md` §2) is verified per role by the runtime's own resolver, wired into `make verify` and exposed as `make tools-check` (`scripts/lade_dev.py tool-surface`). And `agent.disabled_toolsets` MUST NOT list a bundle or posture whose tool set carries tools the role keeps: the runtime subtracts the list at **tool** granularity and **last** (`model_tools._select_tool_names`), so naming such an entry strips the wanted tools even though the toolset was never disabled by name.
- **Context:** A test-battery review found every one of the nine roles running **without `file` and `terminal`**, although §2 declares `file` for all nine and `terminal` for eight. The cause was the single entry `debugging` in each `agent.disabled_toolsets`: it carries `read_file`, `write_file`, `patch`, `search_files`, `terminal`, `process_manage` (plus `web_search`/`web_extract`, already covered by `web`/`search`). Consequences were categorical, not cosmetic: the orchestrator could not write a `task.md`; the implementing roles could not run a test or a formatter; `technical-writer` could not write a document; `reviewer` lost the `terminal` §2 grants it for checks. Nothing in the repository caught it — `./setup.sh --check` exits 0 because it never resolves the tool surface, and the YAML reads as if the toolsets were granted.
- **Alternatives rejected:**
  - Trusting `./setup.sh --check`: it validates layout, links, model drift and skill counts, not the resolved surface (its own §3 checks skills, not tools).
  - Reading the YAML by eye or diffing the list against §2 textually: that is exactly the reasoning that missed the bug — `file`/`terminal` never appear in the deny list.
  - Generating the deny list in `setup.sh` from §2 (deny every toolset whose tools are not wanted): correct in spirit, but a mixed entry such as `debugging` cannot be expressed as a whole-toolset denial without stripping wanted tools, so the derivation needs the tool-level conflict logic this decision puts in the checker. Kept as the preferred follow-up recorded below.
  - Removing only `debugging` and leaving `coding`: `coding` is a posture, so the runtime subtracts only its non-core delta (empty) and it strips nothing today — but it documents a bundle that would strip the whole surface if the runtime ever stops treating it as a posture. Removed from all nine lists.
- **Consequences:**
  - Positive: the drift is fixed for all nine roles and cannot recur silently — `make verify` fails on any tool missing, any tool granted beyond §2, and names the `disabled_toolsets` entry responsible.
  - Negative: `make verify` now depends on the installed Hermes resolver API (`hermes_cli.tools_config._get_platform_tools`, `model_tools._select_tool_names`, `_disabled_entry_tools`), so an upstream rename surfaces as an error in the check rather than silently passing.
- **Affected paths:** `profiles/*/config.yaml` (nine), `scripts/lade_dev.py`, `Makefile`, `.hermes/config/profiles.md` §2.
- **Approval evidence:** pending — maintainer decision required (`config/` is human-write-only).
- **Follow-up (proposed, not decided):** derive the deny list from §2 in `setup.sh` using the conflict logic the checker now implements, so the list stops being hand-maintained; and add the check to the CI gate once required checks exist (`lattinus-code.md` §14).
