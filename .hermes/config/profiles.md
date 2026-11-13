# profiles.md

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `config/profiles.md`
> Normative map from LADE role to Hermes profile: which profile exists, which tool surface it gets and which skills it may load. Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.
> Only humans edit this file (`AGENTS.md` §11). It does not restate approvals — those live in `config/permissions.md`.

## 1. Purpose and precedence

This file defines the **runtime binding** of the role model: one role, one Hermes profile, one tool surface. It is the source that `setup.sh` and each `profiles/<role>/config.yaml` must agree with.

1. `config/permissions.md` and `policies/` define what a role may do; this file defines which tools the runtime gives it. The more restrictive of the two applies.
2. A role absent from §2 has no profile and MUST NOT be invoked as one.
3. Adding a role, or changing a role's tool surface, is a governance change: ADR plus human approval.
4. The mechanism is `agent.disabled_toolsets` in the profile's `config.yaml` (Hermes has no allowlist). Everything not listed as enabled in §2 MUST be disabled there.
5. A profile's skills are symlinks into the single pool `.hermes/skills/`, derived from the role manifest by `setup.sh`. Skills are never copied.

## 2. Role to profile map

| Role | Profile | Enabled toolsets | Terminal | Delegation |
|------|---------|------------------|:--------:|:----------:|
| `orchestrator` | `orchestrator` | `file`, `terminal`, `skills`, `todo`, `clarify`, `delegation` | yes | yes |
| `architect` | `architect` | `file`, `terminal`, `skills`, `todo`, `clarify` | yes | no |
| `software-engineer` | `software-engineer` | `file`, `terminal`, `code_execution`, `skills`, `todo`, `clarify` | yes | no |
| `data-engineer` | `data-engineer` | `file`, `terminal`, `code_execution`, `skills`, `todo`, `clarify` | yes | no |
| `geospatial-engineer` | `geospatial-engineer` | `file`, `terminal`, `code_execution`, `skills`, `todo`, `clarify` | yes | no |
| `ai-engineer` | `ai-engineer` | `file`, `terminal`, `code_execution`, `skills`, `todo`, `clarify` | yes | no |
| `devops-sre` | `devops-sre` | `file`, `terminal`, `skills`, `todo`, `clarify` | yes | no |
| `technical-writer` | `technical-writer` | `file`, `skills`, `todo`, `clarify` | no | no |
| `reviewer` | `reviewer` | `file`, `terminal`, `skills`, `todo`, `clarify` | yes | no |

Rules:
1. Only the orchestrator holds `delegation`; every other role works inside its own profile.
2. Only the orchestrator MAY be configured with an MCP server (Notion, read-only), and only after the integration is authorized. No other profile carries an MCP server.
3. `terminal` implies shell commands under `approvals.mode`; it is granted to roles that must run local checks. `technical-writer` gets none, because documenting is a read-and-write activity.
4. The reviewer keeps `terminal` for checks only. Its read-only constraint on the artifact under review is advisory: the `file` toolset bundles read and write, and file writes are never prompted. Making it structural requires a plugin hook (`Q-NNN`).
5. No profile gets `web`, `browser`, `computer_use`, `image_gen`, `video`, `tts`, `cronjob`, `kanban` or a messaging gateway toolset. Network access is denied by default (`config/tools.md` §6).

## 3. Capability mapping

LADE capability identifiers are policy-level; the runtime binding is a Hermes toolset. The two vocabularies do not map one-to-one.

| LADE capability | Hermes binding | Strength |
|-----------------|----------------|----------|
| `fs.read` | `file` (`read_file`, `search_files`) | Real |
| `fs.write` | `file` (`write_file`, `patch`) | Real, but not separable from read |
| `shell.sandbox` | `terminal` + `approvals.mode` | Partial — approval covers shell, not file writes |
| `quality.runner` | `terminal` or `code_execution` | Real |
| `geo.sample-run` | `code_execution` | Real |
| `git.local` | `terminal` + `policies/git.md` | Partial — the gate is instructed, not enforced |
| `git.draft-pr` | `terminal` + branch protection | Real at the PR, advisory locally |
| `container.build` | `terminal` | Partial |
| `mcp.notion.search` / `.fetch` | MCP server in the orchestrator profile only | Real |

The full strength table lives in the LADE environment skill (`references/enforcement-map.md`). Re-verify toolset names against the running Hermes install before changing §2.

## 4. Provisioning

`setup.sh` at the repository root is the only supported provisioning path. It is idempotent and has a `--check` mode that reports drift without writing. It MUST NOT install packages, create credentials or configure an MCP server.

## 5. Open parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Plugin hook for the reviewer's read-only constraint | Maintainers / devops-sre |
| Per-profile model choice | Maintainers |
| Whether profiles are later packaged as distributions | Maintainers |
| Notion integration authorization and scope | Maintainers |
| Disabling Hermes builtin skills per profile: they stay visible today, so the role's *declared* surface is narrower than its *visible* one | Maintainers |
| Restarting the gateway multiplexer after adding a profile, so its secret scope is served | Maintainers / devops-sre |
