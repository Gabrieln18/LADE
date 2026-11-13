# index.md — devops-sre references

Pointers only. Never copy content from central `references/`.

| Need | Load |
|------|------|
| Infrastructure and deployment contract | `references/lattinus-code.md` §6.2, §10 |
| Observability requirements and signals | `references/lattinus-code.md` §11 |
| Security rules and secrets handling | `references/lattinus-code.md` §10, `policies/safety.md` |
| What is being deployed (module behaviour) | `references/platform/<file>.md` (only the module in the task) |
| Module boundaries and layers | `references/architecture.md` |
| Pipeline operability constraints | `references/engineering/data.md` |
| Python toolchain for images (`uv`) | `references/engineering/python.md` |
| Templates | `templates/implementation-plan.md`, `templates/runbook.md`, `templates/task.md` |

Known gaps (record in `memory/open-questions.md` when hit): registry and hosting target, the sandbox mechanism for `R2` tools (`config/tools.md` §9), and the SBOM format used at release.
