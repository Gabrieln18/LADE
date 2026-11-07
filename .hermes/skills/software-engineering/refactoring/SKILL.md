---
name: refactoring
description: Restructure existing code without changing its observable behavior, using tests as a safety net, small steps and atomic refactor commits. Use whenever a task says refactor, clean up, simplify, rename, extract, split, reduce duplication or complexity, or pay down technical debt, in Python or Go.
---

# Skill: refactoring

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-06 · **Location:** `skills/software-engineering/refactoring/SKILL.md`
> Defines *how to change structure safely*. Commit and PR rules live in `references/lattinus-code.md` (§4, §6). Do not restate them here.

## When to use / not use

**Use:** structural changes where behavior must stay identical.
**Do not use:** when behavior changes (that is `feat` or `fix`; handle separately, even in the same task). Interface or contract changes need `api-design` and may need an ADR.

## Inputs

- `task.md`: `objective`, `acceptance_criteria`, `out_of_scope`.
- The code under change and its existing tests.
- Language skill: `python` or `golang`. Test skill: `testing`.

## Procedure

1. **Declare the equivalence criterion** before touching code: what must remain true (public API, outputs for given inputs, side effects, performance bounds). Write it in the PR.
2. **Establish the baseline.** Run the existing tests and record the result. If they fail, stop: do not refactor on a red baseline.
3. **Check the safety net.** If the affected behavior lacks tests, add *characterization tests* (they pin current behavior, including quirks) in a separate commit *before* refactoring, using the `testing` skill.
4. **Plan small steps.** Each step is one named transformation (rename, extract function, move, inline, split module, replace conditional). List them.
5. **Apply one step at a time.** After each step: format, lint, run tests. Commit when green with a `refactor:` Conventional Commit.
6. **Keep tests unchanged.** Do not edit assertions to make a refactor pass. If a test must change, the change is not a pure refactor: stop and report.
7. **Verify equivalence** against the declared criterion: full suite, and any contract or output comparison relevant to the change.
8. **Report** out-of-scope findings (bugs, smells, dead code elsewhere) in the artifact or `memory/open-questions.md`. Do not fix them here.

## Standards

- No behavior change. No new features, no bug fixes, no dependency changes mixed in.
- One concern per commit. Every commit builds and passes tests (atomic, `lattinus-code.md` §4.1).
- Public interfaces stay stable. If they must change, treat as a breaking change: follow SemVer discipline and the ADR requirement.
- Move before you modify: separate "move code" commits from "change code" commits so diffs stay reviewable.
- Remove dead code only when it is within the declared scope and proven unreferenced.
- Prefer many small safe steps over one large rewrite. If the PR exceeds the size threshold (`TBD` in `lattinus-code.md` §14), propose a split.
- Performance changes require a measurement before and after; otherwise do not claim them.
- Respect the repository's style and tooling (`ruff`, `gofmt`, etc.); do not reformat unrelated files.

## Checklist

- [ ] Equivalence criterion declared in the PR.
- [ ] Baseline was green before the first change.
- [ ] Characterization tests added first where coverage was missing.
- [ ] Existing assertions unchanged.
- [ ] Atomic `refactor:` commits, each green.
- [ ] No behavior, dependency or interface change (or escalated).
- [ ] Out-of-scope findings reported, not fixed.

## Gates

- `git`: before each commit and the PR.
- `dependencies`: if a refactor seems to need a package change, stop; that is out of scope.
- `documentation`: when module structure or documented paths change.

## Anti-patterns

- "While I'm here" fixes and features hidden inside a refactor.
- Editing tests to match new behavior.
- Large-bang rewrites with a single giant commit.
- Refactoring on a failing or untested area without characterization tests.
- Renaming public symbols without a deprecation path.
- Reformatting whole files, burying the real change in noise.
- Claiming performance or readability gains without evidence.

## Escalate when

- The baseline is red and the cause is outside the task.
- Safe refactoring is impossible without changing behavior or a public interface.
- Required characterization tests need production data, network or credentials.
- The scope grows beyond the declared `out_of_scope` boundary or the PR size threshold.