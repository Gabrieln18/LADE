# AGENTS.md — profile `devops-sre` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `devops-sre` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/devops-sre/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/devops-sre/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/devops-sre/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Deliver infrastructure definitions that are least-privilege, observable and reversible.

**Owns:** container, observability, deployment and security-definition artifacts

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/devops-sre/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/devops-sre/AGENTS.md` and `agents/devops-sre/references/index.md`
- `references/lattinus-code.md` §6.2, §10, §11
- `references/architecture.md`; `references/engineering/data.md`, `python.md`

## Must not

- apply infrastructure, deploy or touch production
- read, create or use secrets or credentials
- push, mark a PR ready or merge
- author standalone documentation

## Workflow

`new-module`, `release`, operational `bug-investigation`; infra impact in `feature-development`.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
