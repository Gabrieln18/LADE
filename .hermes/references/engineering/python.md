# python.md — Python Engineering Reference

> **Version:** 0.2.0 (draft) · **Date:** 2026-11-12 · **Location:** `references/engineering/python.md`
> Replaces the 0.1.0 file, which was a verbatim copy of `skills/software-engineering/python/SKILL.md`. Procedure lives in the skill; this file holds **project facts and decisions**.
> Only humans edit this file. Evidence tags as in `references/architecture.md`.

## 1. Toolchain `ACCEPTED` (maintainer decision, 2026-11-12; record in `memory/conventions.md` C-001)

| Purpose | Tool | Commands |
|---------|------|----------|
| Environment, lock, run | **uv** | `uv sync --frozen` · `uv run <cmd>` |
| Lint | **ruff** | `uv run ruff check .` |
| Format | **ruff** | `uv run ruff format .` |
| Tests | **pytest** | `uv run pytest` |
| Lockfile | `uv.lock` | Committed. Never resolved at build or runtime (`skills/infrastructure/containers`) |
| Type checker | `TBD` | Choose via ADR; until then use the repository's configured one (Q-018) |

`poetry` is not used. Any file or eval still mentioning `poetry.lock` is stale.

## 2. Versions

| Item | Value | State |
|------|-------|-------|
| Python | `>=3.12` | `PROPOSED`, unverified: from Notion OBS-STK-001 (Draft, 2026-09-14). Confirm in `pyproject.toml` before relying on it (Q-019) |
| ruff rule set, line length | defined in `pyproject.toml` | `TBD`: read from the repository, never assume |

## 3. Conventions

- Style: PEP 8 (via ruff), PEP 484 type hints on all public API (`lattinus-code.md` §3).
- Config injected through environment or objects (Twelve-Factor, `lattinus-code.md` §7.1).
- Dependency changes follow `policies/dependencies.md`. Adding the tools above to a project that lacks them is itself a dependency proposal.

## 4. Gaps

Type checker choice (Q-018) · Python version confirmation (Q-019) · coverage and complexity thresholds (Q-006).
