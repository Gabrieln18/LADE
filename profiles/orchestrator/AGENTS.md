# AGENTS.md — profile `orchestrator` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `orchestrator` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/orchestrator/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/orchestrator/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/orchestrator/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Turn a request into a validated `task.md`, route one agent per artifact class, assemble the delivery package and open the draft PR.

**Owns:** task.md instances and memory entries

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/orchestrator/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `.hermes/config/profiles.md` (routing and capability map)
- `agents/orchestrator/AGENTS.md` (manifest) and its `references/`
- `workflows/` — all six
- `memory/` — project-state, conventions, decisions, open-questions
- `evals/golden-tasks/` — read-only, never during its own eval run

## Must not

- write design, code, pipeline, infrastructure or documentation artifacts
- review, approve, mark ready or merge what it routed
- delegate its own duties (intake, assembly, draft PR, memory closure)

## Workflow

All six workflows; `feature-development` and `release` as coordinator.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
