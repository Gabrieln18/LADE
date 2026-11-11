---
name: golang
description: Write, modify and review idiomatic Go (gofmt, go vet, Effective Go) with explicit errors, context propagation and table-driven tests. Use whenever a task involves Go code, Go modules, CLIs, services, concurrency or goroutines, even if the user only says "implement" or "fix" in a Go repository.
---

# Skill: golang

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-06 · **Location:** `skills/software-engineering/golang/SKILL.md`
> Defines *how to write Go* in LADE. Acceptance rules live in `references/lattinus-code.md` (§3, §6, §7, §10).

## When to use / not use

**Use:** any Go implementation or Go code review.
**Do not use:** for Python (`python`), API contracts (`api-design`), or test strategy beyond Go specifics (`testing`); combine skills when needed.

## Inputs

- `task.md`: `acceptance_criteria`, `inputs`, `constraints`, `out_of_scope`.
- Repository configuration (`go.mod`, linter config, CI): Go version and extra linters. **Follow it over defaults here.**
- `references/engineering/golang.md`, only if listed in the manifest and needed.

## Tooling

| Purpose | Command |
|---------|---------|
| Format | `gofmt -l .` (must list nothing) |
| Static checks | `go vet ./...` |
| Tests | `go test ./...` (add `-race` when concurrency is involved) |
| Modules | `go mod tidy`, `go mod verify` |

Go version and any additional linter are `TBD`: read them from the repository. Adding a linter or tool is a `dependencies` gate matter.

## Procedure

1. **Read first.** Inspect package layout, naming, error conventions and existing interfaces. Match them.
2. **Design small packages** with clear responsibility. Accept interfaces at the consumer, return concrete types. Define an interface only when there is a consumer that needs it.
3. **Implement** following Standards below.
4. **Test** with table-driven tests (see `testing` skill).
5. **Run** `gofmt`, `go vet`, `go test` (with `-race` if concurrent). Fix findings.
6. **Declare** assumptions and unverified items in the artifact header.

## Standards

- Format with `gofmt`; follow Effective Go and Go Code Review Comments naming (short, no stutter: `user.Service`, not `user.UserService`).
- **Errors are values:** return them, never ignore them. Wrap with context: `fmt.Errorf("load config: %w", err)`. Check with `errors.Is` / `errors.As`. Use `panic` only for programmer errors, never for expected failures.
- **Error messages:** lowercase, no trailing punctuation, no secrets.
- **Context:** first parameter `ctx context.Context` on functions that do I/O, block or run long. Propagate; never store in structs; honor cancellation and deadlines.
- **Concurrency:** every goroutine has a defined owner and exit path. Use `context`, `errgroup` or channels with clear close ownership. Protect shared state or avoid sharing it. Never start a goroutine without knowing how it stops.
- **Resources:** `defer` closes immediately after a successful open; check close errors on writes.
- **Config:** injected through constructors or options, not package-level globals (Twelve-Factor).
- **Logging:** structured (`log/slog` if the repository's Go version supports it); no sensitive data.
- **Exports:** minimal exported surface; doc comment on every exported identifier, starting with its name.
- **Dependencies:** standard library first; `go.mod` and `go.sum` committed; versions pinned. Record purpose, license, maintenance status and alternatives for each new module (`lattinus-code.md` §10.2).
- No dead code, no commented-out blocks, no `init()` side effects.

## Checklist

- [ ] `gofmt -l .` empty; `go vet ./...` clean.
- [ ] Tests pass (with `-race` for concurrent code); new logic covered.
- [ ] No ignored errors; errors wrapped with context.
- [ ] `ctx` propagated on I/O paths; goroutines have exit paths.
- [ ] Exported identifiers documented.
- [ ] No unapproved module added or changed.

## Gates

- `dependencies`: any `go.mod` change that adds, removes or upgrades a module (plus human approval).
- `safety`: file deletion, network calls, `os/exec` against real systems.
- `git`: before any commit.

## Anti-patterns

- `_ = err` or unchecked errors; `panic` for control flow.
- `context.Background()` deep in call chains instead of propagating the caller's context.
- Leaking goroutines; unbounded goroutine creation; sending on channels nobody reads.
- Interfaces defined "just in case"; returning interfaces from constructors without need.
- Global mutable state; `init()` doing I/O.
- Copying a mutex or struct containing one.
- Reformatting unrelated files or "drive-by" cleanups (report them instead).

## Escalate when

- The Go version or module layout is undefined and the task depends on it.
- A needed module is not approved.
- A concurrency design has no clear ownership or shutdown model.
- The task requires touching code outside `can_write`.