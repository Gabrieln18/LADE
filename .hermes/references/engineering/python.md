---
name: python
description: Write, modify and review idiomatic, typed Python (PEP 8, PEP 484) using ruff and pytest. Use whenever a task involves Python code, modules, packages, scripts, CLI tools, services or Python dependencies, even if the user only says "implement", "fix" or "add a function".
---

# Skill: python

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-06 · **Location:** `skills/software-engineering/python/SKILL.md`
> Defines *how to write Python* in LADE. Acceptance rules live in `references/lattinus-code.md` (§3, §6, §7, §10).

## When to use / not use

**Use:** any Python implementation, refactor-adjacent edits, or Python code review.
**Do not use:** for Go (`golang`), API contracts (`api-design`), or geospatial specifics (`geospatial/*`); combine skills when a task spans them.

## Inputs

- `task.md`: `acceptance_criteria`, `inputs`, `constraints`, `out_of_scope`.
- Repository configuration (`pyproject.toml` or equivalent): Python version, ruff config, dependencies. **Follow it over defaults here.**
- `references/engineering/python.md`, only if listed in the manifest and needed.

## Tooling (project standard)

| Purpose | Tool | Command |
|---------|------|---------|
| Lint | ruff | `ruff check .` |
| Format | ruff | `ruff format .` |
| Tests | pytest | `pytest` (see `testing` skill) |
| Type check | `TBD` | Use the repository's configured checker. If none exists, propose one via the `dependencies` gate |

Python version, ruff rule set and line length are `TBD`: read them from the repository, never assume.

## Procedure

1. **Read first.** Inspect existing modules, naming, layout and config before writing. Match local conventions.
2. **Design the unit.** Small functions, explicit inputs and outputs, dependencies passed in (no hidden globals).
3. **Write types.** Annotate all public functions and methods (PEP 484). Avoid `Any`; if unavoidable, comment why.
4. **Write the code** following Standards below.
5. **Write tests** with the `testing` skill. Public behavior first.
6. **Run** `ruff format .`, `ruff check .`, type check (if configured), `pytest`. Fix findings; do not blanket-suppress them.
7. **Declare** assumptions and unverified items in the artifact header.

## Standards

- PEP 8 via ruff. Format is whatever `ruff format` produces.
- Config comes from environment or injected objects, never hard-coded (Twelve-Factor).
- Errors: raise specific exceptions; catch the narrowest type; never bare `except:` or silent `except Exception: pass`. Chain with `raise ... from err`.
- Fail fast on invalid input; validate at the boundary (files, CLI args, network, external data).
- Logging: `logging` module, structured, no `print` in library code, no sensitive data.
- Docstrings on public modules, classes and functions: purpose, arguments, returns, raises. Comments explain intent, not mechanics.
- Use `pathlib`, context managers for resources, `dataclass` or typed models for structured data. No mutable default arguments.
- Imports: absolute, no wildcard, no cycles. Dependencies point inward (`lattinus-code.md` §7.1).
- No dead code, no commented-out blocks.
- Dependencies: pinned versions and committed lockfile. Record purpose, license, maintenance status and alternatives for each new package (`lattinus-code.md` §10.2).
- Reproducibility: seeded randomness, no hidden state.
- Performance: optimize only with a measurement; state complexity for hot paths or large data.

## Checklist

- [ ] `ruff format` and `ruff check` clean.
- [ ] Type check clean (if configured) and public API annotated.
- [ ] Tests pass; new logic covered; regression test for fixes.
- [ ] No secrets, absolute local paths or sensitive data.
- [ ] No unapproved dependency added or changed.
- [ ] Docstrings on public API.

## Gates

- `dependencies`: any add, remove or upgrade (plus human approval).
- `safety`: file deletion, network calls, subprocess or shell execution against real systems.
- `git`: before any commit.

## Anti-patterns

- `# noqa` or `# type: ignore` without a specific code and reason.
- Catching `Exception` to keep going; returning `None` to signal errors.
- Module-level side effects (I/O, network, config reads at import time).
- Loading unbounded data fully into memory.
- Reformatting unrelated files; "drive-by" cleanups outside scope (report them instead).
- `eval`, `exec`, or building shell commands from untrusted strings.

## Escalate when

- The repository has no Python configuration and the task needs one (versions, ruff rules).
- A needed library is not approved.
- Lint or type rules conflict with the task's acceptance criteria.
- The task requires touching code outside `can_write`.