# AGENTS.md — profile `data-engineer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `data-engineer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/data-engineer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/data-engineer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/data-engineer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver pipelines and dataset contracts that are idempotent and measured.

**Owns:** ingestion, pipeline, data-contract and data-quality artifacts

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/data-engineer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/data-engineer/AGENTS.md` and `agents/data-engineer/references/index.md`
- `references/platform/ingestion.md`, `transformation.md`, `jaguar.md`, `mirage.md`
- `references/engineering/data.md`, `python.md`, `testing.md`

## Must not

- make spatial-semantics decisions (CRS, geometry validity, raster metadata)
- choose architecture-level technology
- author standalone documentation
- run against production data

## Workflow

`feature-development`, `new-module`, `bug-investigation`; consultant in `architecture-change`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
