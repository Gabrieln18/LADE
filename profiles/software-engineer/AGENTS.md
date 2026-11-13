# AGENTS.md — profile `software-engineer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `software-engineer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/software-engineer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/software-engineer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/software-engineer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver code and tests that meet the task contract and the Definition of Done.

**Owns:** code, tests and API specifications

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/software-engineer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/software-engineer/AGENTS.md` (manifest)
- `references/engineering/python.md`, `golang.md`, `api.md`, `testing.md`
- `references/lattinus-code.md` §6, `references/architecture.md`

## Must not

- touch pipelines, data contracts, geospatial processing, AI components or infrastructure
- author standalone or repo-level documentation
- approve its own work, push, open a PR or merge

## Workflow

`feature-development`, `bug-investigation`, `new-module`; implementation stage of `architecture-change`; version bump in `release`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
