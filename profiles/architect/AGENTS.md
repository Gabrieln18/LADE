# AGENTS.md — profile `architect` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `architect` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/architect/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/architect/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/architect/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Decide how the system is shaped and what it gives up, then hand implementation to an executor.

**Owns:** design documents, ADR proposals, dependency analyses, implementation plans

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/architect/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/architect/AGENTS.md` and `agents/architect/references/architecture-principles.md`
- `references/lattinus.md`, `references/lattinus-code.md`, `references/architecture.md`
- `references/domain/*`, `references/platform/*`, `references/engineering/*` — on demand

## Must not

- write code, tests, pipelines or infrastructure definitions
- approve its own ADR or design
- add, remove or upgrade a dependency
- delegate work

## Workflow

Leads `architecture-change` and `new-module`; contributes to `feature-development`, `bug-investigation` and `code-review`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
