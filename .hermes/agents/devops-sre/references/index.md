# references/index.md — devops-sre

Pointers only. No copies (`/AGENTS.md` §4.3).

| Need | Read |
|------|------|
| Definition of Done for infra, security, observability | `references/lattinus-code.md` §6.2, §10, §11 |
| System context and boundaries | `references/architecture.md` |
| What each platform component does | `references/platform/*.md` |
| Pipeline operability expectations | `references/engineering/data.md` |

## Agent-specific principles (inline, short)
1. Every deployable unit: pinned base image, non-root, resource limits, health signal.
2. Every service/pipeline: OTel logs/metrics/traces, runbook, rollback path.
3. Every change: reversible as a unit.
4. Secrets: referenced by name only, never by value.

## Known gaps (record in open-questions.md when hit)
CI system, secret mechanism, SLSA level, network allowlist, audit log.
(see `lattinus-code.md` §14 and `permissions.md` §8)