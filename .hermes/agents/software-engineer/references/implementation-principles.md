# implementation-principles.md — software-engineer

> Agent-specific method. Standards live in central `references/`; this file
> only adds how the agent applies them. No duplicated content.

## 1. Where to look (pointers)

| Topic | Source |
|---|---|
| Python / Go conventions | `references/engineering/python.md`, `golang.md` |
| API design and error model | `references/engineering/api.md` |
| Test strategy | `references/engineering/testing.md` |
| Definition of Done, PR format, commits | `references/lattinus-code.md` §4, §6, §7, §12 |
| Module boundaries | `references/architecture.md` |

## 2. Implementation loop

1. **Understand.** Restate the objective and acceptance criteria. List
   assumptions; ask only if the answer changes the result.
2. **Locate.** Read the affected code and existing patterns. Follow them
   unless an ADR says otherwise.
3. **Plan.** Smallest change that satisfies the criteria. Flag any need for
   a new dependency, interface change or ADR, then stop.
4. **Test first when the behavior is clear.** Failing test, then code.
   For bugs: reproduce with a failing test before fixing.
5. **Implement.** Small steps, each leaving the build green.
6. **Verify.** Format, lint, type check, tests. Capture output.
7. **Self-check** against `lattinus-code.md` §6.1 and §6.2 (Code/API).
8. **Report.** Result, reasoning, evidence, assumptions, limitations.

## 3. Rules of thumb

- **Scope:** anything outside acceptance criteria is reported, not changed.
- **Language choice:** follow the task or ADR. Never switch or mix languages
  on your own.
- **Interfaces:** treat public signatures and API specs as contracts.
  Changes need SemVer discipline and a stated backward-compatibility impact.
- **Errors:** explicit and typed; never swallowed. Fail fast on invalid input.
- **Config and secrets:** injected, never hard-coded; no secrets anywhere.
- **Determinism:** tests avoid network, wall-clock and unseeded randomness.
- **Dead code:** no commented-out blocks, no unused abstractions.
- **Performance:** state complexity assumptions on hot paths; optimize only
  with a measurement.
- **Refactoring:** behavior-preserving, covered by tests before and after,
  separate commit from functional change.

## 4. Anti-patterns (stop and rethink)

- Adding a package "just for this".
- Changing a public interface without declaring the impact.
- "Fixing" a failing test by weakening it.
- Claiming tests pass without running them.
- Guessing an API, path or version instead of verifying or labeling it.
- Expanding the diff beyond what the task needs.

## 5. Handoff checklist (before returning the artifact)

- [ ] Every acceptance criterion mapped to evidence
- [ ] Checks run locally; output attached
- [ ] Gates recorded in the header
- [ ] No unapproved dependency, no secrets
- [ ] Assumptions, limitations and out-of-scope findings declared