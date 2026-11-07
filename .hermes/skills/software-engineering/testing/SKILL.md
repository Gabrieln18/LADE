---
name: testing
description: Design and write tests (unit, integration, e2e) and regression tests for bug fixes, in Python (pytest) or Go (go test). Use whenever a task adds or changes logic, fixes a bug, asks for coverage or test strategy, or reviews test quality, even if the user does not say "test" explicitly.
---

# Skill: testing

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-06 · **Location:** `skills/software-engineering/testing/SKILL.md`
> Defines *how to test*. What counts as done lives in `references/lattinus-code.md` (§6, §7). Do not restate it here.

## When to use / not use

**Use:** new or changed logic; bug fixes; test strategy; test review; flaky test diagnosis.
**Do not use:** for data-quality checks inside pipelines (use `data-engineering/data-quality`) or AI evaluations (use `ai/evaluation`).

## Inputs

- `task.md`: `acceptance_criteria`, `inputs`, `constraints`.
- Repository test configuration (runner settings, markers, CI). Follow it over defaults here.
- `references/engineering/testing.md`, only if listed in the manifest and the task needs more detail.

## Procedure

1. **Map criteria to tests.** For each acceptance criterion, name at least one test that proves it. Record the mapping in the PR evidence.
2. **Pick the level** (pyramid, `lattinus-code.md` §7.2):
   - *Unit:* pure logic, no I/O. Fast and numerous.
   - *Integration:* module boundaries, contracts, storage, serialization.
   - *End-to-end:* few, only for critical paths.
3. **Bug fix:** write the failing regression test first, confirm it fails for the right reason, then fix.
4. **Write tests** with Arrange / Act / Assert. One behavior per test. Name tests by behavior: `test_<unit>_<condition>_<expected>`.
5. **Isolate non-determinism:** inject the clock, seed randomness, use temporary directories, fake network and external services. No real network.
6. **Run** the suite locally (commands below) and attach the output as evidence.
7. **Check test quality:** a test that cannot fail is not a test. Break the code once (or reason through it) to confirm the assertion catches it.

## Commands

| Language | Run | Notes |
|----------|-----|-------|
| Python | `pytest` | Project standard (human decision). Use `pytest -x -q` while iterating, full run before delivery |
| Go | `go test ./...` | Add `-race` when concurrency is involved |

If the runner is missing from the repository, propose it via the `dependencies` gate (Python) and wait for human approval.

## Standards

- Deterministic: no network, wall-clock or unseeded randomness without isolation.
- Coverage never replaces meaningful assertions. Thresholds are `TBD`; do not invent them.
- Python: plain `assert`, `pytest.mark.parametrize` for variants, fixtures for setup, `tmp_path` and `monkeypatch` for isolation. No test-order dependencies.
- Go: table-driven tests with `t.Run`, `t.Helper()` in helpers, `t.TempDir()`, interfaces for fakes.
- Fixtures are small, synthetic and free of secrets, personal data and absolute local paths.
- Spatial fixtures declare CRS (EPSG), nodata and dtype explicitly (`lattinus-code.md` §8).
- Never assert on exact free-text output from LLMs (`lattinus-code.md` §9).
- Do not disable, skip or weaken an existing test to make a change pass. Report it instead.

## Checklist

- [ ] Every acceptance criterion maps to at least one test.
- [ ] Bug fixes include a regression test that failed before the fix.
- [ ] Tests pass locally; output attached.
- [ ] No network, wall-clock or unseeded randomness.
- [ ] No skipped or weakened tests without a recorded reason.
- [ ] Fixtures contain no sensitive data.

## Gates

- `dependencies`: adding a test library or plugin.
- `safety`: tests that touch external services, real data or destructive operations.

## Anti-patterns

- Asserting implementation details (private calls, internal order) instead of behavior.
- Shared mutable state between tests; reliance on execution order.
- `sleep()` to wait for results; broad `except` inside tests that hides failures.
- Mocking the unit under test; over-mocking that leaves nothing real exercised.
- Snapshot tests used as a substitute for understanding expected output.
- Chasing a coverage number.

## Escalate when

- Acceptance criteria are not testable as written.
- The only way to test requires network, production data or credentials.
- An existing test fails for reasons outside the task scope.
- Required test tooling is absent and not yet approved.