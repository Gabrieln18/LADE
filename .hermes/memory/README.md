# memory/README.md

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-10 · **Location:** `memory/README.md`
> Write rules and loading rules for LADE (Hermes) memory. Key words **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 2119.
> Only humans edit this file. Summary of writers lives in `AGENTS.md` §9; permissions in `config/permissions.md` §4.

## 1. Purpose

Memory keeps the minimum context that must survive between tasks: current state, approved decisions, conventions, lessons and open questions.

**Memory is context, not authority.** Precedence: `policies/` > `references/` > `memory/`. On conflict the higher source prevails and the conflict is logged in `open-questions.md` (`AGENTS.md` §9).

Memory is NOT for: task history, chat transcripts, artifact content, copies of `references/` or `templates/` (single source of truth).

## 2. File Map

| File | Holds | Writer | Mode | When |
|------|-------|--------|------|------|
| `project-state.md` | Current state of the project and active tasks | Orchestrator | Overwrite | On task closure |
| `decisions.md` | Index of approved ADRs | Orchestrator | Append; only `Status` may change (supersede) | After human approval of an ADR |
| `conventions.md` | Project conventions not already normative elsewhere | Orchestrator | Append | After human approval |
| `lessons.md` | Lessons learned from reviews | Reviewer | Append-only | After a `standard` review, if a lesson exists |
| `open-questions.md` | Unresolved questions, gaps, conflicts | Any agent | Append-only | Any time |

The format of each entry is defined at the top of its own file.

## 3. General Write Rules

1. Every entry has an ISO date (`YYYY-MM-DD`) and a `task_id` (`LADE-YYYYMMDD-NNN`), or `none` with a reason.
2. IDs are sequential and never reused: `ADR-NNNN`, `C-NNN`, `L-NNN`, `Q-NNN`. Next ID = highest existing + 1.
3. **Append-only files** (`lessons.md`, `open-questions.md`): existing entries MUST NOT be edited or deleted by agents. A correction is a new entry that references the old ID.
4. One entry, one idea, at most ~10 lines. Link to artifacts instead of pasting them.
5. Separate **facts** (cite the source file or task section) from **assumptions** (label them) (`SOUL.md` §3).
6. No secrets, credentials, personal data or absolute local paths (`AGENTS.md` §11).
7. Before adding an entry, check the file for the same topic. Extend by reference, do not duplicate.
8. An agent MUST NOT write to a file outside the table in §2 (`config/permissions.md` §4). A needed change to another file is proposed as text in the artifact or as a `Q-NNN`.
9. Approval evidence: entries in `decisions.md` and `conventions.md` MUST cite how the human approved (PR comment, `task.md` field or named decision). See `Q-014`.

## 4. Loading Rules

1. At intake the Orchestrator reads `project-state.md`, `conventions.md` and the `open-questions.md` entries relevant to the task.
2. Other agents load memory on demand. The Orchestrator passes the needed excerpts as `inputs` in `task.md`, since sub-agents start with zero context (bootstrap `AGENTS.md` §5).
3. `lessons.md` is read by the Reviewer and by an agent whose area matches the `Affects` field of an entry.

## 5. Promotion Path

| From | To | Who decides |
|------|----|-------------|
| Lesson | Convention, skill, reference or policy change | Human (agents only propose) |
| Open question, once resolved | Convention or ADR | Human approval, then Orchestrator writes |
| Proposed ADR | `decisions.md` | Human approval, then Orchestrator writes |

## 6. Hygiene

1. Soft limits: ~30 open questions in `open-questions.md`, ~50 entries in `lessons.md`. When exceeded, the Orchestrator flags it to a human in `project-state.md`.
2. Pruning and archiving are human-only. Archive location is `TBD` (`Q-015`).
3. `project-state.md` reflects the present only. History belongs to git and to PRs.

## 7. Maintenance

Humans only. Changes bump `Version` and `Date` and add a `CHANGELOG.md` entry (`TBD`).