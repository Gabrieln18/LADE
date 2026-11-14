# project-state.md

> **Writer:** orchestrator, on task closure. **Mode:** overwrite. Reflects the present only; history belongs to git and PRs (`memory/README.md` §6.3).
> **Last update:** 2026-11-14 · **Structure version:** v2.2.1

## 1. Current state

LADE is at structure v2.2.1: a Markdown core in `.hermes/` plus a thin profile layer in `profiles/`, both in one git repository. The runtime is the Hermes Agent; every role maps to one Hermes profile. There is no adapter, generator or build step, and no `dist/`.

What works today:

- Nine role identities, each self-sufficient as a profile `SOUL.md` (core contract plus role specialization).
- Nine profile homes as real directories inside `$HERMES_HOME`, content symlinked from this repository (`scripts/repair_profile_homes.sh`, `make verify`), so `hermes -p <role>` attaches to the host gateway instead of blocking on a blank screen. v2.2.1 fixed this; the host gateway must be restarted after a layout change.
- One skill pool in `.hermes/skills/`, bound to profiles by symlink, derived from each role manifest by `setup.sh`.
- Memory as git-versioned Markdown in `.hermes/memory/`, with the per-profile `state.db` reserved for harness facts.
- Governance by `CODEOWNERS` plus branch protection; merge is human-only.
- Evals as a manual procedure with 23 golden tasks and fixtures.

What is not built yet:

- Automated eval execution (Q-016).
- Notion MCP wiring in the orchestrator profile (requires an authorized integration).
- Plugin hooks that would make "the reviewer must not write" structural instead of advisory.

## 2. Active tasks

None. The v2.2.1 runtime fix is applied on this machine: layout repaired, `make verify-canonical` reports `ATTACH` for the nine roles. Pending: one host gateway restart (human action), then `make verify` must exit 0. Per-file review and commit are human.

## 3. Known gaps

| Gap | Reference |
|-----|-----------|
| Eval execution procedure | Q-016 |
| Memory archive location and limits | Q-015 |
| Human approval evidence format | Q-014 |
| Notion snapshot refresh | Q-013 |
| Sandbox mechanism for `R2` tools | `config/tools.md` §9 |
| Repository host for draft PRs | `config/tools.md` §9 |
| ADR-0001 says the profiles are "symlinked into `~/.hermes/profiles/<role>`"; v2.2.1 changed the home to a real directory with symlinked content. `decisions.md` is human-written — the wording needs a human edit | ADR-0001 |

## 4. Next structural decisions

1. Whether `memory/` gets a `decisions/` subfolder once approved ADRs exceed ~30 entries.
2. Whether the reviewer profile gets a plugin hook enforcing read-only artifact access.
3. Whether profiles are later packaged as per-profile distributions (`distribution.yaml`) or stay symlinked.
