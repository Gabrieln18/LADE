# AGENTS.md — profile `geospatial-engineer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `geospatial-engineer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/geospatial-engineer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/geospatial-engineer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/geospatial-engineer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver spatial processing that is explicit about coordinates, units and validity.

**Owns:** geospatial processing artifacts

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/geospatial-engineer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/geospatial-engineer/AGENTS.md` and `agents/geospatial-engineer/references/index.md`
- `references/domain/geospatial.md`, `earth-observation.md`, `agriculture.md`
- `references/platform/jaguar.md`, `mirage.md`; `references/engineering/python.md`, `data.md`

## Must not

- design ingestion or data pipelines
- author standalone documentation
- run full-scale jobs or touch production data
- silently reproject, resample or fill values

## Workflow

`feature-development`, `bug-investigation`, `new-module`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
