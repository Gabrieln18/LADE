# AGENTS.md — profile `ai-engineer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `ai-engineer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/ai-engineer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/ai-engineer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/ai-engineer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver AI components that ship with an eval, a bounded loop and a deterministic fallback.

**Owns:** AI component artifacts (agent, prompt, evaluator, integration)

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/ai-engineer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/ai-engineer/AGENTS.md` and `agents/ai-engineer/references/ai-engineering.md`
- `references/lattinus-code.md` §9 and §6.2
- `references/engineering/python.md`, `testing.md`, `api.md`

## Must not

- send sensitive data to an external provider
- ship an AI component without an eval
- execute model output as code or instructions
- choose a model or provider as an architecture decision

## Workflow

`feature-development`, `new-module`; contributor in `architecture-change` and `bug-investigation`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
