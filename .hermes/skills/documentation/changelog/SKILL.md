---
name: changelog
description: Writes and maintains CHANGELOG.md entries for Lattinus Code following Keep a Changelog, Semantic Versioning and Conventional Commits. Classifies changes into sections, maps commit types to sections, flags SemVer impact, marks breaking changes with their ADR, and writes entries for users rather than copies of commit messages. Use whenever a task changes user-visible behavior or a public interface, whenever a PR needs a changelog entry for the Definition of Done, when preparing release notes, or when the user mentions changelog, release notes, version bump or "what changed".
version: 0.1.0
---

# Changelog

Applies `technical-writing` first. Standards: Keep a Changelog, SemVer 2.0.0, Conventional Commits 1.0.0 (`references/lattinus-code.md` §3, §4.1, §6.1).

## Scope

- **In:** entries under `[Unreleased]`, section classification, SemVer impact, release-section preparation when a task asks for it.
- **Out:** deciding or publishing a release (`workflows/release.md`, humans), tagging, pushing, commit-message writing (`policies/git.md`), ADR text (`architecture/adr`).

## Inputs

- `task.md` (objective, `task_id`, `output_language`).
- Commits or diff summary in Conventional Commits form, PR description, related ADRs.
- Existing `CHANGELOG.md`. If absent, start from `templates/changelog.md`.

## Procedure

1. **Decide if an entry is needed.** Required for user-visible or interface changes (DoD §6.1). Omit purely internal changes with no effect on users or interfaces.
2. **Classify** with the table. Use the commit type as a hint, the real effect as the decision.

   | Commit type | Section (EN) | Note |
   |---|---|---|
   | `feat` | Added | |
   | `fix` | Fixed | |
   | `fix` with security impact | Security | Describe impact, never exploit details |
   | `refactor`, `perf` | Changed | Only if users can observe it |
   | deprecation | Deprecated | State the removal window (§7.6 of the contract) |
   | removal of public interface | Removed | Usually breaking |
   | `revert` | By effect | Added, Removed or Fixed |
   | `docs`, `test`, `build`, `ci`, `chore`, `style` | omit | Unless user-visible |

3. **Write each entry.** One line, one change, written for the user.
   - Describe the effect, not the implementation. No commit hashes, no internal jargon.
   - Optional scope prefix: `**<component>:**`.
   - End with the traceability suffix: `(LADE-YYYYMMDD-NNN)` and, when applicable, `ADR-NNNN`.
   - Breaking change: start with `**BREAKING:**`, add the ADR reference and a one-line migration hint. A breaking entry without an ADR is invalid.
   - Language: `output_language` (default PT-BR). Use the section labels below.
4. **Place it.** Under `## [Unreleased]`, in the right section, newest first. Do not create a release section unless the task is a release.
5. **Propose the SemVer impact.**

   | Content of `[Unreleased]` | Impact |
   |---|---|
   | Any **BREAKING** or Removed (public interface) | MAJOR |
   | Added or Deprecated, no breaking | MINOR |
   | Only Fixed, Security or Changed (compatible) | PATCH |

   Pre-1.0 policy is `TBD` (open question). If the version is `0.y.z`, ask before proposing.
6. **If the task is a release.** Move `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` (ISO date, UTC), leave a fresh empty `[Unreleased]`, update compare links. The version number is **proposed**, not decided: a human approves it.
7. **Validate** with the checklist.

## Sections (PT-BR default)

| Section | Label |
|---|---|
| Added | 🚀 Adicionado |
| Changed | 🔄 Alterado |
| Deprecated | ⚠️ Descontinuado |
| Removed | 🗑️ Removido |
| Fixed | 🐛 Corrigido |
| Security | 🔒 Segurança |

The first three emojis come from the Lattinus `CHANGELOG.MD` model. The last three are an extension (open question). If `output_language` is EN, use the Keep a Changelog names without emojis.

## Output

Updated `CHANGELOG.md` (full file or diff, as `task.md` requires) with the traceability header as an HTML comment at the top (see `technical-writing` Output). Include the proposed SemVer impact in the PR description, not in the file.

## Checklist

- [ ] Every user-visible or interface change has an entry; internal-only changes do not.
- [ ] Each entry describes the effect for the user, one line, with `task_id`.
- [ ] Every `BREAKING` entry has an ADR and a migration hint.
- [ ] Every Deprecated entry states a removal window.
- [ ] Sections use the correct labels; entries are under `[Unreleased]` unless releasing.
- [ ] Dates are ISO 8601; compare links updated on release.
- [ ] No secrets, internal paths, exploit details or unverified claims.
- [ ] SemVer impact is stated in the PR as a proposal.

## Boundaries

- Gates: `policies/documentation.md`; `policies/git.md` before any commit.
- Does not choose the final version, tag, push, or publish. Humans decide (`AGENTS.md` §11).
- Does not invent changes. Entries come from commits, diff, task or ADR. Unverified items are labeled or omitted.
- Escalate when commits are not in Conventional Commits form and the effect cannot be inferred, or when a breaking change has no ADR.