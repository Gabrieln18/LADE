# golang.md — Go Engineering Reference

> **Version:** 0.2.0 (draft) · **Date:** 2026-11-12 · **Location:** `references/engineering/golang.md`
> Replaces the 0.1.0 file (a verbatim copy of the `golang` skill). Procedure lives in `skills/software-engineering/golang/SKILL.md`.
> Only humans edit this file.

## 1. Toolchain

| Purpose | Tool | Command |
|---------|------|---------|
| Format | gofmt | `gofmt -l .` (must list nothing) |
| Static checks | go vet | `go vet ./...` |
| Tests | go test | `go test ./...` (`-race` for concurrent code) |
| Modules | go modules | `go mod tidy`, `go mod verify`; `go.mod` and `go.sum` committed |

Baseline: `lattinus-code.md` §3 (`gofmt`, Effective Go, `go vet`).

## 2. Open parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Go version (read from `go.mod`) | Maintainers |
| Extra linters (adding one is a `dependencies` gate matter) | Maintainers |
| Where Go is used in Lattinus Code (no Go module is documented in `references/` yet) | Maintainers / architect |

Agents MUST NOT assume Go is in use for a task unless `task.md` or an approved ADR says so.
