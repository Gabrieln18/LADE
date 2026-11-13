# AGENTS.md — profile `reviewer` (annex)

> **Version:** 0.1.0 (new in v2.2) · **Scope:** profile annex for the `reviewer` role.
> This file is **not** auto-loaded by Hermes: only `SOUL.md` in a profile home is. It exists so a human or a session can find the role's binding in one screen. The normative manifest is `.hermes/agents/reviewer/AGENTS.md`.

## Binding

| Piece | Where |
|-------|-------|
| Identity | `SOUL.md` → `.hermes/agents/reviewer/SOUL.md` |
| Manifest (skills, references, policies, workflows, can_write) | `.hermes/agents/reviewer/AGENTS.md` |
| Tools and skill scoping | `config.yaml` (`agent.disabled_toolsets`, `skills`) |
| Profile metadata | `profile.yaml` |
| Skills | `skills/` — symlinks into `.hermes/skills/`, created by `setup.sh` |

## Role

Decide PASS, REWORK or ESCALATE on evidence, and record what must not repeat.

**Owns:** review reports and lessons

## Load order

1. `.hermes/SOUL.md` and `.hermes/AGENTS.md` — the core contract.
2. `policies/` — blocking rules, always prevailing.
3. `.hermes/agents/reviewer/AGENTS.md` — what this role may load and write.
4. Only what the `task.md` instance needs. Nothing is preloaded.

## Reads

- `.hermes/SOUL.md`, `.hermes/AGENTS.md`, `policies/` (every task)
- `agents/reviewer/AGENTS.md` and `agents/reviewer/references/review-principles.md`
- `references/lattinus-code.md` §6 and §12
- `references/engineering/*`, `domain/*`, `platform/*` — only what the artifact touches

## Must not

- modify the artifact under review
- author documentation or any artifact it reviews
- review an artifact it authored
- judge its own GT-REV-* eval runs

## Workflow

`code-review`; review step of all six workflows.

## Provisioning

Do not edit this profile by hand outside git. Change the source in `.hermes/`, run `./setup.sh`, review the diff and commit.
