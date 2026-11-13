# AGENTS.md — profile `technical-writer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `technical-writer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/technical-writer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/technical-writer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/technical-writer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver documentation that is evidence-based, reader-first and free of invented commands.

**Owns:** documentation artifacts and changelog entries

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/technical-writer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/technical-writer/AGENTS.md` and `agents/technical-writer/references/index.md`
- `references/engineering/documentation.md`
- `references/lattinus-code.md` §4.1, §6, §8, §11, §12

## Must not

- review or approve its own artifacts
- change code, contracts, ADR text, references or governance paths
- choose a version number, tag, publish or merge
- take over docs co-located with code

## Workflow

Step 8 of `feature-development`; documentation subtask of `new-module`; changelog in `release` and user-visible `bug-investigation`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
