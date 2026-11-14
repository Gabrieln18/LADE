# 🧰 LADE (Hermes)

A governed multi-agent engineering environment that turns engineering tasks into reviewed artifacts for **Lattinus Code**.

<p align="center">
  <img src="./.hermes/assets/hermes_agent_wordmark_colored_hero_banner.png" alt="LADE (Hermes)" width="100%" />
</p>

<p align="center">
  <strong>User Task → Orchestrator → Role Profile → Artifact → Policy Gates → Reviewer → Lattinus Code</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-orange" alt="Status" />
  <img src="https://img.shields.io/badge/structure-v2.2.1-blue" alt="Structure" />
  <img src="https://img.shields.io/badge/lang-Markdown-informational" alt="Language" />
  <img src="https://img.shields.io/badge/runtime-Hermes%20Agent-6f42c1" alt="Runtime" />
  <img src="https://img.shields.io/badge/roles-9%20profiles-green" alt="Profiles" />
  <img src="https://img.shields.io/badge/quality-reviewer%20gate-green" alt="Quality" />
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-roles">Roles</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-core-concepts">Core Concepts</a> •
  <a href="#-repository-structure">Repository</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-development">Development</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-security">Security</a> •
  <a href="#-documentation">Documentation</a>
</p>

> **Structure v2.2.1 (2026-11-14).** Content lives in `.hermes/`; each role is also a runnable Hermes profile in `profiles/`. Every file in this repository is written in English; delivered documents follow `output_language` in `task.md` (default PT-BR).

---

## 📌 Overview

**LADE (Lattinus Agent Development Environment)** is a multi-agent environment that receives engineering tasks, distributes the work across specialized roles and delivers reviewed artifacts to the Lattinus Code platform.

It belongs to the **agent-assisted development layer** of the Lattinus ecosystem and provides **orchestration, skills, references, policies, memory and mandatory review** as its core capabilities. Its purpose is to produce technical artifacts with **standardization, traceability and mandatory review**, so that Lattinus maintainers and contributors deliver with more consistency and less rework.

