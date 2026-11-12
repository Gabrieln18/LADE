# Changelog

All notable changes to LADE (`.hermes/`) are recorded here. Format: Keep a Changelog; versioning: Semantic Versioning of the structure (README badge).

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
