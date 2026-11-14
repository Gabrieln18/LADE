# Changelog

All notable changes to LADE (`.hermes/`) are recorded here. Format: Keep a Changelog; versioning: Semantic Versioning of the structure (README badge).

## [2.2.1] - 2026-11-14

Runtime fix: a profile home no longer lives in the repository, so `hermes -p <role>`
attaches instead of blocking on a blank screen. First entry covering the development
tooling added after v2.2.0 (`d468a93`, `4651361`, `b0f2f8d`).

### Fixed
- Profile homes are **real directories** at `$HERMES_HOME/profiles/<role>` (mode 0700) whose content entries (`AGENTS.md`, `SOUL.md`, `config.yaml`, `profile.yaml`, `skills/`, `.env`) are symlinks into this repository, instead of whole-directory symlinks at `<repo>/profiles/<role>`. A home that canonicalizes outside `$HERMES_HOME` made the runtime read the repository as a second Hermes root, classify the live host gateway as another tenant's and start a gateway that could never become attachable: `hermes -p <role>` printed nothing and never returned, for all nine roles.
- `setup.sh` section 2 creates that shape and reports a whole-directory symlink as drift in `--check`.
- Runtime state (`state.db`, `cron/`, `logs/`, `memories/`, `sessions/`) is created by Hermes inside the home; it no longer lands in the repository working tree.

### Added
- `scripts/repair_profile_homes.sh` (`--check` / `--apply`): repairs the home layout in place, idempotent.
- `scripts/lade_dev.py`: the harness behind `make verify`, `verify-canonical`, `roster`, `rescan` and `serve`.
- `Makefile`: provisioning (`setup`, `check`, `repair-homes`), verification (`verify`, `verify-canonical`, `roster`, `links`, `lint`, `doctor`), run/inspect (`run`, `smoke`, `status`, `tools`, `skills`, `logs`, `session`), gateway (`gateway-status`, `gateway-restart`, `rescan`, `serve`) and reset targets (`prune-runtime`, `reset-homes`, `reset-profiles`, `backup`, `restore`).
- `docs/reports/LADE-20261113-profile-home-multiplexer.md`: defect report with root cause, evidence, fix and acceptance criteria.

### Changed
- `README.md`: structure badge and version footer to `v2.2.1`; the provisioning paragraph and the runtime-state note now describe the real-home-plus-symlinks shape instead of symlinked profile directories.

### Affected files
`setup.sh`; `scripts/repair_profile_homes.sh`; `scripts/lade_dev.py`; `Makefile`; `README.md`; `docs/reports/`; `.hermes/memory/project-state.md`; `.hermes/memory/open-questions.md` (Q-017).

## [2.2.0] - 2026-11-13

Structure change: a content-only repository becomes content plus a thin, runnable profile layer. The runtime is the Hermes Agent; one role equals one profile. No adapter, generator or build step was added.

### Added
- `profiles/` with nine role profiles (`orchestrator`, `architect`, `software-engineer`, `data-engineer`, `geospatial-engineer`, `ai-engineer`, `devops-sre`, `technical-writer`, `reviewer`): `SOUL.md` (symlink to the core role identity), `profile.yaml` (metadata), `config.yaml` (toolset and skill scoping), `AGENTS.md` (annex), `skills/` (symlinks into the single pool).
- `.hermes.md` at the repository root: the short pointer and hard rules Hermes loads when it runs at the root.
- `CODEOWNERS`: governance and merge gating; every governance path is human-write-only.
- `setup.sh`: idempotent provisioning (profile symlinks, skill symlinks derived from each manifest, skills trust) with a `--check` drift mode.
- `.gitignore`: keeps profile runtime state (`state.db`, `memories/`, `sessions/`) out of git.
- `.hermes/config/profiles.md`: normative role-to-profile map, with the capability-to-toolset mapping and the true strength of each.
- Missing declared files, created: `agents/orchestrator/references/orchestration.md`, `agents/architect/references/architecture-principles.md`, `agents/reviewer/references/review-principles.md`, `agents/ai-engineer/references/ai-engineering.md`, `agents/{data,devops-sre,geospatial}-engineer/references/index.md`, `references/engineering/documentation.md`.
- Role identities `agents/{orchestrator,architect,software-engineer,data-engineer,geospatial-engineer,ai-engineer,devops-sre}/SOUL.md` — cited by `AGENTS.md` §2, but only the reviewer and the technical-writer had one.
- Memory files `memory/project-state.md`, `memory/decisions.md`, `memory/lessons.md` — cited by `AGENTS.md` §9 and `config/permissions.md` §4 but absent.
- ADR-0001: Hermes Agent as the runtime; one role equals one profile.

### Changed
- Every role `SOUL.md` is now self-sufficient: it opens with a "core contract" block, because a profile session loads only that file and not the root `SOUL.md`. Reviewer and technical-writer rewritten (0.2.0/0.1.0 → 0.3.0) for the same reason.
- `README.md` rewritten in English and corrected: core paths point into `.hermes/`, the asset path resolves, the structure badge is `v2.2.0`, the framework badge names the Hermes Agent, and the roles table reflects `technical-writer` owning documentation.
- Documentation ownership recorded as closed: `technical-writer` authors repo-level docs and the reviewer reviews them (`workflows/feature-development.md` §8).
- `agents/technical-writer/AGENTS.md` 0.2.0: removed the dangling `PATCHES.md` reference.
- Memory policy made explicit: `.hermes/memory/*.md` in git is the single source; the profiles' `state.db` carries harness facts only.

### Removed
- The README claim that `SOUL.md` and `AGENTS.md` sit at the repository root, and the "framework TBD" badge.

### Affected manifests
All of `agents/*/AGENTS.md` (version headers and now-resolving references); `config/profiles.md`; `README.md`; `.hermes.md`; `CODEOWNERS`; `setup.sh`.

## [2.1.0] - 2026-11-12

### Added
- Agent `technical-writer` (`agents/technical-writer/`): owns standalone and repo-level documentation, so the Reviewer no longer authors what it reviews.
- `references/engineering/data.md` (was cited but missing).
- `evals/fixtures/` with sample data for golden tasks; `GT-TW-001`.
- `tools` field in every agent manifest (required by `config/tools.md` §1.4).
- Decision C-001: Python toolchain `uv` + `ruff` + `pytest`.

### Changed
- All agent manifests normalized to one schema with repo-root-relative paths; references cited by skills added to the manifests (`data-engineer`) or removed from skills (`geospatial/earth-observation`).
- `references/engineering/{python,golang,testing}.md` rewritten as real references (they were copies of skills); `api-design.md` replaced by `api.md`.
- `workflows/feature-development.md` 0.2.0: single canonical order; documentation ownership resolved.
- Severity vocabulary unified to `blocker | major | minor | note`; `blocker` and `major` force `REWORK`.
- Golden-task anchors no longer point to the non-existent `bootstrap` document.

### Removed
- `references/engineering/api-design.md` (duplicate of the skill, wrong filename).
- Reviewer authorship of `documentation/*` artifacts.

### Affected manifests
All of `agents/*/AGENTS.md`; new `agents/technical-writer/AGENTS.md`.