LADE does not run the platform. It **produces** the artifacts that feed it. Domain knowledge comes from `.hermes/references/`, derived from the [Notion Lattinus](https://app.notion.com/p/Lattinus-2f673eebda2f80d7973fc08ef9558a2e) workspace.

### Two layers, one source

| Layer | Location | Purpose |
|-------|----------|---------|
| **Core** | `.hermes/` | The single source: identity, rules, skills, references, policies, templates, workflows, memory, evals. |
| **Profiles** | `profiles/<role>/` | The runtime binding: one Hermes profile per role, carrying identity, tool surface and skill scoping. |

The profiles hold no domain content of their own. Their `SOUL.md` is a symlink to the role identity in `.hermes/agents/<role>/SOUL.md`; their `skills/` are symlinks into the single pool `.hermes/skills/`. `setup.sh` derives both from the role manifest, so a manifest change propagates without duplication.

---

## 👥 Roles

Nine roles, nine profiles. One artifact class each.

| Role | Profile | Responsibility |
|------|---------|----------------|
| `orchestrator` | `orchestrator` | Intake, task contract, routing, package assembly, draft PR, memory closure |
| `architect` | `architect` | System design, ADR proposals, dependency analysis, implementation plans |
| `software-engineer` | `software-engineer` | Implementation in Python and Go: code, APIs, tests, refactoring |
| `data-engineer` | `data-engineer` | Ingestion, pipelines, data contracts, data quality |
| `geospatial-engineer` | `geospatial-engineer` | Raster/vector, CRS, Earth Observation, Dask/Xarray, Sedona |
| `ai-engineer` | `ai-engineer` | Agent design, multi-agent, evaluation, LLM integration |
| `devops-sre` | `devops-sre` | Containers, deployment definitions, observability, security |
| `technical-writer` | `technical-writer` | Standalone and repo-level documentation, changelog |
| `reviewer` | `reviewer` | Independent review, verdict, lessons |

Each role declares its skills, references, policies, workflows and write scope in `.hermes/agents/<role>/AGENTS.md`. The role-to-toolset binding lives in `.hermes/config/profiles.md`.

**Out of scope:** running the Lattinus platform in production.

---

## 🏗️ Architecture

```
 USER TASK
     │
     ▼
 ORCHESTRATOR ──(templates/task.md)──▶ ROLE PROFILE(S)
                                          │
                                          ▼
                                      ARTIFACT
                                          │
                                          ▼
                              POLICY GATES (policies/)
                                          │
                                          ▼
                                      REVIEWER
                                          │
                      ┌───────────────────┼───────────────────┐
                      ▼                   ▼                   ▼
                    PASS              REWORK             ESCALATE
                      │            (max. 2 cycles)        (human)
                      ▼
               MEMORY UPDATE
                      │
                      ▼
               LATTINUS CODE
```

**Architectural position**

- **Layer:** agent-assisted development.
- **Upstream:** human tasks (`templates/task.md`) and Lattinus context (`references/`).
- **Downstream:** Lattinus Code (output contract in `references/lattinus-code.md`).

---

## 💡 Core Concepts

- **Precedence:** `policies/` > `SOUL.md` > `AGENTS.md` > role `SOUL.md` > role manifest > `task.md`. The most specific wins, except `policies/`, which always prevail.
- **Manifest:** each role loads on demand only what its manifest declares. Declared-only means absent is denied.
- **Single source:** knowledge in `references/`, templates in `templates/`, skills in `skills/`. No copies.
- **Reviewer loop:** at most 2 `REWORK` cycles, then `ESCALATE` to a human.
- **Memory:** `decisions.md` receives approved ADRs only; `lessons.md` is written by the reviewer; `open-questions.md` accepts any agent. Memory is git-versioned Markdown — the profiles' `state.db` holds harness facts only.
- **Enforcement split:** the runtime imposes the toolset allowlist, the per-profile skill set and merge protection. Everything else — precedence, gates, separation of duties — is policy text the agent must honour. `.hermes/config/profiles.md` §3 states which is which.

---

## 🔌 Interface and Contract Model

| Contract | File | Description |
|----------|------|-------------|
| Handoff | `.hermes/templates/task.md` | Mandatory for delegation between roles |
| Review | `.hermes/templates/review.md` | Checklist + verdict `PASS \| REWORK(role, reason) \| ESCALATE` |
| Decision | `.hermes/templates/adr.md` | Architecture decision record |
| Output | `.hermes/references/lattinus-code.md` | Repository, branch, PR and Definition of Done |

---

## 🧰 Technology Stack

- **Content:** Markdown (`SOUL.md`, `AGENTS.md`, `SKILL.md`).
- **Runtime:** [Hermes Agent](https://hermes-agent.nousresearch.com/docs) — one profile per role.
- **Governance:** `CODEOWNERS` plus branch protection; merge is human-only.
- **Provisioning:** `setup.sh` (bash + python3, idempotent, `--check` for drift).

No adapters, no generator, no build step. Each role's home is a real directory at `~/.hermes/profiles/<role>` whose content entries are symlinked from this repository; nothing is packaged. `scripts/repair_profile_homes.sh --check` is the test.

---

## 📁 Repository Structure

```
LADE/
├── .hermes.md          project context pointer loaded when Hermes runs at the root
├── README.md           this file, for humans
├── CODEOWNERS          governance and merge gating
├── setup.sh            idempotent provisioning: links, skills, trust
├── profiles/<role>/    SOUL.md · profile.yaml · config.yaml · AGENTS.md · skills/ (generated)
└── .hermes/            the core and single source
```

| Path | Purpose | Who writes |
|------|---------|------------|
| `.hermes/config/` | Permissions, tools/MCPs, role→profile binding | Humans |
| `.hermes/agents/<role>/` | `SOUL.md` (identity) and `AGENTS.md` (manifest) | Humans |
| `.hermes/skills/` | Single skill catalog (`SKILL.md`) | Humans |
| `.hermes/references/` | Single source of domain knowledge | Humans |
| `.hermes/memory/` | State, decisions, conventions, lessons, open questions | Agents (see `memory/README.md`) |
| `.hermes/workflows/` | Role sequence, gates and human approvals | Humans |
| `.hermes/templates/` | Single location of templates | Humans |
| `.hermes/policies/` | Blocking gates (safety, dependencies, git, documentation) | Humans |
| `.hermes/evals/` | Golden tasks and per-version reports | Humans / Reviewer |
| `profiles/<role>/` | Role identity binding, tool surface, skill scoping. `skills/` is generated by `setup.sh` and ignored by git | Humans (via git) |

Core identity files: `.hermes/SOUL.md` and `.hermes/AGENTS.md`. They are **not** at the repository root; `.hermes.md` is the pointer that Hermes reads.

---

## 🚀 Getting Started

```bash
git clone https://github.com/Gabrieln18/LADE.git
cd LADE
./setup.sh                 # link the 9 profiles and trust the skill tree
./setup.sh --check         # report drift without writing
hermes profile list        # nine LADE profiles + default
hermes -p orchestrator     # start a session as the orchestrator
```

Then:

1. Describe the task with `.hermes/templates/task.md`.
2. Let the orchestrator pick the workflow, or name it from `.hermes/workflows/`.
3. Follow the artifact, the reviewer verdict and the memory updates.

To work inside Lattinus Code, that repository carries a three-line `.hermes.md` pointing here; start the role's profile from the Lattinus Code root so the domain context resolves.

> Profile runtime state (`state.db`, `memories/`, `sessions/`, `logs/`, `cron/`) is created by Hermes inside `~/.hermes/profiles/<role>`, never in this repository. After a change to the home layout the host gateway must be restarted before the profiles are served again (`make gateway-restart`, then `make verify`).

---

## 🛠️ Development

- **New role:** create `.hermes/agents/<role>/` with `SOUL.md` and `AGENTS.md`, add the row to `.hermes/config/profiles.md` §2, add the role to `setup.sh`, register it in `.hermes/agents/orchestrator/references/routing.md`, create `profiles/<role>/`, run `./setup.sh`.
- **New skill:** create `.hermes/skills/<category>/<name>/SKILL.md` and add it to the manifest of every role that uses it; run `./setup.sh` to bind the symlinks.
- **New workflow:** create `.hermes/workflows/<name>.md` with roles, inputs/outputs, gates and human approvals.
- **Changing a tool surface:** edit `.hermes/config/profiles.md` §2 and the profile's `config.yaml`, then record the change in `.hermes/CHANGELOG.md`.

Never edit a profile's `config.yaml` in isolation: it must agree with `config/profiles.md`, and `./setup.sh --check` is the test.

---

## 🧪 Testing

Golden tasks in `.hermes/evals/golden-tasks/` (`by-agent/` and `by-workflow/`); results per SOUL/skill version in `.hermes/evals/reports/`.

Execution is manual today (`.hermes/evals/README.md` §4): isolate the agent under test from the checks, run once at low/medium risk and three times at high risk, keep the trace, judge against the hard checks. Automated execution is open (`Q-016`).

---

## 🔒 Security

Blocking rules in `.hermes/policies/` (`safety.md`, `dependencies.md`, `git.md`, `documentation.md`). Permissions per role in `.hermes/config/permissions.md`. Tool and network allowlists in `.hermes/config/tools.md`; network is denied by default. Policies always prevail over any agent instruction.

Runtime-side: each profile disables every toolset its role does not need (`config/profiles.md` §2), and only the orchestrator may carry an MCP server. Merge protection lives in `CODEOWNERS` plus branch protection.

---

## 📚 Documentation

| Document | Location |
|----------|----------|
| Global rules for agents | `.hermes/AGENTS.md` |
| Identity and values | `.hermes/SOUL.md` |
| Role → profile binding | `.hermes/config/profiles.md` |
| Memory rules | `.hermes/memory/README.md` |
| Lattinus context (snapshot) | `.hermes/references/lattinus.md` |
| Source of context | [Notion Lattinus](https://app.notion.com/p/Lattinus-2f673eebda2f80d7973fc08ef9558a2e) |
| Changelog | `.hermes/CHANGELOG.md` |

**Version:** v2.2.1 (2026-11-14) · **Changelog:** `.hermes/CHANGELOG.md`
